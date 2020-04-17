                             --------Interview Stage 1--------
        create a new table in postgres and load this CSV that denotes the mapping between pincode and lat/long 
        (https://github.com/sanand0/pincode/blob/master/data/IN.csv).

        Create Two APIs  : Get,Post.
        Post api - /post_location : Post lat,lng of any location with pin code+address+city. This api will add new pin code in db.  
        IMPORTANT: Remember to check if pin code already exists or if there are existing latitude+longitude THAT ARE CLOSE ENOUGH 
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
