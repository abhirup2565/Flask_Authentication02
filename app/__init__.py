from flask import Flask,jsonify
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
    from app.blueprint import auth_blueprint
    from app.blueprint import user_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)

    #load users
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header,jwt_data):
        from app.models.users import User
        identity = jwt_data['sub']
        return User.query.filter_by(username = identity).one_or_none()
    
    #additional claims for jwt
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == "abhirup":
            return{"is_staff":True}
        return{"is_staff":False}
    
    #jwt error handler
    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header,jwt_data):
        return jsonify({"message":"Token is expired","error":"Token expired"}),401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"Signature verification failed","error":"invalid token"}),401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message":"Request does not contain valid token","error":"authorization_header"}),401

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
        from app.models.token import TokenBlockList
        jti = jwt_data['jti']
        token=db.session.query(TokenBlockList).filter(TokenBlockList.jti==jti).scalar()
        return token is not None

    return app

    

    return app