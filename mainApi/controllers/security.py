from cryptography.fernet import Fernet
import pymongo
import env 

def get_key():
    key = pymongo.MongoClient(f'mongodb://{env.databaseIP}:27017/')["focussnap"]["key"].find_one()
    if key:
        return key['key']
    else:
        key = Fernet.generate_key()
        pymongo.MongoClient(f'mongodb://{env.databaseIP}:27017/')["focussnap"]["key"].insert_one({"key": key})
        return key
    

def encrypt(data):
    f = Fernet(get_key())
    return f.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt(data):
    f = Fernet(get_key())
    return f.decrypt(data.encode('utf-8')).decode('utf-8')