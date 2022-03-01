from flask import Flask, json,render_template,request,redirect
import flask
import csv
from pymongo import MongoClient
import certifi
import json
import requests
from requests.auth import HTTPBasicAuth
import time
import datetime
from datetime import date
from datetime import datetime
from difflib import SequenceMatcher
import datetime
import uuid
from bson.objectid import ObjectId





conn = MongoClient('mongodb+srv://saahith:ricky123@cluster0.z2bzi.mongodb.net/test',tlsCAFile=certifi.where())
print("Connected successfully!!!")

today = str(date.today())
run = str(datetime.datetime.now().time())
test = run.split('.')

current_time = test[0]

db = conn['dev']
collection_hotels = db.hotels
collection_passwords = db.passwords
collection_users = db.users

app = Flask(__name__)
YOUR_DOMAIN = 'http://localhost:3000'



@app.route('/customerportal/<room_number>')
def customerportal(room_number):
    #mongo instance to retrieve data needed
    try:
        query = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                sort:[2]
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        #change
        query_door = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                sort: [2]
                filter2: "rooms_sensors.role != '' && DataType == 'DoorData' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        query_temp = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                sort:[2]
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` && DataType == 'TemperatureData' && PlotLabel == 'Fahrenheit' "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        basic = HTTPBasicAuth('utd1', 'NhWv0dEW')


        url = 'https://utd1.safestay365.com/graphql'
        json_query = { 'query' : query }
        json_temp_query = {'query' : query_temp }
        json_door_query = {'query' : query_door } #change

        headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                        }

        r = requests.post(url=url, json=json_query, headers=headers, auth=basic)
        t = requests.post(url=url, json=json_temp_query, headers=headers, auth=basic)
        d = requests.post(url=url, json=json_door_query, headers=headers, auth=basic) #change

        data = json.loads(r.text)
        data_t = json.loads(t.text)
        data_d = json.loads(d.text) #change

        data_room = data['data']['dataset']['streams']['messages']['report']['rows']
        data_temp = data_t['data']['dataset']['streams']['messages']['report']['rows']
        data_door = data_d['data']['dataset']['streams']['messages']['report']['rows']#change

        roomdata = data_room[-1]

        try:
            roomdata_temp = data_temp[-1]
            temp_list = str(roomdata_temp[3]).split('.')
            temperature = int(temp_list[0])
        except:
            temperature = "Unknown"

        try:
            roomdata_door = data_door[-1] #change
        except:
            door = "Unknown"

        print(roomdata_door)
        
        string_data = str(roomdata_door[1])

        
        #change for real
        if roomdata_door[3] == True:
            door = "CLOSED"
        elif roomdata_door[3] == False:
            door = "OPEN"
        else:
            door = "OPEN"

        if(len(string_data)==6):
            if int(string_data[:2]) > 12:
                real_time = str(int(string_data[:2])-12) + ":{}".format(string_data[2:4]) + " PM"
            else:
                real_time = string_data[:2] + ":{}".format(string_data[2:4]) + " AM"
            room = {
                'floor': roomdata[-3],
                'motion': roomdata[3],
                'room': roomdata[-2],
                'role': roomdata[-1],
                'time': real_time,
                'temperature': temperature,
                'door': door #change


                }
        else:
            real_time = string_data[:1] + ":{}".format(string_data[1:3]) + " AM"
            room = {
                'floor': roomdata[-3],
                'motion': roomdata[3],
                'room': roomdata[-2],
                'role': roomdata[-1],
                'time': real_time,
                'temperature': temperature,
                'door': door #change
            }
 
        return room
    except:
        query = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        #change
        query_door = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                filter2: "rooms_sensors.role != '' && DataType == 'DoorData' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today) 
        query_temp = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` && DataType == 'TemperatureData' && PlotLabel == 'Fahrenheit' "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        basic = HTTPBasicAuth('utd1', 'NhWv0dEW')


        url = 'https://utd1.safestay365.com/graphql'

        json_query = { 'query' : query }
        json_temp_query = {'query' : query_temp }
        json_door_query = {'query' : query_door } #change


        headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                        }

        r = requests.post(url=url, json=json_query, headers=headers, auth=basic)
        t = requests.post(url=url, json=json_temp_query, headers=headers, auth=basic)
        d = requests.post(url=url, json=json_door_query, headers=headers, auth=basic) #change


        data = json.loads(r.text)
        data_t = json.loads(t.text)
        data_d = json.loads(d.text) #change

        data_room = data['data']['dataset']['streams']['messages']['report']['rows']
        data_temp = data_t['data']['dataset']['streams']['messages']['report']['rows']
        data_door = data_d['data']['dataset']['streams']['messages']['report']['rows']#change


        try:
            roomdata_door = data_door[-1] #change
            roomdata_temp = data_temp[-1]
            roomdata = data_room[-1]

            temp_list = str(roomdata_temp[3]).split('.')
            temperature = int(temp_list[0])
            string_data = str(roomdata_door[1])

            if roomdata_door[3] == True:
                door = "CLOSED"
            elif roomdata_door[3] == False:
                door = "OPEN"
            else:
                door = "OPEN"

            if(len(string_data)==6):
                if int(string_data[:2]) > 12:
                    real_time = str(int(string_data[:2])-12) + ":{}".format(string_data[2:4]) + " PM"
                else:
                    real_time = string_data[:2] + ":{}".format(string_data[2:4]) + " AM"
                room = {
                    'floor': roomdata[-3],
                    'motion': roomdata[3],
                    'room': roomdata[-2],
                    'role': roomdata[-1],
                    'time': real_time,
                    'temperature': temperature

                    }
            else:
                real_time = string_data[:1] + ":{}".format(string_data[1:3]) + " AM"
                room = {
                    'floor': roomdata[-3],
                    'motion': roomdata[3],
                    'room': roomdata[-2],
                    'role': roomdata[-1],
                    'time': real_time,
                    'temperature': temperature,
                    'door':door,
                }
        except:
            room = {
                    'floor': "Not Active",
                    'motion': "Not Active",
                    'room': "Not Active",
                    'role': "Not Active",
                    'time': "Not Active",
                    'temperature': "Not Active",
                    'door': "Not Active"
                }
 
        return room
@app.route('/floorinfo/<floor_number>')
def floor_json(floor_number):
    sample = collection_hotels.find_one()
    sample_data = sample['data'][floor_number]
    floor_json = json.dumps(sample_data)
    return floor_json

    

@app.route('/roominfo/<room_number>')
def roomnumber(room_number):
    try:
        query = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                sort:[2]
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        #change
        query_door = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                sort: [2]
                filter2: "rooms_sensors.role != '' && DataType == 'DoorData' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        query_temp = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                sort:[2]
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` && DataType == 'TemperatureData' && PlotLabel == 'Fahrenheit' "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        basic = HTTPBasicAuth('utd1', 'NhWv0dEW')


        url = 'https://utd1.safestay365.com/graphql'
        json_query = { 'query' : query }
        json_temp_query = {'query' : query_temp }
        json_door_query = {'query' : query_door } #change

        headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                        }

        r = requests.post(url=url, json=json_query, headers=headers, auth=basic)
        t = requests.post(url=url, json=json_temp_query, headers=headers, auth=basic)
        d = requests.post(url=url, json=json_door_query, headers=headers, auth=basic) #change

        data = json.loads(r.text)
        data_t = json.loads(t.text)
        data_d = json.loads(d.text) #change

        data_room = data['data']['dataset']['streams']['messages']['report']['rows']
        data_temp = data_t['data']['dataset']['streams']['messages']['report']['rows']
        data_door = data_d['data']['dataset']['streams']['messages']['report']['rows']#change

        password_data = collection_passwords.find_one()
        pass_data = password_data["data"]
        room_key = ""
        user = ""

        for key, value in pass_data.items():
            if room_number == key:
                room_key = value
                break
            else:
                room_key = "No Password"

        try:
            data_user = collection_users.find_one({"data.room":room_number})
            user = data_user["data"]["lastname"]     
        except:
            user = "No User"

        def training():
            d = True
            m = False
            mth = False
            room = []
                    
            for rows in data_room:
                if rows[-1] == 'M':
                    m = rows[-7]
                elif rows[-1] == 'MTH':
                    mth = rows[-7]
                else:
                    d = rows[-7]

            room = [d,m,mth]       

            return room  

        def presence():
            presence = False
            room_list = training()
            print(room_list)

            if room_list == ['True','False','True'] or room_list == ['True','True','True'] or room_list == ['True','True','False'] or room_list == ['False','True','True'] or room_list == ['False','True','False']:
                presence = True
            else:
                presence = False

            return presence    

        try:
            print("Presence: "+ str(presence()))
        except:
            print("Presence not detected!")



        roomdata = data_room[-1]

        try:
            roomdata_temp = data_temp[-1]
            temp_list = str(roomdata_temp[3]).split('.')
            temperature = int(temp_list[0])
        except:
            temperature = "Unknown"

        try:
            roomdata_door = data_door[-1] #change
        except:
            door = "Unknown"

        print(roomdata_door)
        string_data = str(roomdata_door[1])

        if roomdata_door[3] == 'True':
            door = "CLOSED"
        elif roomdata_door[3] == 'False':
            door = "OPEN"
        else:
            door = "OPEN"


        if(len(string_data)==6):
            if int(string_data[:2]) == 12:
                real_time = string_data[:2] + ":{}".format(string_data[2:4]) + " PM"
            elif int(string_data[:2]) > 12:
                real_time = str(int(string_data[:2])-12) + ":{}".format(string_data[2:4]) + " PM"
            else:
                real_time = string_data[:2] + ":{}".format(string_data[2:4]) + " AM"
            room = {
                'floor': roomdata[-3],
                'user': user,
                'key': room_key,
                'motion': str(presence()),
                'room': roomdata[-2],
                'role': roomdata[-1],
                'time': real_time,
                'temperature': temperature,
                'door': door #change


                }
        else:
            if string_data[:1] == 0:
                real_time = "12" + ":{}".format(string_data[1:3]) + " AM"
            else:
                real_time = string_data[:1] + ":{}".format(string_data[1:3]) + " AM"
            room = {
                'floor': roomdata[-3],
                'user': user,
                'key': room_key,
                'motion': str(presence()),
                'room': roomdata[-2],
                'role': roomdata[-1],
                'time': real_time,
                'temperature': temperature,
                'door': door #change
            }
 
        return room
    except:
        query = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        #change
        query_door = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                filter2: "rooms_sensors.role != '' && DataType == 'DoorData' && room.name == '%s' && MessageDate.date >= `%s` "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today) 
        query_temp = """
        query {
        dataset {
            streams {
            messages {
                report(
                cores: 10
                dims: "DataMessageGUID"
                vals: "MessageDate.time, DataType, DataValue, PlotLabel, Battery, SignalStrength, floor.name, room.name, rooms_sensors.role"
                filter2: "rooms_sensors.role != '' && room.name == '%s' && MessageDate.date >= `%s` && DataType == 'TemperatureData' && PlotLabel == 'Fahrenheit' "
                ) {
                size
                rows(take: -1)
                }
            }
            }
        }
        }
        """ % (room_number,today)
        basic = HTTPBasicAuth('utd1', 'NhWv0dEW')


        url = 'https://utd1.safestay365.com/graphql'

        json_query = { 'query' : query }
        json_temp_query = {'query' : query_temp }
        json_door_query = {'query' : query_door } #change


        headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                        }

        r = requests.post(url=url, json=json_query, headers=headers, auth=basic)
        t = requests.post(url=url, json=json_temp_query, headers=headers, auth=basic)
        d = requests.post(url=url, json=json_door_query, headers=headers, auth=basic) #change


        data = json.loads(r.text)
        data_t = json.loads(t.text)
        data_d = json.loads(d.text) #change

        data_room = data['data']['dataset']['streams']['messages']['report']['rows']
        data_temp = data_t['data']['dataset']['streams']['messages']['report']['rows']
        data_door = data_d['data']['dataset']['streams']['messages']['report']['rows']#change

        for key, value in pass_data.items():
            if room_number == key:
                room_key = value
                break
            else:
                room_key = "No Password"
        try:
            data_user = collection_users.find_one({"data.room":room_number})
            user = data_user["data"]["lastname"]
            print("IT WORKED",str(user))
            
        except:
            print("IT DID NOT WORK")
            user = "No User"

        def training():
            d = True
            m = False
            mth = False
            room = []
                    
            for rows in data_room:
                if rows[-1] == 'M':
                    m = rows[-7]
                elif rows[-1] == 'MTH':
                    mth = rows[-7]
                else:
                    d = rows[-7]

            room = [d,m,mth]       

            return room  

        def presence():
            presence = False
            room_list = training()
            print(room_list)

            if room_list == ['True','False','True'] or room_list == ['True','True','True'] or room_list == ['True','True','False'] or room_list == ['False','True','True'] or room_list == ['False','True','False']:
                presence = True
            else:
                presence = False

            return presence    

        try:
            print("Presence: "+ str(presence()))
        except:
            print("Presence not detected!")

        try:
            roomdata_door = data_door[-1] #change
            roomdata_temp = data_temp[-1]
            roomdata = data_room[-1]

            temp_list = str(roomdata_temp[3]).split('.')
            temperature = int(temp_list[0])
            string_data = str(roomdata_door[1])

            print(roomdata_door[3])
            print(roomdata_door)

            if roomdata_door[3] == 'True':
                door = "CLOSED"
            elif roomdata_door[3] == 'False':
                door = "OPEN"
            else:
                door = "OPEN"

            if(len(string_data)==6):
                if int(string_data[:2]) > 12:
                    real_time = str(int(string_data[:2])-12) + ":{}".format(string_data[2:4]) + " PM"
                else:
                    real_time = string_data[:2] + ":{}".format(string_data[2:4]) + " AM"
                room = {
                    'floor': roomdata[-3],
                    'user': user,
                    'key': room_key,
                    'motion': str(presence()),
                    'room': roomdata[-2],
                    'role': roomdata[-1],
                    'time': real_time,
                    'temperature': temperature

                    }
            else:
                real_time = string_data[:1] + ":{}".format(string_data[1:3]) + " AM"
                room = {
                    'floor': roomdata[-3],
                    'user': user,
                    'key': room_key,
                    'motion': str(presence()),
                    'room': roomdata[-2],
                    'role': roomdata[-1],
                    'time': real_time,
                    'temperature': temperature,
                    'door':door,
                }
        except:
            room = {
                    'floor': "Not Active",
                    'user': user,
                    'key': room_key,
                    'motion': "Not Active",
                    'room': "Not Active",
                    'role': "Not Active",
                    'time': "Not Active",
                    'temperature': "Not Active",
                    'door': "Not Active"
                }
 
        return room


@app.route('/roominfo', methods=['POST'])
def roominfo():
    var = request.form.get('roominfo')
    return redirect('/roominfo/{}'.format(var))
@app.route('/floorinfo', methods=['POST'])
def floorinfo():
    var = request.form.get('floorinfo')
    return redirect('/floorinfo/{}'.format(var))




@app.route('/createdhotelportal', methods = ['GET'])
def getdata():
    hotel = collection_hotels.find_one()
    hotel_json = hotel['data']
    def getList(hotel_json):
        return list(hotel_json.keys())
    hotel_json_temp = getList(hotel_json)
    print(hotel_json_temp)
    hotel_jsonreal = json.dumps(hotel_json_temp)
    return hotel_jsonreal
    

@app.route('/createportal')
def home():
    return render_template('createportal.html')

@app.route('/hotelportal')
def hotelportal():
    return render_template('hotelportal.html')

@app.route('/usersignin', methods=['POST'])
def usersignin():
    password = request.form.get("pass")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    departure_date = request.form.get("date")

    room = ""
    user = {}
    incorrect = "Incorrect Password"
    data_passwords = collection_passwords.find_one()
    data_pass = data_passwords["data"]

    for key, value in data_pass.items():
            if password == value:
                room = key
                break
            else:
                room = incorrect

    if room != incorrect:
        user['firstname'] = firstname
        user['lastname'] = lastname
        user['depart_date'] = departure_date
        user['room'] = room
        collection_users.insert_one({'data': user})
    else:
        room = incorrect
    
    if room == incorrect:
        return redirect('http://localhost:3000/error')
    else:
        return redirect('http://localhost:3000/customerportal/{}'.format(room))

@app.route('/createhotelportal', methods = ['POST'])
def createhotelportal():
    data = {}
    # Open a csv reader called DictReader
    with open(request.form.get('myfile'), encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary keyx
            try:
                if(rows['col9'] not in data[str(rows['col9'])[:1]]):
                    data[str(rows['col9'])[:1]].append(str(rows['col9']))
            except:
                data[str(rows['col9'])[:1]] = []
                data[str(rows['col9'])[:1]].append(str(rows['col9']))
            
    for key in data:
        for el in range(0, len(data[key])):
            data[key][el] = int(data[key][el])
        data[key].sort()

            # if(rows['col9'] in data):
            #     pass
            # else:
            #     data.append(rows['col9'])
    
    print(data)
    #insert password generation code here
    pass_dict = {}

    i = str(uuid.uuid4())
    password = i.split('-')[0]
    print(password)
    print(type(password))


    for floor in data:
        for room in data[floor]:
            str_room = str(room)
            uid = str(uuid.uuid4())
            password = uid.split('-')[0]
            pass_dict[str_room] = password
    
    collection_passwords.insert_one({"data":pass_dict,"id":"hotelpasswords"})
    collection_hotels.insert_one({"data":data})
    return redirect(YOUR_DOMAIN+"/hotelportal")


@app.route('/create-portal', methods=['POST'])
def createportaljs():
    success_url=YOUR_DOMAIN + '?success=true&session_id=create-portal',
    return redirect(success_url, code=303)

@app.route('/refreshuser', methods=['POST'])
def refreshuser():
    room = request.form.get("roominfo")
    print(room)
    uid = str(uuid.uuid4())
    password = uid.split('-')[0]
    print(password)
    collection_passwords.update_one(
            {"id": "hotelpasswords"},
            {"$set":
             {"data.{}".format(room):password}}
        )
    collection_users.delete_many({"data.room":room})
    return redirect('http://localhost:3000/hotelportal')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')