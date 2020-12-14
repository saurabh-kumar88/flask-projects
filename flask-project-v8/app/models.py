import os, os.path as op

from flask import url_for, abort, redirect, request, flash

from flask_security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin,
                            login_required,
                            current_user)
from flask_security.utils import encrypt_password
from flask_security.forms import RegisterForm, Required, StringField
from wtforms import TextField


from app import db
from sqlalchemy import DateTime,event
from flask_admin.contrib import sqla

from flask_admin import form

from wtforms import fields, widgets, Form

from jinja2 import Markup

from sqlalchemy.event import listens_for
from sqlalchemy.orm import column_property,mapper

import app
# Look-up table for relating street name to
# Corrosponding table


"""
Note: Tree Id  = 3 digit zone code + 2 digit street code + 3 digit tree S.no
e.g 40022158

"""


#_______________________test code________________
#_____________botanical and specie code auto fill________________

specie_names = {'Peepal'        : 'Ficus_religiosa',
                'Bargad'        : 'Ficus_benghalensis',
                'Amaltas'       : 'Cassia_fistula',
                'Gulmohar'      : 'Delonix_regia',
                'Arjun'         : 'Terminalia_arjuna',
                'Drum_Stick'    : 'Moringa_oleifera',
                'Semal'         : 'Bombax_ceiba',
                'Safeda'        : 'Eucalyptus',
                'Scholar_tree'  : 'Alstonia_scholaris',
                'Neem'          : 'Azadirachta_indica',
                'Bakayan'       : 'Melia_azedarach',
                'False_ashoka'  : 'Polyalthia_longifolia',
                'Pilkhan'       : 'Ficus_virens',
                'Sausage_tree'  : 'Kigelia_africana',
                'Sentang'       : 'Azadirachta_excelsa',
                'Kikar'         : 'Vachellia_nilotica',
                'Bottlebrush'   : 'Callistemon',
                'Mango'         : 'Mangifera_indica',
                'Mulberry'      : 'Morus',
                'Palm'          : 'Arecaceae',
                'Jamun'         : 'Syzygium_cumini',

                'Unknown'       : 'Unknown',

                None            : 'Default'
               }

specie_codes = {'Peepal'        : 1621,
                'Bargad'        : 1622,
                'Amaltas'       : 1321,
                'Gulmohar'      : 1421,
                'Arjun'         : 2121,
                'Drum_Stick'    : 1921,
                'Semal'         : 1221,
                'Safeda'        : 1521,
                'Scholar_tree'  : 1021,
                'Neem'          : 1121,
                'Bakayan'       : 1821,
                'False_ashoka'  : 2021,
                'Pilkhan'       : 1623,
                'Sausage_tree'  : 1721,
                'Sentang'       : 1122,
                'Kikar'         : 1010,
                'Bottlebrush'   : 1002,
                'Mango'         : 1003,
                'Mulberry'      : 1004,
                'Palm'          : 1005,
                'Jamun'         : 1006,

                'Unknown'       : 1001,
                None            : 'Default'
               }

        




# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)




class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

# Extra fields added to flask-security registration form
class ExtendedConfirmRegisterForm(RegisterForm):
    first_name = StringField('First Name', [Required()])
    last_name = StringField('Last Name', [Required()])




#__________________USER DEFINED MODELS STARTS FROM HERE________________

"""
db.Numeric(9,7) Note: After two days of extensive digging i finally found the correct
method of defining precision in db.numerci field
Numeric(M,D) means, e.g for representing 22.123 we have to write Numeric(5,3)
i.e M = Sum of (No. of digits before decimal point + no. of digits after decimal point), D = no. of digits after decimal point
"""


#_______________________________CITY WIDE SATISTICS________________________________


class Specie_Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specie = db.Column(db.String(45), unique=True)
    count = db.Column(db.String(45))
    percentage = db.Column(db.String(45))


class Citywide_Benefits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carbon_dioxide = db.Column(db.String(45), unique=True)
    SCC = db.Column(db.String(45))

class Complains_Maintenance_requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, server_default=db.func.now() )
    TreeCode = db.Column(db.String(8) )
    maintenance_options = db.Column(db.String(250))
    post_text = db.Column(db.String(250))

class Maintenance_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TreeCode = db.Column(db.String(8))
    datetime = db.Column(db.DateTime, server_default=db.func.now())
    maintenanceType = db.Column(db.String(100))

    def __unicode__(self):
        return self.name


#------------Zone1--------------#
class Akbar_Road(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name

@event.listens_for(Akbar_Road, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Akbar_Road, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))

class Akbar_Road_Saplings(db.Model):

    id  = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    Height = db.Column(db.Float, nullable=False)
    New_Height = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(45), nullable=False)
    Growth_percentage = column_property( (New_Height - Height)/Height *100 )


    def __unicode__(self):
        return self.name


@event.listens_for(Akbar_Road_Saplings, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))
        

@event.listens_for(Akbar_Road_Saplings, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))


class Akbar_Road_Saplings_growth_data(db.Model):

    id  = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    avg_growth = db.Column(db.Float)

    def __unicode__(self):
        return self.name

#------------Zone2--------------#
class Aurangzeb_Lane(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name

@event.listens_for(Aurangzeb_Lane, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Aurangzeb_Lane, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


#------------Zone3--------------#
class Jashwant_singh_Road(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name


@event.listens_for(Jashwant_singh_Road, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Jashwant_singh_Road, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


#------------Zone4--------------#
class BD_Marg(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name

@event.listens_for(BD_Marg, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(BD_Marg, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))



class BD_Marg_Saplings(db.Model):

    id  = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(8), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    Height = db.Column(db.Float, nullable=False)
    New_Height = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(45), nullable=False)
    Growth_percentage = column_property( (New_Height - Height)/Height *100 )

    def __unicode__(self):
        return self.name


@event.listens_for(BD_Marg_Saplings, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))
        


@event.listens_for(BD_Marg_Saplings, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))


class BD_Marg_Saplings_growth_data(db.Model):

    id  = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    avg_growth = db.Column(db.Float)

    def __unicode__(self):
        return self.name


class BK_Singh_Marg(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name


@event.listens_for(BK_Singh_Marg, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(BK_Singh_Marg, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))




class BK_Singh_Marg_Saplings(db.Model):

    id  = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    Height = db.Column(db.Float, nullable=False)
    New_Height = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(45), nullable=False)
    Growth_percentage = column_property( (New_Height - Height)/Height *100 )

    def __unicode__(self):
        return self.name

@event.listens_for(BK_Singh_Marg_Saplings, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))
        


@event.listens_for(BK_Singh_Marg_Saplings, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))



class BK_Singh_Marg_Saplings_growth_data(db.Model):

    id  = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    avg_growth = db.Column(db.Float)

    def __unicode__(self):
        return self.name


class RK_Ashram_Marg(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45) )
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    specie_code = db.Column(db.Integer)
    
    
    

    def __unicode__(self):
        return self.name

@event.listens_for(RK_Ashram_Marg, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(RK_Ashram_Marg, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))
       

class RK_Ashram_Marg_Saplings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45))
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    Height = db.Column(db.Float, nullable=False)
    New_Height = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(45) , nullable=False)
    Growth_percentage = column_property( (New_Height - Height)/Height *100 )

    def __unicode__(self):
        return self.name

@event.listens_for(RK_Ashram_Marg_Saplings, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))
        


@event.listens_for(RK_Ashram_Marg_Saplings, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.sceintific_name = specie_names.get(str(target.common_name))
        

class RK_Ashram_Marg_Saplings_growth_data(db.Model):

    id  = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    avg_growth = db.Column(db.Float)

    def __unicode__(self):
        return self.name



#------------Zone5--------------#
class Abdul_Fazal_Road(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name

@event.listens_for(Abdul_Fazal_Road, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Abdul_Fazal_Road, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))





#------------Zone6--------------#
class Arch_Bishop_Marg(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)
    
    def __unicode__(self):
        return self.name


@event.listens_for(Arch_Bishop_Marg, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Arch_Bishop_Marg, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


#------------Zone7--------------#
class Aurobindo_Marg(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name


@event.listens_for(Aurobindo_Marg, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Aurobindo_Marg, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))

#------------Zone8--------------#
class Sardar_Patel_Marg(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name

@event.listens_for(Sardar_Patel_Marg, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Sardar_Patel_Marg, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))

#------------Zone9--------------#
class Safdarjung_Road(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Tree_code = db.Column(db.String(8), unique=True, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    common_name = db.Column(db.String(45), nullable=False)
    sceintific_name = db.Column(db.String(45), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.Float, nullable=False)
    Diameter_girth = db.Column(db.Float, nullable=False)
    closest_address = db.Column(db.String(45), nullable=False)
    Longitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    Latitude = db.Column(db.Numeric(8,6), unique=True, nullable=False)
    specie_code = db.Column(db.Integer)

    def __unicode__(self):
        return self.name

@event.listens_for(Safdarjung_Road, 'before_insert')
def before_insert_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))


@event.listens_for(Safdarjung_Road, 'before_update')
def before_update_function(mapper, connection, target):
        # 'target' is your object
        target.common_name
        target.specie_code
        target.sceintific_name = specie_names.get(str(target.common_name))
        target.specie_code = specie_codes.get(str(target.common_name))

#___________________________________________________________________________________


#___________________________ADMIN AUTHENTICATION________________________
# Create customized model view class


    


class MyModelView(sqla.ModelView):

#flask ModelView Configuration Attributes
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = False
    page_size = 10
    #create_modal_template = 'admin/model/create.html'
    #edit_modal_template = 'admin/model/edit.html'
    
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    form_choices = { 'common_name': [ ('Amaltas', 'Amaltas'), 
                                      ('Arjun', 'Arjun'),
                                      ('Bargad','Bargad'),
                                      ('Drum_Stick','Drum Stick'),
                                      ('False_ashoka','False ashoka'),
                                      ('Gulmohar','Gulmohar'),
                                      ('Neem','Neem'),
                                      ('Peepal','Peepal'),
                                      ('Pilkhan','Pilkhan'),
                                      ('Safeda','Safeda'),
                                      ('Sausage_tree','Sausage tree'),
                                      ('Scholar_tree','Scholar tree'),
                                      ('Semal','Semal')
                                    ],
                    
                     'condition': [ ('Good/Healthy','Good/Healthy'), 
                                    ('Dead/Gone','Dead/Gone'),
                                    ('Bad/Damaged/Sick','Bad/Damaged/Sick'),
                                    ('Bad/Bark-damaged','Bad/Bark-damaged')
                                    
                                  ]
                    }

    

#define a custom wtforms widget and field.
# see https://wtforms.readthedocs.io/en/latest/widgets.html#custom-widgets
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()




class Config(object):
    # ...
    POSTS_PER_PAGE = 3







































