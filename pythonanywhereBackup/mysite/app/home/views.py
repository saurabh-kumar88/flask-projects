from __future__ import division
from flask import render_template, abort, request, flash

from . import home

from .. import db #go back two steps in dir
from ..models import *
from sqlalchemy import *
from sqlalchemy import func, text, update,or_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

import mysql.connector
from mysql.connector import Error
from tree_density import density

from street_names import *

from specie_list import specie_list

# an Engine, which the Session will use for connection
# resources
some_engine = create_engine('mysql+mysqlconnector://saurabh88:cyclotron19@saurabh88.mysql.pythonanywhere-services.com/saurabh88$zone0')
conn = some_engine.connect()

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()

@home.route('/homepage')

def homepage():
    """
    Render the homepage template on the / route
    """
#_________________UPDATE CITYWIDE DATABASE___________________
#_____________Run this function once to update citywide database tables_________

    #Update_Citywide_database()

#______________________________________________________________________________

    data = Specie_Database.query.with_entities(Specie_Database).all()
    species_count = len(data)

    #___________________TOTAL TREES MAPPED____________

    mapped_obj = City_wide_data()
    mapped_trees = mapped_obj.Mapped_trees()

    #____most common specie

    # To get max specie count
    max_count = 0
    testCount = []
    testdata = Specie_Database.query.with_entities(Specie_Database.count).all()
    for x in testdata:
        testCount.append(int(x.count))

    max_count = max(testCount)
    # To retrive complete data of most common specie
    most_common_species = session.query(Specie_Database).filter_by(count=max_count)

    benefits_yr = Citywide_Benefits.query.with_entities(Citywide_Benefits).all()

#____________test code for saplings growth updates_______________



#____________________________________


    return render_template('home/homepage.html', title="Welcome",
                           mapped_trees = mapped_trees,
                           species_count = species_count,
                           most_common_species = most_common_species,
                           benefits_yr = benefits_yr )

#________________To hold data coming from sql BaseQuery as class objects temporarily______________
class tempclass:
    def __init__(self,Code,specie,specieCode,sceintificName,age,h,d,lon,lat):
        self.Code = Code
        self.specie = specie
        self.specieCode = specieCode
        self.sceintificName = sceintificName
        self.age = age
        self.h = h
        self.d = d
        self.lon = lon
        self.lat = lat

#___________________________FILTER BY AGE GROUP__________________________________________

@home.route('/filter_by_age', methods=['GET', 'POST'])
def filter_by_age():

    tree_count = []  # To hold the counts of tree of requested specie
    co2 =  []        # To hold total co2 reduced by particular specie each year
    scc =  []        # To hold total SCC saved by specie each year
    temp = []
    Age_gp = ""
    filter_data = []
    tempList = []


    if request.method == 'POST':
        age_group =  request.form['options']

    if age_group == "G_100":
        Age_gp = "Greater then 100 Yrs."
        for k in street_names.keys():
            table_name = street_names.get(k)
            filter_data = table_name.query.with_entities(table_name).filter(table_name.Age > '100')
            for x in filter_data:
                tempList.append(tempclass(Code=x.Tree_code,specieCode=x.specie_code,specie=x.common_name,\
                    sceintificName=x.sceintific_name,age=x.Age,\
                    h=x.Height,d=x.Diameter_girth,\
                    lon=x.Longitude,lat=x.Latitude))


    elif age_group == "U_100":
        Age_gp = "Under 100 Yrs."
        for k in street_names.keys():
            table_name = street_names.get(k)
            filter_data = table_name.query.with_entities(table_name).filter(table_name.Age <= '100')
            for x in filter_data:
                tempList.append(tempclass(Code=x.Tree_code,specieCode=x.specie_code,specie=x.common_name,\
                    sceintificName=x.sceintific_name,age=x.Age,\
                    h=x.Height,d=x.Diameter_girth,\
                    lon=x.Longitude,lat=x.Latitude))

    elif age_group == "U_50":
        Age_gp = "Under 50 Yrs"
        for k in street_names.keys():
            table_name = street_names.get(k)
            filter_data = table_name.query.with_entities(table_name).filter(table_name.Age <= '50')
            for x in filter_data:
                tempList.append(tempclass(Code=x.Tree_code,specieCode=x.specie_code,specie=x.common_name,\
                    sceintificName=x.sceintific_name,age=x.Age,\
                    h=x.Height,d=x.Diameter_girth,\
                    lon=x.Longitude,lat=x.Latitude))

    elif age_group == "U_10":
        Age_gp = "Under 10 Yrs."
        for k in street_names.keys():
            table_name = street_names.get(k)
            filter_data = table_name.query.with_entities(table_name).filter(table_name.Age <= '10')
            for x in filter_data:
                tempList.append(tempclass(Code=x.Tree_code,specieCode=x.specie_code,specie=x.common_name,\
                    sceintificName=x.sceintific_name,age=x.Age,\
                    h=x.Height,d=x.Diameter_girth,\
                    lon=x.Longitude,lat=x.Latitude))

    # Calculating co2 and scc saved by requested specie
    for x in tempList:
        tree_count.append(x.Code)
        temp.append(social_cost_of_carbon(age=x.age, H=x.h,D=x.d))

    for x in temp:
        co2.append(round(float(x[0]) * 1000, 2) )
        scc.append(round(float(x[1]), 2) )


    total_co2 = sum(co2)
    total_scc = sum(scc)
    total_trees = len(tree_count)

    # storing longitude and latitudes and other data
    # as strings to pass them into Javascript of template

    lon_str = ""
    lat_str = ""
    tree_code = ""
    specie = ""
    specieCode = ""

    # Note: this Space  ( + " ")allows us to split desired parts of string

    for x in tempList:
        lon_str    += (str(x.lon)               + " ")
        lat_str    += (str(x.lat)               + " ")
        tree_code  += (str(x.Code)              + " ")
        specie     += (str(x.specie)            + " ")
        specieCode += (str(x.specieCode)        + " ")


    return render_template('home/citywide_map.html',
                            Age_gp = Age_gp,
                            filter_data = filter_data,
                            total_trees = total_trees,
                            total_co2=total_co2,
                            total_scc=total_scc,
                            lon_str=lon_str,
                            lat_str=lat_str,
                            tree_code=tree_code,
                            specie=specie,
                            specieCode=specieCode)

#______________________________FILTER BY SPECIE______________________________________________

@home.route('/filter_by_specie', methods=['GET', 'POST'])
def filter_by_specie():

    tree_count = [] # To hold the counts of tree of requested specie
    co2 =  [] # To hold total co2 reduced by particular specie each year
    scc =  [] # To hold total SCC saved by specie each year
    temp = []
    tempList = []

    if request.method == 'POST':
        specie_name = request.form.get('specie')
        print"\n_______________________________________",specie_name
    for k in street_names.keys():
        table_name = street_names.get(k)
        filter_data = table_name.query.with_entities(table_name).\
        filter(or_(table_name.common_name == specie_name , table_name.sceintific_name == specie_name))
        for x in filter_data:
            tempList.append(tempclass(Code=x.Tree_code,specieCode=x.specie_code,specie=x.common_name,\
            sceintificName=x.sceintific_name,age=x.Age,\
            h=x.Height,d=x.Diameter_girth,\
            lon=x.Longitude,lat=x.Latitude))
    # Calculating co2 and scc saved by requested specie
    for x in tempList:
        tree_count.append(x.Code)
        temp.append(social_cost_of_carbon(H=x.h,D=x.d,age=x.age) )

    for x in temp:
        co2.append(round(float(x[0]) * 1000, 2) )
        scc.append(round(float(x[1]), 2) )


    total_co2 = sum(co2)
    total_scc = sum(scc)
    total_trees = len(tree_count)

    # storing longitude and latitudes and other data
    # as strings to pass them into Javascript of template

    lon_str = ""
    lat_str = ""
    tree_code = ""
    specie = ""
    specieCode = ""

    # Note: this Space  ( + " ")allows us to split desired parts of string

    for x in tempList:
        lon_str    += (str(x.lon)             + " ")
        lat_str    += (str(x.lat)             + " ")
        tree_code  += (str(x.Code)            + " ")
        specie     += (str(x.specie)          + " ")
        specieCode += (str(x.specieCode)      + " ")


    return render_template('home/citywide_map.html',
                            specie_name = specie_name,
                            filter_data = filter_data,
                            total_trees = total_trees,
                            total_co2=total_co2,
                            total_scc=total_scc,
                            lon_str=lon_str,
                            lat_str=lat_str,
                            tree_code=tree_code,
                            specie=specie,
                            specieCode=specieCode
                            )

#_________________Local functions______________________________

# SOCIAL COST OF CARBON: based on tree height, trunk diameter, and age
# we can calculate total co2 removed/squestered from atmosphere per year by individual tree, and then
# calculate social cost carbon saved by him, current rate is 417$ per ton of co2
from tree_density import density
def social_cost_of_carbon(H,D,age):

    co2_and_social_cost = []

# above ground weight
    if D < 11:
        W = (0.25 * pow(D,2) * H)
    elif D >= 11:
        W = (0.15 * pow(D, 2) * H)


# W = above ground weight in lbs, D = diameter in inches, H = height in feet

# total green weight including root system

    Green_weght = W + (W * 0.2) # roots systems have 20% more of aove ground weight
    dry_weight = Green_weght * 0.725 # tree contain 72.5% dry mass and 27.5% moisture
    carbon_weight = dry_weight * 0.5 # tree contain average of 50% carbon of total dry weight
# total co2 squesterd by tree upto present date
    co2_sqtrd = carbon_weight * 3.6663

# 3.6663 is the constant which is the ratio of atomic weights of Co2/C

# Co2 sequesterd each year in lbs to ton since 1 lbs = 0.0005 ton

    co2_sqtrd_yr =  (co2_sqtrd / age) * 0.0005

# social cost of carbon by current rate which is $417 into Rs.
# current rate is $1 = 70.30 Rs 19/12/2018
    social_cost = co2_sqtrd_yr * 86 * 70.30

    co2_and_social_cost.append(str(co2_sqtrd_yr))
    co2_and_social_cost.append(str(social_cost))

    return (co2_and_social_cost)

# __________________considering density of tree specie_____________

# This function uses density of tree specie isteasd of constants
# 0.25 to 0.15 and all calculations are in SI units
def social_cost_of_carbon_matric(H,D,age,sceintificName):

    co2_and_social_cost = []

    H = H * 0.3048
    D = D * 0.0254

# above ground weight
    W =  (0.785 * pow(D,2) * H) * density[sceintificName]

# W = above ground weight in lbs, D = diameter in inches, H = height in feet

# total green weight including root system

    Green_weght = W + (W * 0.2) # roots systems have 20% more of aove ground weight
    dry_weight = Green_weght * 0.725 # tree contain 72.5% dry mass and 27.5% moisture
    carbon_weight = dry_weight * 0.5 # tree contain average of 50% carbon of total dry weight
# total co2 squesterd by tree upto present date
    co2_sqtrd = carbon_weight * 3.6663

# 3.6663 is the constant which is the ratio of atomic weights of Co2/C

# Co2 sequesterd each year in kgs to ton since 1 ton = 1000 kg

    co2_sqtrd_yr =  (co2_sqtrd / age) / 1000

# social cost of carbon for india is $86 USD per ton of Co2 emission.
# current rate is $1 = 70.30 Rs 19/12/2018
    social_cost = co2_sqtrd_yr * 86 * 70.30

    co2_and_social_cost.append(str(co2_sqtrd_yr))
    co2_and_social_cost.append(str(social_cost))

    return (co2_and_social_cost)


# Plantaion Date Estimator

# Note: we have to take age as Float like 100.3 yrs means 100yrs and 3 months
# Subtract this from measurment date
# Take 3 to 5 yrs as Correction factor because this is the average time
# a tree takes in nursery to grow from seedling to a plantable sapling
def plantation_date_est(age, date):
 # convert date string in array
    # convert date string in array
    months = {"Jan" :1,"Feb" :2,"Mar" :3,"Apr" :4,"May" :5,"Jun" :6,"Jul" :7,"Aug" :8,"Sep" :9,"Oct" :10,"Nov" :11,"Dec" :12}
    plantation_date = ""
    m_date = []
    measurment_date  = date.split(" ")
    measurment_month = int(months[ measurment_date[1] ])
    measurment_yr = int(measurment_date[2])
    tree_yr = int(age)
    tree_m = int((age * 10) % 10)
    if tree_m > measurment_month:
        # Borrow a year
        measurment_month += 12
        measurment_yr -= 1
        plantation_mon = (measurment_month  - tree_m)
        plantation_yr = (measurment_yr - tree_yr)
    else:
        plantation_mon = (measurment_month - tree_m)
        plantation_yr = (measurment_yr - tree_yr)

    plantation_date += str(months.keys()[months.values().index(plantation_mon)]) + " "
    # Seedling correction factor is between 3 to 5 yrs
    plantation_date += str(plantation_yr - 5)

    return (plantation_date)

#_____________________________UPDATE CITYWIDE DATABAS_________________________________


def Update_Citywide_database():
    obj = City_wide_data()
    mapped_trees =  obj.Mapped_trees()
    most_common =   obj.Most_common_trees()
    benefits = obj.Co2_and_SCC()

    conn = some_engine.connect()
#____updating specie databse table
    for x in most_common:
        data = update(Specie_Database).where(Specie_Database.specie == x.specie).values(count= (x.count), percentage= (x.count/mapped_trees)*100 )
        conn.execute(data)

#_____updating benefits database table

    stm = update(Citywide_Benefits).where(Citywide_Benefits.id == '1').values(carbon_dioxide= benefits[0], SCC= benefits[1] )
    conn.execute(stm)



class mostCommon:
    def __init__(self, specie, count):
        self.specie = specie
        self.count = count


class City_wide_data:

    def Mapped_trees(self):
        mapped_trees = 0
        test_arr = []
        for k in street_names.keys():
            table_name = street_names.get(k)
            rows = table_name.query.with_entities(table_name).all()
            test_arr.append(int(len(rows)))
        mapped_trees = sum(test_arr)
        return mapped_trees

    def Most_common_trees(self):
        most_common = []
        specie_name = []
        for k in street_names.keys():
            table_name = street_names.get(k)
            tree_types = table_name.query.with_entities(table_name).all()
            for x in tree_types:
                specie_name.append(x.common_name)

        for x in specie_list:
            most_common.append(mostCommon(specie=x, count=specie_name.count(x)) )

        return most_common

    def Co2_and_SCC(self):
        co2_absorbed_yr = 0
        total_carbon_cost = 0
        total_benefits = []
        for k in street_names.keys():
            table_name = street_names.get(k)
            rows = table_name.query.with_entities(table_name).all()
            for y in rows:
                benefit = social_cost_of_carbon(H=y.Height,D=y.Diameter_girth,age=y.Age)
                # converting into Kg/yr from ton/yr
                co2_absorbed_yr += round((float(benefit[0]) * 1000) ,2)
                total_carbon_cost += round(float(benefit[1]), 2)
        total_benefits.append(str(co2_absorbed_yr))
        total_benefits.append(str(total_carbon_cost))

        return(total_benefits)
#_________________Update % growth in every sapling database table_______________










