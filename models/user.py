# models/user.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User:
    def __init__(self, mongo):
        self.mongo = mongo
        self.collection = mongo.db.users
    
    def create(self, email, password, name=""):
        user = {
            "email": email,
            "password": generate_password_hash(password),
            "name": name,
            "created_at": datetime.utcnow()
        }
        return self.collection.insert_one(user).inserted_id
    
    def find_by_email(self, email):
        return self.collection.find_one({"email": email})
    
    def find_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})
    
    def verify_password(self, user, password):
        return check_password_hash(user["password"], password)