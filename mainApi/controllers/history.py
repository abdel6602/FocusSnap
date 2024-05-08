import pymongo

class HistoryController :
    def __init__(self):
        self.db = pymongo.MongoClient("mongodb://localhost:27017/")["focussnap"]