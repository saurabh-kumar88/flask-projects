class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments
    DEBUG = False
    TESTING = False
    # Create in-memory database
    #DATABASE_FILE = 'sample_db.sqlite'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://saurabh88:cyclotron19@saurabh88.mysql.pythonanywhere-services.com/saurabh88$zone0'


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    # Create dummy secrey key so we can use sessions
    SECRET_KEY = '123456790'

    # Create in-memory database
    #DATABASE_FILE = 'sample_db.sqlite'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://saurabh88:cyclotron19@saurabh88.mysql.pythonanywhere-services.com/saurabh88$zone0'


    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security config
    SECURITY_URL_PREFIX = "/users"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/users/"

    SECURITY_POST_LOGOUT_VIEW = "/homepage"
    SECURITY_POST_REGISTER_VIEW = "/login/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Flask-Admin themes

    #FLASK_ADMIN_SWATCH = 'default'
    FLASK_ADMIN_SWATCH = 'cosmo'
    #FLASK_ADMIN_SWATCH = 'cerulean'
    #FLASK_ADMIN_SWATCH = 'readable'
    #FLASK_ADMIN_SWATCH = 'simplex'
    #FLASK_ADMIN_SWATCH = 'slate'
    #FLASK_ADMIN_SWATCH = 'spacelab'
    #FLASK_ADMIN_SWATCH = 'superhero'
    #FLASK_ADMIN_SWATCH = 'united'

    TESTING = False
    DEBUG = True




class ProductionConfig(Config):
    """
    Production configurations
    """
    FLASK_ADMIN_SWATCH = 'cosmo'




app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig

}



