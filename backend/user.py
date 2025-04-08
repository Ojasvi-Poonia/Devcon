from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel,EmailStr
from typing import List, Optional
from bson import ObjectId
from database import user_collection
from auth import get_current_user
from datetime import datetime
from fastapi.encoders import jsonable_encoder

router = APIRouter()

class SocialLinks(BaseModel):
    github: Optional[str]= None
    linkedIn: Optional[str]= None
    leetcode: Optional[str]= None
    twitter: Optional[str]= None

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str]= None
    skills: Optional[list[str]]= None
    college: Optional[str]= None
    experience: Optional[str]= None
    social: Optional[SocialLinks]= None
    profile_picture: Optional[str]= None
@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    user = await user_collection.find_one({"email": current_user["email"]})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404,detail="User not found")
@router.put("/update")
async def update_profile(data: UserProfileUpdate, current_user: dict = Depends(get_current_user)):
    update_data = {k: v for k,v in data.dict(exclude_unset=True).items()}
    update_data["updated_at"] = datetime.utcnow()
    result = await user_collection.update_one(
        {"email": current_user["email"]},
        {"$set": update_data}
    )
    if result.modified_count== 1:
        updated_user = await user_collection.find_one({"email": current_user["email"]})
        if updated_user:
            updated_user["_id"] = str(updated_user["_id"])
            return updated_user
        return {"message":"Profile updated"}
    return {"message":"No changes made"}
@router.delete("/delete")
async def delete_profile(current_user: dict = Depends(get_current_user)):
    result = await user_collection.delete_one({"email":current_user["email"]})
    if result.deleted_count == 1:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404,detail="User not found")
@router.get("/all")
async def get_all_users():
    users = []
    async for user in user_collection.find():
        user["_id"] = str(user["_id"])
        user_data = {
            "_id": user["_id"],
            "name": user.get("name"),
            "bio": user.get("bio"),
            "skills": user.get("skills"),
            "college": user.get("college"),
            "social": user.get("social"),
            "profile_picture": user.get("profile_picture")
        }
        users.append(user_data)
    return users
@router.get("/{user_id}")
async def get_user_by_id(user_id: str):
    try:
        object_id = ObjectId(user_id)
        user = await user_collection.find_one({"_id": object_id})
        if user:
            user["_id"] = str(user["_id"])
            return{
                "_id": user["_id"],
                "name": user.get("name"),
                "bio": user.get("bio"),
                "skills": user.get("skills"),
                "college": user.get("college"),
                "social": user.get("social"),
                "profile_picture": user.get("profile_picture")
            }
        raise HTTPException(status_code=404, detail="User not found")
    except :
        raise HTTPException(status_code=404, detail="Invalid user id format")
