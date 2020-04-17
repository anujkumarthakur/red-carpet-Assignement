from flask import Flask
from flask import jsonify
from flask import flash, request
import psycopg2
import os
import math

'''
database Entities
pincode   address   city_name latitude  longitude accuracy
'''


app = Flask(__name__)


#postres database connection configuration 
def DbConfig():
    conn = psycopg2.connect(user=os.environ["DBUSER"],
                    password=os.environ["DBPASS"],
                    host=os.environ["DBHOST"],
                    port=os.environ["DBPORT"],
                    database=os.environ["DBNAME"])
    return conn

#function is posting data in database by json 
@app.route('/post_location', methods=['POST'])
def PostLocation():
    try:
        json         = request.json
        pincode      = json['pincode']
        address      = json['address']
        city_name    = json['city_name']
        latitude     = json['latitude']
        longitude    = json['longitude']
        accuarcy     = json['accuracy']
        # validate the received values
        if pincode and  address and  city_name and latitude  and longitude and accuracy and request.method == 'POST':
            sql = "INSERT INTO pincode(pincode, address, city_name, latitude, longitude, accuracy) VALUES(%s, %s, %s, %s, %s,%s)"
            sql1 = "SELECT * FROM pincode WHERE pincode = %s"
            data = (pincode, address, city_name, latitude, longitude, accuracy)
            conn = DbConfig()
            cursor = conn.cursor()

            cursor.execute(sql1, data[0])
            result = cursor.fetchone()
            if result == None:
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('Data added successfully!')
                resp.status_code = 200
                return resp
            else:
                return not_found()
    except Exception as e:
        print(e)

#function is getting specifice lat,long data
@app.route('/get_location/<float:lat>/<float:long>', methods=['GET'])
def GetLocation(lat, long):
    try:
        conn = conn = DbConfig()
        cursor = conn.cursor()
        sql = "SELECT * from pincode WHERE latitude=%s and longitude=%s"
        cursor.execute(sql, (lat, long))
        row = cursor.fetchone()
        resp = jsonify([row])
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#haversone algorithm for calculate distnace betweeen two earth point
@app.route('/radius/<float:lat1>/<float:long1>/<int:distance>', methods=['GET'])
def Radius(lat1,long1, distance):
    neareast_location = []
    try:
        conn = DbConfig()
        cursor = conn.cursor()
        sql = "SELECT count(*) from pincode"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result is not None:
            sql = "SELECT latitude, longitude from pincode"
            cursor.execute(sql)
            result = cursor.fetchone()
            lat2 = float(result[0])
            long2 = float(result[1])

            dLat = (lat2 - lat1) * math.pi / 180.0
            dLon = (lon2 - lon1) * math.pi / 180.0
            lat1 = (lat1) * math.pi / 180.0
            lat2 = (lat2) * math.pi / 180.0

            a = (pow(math.sin(dLat / 2), 2) +
                    pow(math.sin(dLon / 2), 2) *
                    math.cos(lat1) * math.cos(lat2));
            rad = 6371
            c = 2 * math.asin(math.sqrt(a))
            if(rad * c <= distance):
                sql = "SELECT * FROM pincode where latitude=%s and longitude=%s"
                value = (lat2, long2)
                cursor.execute(sql, value)
                result = cursor.fetchone()
                neareast_location.append(result)
        resp = jsonify(neareast_location)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

#404 Error
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()
