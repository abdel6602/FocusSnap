from flask import Flask, request
from controllers.auth import Authenticator
from controllers.history import HistoryController
import threading
import random
import time
import pymongo
import atexit
import env

authenticator = Authenticator()
history_controller = HistoryController()
print(env.databaseIP)
connectionString = f'mongodb://{env.databaseIP}/:27017'

app = Flask(__name__)
#check if the key exists in the database
if pymongo.MongoClient(connectionString)["focussnap"]["keyWord"].find_one() == None:
    pymongo.MongoClient(connectionString)["focussnap"]["keyWord"].insert_one({"key": "secret1234"})

# thread function that refreshes the key every 5 minutes
def refresh_key():
    while True:
        pymongo.MongoClient(connectionString)["focussnap"]["keyWord"].update_one({}, {"$set": {"key": "secret" + str(random.randint(1000, 9999))}})
        time.sleep(300)  # Delay for 5 minutes

# Spawn a new thread that runs the refresh key function
thread = threading.Thread(target=refresh_key)
thread.start()

@app.route('/', methods = ['GET'])
def index():
    return {
        "message": "Hello, World!"
    }

@app.route('/api/auth/signup', methods = ['POST'])
def signup_end_point():
    status, error = authenticator.signup(str(request.json['email']), str(request.json['password']))
    if status == True:
        return {
            "message": "User signed up successfully",
            "user_id": str(error)
        }, 201
    else:
        return {
            "message": str(error)
        }, 400

@app.route('/api/auth/login', methods = ['GET','POST'])
def login_end_point():
    status, error = authenticator.login(str(request.json['email']), str(request.json['password']))
    if status == True:
        return {
            "message": "User logged in successfully",
            "session_id": str(error)
        }, 200
    else:
        return {
            "message": str(error)
        }, 400 
    

@app.route('/api/auth/refreshToken', methods = ['GET'])
def Refresh_token_end_point():
    token = request.headers.get('Authorization')
    new_token = authenticator.refresh_token(token)
    return {
        "message": "Token refreshed",
        "session_id": new_token
    }, 200

@app.route('/api/auth/logout', methods = ['GET'])
def logout_end_point():
    token = request.headers.get('Authorization')
    status, error = authenticator.logout(token)
    if status == True:
        return {
            "message": "User logged out successfully"
        }, 200
    else:
        return {
            "message": str(error)
        }, 400
    

def close_cleanup():
    connection = pymongo.MongoClient(connectionString)
    connection["focussnap"]["active-sessions"].delete_many({})
    connection.close() 

atexit.register(close_cleanup)


if __name__ == "__main__":
    app.run(debug=True) 