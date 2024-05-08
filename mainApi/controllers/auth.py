import re
import pymongo
import bcrypt
from .security import encrypt, decrypt
from datetime import datetime, timedelta
from bson.objectid import ObjectId

class Authenticator:
    def __init__(self):
        self.db = pymongo.MongoClient("mongodb://172.17.0.1:27017/")["focussnap"]


    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def signup(self, email, password):
        #check if the email is valid temporarily
        if re.search("^([^\s@]+@[^\s@]+\.[^\s@]+)$", email):
            #check if the user already exists
            try:
                if self.db['users'].find_one({"email" : email}):
                    return False, "user already exists"
            except:
                print("failed")     
            else: 
                hashed_password = self.hash_password(password)
                user = self.db['users'].insert_one({"email": email, "password": hashed_password})
                return True, user.inserted_id
        else:
            return False, "invalid email address"
    
    def login(self, email, password):
        #check if the email is valid temporarily
        if re.search("^([^\s@]+@[^\s@]+\.[^\s@]+)$", email):
            user = self.db['users'].find_one({"email": email})
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                    #create a session token and return it
                    current_keyWord = self.db["keyWord"].find_one()
                    current_key = current_keyWord['key'][-4:]
                    token = encrypt(str(user['_id'])) + current_key
                    timestamp = datetime.utcnow()
                    self.db["active-sessions"].insert_one({
                        "user_id": user['_id'],
                        "token": token,
                        "last_refresh": timestamp
                    })

                    return True, token
                else:
                    return False, "incorrect password"
            else:
                return False, "user does not exist"
        else:
            return False, "invalid email address"
        

    def refresh_token(self, old_token):
        user_id = old_token[:-4]
        decrypted_id = decrypt(user_id)
        new_keyword = self.db["keyWord"].find_one()['key'][-4:]
        new_token = encrypt(decrypted_id) + str(new_keyword)
        self.db["active-sessions"].update_one({user_id: ObjectId(decrypted_id)}, {"$set": {"token": new_token, "last_refresh": datetime.utcnow()}})
        return new_token
    
    
    def verify_token(self, token):
        user_id = token[:-4]
        decrypted_id = decrypt(user_id)
        user = self.db["active-sessions"].find_one({"user_id": decrypted_id})
        if user:
            if user['last_refresh'] < datetime.utcnow() + timedelta(minutes=30):
                return True, None
            return False, None
        else:
            return False, "user not online"

    def logout(self, token):
        user_id = token[:-4]
        decrypted_id = decrypt(user_id)
        try:
            self.db["active-sessions"].delete_one({"user_id": ObjectId(decrypted_id)})
            return True, None
        except:
            return False, "user not online"