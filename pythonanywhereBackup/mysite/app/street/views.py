from __future__ import division
from flask import render_template, abort,request, flash, redirect, url_for, Markup


from . import street
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

import datetime


from flask_paginate import Pagination, get_page_args,get_page_parameter

# an Engine, which the Session will use for connection
# resources
some_engine = create_engine('mysql://saurabh88:cyclotron19@saurabh88.mysql.pythonanywhere-services.com/saurabh88$zone0',pool_recycle=280)

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()



#_____________________SEARCH TREE BY ID CODE______________________


@street.route('/search_tree_by_code', methods=['GET', 'POST'])
def search_tree_by_code():

    if request.method == 'POST':
        code = request.form.get('tree_code')
        # loop through dictionory to get table class name

        for k in street_names.keys():
            table_name = street_names.get(k)
            # check weather row exists or not
            exists = db.session.query(db.session.query(table_name).filter_by(Tree_code= code).exists()).scalar()
            if exists:
                tree_data = table_name.query.with_entities(table_name).filter_by(Tree_code= code)
                #__getting street name for image path
                #_____________key from value python dict__________
                street_name = list(street_names.keys())[list(street_names.values()).index(table_name)]
                for x in tree_data:
                    Lon = x.Longitude
                    Lat = x.Latitude
                    treeCode = x.Tree_code
                    specie = x.common_name
                    botanicalName = x.sceintific_name
                    age = x.Age
                    diameter = x.Diameter_girth
                    height = x.Height
                    address = x.closest_address
                    created = x.created
                    updated = x.updated
                    condition = x.condition
                    specieCode = x.specie_code

                    path = ImagePathCreator(treeCode, street_name)
                    image_1 = path + "__img1.jpg"
                    image_2 = path + "__img2.jpg"
                    tree_icon = specie + ".png"
                    leaf_image = botanicalName + ".jpg"

                    if condition == "Dead/Gone":
                        return render_template('street/deadTree.html')

                break

            else:
                continue

        if not exists:
            return render_template('errorPage.html', tree_code=code)


        # Benefits calculation
        # invoking func. to calculate Co2 squesterd and social cost of carbon saving by
        # this tree

        benefit = social_cost_of_carbon(H=float(height),D=float(diameter),age=int(age) )
        # converting into Kg/yr from ton/yr
        co2_absorbed_yr = str(round((float(benefit[0]) * 1000) ,2))
        social_cost_of_carbon_yr = round(float(benefit[1]), 2)
        est_plantation_date = plantation_date_est(str(age), str(created.strftime("%m%Y")) )


        #____________Maintenance log_________________

        maintenance = db.session.query(db.session.query(Maintenance_log).filter_by(TreeCode= code).exists()).scalar()
        if maintenance:
            logs = Maintenance_log.query.with_entities(Maintenance_log).filter_by(TreeCode= code)
        else:
            logs = None

    return render_template('street/tree_view.html',
                    tree_data = tree_data, exists = exists,
                    Lon = Lon, Lat = Lat,
                    treeCode=treeCode,
                    specie=specie,
                    botanicalName = botanicalName,
                    age = age,
                    diameter = diameter,
                    height = height,
                    created = created,
                    updated = updated,
                    address = address,
                    image_1 = image_1,
                    image_2 = image_2,
                    leaf_image = leaf_image,
                    tree_icon = tree_icon,
                    co2_absorbed_yr = co2_absorbed_yr,
                    social_cost_of_carbon_yr = social_cost_of_carbon_yr,
                    maintenance = maintenance,
                    logs = logs,
                    est_plantation_date = est_plantation_date,
                    specieCode = specieCode
                    )

#__________________________SEARCH TREE BY QR-CODE_____________________

@street.route('/search_tree_by_qrcode')
def search_tree_by_qrcode():

    if request.method == 'GET':
        code = request.args.get('ID')
        # loop through dictionory to get table class name
        for k in street_names.keys():
            table_name = street_names.get(k)
            # check weather row exists or not
            exists = db.session.query(db.session.query(table_name).filter_by(Tree_code = str(code)).exists()).scalar()
            if exists:
                tree_data = table_name.query.with_entities(table_name).filter_by(Tree_code= str(code))
                #__getting street name for image path
                #_____________key from value python dict__________
                street_name = list(street_names.keys())[list(street_names.values()).index(table_name)]
                for x in tree_data:
                    Lon = x.Longitude
                    Lat = x.Latitude
                    treeCode = x.Tree_code
                    specie = x.common_name
                    botanicalName = x.sceintific_name
                    age = x.Age
                    diameter = x.Diameter_girth
                    height = x.Height
                    address = x.closest_address
                    created = x.created
                    updated = x.updated
                    condition = x.condition
                    specieCode = x.specie_code

                    path = ImagePathCreator(treeCode, street_name)
                    image_1 = path + "__img1.jpg"
                    image_2 = path + "__img2.jpg"
                    tree_icon = specie + ".png"
                    leaf_image = botanicalName + ".jpg"

                    if condition == "Dead/Gone":
                        return render_template('street/deadTree.html')
                        break
                    else:
                        continue

                    if not exists:
                        return render_template('errorPage.html', tree_code=code)


        # Benefits calculation
        # invoking func. to calculate Co2 squesterd and social cost of carbon saving by
        # this tree

        benefit = social_cost_of_carbon(H=float(height),D=float(diameter),age=int(age) )
        # converting into Kg/yr from ton/yr
        co2_absorbed_yr = str(round((float(benefit[0]) * 1000) ,2))
        social_cost_of_carbon_yr = round(float(benefit[1]), 2)
        est_plantation_date = plantation_date_est(str(age), str(created.strftime("%m%Y")) )


        #____________Maintenance log_________________

        maintenance = db.session.query(db.session.query(Maintenance_log).filter_by(TreeCode= code).exists()).scalar()
        if maintenance:
            logs = Maintenance_log.query.with_entities(Maintenance_log).filter_by(TreeCode= code)
        else:
            logs = None

    return render_template('street/tree_view.html',
                    tree_data = tree_data, exists = exists,
                    Lon = Lon, Lat = Lat,
                    treeCode=treeCode,
                    specie=specie,
                    botanicalName = botanicalName,
                    age = age,
                    diameter = diameter,
                    height = height,
                    created = created,
                    updated = updated,
                    address = address,
                    image_1 = image_1,
                    image_2 = image_2,
                    leaf_image = leaf_image,
                    tree_icon = tree_icon,
                    co2_absorbed_yr = co2_absorbed_yr,
                    social_cost_of_carbon_yr = social_cost_of_carbon_yr,
                    maintenance = maintenance,
                    logs = logs,
                    est_plantation_date = est_plantation_date,
                    specieCode = specieCode
                    )


#_______________________________ENDS___________________________________






@street.route('/Complains')
def Complains():

    treeID = request.args.get('my_var', None)
    return render_template('street/report_maintenance.html',treeID=treeID)


@street.route('/ComplainForm', methods=['GET', 'POST'])
def ComplainForm():
    maintenance = ""
    post = ""
    # Some useful flags
    maintenance_flag, post_flag = False, False

    conn = some_engine.connect()

    if request.method == 'POST':
        treeCode = request.form['IDCode']
        post_complain =  request.form['text']
        if request.form.get('option1'):
            maintenance += "Watering/ "
        if request.form.get('option2'):
            maintenance += "Weed control/ "
        if request.form.get('option3'):
            maintenance += "Waste or Liiter cleaning required/ "
        if request.form.get('option4'):
            maintenance += "Postersa and banners/ "
        if request.form.get('option5'):
            maintenance += "Annual flowering required/ "
        if request.form.get('option6'):
            maintenance += "Mulch and soil/ "
        if request.form.get('option7'):
            maintenance += "Pruning/ "
        if request.form.get('option8'):
            maintenance += "Tree Guard needed/ "
        if request.form.get('option9'):
            maintenance += "Remove/dangerous tree/ "
        if request.form.get('option10'):
            maintenance += "Bed modification/ "
        if request.form.get('option11'):
            maintenance += "Missing or damaged/ "

    if len(maintenance) !=0:
        maintenance_flag = True

    if post_complain:
        post_flag = True

    if maintenance_flag == True or post_flag == True:

        stm = Complains_Maintenance_requests(TreeCode=treeCode, \
                maintenance_options=maintenance, post_text=post_complain)

        db.session.add(stm)
        db.session.commit()
    else:
        return redirect(url_for('home.homepage'))


    flash(' Your request have been stored successfully...','success')
    return redirect(url_for('home.homepage'))




#________________________SEARCH STREET BY NAME________________________



# -----------test code-----------
#test code
users = list(range(100))
def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]

@street.route('/myview/',defaults={'page':1})
@street.route('/myview/page/<int:page>',methods=['POST','GET'])
def view(page):
    per_page = 5
    posts = RK_Ashram_Marg.query.paginate(page,per_page,error_out=False)
    return render_template('street/view.html',posts=posts)


@street.route('/custom_markers')
def custom_markers():
    return render_template('street/custom_markers.html')


#----------------------Ends-----------------

@street.route('/search_street_by_name', methods=['POST', 'GET'])
def search_street_by_name():
    # local varables

    if request.method == 'POST':
        street_name = request.form.get('street_name')

        table_name = street_names.get(street_name)


        if not table_name:
            return render_template('errorPage.html', street_name=street_name)
        table_data = table_name.query.all()
        # Table.query() method
        # Table.query.with_entities(Table.column, func.count(Table.column)).group_by(Table.column).all()

        # session.query() method
        # session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()

        tree_types = table_name.query.with_entities(table_name.common_name, func.count(table_name.common_name)).group_by(table_name.common_name).all()
        rows = table_name.query.with_entities(table_name).all()


        total_trees = len(rows)

        # sqlalchemy filter methods for required data retrival
        # Table_class_name.query.with_entities(Table_class_name).filter(Table_class_name.Column < or > or == 'subject')
        # Note: After 2 days of Brainstorming i have found that this stupid .filter_by() method allows simplest operation like '=' only
        # .filter_by() method allows all pythonic operator.

        # Displaying Special Trees of Street
        special_trees_query = table_name.query.with_entities(table_name).filter(table_name.Age >= '100')

        special_trees = []
        for x in special_trees_query:

            path = ImagePathCreator(treeCode=x.Tree_code,tableName=street_name)

            special_trees.append(tempclass(Code=x.Tree_code,\
                specie=x.common_name, age=x.Age, img_path=(path + "__img1.jpg")) )

        # storing longitude and latitudes and other data
        # as strings to pass them into Javascript of template

        lon_str = ""
        lat_str = ""
        tree_code = ""
        specie = ""
        specieCode = ""

        # Note: this Space  ( + " ")allows us to split desired parts of string
        # For ecological benefits calculation
        total_carbon_cost = 0
        co2_absorbed_yr = 0

        for y in table_data:
            lon_str    += (str(y.Longitude)   + " ")
            lat_str    += (str(y.Latitude)    + " ")
            tree_code  += (str(y.Tree_code)   + " ")
            specie     += (str(y.common_name) + " ")
            specieCode += (str(y.specie_code) + " ")

            benefit = social_cost_of_carbon(H=y.Height,D=y.Diameter_girth,age=y.Age)
            # converting into Kg/yr from ton/yr
            co2_absorbed_yr += round((float(benefit[0]) * 1000) ,2)
            total_carbon_cost += round(float(benefit[1]), 2)

#______________________STREET WISE SAPLINGS DATABASE_________________


        labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
        ]

        values = [  ]

        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"
        ]

        survival_rate = 0

        saplings_data = saplings.get(street_name + "_Saplings")
        if  saplings_data:
            saplings_db = saplings_data.query.with_entities(saplings_data).all()
            saplings_growth_data = saplings.get(street_name + "_Saplings_growth_data")
            growth_data = saplings_growth_data.query.with_entities(saplings_growth_data).all()
            dead = 0
            for x in growth_data:
                values.append(x.avg_growth)

            for y in saplings_db:
                if y.condition == "Dead/Gone":
                    dead += 1
            survival_rate = (len(saplings_db) - dead)/len(saplings_db) * 100

        else:
            saplings_db = None

#_______________________________________________________________________________



    return render_template('street/streetView.html', street_name=street_name,
                            table_data=table_data, tree_types=tree_types,
                            total_trees=total_trees, special_trees=special_trees,
                            lon_str=lon_str,
                            lat_str=lat_str,
                            tree_code = tree_code,
                            specie = specie,
                            table_name = table_name,
                            total_carbon_cost = total_carbon_cost,
                            co2_absorbed_yr = co2_absorbed_yr,
                            saplings_db = saplings_db,
                            values=values,
                            labels=labels,
                            colors=colors,
                            max=100,
                            survival_rate = survival_rate,
                            specieCode=specieCode )


#______________________EXPLORE COMPLETE DATABASE__________________________

@street.route('/search_street', methods=['GET','POST'])
def search_street():
    """
    Render the homepage template on the / route
    """
    if request.method == 'POST':
        street_name = request.form.get('category')

        table_name = street_names.get(street_name)

        table_data = table_name.query.with_entities(table_name).all()
        # Table.query() method
        # Table.query.with_entities(Table.column, func.count(Table.column)).group_by(Table.column).all()

        # session.query() method
        # session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()

        #----------test code Server-side--------------
        page, per_page, offset = get_page_args(page_parameter='page',\
                                           per_page_parameter='per_page')
        total = len(table_data)
        pagination_users = get_users(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')

        #-------------------------------------------------------------

        tree_types = table_name.query.with_entities(table_name.common_name, func.count(table_name.common_name)).group_by(table_name.common_name).all()
        rows = table_name.query.with_entities(table_name).all()

        total_trees = len(rows)

        # Display special trees of this road
        special_trees_query = table_name.query.with_entities(table_name).filter(table_name.Age >= '100')

        special_trees = []
        for x in special_trees_query:

            path = ImagePathCreator(treeCode=x.Tree_code,tableName=street_name)

            special_trees.append(tempclass(Code=x.Tree_code,\
                specie=x.common_name, age=x.Age, img_path=(path + "__img1.jpg")) )

        # storing longitude and latitudes and other data
        # as strings to pass them into Javascript of template

        lon_str = ""
        lat_str = ""
        tree_code = ""
        specie = ""
        specieCode = ""


        # Note: this Space  ( + " ")allows us to split desired parts of string

        # For ecological benefits calculation
        total_carbon_cost = 0
        co2_absorbed_yr = 0

        for x in table_data:
            lon_str   += (str(x.Longitude)   + " ")
            lat_str   += (str(x.Latitude)    + " ")
            tree_code += (str(x.Tree_code)   + " ")
            specie    += (str(x.common_name) + " ")
            specieCode += (str(x.specie_code) + " ")

            benefit = social_cost_of_carbon(H=x.Height,D=x.Diameter_girth,age=x.Age)
            # converting into Kg/yr from ton/yr
            co2_absorbed_yr += round((float(benefit[0]) * 1000) ,2)
            total_carbon_cost += round(float(benefit[1]), 2)


    #______________________STREET WISE SAPLINGS DATABASE_________________


        labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
        ]

        values = [  ]

        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"
        ]

        survival_rate = 0
        saplings_data = saplings.get(street_name + "_saplings")
        if  saplings_data:
            saplings_db = saplings_data.query.with_entities(saplings_data).all()
            saplings_growth_data = saplings.get(street_name + "_saplings_growth_data")
            growth_data = saplings_growth_data.query.with_entities(saplings_growth_data).all()
            dead = 0
            for x in growth_data:
                values.append(x.avg_growth)

            for y in saplings_db:
                if y.condition == "Dead/Gone":
                    dead += 1
            survival_rate = (len(saplings_db) - dead)/len(saplings_db) * 100

        else:
            saplings_db = None
    #___________________________________________________________


    return render_template('street/streetView.html',
                            street_name=street_name,
                            table_data=table_data, tree_types=tree_types,
                            total_trees=total_trees, special_trees=special_trees,
                            lon_str=lon_str,
                            lat_str=lat_str,
                            tree_code = tree_code,
                            specie = specie,
                            table_name = table_name,
                            total_carbon_cost = total_carbon_cost,
                            co2_absorbed_yr = co2_absorbed_yr,
                            saplings_db = saplings_db,
                            values=values,
                            labels=labels,
                            colors=colors,
                            max=100,
                            survival_rate = survival_rate,
                            specieCode=specieCode,
                            users=pagination_users,
                            page=page,
                            per_page=per_page,
                            pagination=pagination,
                            )

#_____________________________ENDS___________________________________________








#___To hold data coming from sql BaseQuery as class objects temporarily__________
class tempclass:
    def __init__(self,Code,specie,age,img_path):
        self.Code = Code
        self.specie = specie
        self.age = age
        self.img_path = img_path





@street.route('/maps')
def maps():
    return render_template('street/maps.html')


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
    months = {"Jan" :1,"Feb" :2,"Mar" :3,"Apr" :4,"May" :5,"Jun" :6,"Jul" :7,"Aug" :8,"Sep" :9,"Oct" :10,"Nov" :11,"Dec" :12}
    plantation_date = ""
    m_date = []

    measurment_month = int(date[0:2])
    measurment_yr = int(date[2:6])
    tree_yr = int(age)
    tree_m = 0
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




#_______Crude logic to create image path from sql base query________
#________Images are store in server's file system______________

def ImagePathCreator(treeCode, tableName):

    Image_path = ""
    if treeCode[0] == '1':
        Image_path += "/zone1/" + tableName + "/" + treeCode
    elif treeCode[0] == '2':
        Image_path += "/zone2/" + tableName + "/" + treeCode
    elif treeCode[0] == '3':
        Image_path += "/zone3/" + tableName + "/" + treeCode
    elif treeCode[0] == '4':
        Image_path += "/zone4/" + tableName + "/" + treeCode
    elif treeCode[0] == '5':
        Image_path += "/zone5/" + tableName + "/" + treeCode
    elif treeCode[0] == '5':
        Image_path += "/zone5/" + tableName + "/" + treeCode
    elif treeCode[0] == '5':
        Image_path += "/zone6/" + tableName + "/" + treeCode
    elif treeCode[0] == '6':
        Image_path += "/zone6/" + tableName + "/" + treeCode

    return Image_path


# Temp code for tree images path craetion Note: For temporiry use only

def temp_image_path(specie):

    path = []

# if-else for to search specie image
    if specie == "Amaltas":
        path[0] = "static/images/tree-images/amaltas.jpg"
        path[1] = "static/images/tree-images/amaltas2.jpg"
    elif specie == "Arjun":
        path[0] = "static/images/tree-images/arjun.jpg"
        path[1] = "static/images/tree-images/arjun2.jpg"
    elif specie == "Bargad":
        path[0] = "static/images/tree-images/bargad.jpg"
        path[1] = "static/images/tree-images/bargad2.jpg"
    elif specie == "Drum_Stick":
        path[0] = "static/images/tree-images/drum-stick.jpg"
        path[1] = "static/images/tree-images/drum-stick2.jpg"
    elif specie == "Flase_ashoka":
        path[0] = "static/images/tree-images/false-ashoka.jpg"
        path[1] = "static/images/tree-images/false-ashoka2.jpg"
    elif specie == "Gulmohar":
        path[0] = "static/images/tree-images/gulmohar.jpg"
        path[1] = "static/images/tree-images/gulmohar2.jpg"
    elif specie == "Neem":
        path[0] = "static/images/tree-images/neem.jpg"
        path[1] = "static/images/tree-images/neem2.jpg"
    elif specie =="Peepal":
        path[0] = "static/images/tree-images/peepal.jpg"
        path[1] = "static/images/tree-images/peepal2.jpg"
    elif specie =="Pilkhan":
        path[0] = "static/images/tree-images/pilkan.jpg"
        path[1] = "static/images/tree-images/pilkhan2.jpg"
    elif specie == "Safeda":
        path[0] = "static/images/tree-images/safeda.jpg"
        path[1] = "static/images/tree-images/safeda2.jpg"
    elif specie == "Sausage_tree":
        path[0] = "static/images/tree-images/Sausage_tree.jpg"
        path[1] = "static/images/tree-images/Sausage_tree2.jpg"
    elif specie == "Scholar_tree":
        path[0] = "static/images/tree-images/Scholar_tree.jpg"
        path[1] = "static/images/tree-images/Scholar_tree2.jpg"
    elif specie == "Semal":
        path[0] = "static/images/tree-images/Semal.jpg"
        path[1] = "static/images/tree-images/Semal2.jpg"
    elif specie == "Kikar":
        path[0] = "static/images/tree-images/Kikar.jpg"
        path[1] = "static/images/tree-images/Kikar2.jpg"
    elif specie == "Weeping_bottelbrush":
        path[0] = "static/images/tree-images/Weeping_bottelbrush.jpg"
        path[1] = "static/images/tree-images/Weeping_bottelbrush2.jpg"
    elif specie == "Mulberry":
        path[0] = "static/images/tree-images/Mulberry.jpg"
        path[1] = "static/images/tree-images/Mulberry2.jpg"
    elif specie == "Royal_palm":
        path[0] = "static/images/tree-images/Royal_palm.jpg"
        path[1] = "static/images/tree-images/Royal_palm2.jpg"
    elif specie == "Jamun":
        path[0] = "static/images/tree-images/Jamun.jpg"
        path[1] = "static/images/tree-images/Jamun2.jpg"
    elif specie == "Jungle_jalebi":
        path[0] = "static/images/tree-images/Jungle_jalebi.jpg"
        path[1] = "static/images/tree-images/Jungle_jalebi2.jpg"
    elif specie == "Maharukh":
        path[0] = "static/images/tree-images/maharukh.jpg"
        path[1] = "static/images/tree-images/maharukh2.jpg"

    return path









