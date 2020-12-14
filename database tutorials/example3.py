import time
from datetime import datetime
import random
import mysql.connector
from mysql.connector import Error
from ConfigParser import ConfigParser
#---------for image --------
import sys
from PIL import Image
import base64
import cStringIO
import PIL.Image


#Create Table
def mysql_table(DataBase_name):
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = DataBase_name
                                    )
    

    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS RK_Ashram_marg 
                    (   id INT(11) , 
                        Tree_code VARCHAR(255) NOT NULL, 
                        Date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        common_name VARCHAR(255) NOT NULL, 
                        scientific_name VARCHAR(255) NOT NULL,
                        Age INT(11) NOT NULL, 
                        Height FLOAT NOT NULL,
                        Diameter_girth FLOAT NOT NULL,
                        Longitude FLOAT NOT NULL, 
                        Latitude FLOAT NOT NULL) """)

    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print"\n",x
    mydb.close()
    
def mysql_insert():
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = 'NDMC_Streets'
                                    )
    
    mycursor = mydb.cursor()
    
#-----Dummy data-------------------------------------------
    id = 1
    Tree_code = 'Z4S10ALS12'
    Age = random.randint(18,65)

    now = datetime.now()
    Date = now.strftime('%Y-%m-%d %H:%M:%S')

    common_name = 'Neem'
    scientific_name = 'Azadirachta indica'

    Height = round(random.uniform(20,250), 5)
    Diameter_girth = round(random.uniform(1,10), 5)
    Longitude = round(random.uniform(0,100), 6)
    Latitude =  round(random.uniform(0,100), 6)
#-----------------------------------------------------------

    
    mycursor.execute("""INSERT INTO RK_Ashram_marg (id, Tree_code, Age, Date, common_name, scientific_name, Height, Diameter_girth, Longitude, Latitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" , 
                    (id, Tree_code, Age, Date, common_name, scientific_name, Height, Diameter_girth, Longitude, Latitude) )
    mydb.commit()
    mydb.close()

def mysql_read(DataBase_name):
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = DataBase_name
                                    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM  RK_Ashram_marg")
    table = mycursor.fetchall()
    for x in table:
        print x
    mydb.close()


if __name__ == "__main__":
    mysql_table("NDMC_Streets")
    #mysql_insert()
    #for x in range(10):
        #time.sleep(1)
        #mysql_insert()
    mysql_read("NDMC_Streets")
    