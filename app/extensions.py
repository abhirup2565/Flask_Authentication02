from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_apscheduler.scheduler import BackgroundScheduler 

db = SQLAlchemy()
jwt = JWTManager()
cron = BackgroundScheduler()
