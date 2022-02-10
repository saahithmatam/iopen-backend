from flask import Flask, json,render_template,request,redirect
import csv
from pymongo import MongoClient
import certifi
import json

try:
    conn = MongoClient('mongodb+srv://4485:4485123@cluster0.z2bzi.mongodb.net/test',tlsCAFile=certifi.where())
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn['dev']
collection_hotels = db.hotels

app = Flask(__name__)
YOUR_DOMAIN = 'http://localhost:3000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roominfo',methods=['GET','POST'])
def roominfo():
    var = request.form.get('roominfo')
    print(str(var))
    print("This is the NUMBER")
    hotel = collection_hotels.find_one()
    hotel_room = hotel['data']
    for i in hotel_room:
        if(i['RoomNumber']==var):
            hotel_room_object = i
            break
    hotel_room_json = json.dumps(hotel_room_object)
    return hotel_room_json

@app.route('/createdhotelportal', methods = ['GET','POST'])
def getdata():
    hotel = collection_hotels.find_one()
    hotel_json = hotel['data']
    hotel_jsonreal = json.dumps(hotel_json)
    return hotel_jsonreal

@app.route('/createportal')
def home():
    return render_template('createportal.html')

@app.route('/hotelportal')
def hotelportal():
    return render_template('hotelportal.html')

@app.route('/createhotelportal', methods = ['POST'])
def createhotelportal():
    data = []
     
    # Open a csv reader called DictReader
    with open(request.form.get('myfile'), encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            data.append(rows)
    collection_hotels.insert_one({"data":data})
    print(str(data))
    return redirect(YOUR_DOMAIN)


@app.route('/create-portal', methods=['POST'])
def createportaljs():
    success_url=YOUR_DOMAIN + '?success=true&session_id=create-portal',
    return redirect(success_url, code=303)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')