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
import io

def create_table():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='mysql',
                                       user='root',
                                       password='saw99'
                                    )

        if conn.is_connected():
            print "Connected to MYSQL"
    except Error as e:
        print (e)
    finally:
        conn.close()


def connect():
    """ Connect to MYSQL"""
    global conn
    try:
        conn = mysql.connector.connect(host='localhost',
                                    database='NDMC_Streets',
                                    user='root',
                                    password='saw99'
                                    )

        if conn.is_connected():
            print "Connected to MYSQL"
    except Error as e:
        print (e)
    finally:
        conn.close()



#------------------create table----------------------
def create_db():
    global mycursor

    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',

                                    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS mysql_test_db")
    
   
    mycursor.execute("SHOW DATABASES")
    #mycursor.execute("SHOW TABLES")

    for x in mycursor:
        print"\n",x

def mysql_table(DataBase_name):
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = DataBase_name
                                    )
    

    mycursor = mydb.cursor()
    #mycursor.execute("CREATE TABLE IF NOT EXISTS Tree_data ( unix INT(4) UNSIGNED, date TEXT, Specie TEXT ) ")
    #mycursor.execute("CREATE TABLE IF NOT EXISTS employee ( name VARCHAR(255), age INT ")
    #mycursor.execute("ALTER TABLE employee MODIFY salary DOUBLE")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Tree_images (pic LONGBLOB) ")
    #mycursor.execute("ALTER TABLE employee MODIFY salary DOUBLE")
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print"\n",x

def mysql_image():
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = 'mysql_test_db'
                                    )
    
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Tree_images (id INT(11), pic LONGBLOB) ")

#------------<--------------code for image-------------------<----------
    with open("//home//yking18//Desktop//tree_lined.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    #image = Image.open('//home//yking18//Desktop//tree_lined.jpg')
    #img = open('//home//yking18//Desktop//tree_lined.jpg', 'rb').read()
    
    
    mycursor.execute("""INSERT INTO Tree_images (pic) VALUES(%s)""",(encoded_string,) )
    #mycursor.execute("""INSERT INTO employee (name, age, datetime, salary, img) VALUES (%s, %s, %s, %s, %s)""" , 
                    #(name, age, formatted_datetime, emp_salary, blob_value) )
    mydb.commit()

    
    """
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y  %H:%M:%S') )
    Specie = 'sacred fig' """
   
   

    
def mysql_read(DataBase_name):
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = DataBase_name
                                    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name FROM employee ")
    table = mycursor.fetchall()
    for x in table:
        print x


def mysql_rander_image(DataBase_name):
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = DataBase_name
                                    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT img FROM Tree_images WHERE idpic = %s", ('1',))
    data = mycursor.fetchall()
    mydb.close()
    #print type(data[0][0])
    #image_data = base64.b64decode(data[0][0])
    #file_like = cStringIO.StringIO(image_data)
    file_like = io.BytesIO(data[0][0])
    
    raw_img = PIL.Image.open(file_like)
    raw_img.show()
    
    
        
if __name__ == "__main__":
    #connect()
    #create_db()
    #mysql_table("mysql_test_db")
    #mysql_insert()
    #for x in range(10):
        #time.sleep(0.5)
        #mysql_image()
    #mysql_read("mysql_test_db")
    mysql_rander_image("mysql_test_db")