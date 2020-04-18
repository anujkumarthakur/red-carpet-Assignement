#this program is reading data from location json file and inserting usefull data in DB
#Entities-:
#       Id, City_name, Type, Parent_city, City_shape, Latitude, Longigute

import json 
import psycopg2
import os

#postres database connection configuration 
def DbConfig():
    conn = psycopg2.connect(user=os.environ["DBUSER"],
                    password=os.environ["DBPASS"],
                    host=os.environ["DBHOST"],
                    port=os.environ["DBPORT"],
                    database=os.environ["DBNAME"])
    return conn

#loda json file 
f = open('location.json',)
data = json.load(f)
for cord in data['features']:
    val = []
    properties      = cord["properties"]
    geometry        = cord["geometry"]
    for value in properties.values():
        val.append(value)
    print(val)                        #3. city_name, type, parent_city
    print(geometry["type"])           #1. shape
    shape = geometry["type"]
    conn = DbConfig()
    cursor = conn.cursor()
    for i in range(len(geometry["coordinates"][0])):
        lat_long= geometry["coordinates"][0][i]
        sql = "INSERT INTO location(city_name, type, parent_city, city_shape, latitude, longitude) VALUES(%s, %s, %s, %s, %s,%s)"
        data_val = (val[0], val[1], val[2], shape,lat_long[0], lat_long[1])
        cursor.execute(sql, data_val)
        conn.commit()
    print("Record Inserted!")
# Closing file 
f.close() 


'''
create table location(id serial primary key, city_name varchar(100), type varchar (100),
parent_city varchar(100),  city_shape varchar(100), latitude float, longitude float);
'''
