from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from env import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
Interview_Guide: AsyncIOMotorDatabase = client["Interview_Guide"]
googleAuth: AsyncIOMotorCollection = Interview_Guide["googleAuth"]
userNotes: AsyncIOMotorCollection = Interview_Guide["userNotes"]
waitList: AsyncIOMotorCollection = Interview_Guide["waitlist"]
blogPostWaitList: AsyncIOMotorCollection = Interview_Guide["blogPostWaitList"]