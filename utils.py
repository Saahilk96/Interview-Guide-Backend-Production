from fastapi import Header, HTTPException, status
from env import ACCESS_KEY
import myPrompts
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Any,Optional,Union
from bson import ObjectId
from typing import Any
from env import API_KEY,FOLDER_ID,CSV_FILE_ID,GOOGLEAPIDRIVE
from pydantic import BaseModel
import os
import base64
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def generatePrompts(data):
    data1 = "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")
    prompts = [
         myPrompts.company_research_fun("{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']),
         myPrompts.product_research_fun("{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']),
         myPrompts.job_description_analysis_fun(data1),
         myPrompts.resume_experience_to_highlight_to_stand_out_fun(data1),
        "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")+".Your goal is to just Generate entire Output of 'Hiring Manager Round' Array Data. Add more points,values, etc. as per your understanding and I want json data to be more so add accordingly. Result should contain all sub modules and it is fixed : 'Phase 1: Introduction & Background', 'Phase 2: Product Experience Deep Dives', 'Phase 3: Product Methodology Assessment', 'Phase 4: Cross-Functional Collaboration', 'Phase 5: Strategic Thinking', 'Phase 6: Technical Understanding', 'Phase 7: Role-Specific Challenges'. And give me JSON data of 'Hiring Manager Round' only and 'STRICTLY do not include any silly mistake in this JSON OUTPUT e.g. brackets, comas, quatations,'\\n'','\\t',etc.' and completed must be 'false' only so provide me entire full JSON Data in this exact JSON format only:{quick_summary:'',sub_modules:[{title:'Phase 1: Introduction & Background',completed:false,summary:'',content:'some text content only',points:[{main:'title of point can be short text or little long short text',subPoints:['value1 can be text only','value2',..]},{main:'',subPoints:['value1',..]},..]},{title:'Phase 2: Product Experience Deep Dives',completed:false,summary:'',content:'',points:[]}\\}...]}",
        "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")+".Generate 15 behavioral questions that focus on: leadership, conflict resolution, failure recovery, crossfunctional collaboration, Decision Making, Communication style, prioritization style for this job description. Mention all the questions"+". Add more points,values, etc. as per your understanding and I want json data to be more so add accordingly. Result should contain all sub modules and it is fixed : STAR Method for Behavioral Questions,Essential Behavioral Interview Questions Decision Making & Problem Solving, Taking Initiative, Customer/Client Focus, Teamwork & Collaboration, Leadership, Adaptability, Results & Accountability, Innovation & Creativity, Communication, Integrity & Ethics. And give me JSON data of 'Behavioral Interview' only and 'STRICTLY do not include any silly mistake in this JSON OUTPUT e.g. brackets, comas, quatations,'\\n'','\\t',etc.' and completed must be 'false' only so provide me entire full JSON Data in this  exact JSON format only:{quick_summary:'',sub_modules:[{title:'...',completed:false,summary:'',content:'some text content only',points:[{main:'title of point can be short text or little long short text',subPoints:['value1 can be text only','value2',..]},{main:'',subPoints:['value1',..]},..]},{title:'',completed:false,summary:'',content:'',points:[]}\\}...]}",
        myPrompts.recruiter_screen_preparation_fun(data1),        
        myPrompts.favorite_product_question_fun(data1),
        myPrompts.product_design_fun(data1),
        "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")+". The questions should be composed of: **2-3 Analytical Questions:**, **2-3 A/B Testing Scenarios:**"+" .  Your goal is to just Generate entire Output of 'Product Sense' Array Data. Add more points,values, etc. as per your understanding and I want json data to be more so add accordingly.And give me JSON data of 'Product Sense' only and 'STRICTLY do not include any silly mistake in this JSON OUTPUT e.g. brackets, comas, quatations,'\\n'','\\t',etc.' and *completed must be 'false' only so provide me entire full JSON Data in this exact JSON format only ensure atleast `2 subPoints` should,must be filled in each object of sub_modules*:{quick_summary:'',sub_modules:[{title:'Important title text',completed:false,summary:'',content:'some text content only',points:[{main:'title of point can be short text or little long short text',subPoints:['value1 can be text only','value2',..]},{main:'',subPoints:['value1',..]},..]},{title:'Important title text',completed:false,summary:'',content:'',points:[]}\\}...]}",
        "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")+".Generate 7 strategic product questions for a this role at this company. Company:... Product: ... Industry: ... Competitors: ... Mix of question types: - Product investment: 'Why should this company continue investing in product?' - Competitive strategy: 'How would you respond to competitor's new features?' - Market expansion: 'Should this company enter new market?' - Metrics & goals: 'What metrics would you track for product?' - Industry trends: 'How should this company adapt to industry trend ?' Make questions specific to real products, competitors, and industry challenges. '+' . Add more points,values, etc. as per your understanding and I want json data to be more so add accordingly.  'STRICTLY do not include any silly mistake in this JSON OUTPUT e.g. brackets, comas, quatations,'\\n'','\\t',etc.' and completed must be 'false' only so provide me entire full JSON Data in this  exact JSON format only:{quick_summary:'',sub_modules:[{title:'some important title..',completed:false,summary:'',content:'some text content only',points:[{main:'title of point can be short text or little long short text',subPoints:['value1 can be text only','value2',..]},{main:'',subPoints:['value1',..]},..]},{title:'some important title...',completed:false,summary:'',content:'',points:[]}\\}...]}",
        "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")+".Generate a list of market sizing interview questions that test a candidate's estimation and analytical skills. 'Guidelines • Focus on strategic understanding and market potential, • Cover diverse industries and technologies', 'Question Types 1. Total Addressable Market (TAM) estimates, 2. Revenue potential calculations, 3. User base or adoption rate projections,4. Infrastructure and operational cost estimations'"+" . Add more points,values, etc. as per your understanding and I want json data to be more so add accordingly. And give me JSON data of 'Analytical Estimation' only and 'STRICTLY do not include any silly mistake in this JSON OUTPUT e.g. brackets, comas, quatations,'\\n'','\\t',etc.' and completed must be 'false' only so provide me entire full JSON Data in this  exact JSON format only:{quick_summary:'',sub_modules:[{title:'some important title..',completed:false,summary:'',content:'some text content only',points:[{main:'title of point can be short text or little long short text',subPoints:['value1 can be text only','value2',..]},{main:'',subPoints:['value1',..]},..]},{title:'some important title...',completed:false,summary:'',content:'',points:[]}\\}...]}",
        "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")+".Generate a comprehensive list of technical interview questions that probe the candidate's expertise in key areas mentioned in the job description. Question types: high level understanding based questions on key technical concepts mentioned in JD Experience-based scenario questions based on resume, The candidate’s experience collaborating with engineers, Their understanding of technical trade-offs, implementation complexity, or API design Probing questions about past projects that demonstrate proficiency"+" . Add more points,values, etc. as per your understanding and I want entire json data to be more so add accordingly. And give me JSON data of 'Technical' only and 'STRICTLY do not include any silly mistake in this JSON OUTPUT e.g. brackets, comas, quatations,'\\n'','\\t',etc.' and completed must be 'false' only so provide me entire full JSON Data in this  exact JSON format only:{quick_summary:'',sub_modules:[{title:'some important title..',completed:false,summary:'...',content:'some text content only',points:[{main:'title of point can be short text or little long short text',subPoints:['value1 can be text only','value2',..]},{main:'',subPoints:['value1',..]},..]},{title:'some important title...',completed:false,summary:'',content:'',points:[]}\\}...]}",
        "{\\n company_name:'"+data['company_name']+(f",\n company_website:{data.get('company_website', '')}" if data.get("company_website") else "")+"',\\n job_role:'"+data['job_role']+"',\\n job_description:'"+data['job_description']+("',\\n resume:'"+data['resume']+"'\\n }" if data['resume'] else "")+".Generate a list of 15 leadership interview questions that assess the candidate's ability to lead and influence. Question types: Strategic vision and alignment with company goals Experience managing crossfunctional stakeholders Decision-making and prioritization approaches Team leadership and development capabilities Communication and influence strategies Handling organizational challenges and change"+" . Add more points,values, etc. as per your understanding and I want json data to be more so add accordingly.'STRICTLY do not include any silly mistake in this JSON OUTPUT e.g. brackets, comas, quatations,'\\n'','\\t',etc.' and completed must be 'false' only so provide me entire full JSON Data in this  exact JSON format only:{quick_summary:'',sub_modules:[{title:'some important title..',completed:false,summary:'',content:'some text content only',points:[{main:'title of point can be short text or little long short text',subPoints:['value1 can be text only','value2',..]},{main:'',subPoints:['value1',..]},..]},{title:'some important title...',completed:false,summary:'',content:'',points:[]}\\}...]}"
        ]
    return prompts

def get_response(question, results, errorJsons, citations1, index):
    model = "google/gemini-2.5-flash-preview"
    plugins = [{"id": "web", "max_results": 10}] if index in (0, 1) else []

    print(f"Index: {index}, Model: {model}, Plugins: {plugins}")

    # Structured function call setup
    request_payload = {
        "model": model,
        "plugins": plugins,
        "messages": [
            {"role": "user", "content": question}
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "structured_module_output",
                    "description": "",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "quick_summary": {
                                "type": "string",
                                "description": ""
                            },
                            "sub_modules": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "description": ""},
                                        "completed": {"type": "boolean", "description": ""},
                                        "summary": {"type": "string", "description": ""},
                                        "content": {"type": "string", "description": ""},
                                        "points": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "main": {"type": "string", "description": ""},
                                                    "subPoints": {
                                                        "type": "array",
                                                        "items": {"type": "string"},
                                                        "description": ""
                                                    }
                                                },
                                                "required": ["main", "subPoints"]
                                            }
                                        }
                                    },
                                    "required": ["title", "completed", "summary", "content", "points"]
                                }
                            }
                        },
                        "required": ["quick_summary", "sub_modules"]
                    }
                }
            }
        ],
        "tool_choice": {
            "type": "function",
            "function": {
                "name": "structured_module_output"
            }
        }
    }

    jdumps = json.dumps(request_payload)

    # Retry loop
    while True:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + API_KEY},
                data=jdumps
            )

            data = response.json()

            # Collect citations if applicable
            if index in (0, 1):
                annotations = data.get("choices", [])[0].get("message", {}).get("annotations", [])
                citations = []
                for annotation in annotations:
                    url_citation = annotation.get("url_citation", {})
                    url_citation.pop("start_index", None)
                    url_citation.pop("end_index", None)
                    citations.append(url_citation)
                citations1[index] = citations

            # Store structured response
            tool_args = data.get("choices", [])[0].get("message", {}).get("tool_calls", [])[0].get("function", {}).get("arguments", "{}")
            results[index] = json.loads(tool_args)
            break

        except Exception as e:
            print(f"Error occurred: {e}. Retrying in 2 seconds...")
            time.sleep(2)

def structureGuide(results: List[Dict[str, Any]], citations: List[List[Dict[str, str]]], companyData: Dict[str, Any], id: str) -> Dict[str, Any]:

    sections = [
        "company_research",
        "product_research",
        "job_description_analysis",
        "resume_experience_to_highlight_to_stand_out",
        "hiring_manager_round",
        "behavioral_interview",
        "recruiter_screen_preparation",
        "favorite_product_question",
        "product_design",
        "product_sense",
        "product_strategy",
        "analytical_estimation",
        "technical",
        "leadership"
    ]

    return {
        "id": id,
        "datetime": datetime.now().isoformat(),
        "companyData": companyData,
        "citations": {
            section: citations[idx] if idx < len(citations) else []
            for idx, section in enumerate(sections)
        },
        "result": {
            section: results[idx] if idx < len(results) else {}
            for idx, section in enumerate(sections)
        }
    }

def convert_objectid(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {
            key: str(value) if isinstance(value, ObjectId) else convert_objectid(value)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    else:
        return obj

def verify_access_key(x_api_key: str = Header(...)):
    if x_api_key != ACCESS_KEY:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing or invalid access key")

class TokenPayload(BaseModel):
    token: str

class NoteItem(BaseModel):
    type: str
    content: Union[str, Dict[str, Any], List[Any]]

class NoteData(BaseModel):
    note: Optional[List[NoteItem]] = None

SCOPES = [GOOGLEAPIDRIVE]

def save_service_account_file():
    b64_creds = os.environ.get("GOOGLE_CREDENTIALS_BASE64")
    if not b64_creds:
        raise Exception("Missing GOOGLE_CREDENTIALS_BASE64 environment variable")

    decoded = base64.b64decode(b64_creds)
    file_path = "service_account.json"

    with open(file_path, "wb") as f:
        f.write(decoded)

    return file_path

SERVICE_ACCOUNT_FILE = save_service_account_file()

# Convert MongoDB collection data to CSV
async def fetch_data_and_convert_to_csv(collection):
    cursor = collection.find({}, {'_id': 0, 'name': 1, 'email': 1, 'createdAt': 1})
    data = await cursor.to_list(length=None)

    for doc in data:
        if 'createdAt' in doc and isinstance(doc['createdAt'], datetime):
            doc['createdAt'] = doc['createdAt'].strftime('%d %b, %Y %H:%M:%S')
        elif 'createdAt' in doc:
            try:
                doc['createdAt'] = datetime.fromisoformat(
                    str(doc['createdAt']).replace('Z', '+00:00')
                ).strftime('%d %b, %Y %H:%M:%S')
            except Exception:
                doc['createdAt'] = ''

    df = pd.DataFrame(data)
    csv_path = "data.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

# Upload or update CSV to Google Drive
def upload_csv_to_drive(file_path):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': 'data.csv',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [FOLDER_ID],
    }
    media = MediaFileUpload(file_path, mimetype='text/csv')

    if CSV_FILE_ID:
        service.files().update(fileId=CSV_FILE_ID, media_body=media).execute()
    else:
        file = service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        print(f"Uploaded CSV File ID: {file.get('id')}")