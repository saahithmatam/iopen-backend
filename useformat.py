from pymongo import MongoClient
import certifi
import json
import uuid
from bson.objectid import ObjectId

conn = MongoClient('mongodb+srv://saahith:ricky123@cluster0.z2bzi.mongodb.net/test',tlsCAFile=certifi.where())
db = conn['dev']
collection_hotels = db.hotels
collection_passwords = db.passwords
collection_users = db.users


def activeusers():
    data = []
    data_users = collection_users.find({})
    count=1;
    print(str(data_users))
    for user in data_users:
        user_dict = {}
        user_dict['id']= count
        user_dict['name']=user['data']['firstname']+" "+user['data']['lastname']
        user_dict['room']= user['data']['room']
        user_dict['dateCreated']= user['data']['date']
        user_dict['time']= user['data']['time']
        data.append(user_dict)
        count = count + 1
    activeofficialusers = json.dumps(data)
    return activeofficialusers


print(activeusers())