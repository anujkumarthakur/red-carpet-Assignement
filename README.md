                        ----------------Interview Stage 1-----------------
        create a new table in postgres and load this CSV that denotes the mapping between pincode and lat/long 
        (https://github.com/sanand0/pincode/blob/master/data/IN.csv).

        Create Two APIs  : Get,Post.
        Post api - /post_location : Post lat,lng of any location with pin code+address+city. This api will add new pin code in db.  
        IMPORTANT: Remember to check if pin code alrelow eady exists or if there are existing latitude+longitude THAT ARE CLOSE ENOUGH 
        TO BE THE SAME (dont assume that they will exactly be the same.)
 
        Get api - /get_location : Given lat,lng ... it will fetch pin code, address, city as a json response.
 
        Write testcases using pytest.

        Answer-1:
        step-1: create database pincode;
        
        step-2: \c pincode
        
        step-3: create table pincode(id serial NOT NULL, pincode varchar(20) ,address varchar(100), 
                city_name varchar(100), latitude float, longitude float, accuracy float); 
        
        step-4: COPY pincode(pincode, address, city_name, latitude, longitude, accuracy) 
                FROM '/home/anuj/Desktop/red-carpet/IN.csv' DELIMITER ',' CSV HEADER;
        
        step-5: create run_script.sh file and put below db text        
                export DBUSER="postges-username"
                export DBPASS="password"
                export DBHOST="hostname"
                export DBPORT="port-name"
                export DBNAME="database-name"
                
                python3 main.py
       step-6: chmod +x run_script.sh
       step-7: ./run_script
       
       step-8: you can try to use postman
               example-ubuntu terminal-:
                GET   curl localhost:5000/get_location/lat/long 
                POST  curl localhost:5000/post_location
                    {
                        "pincode":"IN/1234"
                        "address":""
                        "city_name":""
                        "latitude":""
                        "longitude":""
                        "accuracy":""
                    }

                  ---------------------Interview Stage 2------------------------
        You will write the following functionality : Given a location, fetch all the nearby pin codes 
        within a radius. For example, I can ask - give me all points within 5km radius of (45.12, 71.12) .
 
        To do this you will need to do mathematical computation of radius. 
        there are two ways to do this. So you will create two different api:
        1.  /get_using_postgres - You can use postgres "earthdistance" to compute all points in 5km radius
        2. /get_using_self - Implement the mathematical computation yourself.  
 
        Write testcases using Pytest. Importantly, test+compare results between /get_using_postgres and /get_using_self.
 
        Answer-2:
        I have choosed second option and solved by Haversign formula

        example - :
                    localhost:5000/radius/lat1/long2/<int:5 or 6 or etc..>

                        --------Interview Stage 3--------
        a Geojson is a json file which defines shapes of locations - for example the shape of delhi, gurgaon, etc.
 
        https://gist.github.com/ramsingla/6202001?short_path=7d9a995 - This geojson is used to define delhi and its areas.
        NOTE: you can check it out by going to http://geojson.io and pasting the raw json on the right side (on tab marked JSON).
 
        Write code to parse this json, and load the boundaries latitude and longitude (geometry -> coordinates) 
        into postgresql in a new table. IMPORTANT: you can use any database/table structure ... but remember that
        one place (like "Delhi") will have lots of lat/long (because it marks the boundaries).
        Write a new API "/detect" : It will take input as latitude + longitude, it will tell you which place it falls within.

        Answer-3:
        I Wrote seperate read.py and json_read.sh file
        in this repo there are two .sh binary file you just open two terminal and run
        terminal- ./run_script
        terminal- ./json_read
        example-:
            localhost:5000/detect/{lat}/{long}

