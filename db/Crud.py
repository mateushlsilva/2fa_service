from models.user_model import UserModel
from core.deps import get_db

class Crud:
    def __init__(self):
        self.db = get_db

    async def post(self, user: UserModel):
        await self.db.users.insert_one(user.to_dict())

    async def get(self, username: str):
        return await self.db.users.find_one({"username": username})

    async def delete(self, username: str):
        return await self.db.users.delete_one({"username": username})
    
    async def put(self, username, user: UserModel):
        result = await self.db.users.update_one(
            {"username": username}, 
            {"$set": user}           
        )
        return {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        } 