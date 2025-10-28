from models.user_model import UserModel
from pymongo.errors import DuplicateKeyError

class Crud:
    def __init__(self, db):
        self.db = db

    async def post(self, user: UserModel):
        try:
            await self.db.users.insert_one(user.to_dict())
        except DuplicateKeyError:
            return

    async def get(self, username: str):
        return await self.db.users.find_one({"username": username})

    async def delete(self, username: str):
        return await self.db.users.delete_one({"username": username})
    
    async def put(self, username, user: UserModel):
        result = await self.db.users.update_one(
            {"username": username}, 
            {"$set": user.to_dict()}           
        )
        return {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        } 