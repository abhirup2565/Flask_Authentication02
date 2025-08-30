from flask import Blueprint,jsonify,request
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity
)
from app.models import User,TokenBlockList

auth_blueprint =  Blueprint('auth',__name__)

@auth_blueprint.route('/register',methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))
        if user is not None:
            return jsonify({"error":"user already exist"},409)
        new_user = User(username=data.get('username'),email=data.get('email'))
        new_user.set_password(password = data.get('password'))
        new_user.save()
        return jsonify({"message":"user created"}),200
    except Exception as e:
        return jsonify({"Something went wrong":str(e)}),500
    
@auth_blueprint.route('/login',methods=["POST"])
def login():
    from datetime import timedelta
    try:
        data = request.get_json()
        user = User.get_user_by_username(username = data.get('username'))
        if user and user.check_password(password = data.get('password')):
            access_token = create_access_token(identity=user.username,expires_delta=timedelta(minutes=10))
            refresh_token = create_refresh_token(identity=user.username,expires_delta=timedelta(minutes=20))
            return jsonify({
                "message":"logged in successfully",
                "access Token":access_token,
                "refresh Token": refresh_token
            }),200
        return jsonify({"error":"invalid credential"}),400
    except Exception as e:
        return jsonify({"error":str(e)})
    
@auth_blueprint.route('/who',methods=['GET'])
@jwt_required()
def who():
    return jsonify({
        "message":"user Details",
        "userdetail":{"username":current_user.username,"email":current_user.email}
    })

@auth_blueprint.route('/refresh',methods=["GET"])
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"NEW Access Token":access_token})

@auth_blueprint.route('/logout',methods=["GET"])
@jwt_required(verify_type=False)
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']
    token_block_list = TokenBlockList(jti=jti)
    token_block_list.save()
    return jsonify({"Message":f"{token_type} is revoked successfully"}),200

@auth_blueprint.route('/blocklist',methods=['GET'])
def view_blockList():
    from app.schema import TokenBlockListSchema
    try:
        blockLists = TokenBlockList.query.all()
        result = TokenBlockListSchema().dump(blockLists,many=True)
        jti_list = []
        for blockList in result:
            jti_list.append(blockList.get('jti'))
        return jsonify({"message":result,"jti":jti_list})
    except Exception as e:
        return jsonify({"Something went wrong":str(e)})
    
@auth_blueprint.route('/clearblocklist',methods=["DELETE"])
def clear_blockList():
    from datetime import datetime,timezone,timedelta
    from app.models import TokenBlockList
    try:
        expiryTime = datetime.now(timezone.utc)-timedelta(minutes=10)
        expiryTokens = TokenBlockList.query.filter(TokenBlockList.created_at < expiryTime).all()
        if expiryTokens:
            for expiryToken in expiryTokens:
                expiryToken.deleteBlockList()
            return jsonify({"messages":"all expired tokens were deleted"})
        return jsonify({"message":"No expired Token in db"})
    except Exception as e:
        return jsonify({"error":str(e)})
