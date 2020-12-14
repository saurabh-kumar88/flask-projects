import sqlite3
import time
import datetime
import random
import mysql.connector
from mysql.connector import Error
from ConfigParser import ConfigParser   




#make data base file
conn = sqlite3.connect('database.db')

c = conn.cursor() #create cursor object

#UPPER_CASE letters are sqlite commands
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Streets(unix REAL, datestamp TEXT, Type TEXT, geolocation FLOAT)')

#Hardcoding data entry
def data_entry():
    c.execute("INSERT INTO Streets VALUES(1245, 'R.K Ashram marg', 'Near Laal school', 45454578)")
    conn.commit() #making connection with database
    c.close() #closing file
    conn.close() #closing connection with database

#Example of dynamic data entry with timestamp 
def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y  %H:%M:%S') )
    Type = 'sacred fig'
    geolocation = round(random.uniform(0,9), 5)
    c.execute("INSERT INTO Streets (unix , datestamp, Type, geolocation)   VALUES(?,?,?,?)",
    (unix, date, Type, geolocation) )
    conn.commit()

def read_from_db():
    #c.execute('SELECT * FROM Streets ') #this command will copy all data in table
    #Searching through table
    #c.execute('SELECT * FROM Streets WHERE geolocation = 1.55169 AND unix =  1538127005.379715' )
    #c.execute('SELECT * FROM Streets WHERE unix < 1538126641.679276' )
    c.execute('SELECT Type, geolocation, datestamp, unix FROM Streets' )
    data = c.fetchall()
    for row in data:
        print"\n" , row
    

def del_and_update():
    c.execute('SELECT * FROM Streets')
    for row in c.fetchall():
        print (row)

    c.execute('UPDATE Streets SET Type = "peepal"  WHERE Type = "sacred fig" ')
    conn.commit()
    for row in c.fetchall():
        print (row)

#----------------------------------------------------------------------------------
#----------------------------MYSQL----------------------------------------------------
#----------------------------------------------------------------------------------

def connect():
    """ Connect to MYSQL"""
    global conn
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

def mysql_create_table(DataBase_name):
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = DataBase_name
                                    )
    

    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Tree_data ( unix INT(4) UNSIGNED, date TEXT, Specie TEXT ) ")
    #mycursor.execute("CREATE TABLE IF NOT EXISTS customer ( name VARCHAR(255), address VARCHAR(255) ) ")
    #mycursor.execute("ALTER TABLE customer ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print"\n",x

def mysql_insert():
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = 'mysql_test_db'
                                    )
    
    #sql_insert = """INSERT INTO customer(id, name, address) VALUES(1, 'Anikeit', 'Dilshad garden') """
    #sql_insert = """INSERT INTO customer(id, name, address) VALUES(ID, Name, Address) """
    #result = mycursor.execute(sql_insert)
    
    #sql_insert = "INSERT INTO customer (id, name, address) VALUES (%d,%s,%s)"
    #val = (ID,Name, Address)
    
    #mycursor = mydb.cursor()
    #mycursor.execute(joinsql,val)
           
   
    mycursor = mydb.cursor()
    
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y  %H:%M:%S') )
    Specie = 'sacred fig'
    sql_insert = "INSERT INTO Tree_data (unix, date, Specie) VALUES (%d,%s,%s)"
    val = (unix, date, Specie)
    mycursor.execute(sql_insert, val)
    mydb.commit()
   
   

    
def mysql_read(DataBase_name):
    mydb =  mysql.connector.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'saw99',
                                    database = DataBase_name
                                    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Tree_data ")
    table = mycursor.fetchall()
    for x in table:
        print x














if __name__ == "__main__":
    #connect()
    #create_db()
    #mysql_create_table("mysql_test_db")
    #mysql_insert()
    for x in range(10):
        mysql_insert()
    mysql_read("mysql_test_db")
    
    
    
    
    
    
    #del_and_update()
    #read_from_db()
    
    #create_table()
    #data_entry()
    """
    for i in range(10):
        dynamic_data_entry()
        time.sleep(1)
    c.close()
    conn.close()
    """
