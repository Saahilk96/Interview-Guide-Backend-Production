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
from database import googleAuth, userNotes,waitList,blogPostWaitList,pricingWaitList
import utils
import asyncio
import aiohttp
from env import API_KEY

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
            if user["limit"]==2:
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token structure"
            )

        user = await googleAuth.find_one({"email": user_email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # If no resume uploaded, check user's existing resume
        if not resume or resume.filename == "":
            user_history = user.get("history", [])
            existing_resumes = [
                h["companyData"]["resume"]
                for h in user_history
                if h.get("companyData", {}).get("resume")
            ]

            if not existing_resumes:
                return JSONResponse(
                    status_code=200,
                    content={"status": "Not Ok", "message": "Existing resume not found"}
                )

        return JSONResponse(
            status_code=200,
            content={"status": "Ok", "message": "Resume exists"}
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
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
            "uNotes": haveNotes,
            "resume":True if user["history"] else False
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
        file_path = await utils.fetch_data_and_convert_to_csv(googleAuth,waitList,blogPostWaitList,pricingWaitList)
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

@app.post("/join_waitlist_from_blog")
async def join_waitlist_from_blog(
    x_api_key: str = Header(..., alias="x-api-key"),
    email: str = Form(...)
):
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    try:    
        alreadyWaitlistUser = await blogPostWaitList.find_one({"user_email":email})
        if alreadyWaitlistUser:
            return JSONResponse(
            status_code=208,
            content={"message": "Already in waitlist"}
        )

        result = await blogPostWaitList.insert_one({"user_email":email})
        return JSONResponse(
            status_code=200,
            content={"message": "Joined waitlist"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/join_waitlist_from_pricing")
async def join_waitlist_from_pricing(
    x_api_key: str = Header(..., alias="x-api-key"),
    email: str = Form(...),
    feature: str = Form("N/A"),
    pay_range: str = Form("N/A")
):
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    try:    
        alreadyWaitlistUser = await pricingWaitList.find_one({"user_email":email})
        if alreadyWaitlistUser:
            await pricingWaitList.update_one({"user_email":email},{"$set":{"pay_range":pay_range,"feature":feature}})
            return JSONResponse(
            status_code=208,
            content={"message": "user pricing waitlist updated"}
        )

        result = await pricingWaitList.insert_one({"user_email":email,"pay_range":pay_range,"feature":feature})
        return JSONResponse(
            status_code=200,
            content={"message": "Joined waitlist"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_answer")
async def generate_answer(
    x_api_key: str = Header(..., alias="x-api-key"),
    question: str = Form(...)
):
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=400, detail="Missing or invalid access key")

    try:
        answer = await utils.generate_answer(question)
        return {
                "status": "Ok",
                "message":"Answer generated successfully",
                "answer":answer
            }


    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @app.post("/delete_user")
# async def delete_user(
#     email: str = Form(...)
# ):
   
#     await googleAuth.delete_many({"email":email,"history":[]})

#     return JSONResponse(
#             status_code=200,
#             content={"message": "Deleted user"}
#         )

# @app.post("/test_module")
# async def test_module(
#     x_api_key: str = Header(..., alias="x-api-key"),
#     company_name: str = Form(...),
#     job_role: str = Form(...),
#     job_description: str = Form(...),
#     token: str = Form(...),
#     resume: Optional[UploadFile] = File(None)
# ):
#     if x_api_key != ACCESS_KEY:
#         raise HTTPException(status_code=400, detail="Missing or invalid access key")

#     try:
#         resume_text = ''
        
#         if resume and resume.filename != '':
#             filename = secure_filename(resume.filename)
#             file_path = os.path.join(UPLOAD_FOLDER, filename)
#             with open(file_path, "wb") as f:
#                 f.write(await resume.read())

#             reader = PyPDF2.PdfReader(file_path)
#             for page in reader.pages:
#                 resume_text += page.extract_text() or ""

#             os.remove(file_path)
#         else:
#             raise HTTPException(status_code=400, detail="Resume is required")

#         data = {
#             "company_name": company_name,
#             "job_role": job_role,
#             "job_description": job_description,
#             "token": token,
#             "resume": resume_text
#         }

#         company_research = (f'''
# <role>
# You are an expert research assistant specializing in company intelligence for job interview preparation.
# You use web search (powered by Exa AI through OpenRouter) to gather and verify current information about companies.
# Model: Gemini 2.5 Flash
# </role>

# <task>
# Create a concise, visually rich company profile in **HTML using Tailwind CSS** for interview candidates.
# Input data: {data}
# </task>

# <requirements>
# ⚠️ REQUIREMENTS:
# - Do **not** include `<!DOCTYPE html>`, `<html>`, `<head>`, or `<body>`
# - Do **not** add any class or attributes to the topmost parent `<div>`
# - Start directly with styled content blocks
# - Wrap **all URLs** in `<a>` tags with Tailwind styling
# - Include relevant **images** using `<img>` tags with proper sizing, alignment, shape, and alt text where it adds value
# </requirements>

# <writing_style>
# Style: “Smart Brief” – like a sharp friend prepping you fast.
# - Max 20 words per sentence
# - Active voice
# - Add context that matters
# - Be concise, not robotic or flowery
# </writing_style>

# <output_format>
# ✅ Begin output with HTML content only (no document structure)  
# ✅ Use Tailwind CSS classes for all formatting  

# ✅ Sections:
# ```html
# <div class="bg-white p-6 rounded-xl shadow border-l-4 border-blue-600 space-y-2">
# ✅ Headings:

# Title:

# html
# Copy
# Edit
# <h1 class="text-3xl font-extrabold text-center text-gray-900 mb-6">[Company Name] – Interview Brief</h1>
# Section header:

# html
# Copy
# Edit
# <h2 class="text-2xl font-bold text-blue-800 mb-2">
# ✅ Text:

# Paragraph: <p class="text-gray-700 leading-relaxed">

# Missing info: <p class="text-gray-500 italic">Information not available from current sources.</p>

# Emphasize key terms with: <strong class="text-gray-900 font-semibold">

# ✅ Lists:

# html
# Copy
# Edit
# <ul class="list-disc list-inside marker:text-green-600 text-gray-700 space-y-1">
#   <li>Global team spread across 15 countries</li>
# </ul>
# ✅ Tables:

# html
# Copy
# Edit
# <table class="w-full border-collapse text-sm text-left">
#   <thead class="bg-gray-100 text-gray-700">
#     <tr>
#       <th class="px-4 py-2 font-semibold">Fact</th>
#       <th class="px-4 py-2">Details</th>
#     </tr>
#   </thead>
#   <tbody class="divide-y divide-gray-200">
#     <tr>
#       <td class="px-4 py-2 font-medium text-gray-800">Founded</td>
#       <td class="px-4 py-2">2014 by ex-Amazon engineers</td>
#     </tr>
#   </tbody>
# </table>
# ✅ URLs (always clickable):

# html
# Copy
# Edit
# <a href="https://example.com" class="text-blue-600 underline hover:text-blue-800" target="_blank" rel="noopener noreferrer">example.com</a>
# ✅ Badges:

# html
# Copy
# Edit
# <span class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">Private</span>
# ✅ Separators:

# html
# Copy
# Edit
# <hr class="my-6 border-t border-gray-300">
# ✅ Emojis:
# Use to enhance clarity (📍 location, 💼 team, 🚀 product, 🧠 insight, 🔒 security)

# ✅ ✅ Images:
# Use only when relevant — e.g., product images, team photos, logos, UI screenshots, etc.
# Use this pattern:

# html
# Copy
# Edit
# <img src="https://example.com/logo.png" alt="Company logo" class="w-32 h-32 object-contain mx-auto rounded-full shadow mb-4" />
# w-32 h-32 for controlled size

# mx-auto for center alignment

# rounded, rounded-full, shadow, object-contain for clean UI look

# ✅ Sections to Include:

# Company Snapshot

# Key Facts

# What They Build

# Business Model

# Target Market

# Market Position

# Leadership

# Recent Momentum

# Sources (with all links in <a>)

# ✅ Content limit: Under 500 words (excluding HTML)
# </output_format>

# <search_requirements>

# Use search for every section

# At least 2 sources per fact (1 if from company website or SEC)

# Prioritize 2020–2025 events
# </search_requirements>

# <company_identification>

# Match using COMPANY NAME and WEBSITE

# Cross-check with job description and industry
# </company_identification>

# <search_strategy>
# Use focused searches:

# "[Company Name] company profile"

# "[Company Name] founder and start year"

# "[Company Name] headquarters employee count"

# "[Company Name] product offerings"

# "[Company Name] revenue model"

# "[Company Name] customer base"

# "[Company Name] main competitors"

# "[Company Name] CEO 2024"

# "[Company Name] recent funding, acquisition, layoffs 2020–2025"
# </search_strategy>

# <missing_information_handling>
# If info is not found or verified:

# Use: <p class="text-gray-500 italic">Information not available from current sources.</p>
# </missing_information_handling>

# <leadership_verification>

# Find current CEO, Head of Product, and Head of Engineering (2024–2025)

# Use company site, press, or LinkedIn

# Use placeholder if not found:

# html
# Copy
# Edit
# <p class="text-gray-500 italic">Current [position] not available</p>
# </leadership_verification>

# <quality_requirements>

# Prioritize clarity, usefulness, and strong visual layout

# Every sentence must add new insight

# Avoid repetition, vague phrases, or unnecessary detail

# Use layout spacing, color, icons, and media for strong UI
# </quality_requirements>
# ''')
        
#         async with aiohttp.ClientSession() as session:
#             async with session.post(
#                 url="https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json"
#         },
#         data=json.dumps({
#         "model": "google/gemini-2.5-flash-preview-05-20",
#         "plugins": [{"id": "web", "max_results": 10}],
#         "messages": [
#             {"role": "user", "content": company_research}
#         ],
#         "tools":[
#             {
#   "name": "generateHtmlWithTailwind",
#   "description": "Generates HTML content styled with Tailwind CSS based on a user query",
#   "parameters": {
#     "type": "object",
#     "properties": {
#       "topic": {
#         "type": "string",
#         "description": "The topic to generate HTML content for"
#       }
#     },
#     "required": ["topic"]
#   }
# }
#         ],
#          "tool_choice": {
#             "type": "function",
#             "function": {
#                 "name": "generateHtmlContent"
#             }
#         }
#         })
#         ) as response:
#                 data = await response.json()

#                 citations = []
#                 annotations = data.get("choices", [])[0].get("message", {}).get("annotations", [])
#                 for annotation in annotations:
#                     url_citation = annotation.get("url_citation", {})
#                     url_citation.pop("start_index", None)
#                     url_citation.pop("end_index", None)
#                     citations.append(url_citation)

#                 # tool_args = data.get("choices", [])[0].get("message", {}).get("tool_calls", [])[0].get("function", {}).get("arguments", "{}")
#                 # parsed_response = json.loads(tool_args)

#                 # return parsed_response, citations, None
#                 return {"data":data}

#     except ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)