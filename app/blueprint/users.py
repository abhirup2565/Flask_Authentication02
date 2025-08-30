from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt
from app.models import User
from app.schema import UserSchema

user_blueprint = Blueprint('users',__name__)

@user_blueprint.route("/all",methods=["GET"])
@jwt_required()
def get_all_users():
    claims = get_jwt()
    print(claims)
    if claims.get("is_staff"):
        page = request.args.get('page',default=1,type=int)
        per_page = request.args.get('per_page',default=3,type=int)
        user = User.query.paginate(page=page,per_page=per_page)
        result = UserSchema().dump(user,many=True)

        return jsonify(
            {
                "users":result,
            }
        ),200
    return jsonify({"message":"You are not authorized"}),403