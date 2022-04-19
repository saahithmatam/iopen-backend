import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
import csv



fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

door_default = []
door_data = []
kitchen_default = []
kitchen_data = []
presence_list = []

d = 30
k = 30
r = 30

room_list = ["","",""]
x_label = []

room_default = []
room_data = []
count = 0
  
with open('room503.csv', encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            x_label.append(count)
            try:
                if room_list == ['True','False','True'] or room_list == ['True','True','True'] or room_list == ['True','True','False'] or room_list == ['False','True','True'] or room_list == ['False','True','False']:
                    presence = 70
                else:
                    presence = 20
            except:
                print("Error Assigning Presence")
            if rows['col10'] == "D":
                if rows['col4'] == "False":
                    room_list[0] = "False"
                    d = 30
                    door_data.append(d)
                    kitchen_data.append(k)
                    presence_list.append(presence)
                    room_data.append(r)
                    count = count + 1
                elif rows['col4'] == "True":
                    room_list[0] = "True"
                    d = 50
                    door_data.append(d)
                    kitchen_data.append(k)
                    presence_list.append(presence)
                    room_data.append(r)
                    count = count + 1
                else:
                    room_list[0] = "False"
                    d = 30
                    door_data.append(d)
                    kitchen_data.append(k)
                    presence_list.append(presence)
                    room_data.append(r)
                    count = count + 1
            elif rows['col10'] == "M":
                if rows['col4'] == "False":
                    room_list[1] = "False"
                    k = 30
                    kitchen_data.append(k)
                    room_data.append(r)
                    presence_list.append(presence)
                    door_data.append(d)
                    count = count + 1
                elif rows['col4'] == "True":
                    room_list[1] = "True"
                    k = 50
                    kitchen_data.append(k)
                    room_data.append(r)
                    presence_list.append(presence)
                    door_data.append(d)
                    count = count + 1
                else:
                    room_list[1] = "False"
                    k = 30
                    kitchen_data.append(k)
                    room_data.append(r)
                    presence_list.append(presence)
                    door_data.append(d)
                    count = count + 1
            elif rows['col10'] == "MTH":
                if rows['col4'] == "False":
                    room_list[2] = "False"
                    r = 30
                    kitchen_data.append(k)
                    room_data.append(r)
                    presence_list.append(presence)
                    door_data.append(d)
                    count = count + 1
                elif rows['col4'] == "True":
                    room_list[2] = "True"
                    r = 50
                    kitchen_data.append(k)
                    room_data.append(r)
                    presence_list.append(presence)
                    door_data.append(d)
                    count = count + 1
                else:
                    room_list[2] = "False"
                    r = 30
                    kitchen_data.append(k)
                    room_data.append(r)
                    presence_list.append(presence)
                    door_data.append(d)
                    count = count + 1

  
plt.plot(x_label, door_data, color = 'g', linestyle = 'dashed', marker = 'o',label = "Door Data")
plt.plot(x_label, presence_list, color = 'r', linestyle = 'dashed', marker = 'o',label = "Presence Data")
plt.plot(x_label, kitchen_data, color = 'b', linestyle = 'dashed', marker = 'o',label = "Kitchen Data")
plt.plot(x_label, room_data, color = 'y', linestyle = 'dashed', marker = 'o',label = "Living Room Data")
plt.axis([0, len(x_label), 0, 100])


axpos = plt.axes([0.2, .1, .65, .03])

spos = Slider(axpos, 'Pos', 0.0, len(x_label))

def update(val):
    pos = spos.val
    ax.axis([pos,pos+10,0,100])
    fig.canvas.draw_idle()

spos.on_changed(update)

ax.legend()
plt.show()
# plt.plot(x_label, kitchen_data, color = 'b', linestyle = 'dashed',
#          marker = 'o',label = "Kitchen Sensor")
# plt.plot(x_label, room_data, color = 'r', linestyle = 'dashed',
#          marker = 'o',label = "Living Room Sensor")
  
# plt.xticks(rotation = 25)
# plt.xlabel('Time')
# plt.ylabel('True or False')
# plt.title('IOPEN Data Analysis', fontsize = 20)
# plt.grid()
# plt.legend()
# plt.show()