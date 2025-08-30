from flask import Flask
from app.extensions import db,jwt
from dotenv import load_dotenv
load_dotenv()

def createapp():
    app = Flask(__name__)

    #config files
    app.config.from_prefixed_env()

    #initialize app extensions
    db.init_app(app)
    jwt.init_app(app)
    
    #initializing blueprint 
    

    return app