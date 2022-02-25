import csv


def training(var):
    d = True
    m = False
    mth = False
    room = []
    with open(var, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            
            for rows in csvReader:
                if rows['col10'] == 'M':
                    m = rows['col4']
                elif rows['col10'] == 'MTH':
                    mth = rows['col4']
                else:
                    d = rows['col4']

            room = [d,m,mth]       

    return room       
                
def presence(file):
    presence = False
    room_list = training(file)
    print(room_list)

    if room_list == ['True','False','True'] or room_list == ['True','True','True'] or room_list == ['True','True','False'] or room_list == ['False','True','True'] or room_list == ['False','True','False']:
        presence = True
    else:
        presence = False

    return presence

print("Presence: "+ str(presence('Training.csv')))