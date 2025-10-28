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

    async def get(self, identifier: str):
        return await self.db.users.find_one({"identifier": identifier})

    async def delete(self, identifier: str):
        return await self.db.users.delete_one({"identifier": identifier})
    
    async def put(self, identifier, user: UserModel):
        result = await self.db.users.update_one(
            {"identifier": identifier}, 
            {"$set": user}           
        )
        return {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        } 