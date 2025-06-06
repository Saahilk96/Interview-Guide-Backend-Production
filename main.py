from fastapi import FastAPI, File, UploadFile, Form, Header, HTTPException, Path, status, Depends, Request, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from jose import jwt, ExpiredSignatureError, JWTError
import os
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import PyPDF2
import json
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from env import SECRET_KEY,ACCESS_KEY,UPDATE_CSV_KEY
from database import googleAuth, userNotes,waitList
import utils
import asyncio

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

origins = [
    "https://www.eukaai.com",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/generate_guide")
async def generate_guide(
    x_api_key: str = Header(..., alias="x-api-key"),
    company_name: str = Form(...),
    job_role: str = Form(...),
    job_description: str = Form(...),
    token: str = Form(...),
    resume: Optional[UploadFile] = File(None)
):
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    try:
        resume_text = ''
        
        if resume and resume.filename != '':
            filename = secure_filename(resume.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, "wb") as f:
                f.write(await resume.read())

            reader = PyPDF2.PdfReader(file_path)
            for page in reader.pages:
                resume_text += page.extract_text() or ""

            os.remove(file_path)

        idinfo = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])["idinfo"]
        user_email = idinfo['email']

        user = await googleAuth.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user_email!="karkerasaahil@gmail.com" and user_email!="shahreenhossain22@gmail.com" and user_email!="aletishiva218@gmail.com":
            if user["limit"]==3:
                raise HTTPException(status_code=405, detail="Reached limit, upgrade to pro")

        if not resume or resume.filename == '':
            user_history = json.loads(dumps(user)).get("history", [])
            resumes = [h["companyData"]["resume"] for h in user_history if "companyData" in h and h["companyData"].get("resume")]
            if not resumes:
                return JSONResponse(status_code=200, content={"status": "Not Ok", "error": "Existing resume not found"})
            resume_text = resumes[-1]

        updated_data = {
            "company_name": company_name,
            "job_role": job_role,
            "job_description": job_description,
            "token": token,
            "resume": resume_text
        }

        prompts = utils.generatePrompts(updated_data)
        
        results_with_meta = await asyncio.gather(
        *[utils.get_response(prompt, i) for i, prompt in enumerate(prompts)]
        )

        results, citations, errorJsons = zip(*results_with_meta)
        results = list(results)
        citations = list(citations)
        errorJsons = list(errorJsons)

        guide_id = str(uuid4())
        newGuide = utils.structureGuide(list(results), list(citations), updated_data, guide_id)

        user_history = user.get("history", [])
        user_history.append(newGuide)

        updatedLimit = user["limit"]+1 if (user_email!="karkerasaahil@gmail.com" and user_email!="shahreenhossain22@gmail.com" and user_email!="aletishiva218@gmail.com") else user["limit"]
    
        result = await googleAuth.update_one({"email": user_email}, {"$set": {"history": user_history,"limit":updatedLimit}})
        
        notes = {
            "guideId": guide_id,
            "company_research": [], "product_research": [], "job_description_analysis": [],
            "resume_experience_to_highlight_to_stand_out": [], "hiring_manager_round": [],
            "behavioral_interview": [], "recruiter_screen_preparation": [], "favorite_product_question": [],
            "product_design": [], "product_sense": [], "product_strategy": [], "analytical_estimation": [],
            "technical": [], "leadership": []
        }
        await userNotes.insert_one(notes)

        if result.matched_count:
            return {
                "status": "Ok",
                "message": "User updated",
                "history": user_history,
                "guide": newGuide,
                "notes": utils.convert_objectid(notes)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update user history")

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/check_resume")
async def check_resume(
    token: str = Form(...),
    resume: Optional[UploadFile] = File(None),
    x_api_key: str = Depends(utils.verify_access_key)
):
    try:
        # Decode and validate JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("idinfo", {}).get("email")

        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token structure")

        user = await googleAuth.find_one({"email": user_email})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # If no resume is uploaded
        if resume is None or resume.filename == "":
            userHistory = user.get("history", [])
            existsResumes = [
                history["companyData"]["resume"]
                for history in userHistory
                if history.get("companyData", {}).get("resume")
            ]

            if not existsResumes:
                return JSONResponse(
                    status_code=200,
                    content={"status": "Not Ok", "message": "Existing resume not found"}
                )

        return JSONResponse(status_code=200, content={"status": "Ok", "message": "Resume exists"})

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/google-login")
async def google_login(payload: utils.TokenPayload, x_api_key: str = Depends(utils.verify_access_key)):
    try:
        # Decode token
        decoded_token = jwt.decode(payload.token, SECRET_KEY, algorithms=["HS256"])
        idinfo = decoded_token.get("idinfo", {})
        user_email = idinfo.get("email")
        user_name = idinfo.get("name")

        if not user_email or not user_name:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = await googleAuth.find_one({"email": user_email})
        if user is None:
            user = {
                "name": user_name,
                "email": user_email,
                "limit": 0,
                "history": [],
                "createdAt": datetime.now()
            }
            googleAuth.insert_one(user)
        
        # Prepare uNotes
        uNotes = []
        async for note in userNotes.find({}):
            if any(len(note[field]) > 0 for field in [
                'company_research', 'product_research', 'job_description_analysis',
                'resume_experience_to_highlight_to_stand_out', 'leadership',
                'behavioral_interview', 'recruiter_screen_preparation',
                'favorite_product_question', 'product_design', 'product_sense',
                'product_strategy', 'analytical_estimation', 'technical'
            ]):
                uNotes.append({"note": utils.convert_objectid(note), "haveNotes": True})
            else:
                uNotes.append({"note": utils.convert_objectid(note), "haveNotes": False})

        # Filter user's existing notes
        filteredNotes = [entry["id"] for entry in user.get("history", [])]
        haveNotes = [note for note in uNotes if note["note"]["guideId"] in filteredNotes]

        return JSONResponse(content=jsonable_encoder({
            "status": "Ok",
            "message": "Login Successful",
            "user": utils.convert_objectid(user),
            "uNotes": haveNotes
        }))

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-token")
async def generate_token(request: Request, x_api_key: str = Header(None)):
    # Validate API key header
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    # Get JSON body
    data = await request.json()

    # Create JWT payload with expiration and issued-at
    payload = {
        "idinfo": data,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
    }

    # Encode JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return JSONResponse(content={"status": "Ok", "token": token})

@app.get("/guide/{id}")
async def get_guide(
    id: str = Path(..., description="Guide ID"),
    x_api_key: str = Header(..., alias="x-api-key"),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    # Validate access key
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        idinfo = payload.get("idinfo", {})
        user_email = idinfo.get("email")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token payload: missing email")

        # Find user in DB
        user = await googleAuth.find_one({"email": user_email})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        history = user.get("history", [])
        # Find guide in user's history
        guide = next((g for g in history if g.get("id") == id), None)
        if guide is None:
            raise HTTPException(status_code=404, detail="Guide not found with this id")

        # Find or create notes document for this guide
        uNotes = await userNotes.find_one({"guideId": id})
        if uNotes is None:
            notes_template = {
                "guideId": id,
                "company_research": [],
                "product_research": [],
                "job_description_analysis": [],
                "resume_experience_to_highlight_to_stand_out": [],
                "hiring_manager_round": [],
                "behavioral_interview": [],
                "recruiter_screen_preparation": [],
                "favorite_product_question": [],
                "product_design": [],
                "product_sense": [],
                "product_strategy": [],
                "analytical_estimation": [],
                "technical": [],
                "leadership": []
            }
            insert_result = await userNotes.insert_one(notes_template)
            notes = notes_template
            notes["_id"] = str(insert_result.inserted_id)
        else:
            notes = utils.convert_objectid(uNotes)

        guide = utils.convert_objectid(guide)

        return JSONResponse(content=jsonable_encoder({"status": "Ok", "guide": guide, "notes": notes}))

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.post("/save_note/{guideId}/{moduleName}")
async def save_note(
    guideId: str,
    moduleName: str,
    note_data: utils.NoteData,
    x_api_key: str = Header(...),
    Authorization: str = Header(None)
):
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = Authorization.split(" ")[1]
        idinfo = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_email = idinfo["idinfo"]["email"]

        user = await googleAuth.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        uNotes = await userNotes.find_one({"guideId": guideId})
        if not uNotes:
            raise HTTPException(status_code=404, detail="Notes not found for this Id")

        note_dicts = [note.dict() for note in note_data.note]

        # Remove _id and update note data in that specific module
        uNotes.pop("_id", None)
        uNotes[moduleName] = note_dicts

        await userNotes.update_one({"guideId": guideId}, {"$set": uNotes})
        return JSONResponse(content={"status": "Ok", "message": "Note saved successfully"})

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        return JSONResponse(status_code=400, content={
            "status": "Not Ok",
            "error": f"Unexpected error: {str(e)}"
        })

@app.delete("/guide/{id}")
async def delete_guide(
    id: str,
    x_api_key: str = Header(...),
    Authorization: str = Header(None)
):
    # Check access key
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    # Check token
    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = Authorization.split(" ")[1]
        idinfo = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_email = idinfo["idinfo"]["email"]

        user = await googleAuth.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        history = user.get("history", [])
        guide_index = next((index for index, g in enumerate(history) if g.get("id") == id), None)

        if guide_index is None:
            raise HTTPException(status_code=401, detail="Guide not found with this id")

        # Remove the guide from user's history
        history.pop(guide_index)
        googleAuth.update_one(
            {"email": user_email},
            {"$set": {"history": history}}
        )

        # Delete associated user notes if they exist
        if await userNotes.find_one({"guideId": id}):
            await userNotes.delete_one({"guideId": id})

        return JSONResponse(status_code=200, content={
            "status": "Ok",
            "message": "Guide deleted successfully"
        })

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        return JSONResponse(status_code=400, content={
            "status": "Not Ok",
            "error": str(e)
        })

@app.put("/markcomplete/{guideId}/{mainModule}/{subModuleInd}")
async def mark_as_complete(
    guideId: str,
    mainModule: str,
    subModuleInd: int = Path(..., ge=0),
    x_api_key: str = Header(...),
    Authorization: str = Header(None)
):
    # Access key validation
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    # Token check
    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = Authorization.split(" ")[1]
        idinfo = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_email = idinfo["idinfo"]["email"]

        user = await googleAuth.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        history = user.get("history", [])
        guide = next((g for g in history if g["id"] == guideId), None)

        if not guide:
            raise HTTPException(status_code=401, detail="Guide not found with this id")

        if mainModule not in guide["result"]:
            raise HTTPException(status_code=401, detail="Module not found with this id")

        sub_modules = guide["result"][mainModule]["sub_modules"]

        if subModuleInd >= len(sub_modules):
            raise HTTPException(status_code=401, detail="Index overlaps")

        # Mark submodule as complete
        for g in history:
            if g["id"] == guideId:
                g["result"][mainModule]["sub_modules"][subModuleInd]["completed"] = True
                break

        await googleAuth.update_one({"email": user_email}, {"$set": {"history": history}})

        return JSONResponse(status_code=200, content={
            "status": "Ok",
            "message": "Sub Module marked successfully"
        })

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        return JSONResponse(status_code=400, content={
            "status": "Not Ok",
            "error": str(e)
        })

@app.get("/update-csv")
async def update_csv(updatecsvkey: str = Query(...)):
    if updatecsvkey != UPDATE_CSV_KEY:
        raise HTTPException(status_code=400, detail="Incorrect CSV key")

    try:
        file_path = await utils.fetch_data_and_convert_to_csv(googleAuth)
        utils.upload_csv_to_drive(file_path)
        return JSONResponse(
            status_code=200,
            content={"message": "CSV updated in Google Drive successfully!"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update CSV: {str(e)}")

@app.post("/join_waitlist")
async def join_waitlist(
    x_api_key: str = Header(..., alias="x-api-key"),
    token: str = Form(...),
    email: str = Form(...),
    feature: str = Form("N/A"),
    pay_range: str = Form("N/A")
):
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    try:
        idinfo = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])["idinfo"]
        user_email = idinfo['email']

        user = await googleAuth.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        alreadyWaitlistUser = await waitList.find_one({"user_email":user_email})
        if alreadyWaitlistUser:
            result = await waitList.update_one({"user_email":user["email"]},{"$set":{"formData":{"email":email,"feature":feature,"pay_range":pay_range}}})

            return JSONResponse(
            status_code=208,
            content={"message": "Updated user waitlist"}
        )

        result = await waitList.insert_one({"user_email":user["email"],"user_name":user["name"],"formData":{"email":email,"feature":feature,"pay_range":pay_range}})
        return JSONResponse(
            status_code=200,
            content={"message": "Joined waitlist"}
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)