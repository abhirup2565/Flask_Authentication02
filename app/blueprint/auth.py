from flask import Blueprint,jsonify,request
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user
)
from app.models import User,TokenBlockList

auth_blueprint =  Blueprint('auth',__name__)

@auth_blueprint.route('/register',methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))
    
    except Exception as e
