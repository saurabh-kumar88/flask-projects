# third-party imports
import os, os.path
from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand

from flask_bootstrap import Bootstrap
from flask_admin import Admin,  AdminIndexView

from flask_admin.contrib.sqla import ModelView
from flask_security import ( Security, 
                             SQLAlchemyUserDatastore, 
                             UserMixin, 
                             RoleMixin, 
                             login_required,
                             current_user 
                            
                            )

from flask_security.utils import encrypt_password
from flask_admin import helpers as admin_helpers


from flask_admin.contrib import sqla
from flask_script import Manager


# google OAuth2
# client ID: 654434421597-cmrkp2eatave6cksuvm6ti79kh3o72tu.apps.googleusercontent.com
# client secret: 67lyeL6wdHghb7TElx8dfKod


class UserModelView(ModelView):
    create_modal = True
    edit_modal = True
    can_export = True 


'''
Note: flask_migrate commands:
$ flask db init --multidb (for mulitple databases) 
$ flask db migrate
$ flask db upgrade

'''

'''
admin: saurabh@admin.com
password: imgoingin

'''



#local imports
from config import app_config

#db Initialization
db = SQLAlchemy()



def create_app(config_name):
    app = Flask(__name__, static_url_path='/static')
    
    app.config.from_object(app_config['development'])  
    #app.config.from_pyfile('config.py')

    db.init_app(app)

    # This migrate object allow us to run migrations happends in 
    # Database using Flask-Migrate
    # flask migration is so messy and shitty...trying to find some clean alternatives
    migrate = Migrate(app, db)
    
    admin = Admin(app ,'NDMC Streets Trees',
                  base_template='master.html',
                  template_mode='bootstrap3',
                  index_view = AdminIndexView(url='/users'),
                 )

    from models import Role, User, MyModelView, ExtendedConfirmRegisterForm

    
    # zone0
    from models import Specie_Database,Citywide_Benefits,\
    Complains_Maintenance_requests,Maintenance_log

    # zone1 streets 
    from models import Akbar_Road
    
    # zone2 streets 
    from models import Aurangzeb_Lane
    
    # zone3 streets 
    from models import Jashwant_singh_Road
    
    # zone4 streets 
    from models import BD_Marg, BD_Marg_Saplings, BD_Marg_Saplings_growth_data
    from models import BK_Singh_Marg, BK_Singh_Marg_Saplings, BK_Singh_Marg_Saplings_growth_data
    from models import RK_Ashram_Marg, RK_Ashram_Marg_Saplings, RK_Ashram_Marg_Saplings_growth_data
    
    # zone5 streets 
    from models import Abdul_Fazal_Road

    # zone6 streets 
    from models import Arch_Bishop_Marg

    # zone7 streets 
    from models import Aurobindo_Marg
    
    # zone8 streets 
    from models import Sardar_Patel_Marg
    
    # zone9 streets 
    from models import Safdarjung_Road
    
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    
    
    security = Security(app, user_datastore, register_form=ExtendedConfirmRegisterForm)
    
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(UserModelView(Role, db.session))
    
    #-----------zone0---------
    admin.add_view(MyModelView(Specie_Database, db.session, category="Citywide"))
    admin.add_view(MyModelView(Citywide_Benefits, db.session, category="Citywide"))
    admin.add_view(MyModelView(Complains_Maintenance_requests, db.session, category="Citywide"))
    admin.add_view(MyModelView(Maintenance_log, db.session, category="Citywide"))


    #-----------Zone1---------
    admin.add_view(MyModelView(Akbar_Road, db.session, category="Zone1"))

    #-----------Zone2---------
    admin.add_view(MyModelView(Aurangzeb_Lane, db.session, category="Zone2"))

    #-----------Zone3---------
    admin.add_view(MyModelView(Jashwant_singh_Road, db.session, category="Zone3"))

    #-----------Zone4---------
    admin.add_view(MyModelView(BD_Marg, db.session, category="Zone4"))
    admin.add_view(MyModelView(BD_Marg_Saplings, db.session, category="Zone4"))
    admin.add_view(MyModelView(BD_Marg_Saplings_growth_data, db.session, category="Zone4"))


    admin.add_view(MyModelView(BK_Singh_Marg, db.session, category="Zone4"))
    admin.add_view(MyModelView(BK_Singh_Marg_Saplings, db.session, category="Zone4"))
    admin.add_view(MyModelView(BK_Singh_Marg_Saplings_growth_data, db.session, category="Zone4"))

    admin.add_view(MyModelView(RK_Ashram_Marg, db.session, category="Zone4"))
    admin.add_view(MyModelView(RK_Ashram_Marg_Saplings, db.session, category="Zone4"))
    admin.add_view(MyModelView(RK_Ashram_Marg_Saplings_growth_data, db.session, category="Zone4"))

    #-----------Zone5---------
    admin.add_view(MyModelView(Abdul_Fazal_Road, db.session, category="Zone5"))

    #-----------Zone6---------
    admin.add_view(MyModelView(Arch_Bishop_Marg, db.session, category="Zone6"))

    #-----------Zone7---------
    admin.add_view(MyModelView(Aurobindo_Marg, db.session, category="Zone7"))

    #-----------Zone8---------
    admin.add_view(MyModelView(Sardar_Patel_Marg, db.session, category="Zone8"))

    #-----------Zone9---------
    admin.add_view(MyModelView(Safdarjung_Road, db.session, category="Zone9"))
     

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    #register blueprints here



    #from .admin import admin as admin_blueprint
    #app.register_blueprint(admin_blueprint, url_prefix='/admin')

    #from .auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .street import street as street_blueprint
    app.register_blueprint(street_blueprint)
    
    from .streetTrees import streetTrees as streetTrees_blueprint
    app.register_blueprint(streetTrees_blueprint)

    from .developer import developer as developer_blueprint
    app.register_blueprint(developer_blueprint)

    from .aboutMap import aboutMap as aboutMap_blueprint
    app.register_blueprint(aboutMap_blueprint)

    from .DosAndDonts import DosAndDonts as DosAndDonts_blueprint
    app.register_blueprint(DosAndDonts_blueprint)

    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    from .userAccount import userAccount as userAccount_blueprint
    app.register_blueprint(userAccount_blueprint)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errorPage.html', error=e)
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errorPage.html', error=e)

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errorPage.html', error=e)
    
    
    return app








    







'''
We've created a function, create_app that, given a configuration name, 
loads the correct configuration from the config.py file, as well as 
the configurations from the instance/config.py file. 
We have also created a db object which we will use to interact with the database.
'''

