from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCESS_KEY = os.getenv("ACCESS_KEY")
UPDATE_CSV_KEY = os.getenv("UPDATE_CSV_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")
CSV_FILE_ID = os.getenv("CSV_FILE_ID")
GOOGLEAPIDRIVE = os.getenv("GOOGLEAPIDRIVE")
SECRET_KEY=os.getenv("SECRET_KEY")
YOUR_GOOGLE_CLIENT_ID=os.getenv("YOUR_GOOGLE_CLIENT_ID")
MONGO_URI=os.getenv("MONGO_URI")