# models/script.py
from datetime import datetime
from bson.objectid import ObjectId

class Script:
    def __init__(self, mongo):
        self.mongo = mongo
        self.collection = mongo.db.scripts
    
    def create(self, user_id, title, content, tone="informative"):
        script = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "tone": tone,
            "length": len(content.split()),
            "created_at": datetime.utcnow()
        }
        return self.collection.insert_one(script).inserted_id
    
    def find_by_user(self, user_id):
        return list(self.collection.find({"user_id": user_id}).sort("created_at", -1))
    
    def find_by_id(self, script_id, user_id=None):
        query = {"_id": ObjectId(script_id)}
        if user_id:
            query["user_id"] = user_id
        return self.collection.find_one(query)