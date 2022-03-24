import re
import os
import datetime
from service.user_service import User_service
from flask import Blueprint, Response, request

user_routes=Blueprint('user_routes', __name__)

@user_routes.route('/v1/user/self', methods=['GET'])
def get_user():
    try:
        auth_header=request.headers.get('Authorization')
        user_service = User_service()
        [username, password] = user_service.split_username_password(auth_header=auth_header)
        return user_service.get_user(username,password,Response)
    except Exception as e:
        user_service=User_service()
        user_service.create_log(api_name='/v1/user/self', api_type='GET', log_type='Error', log_message=str(e), create_date= str(datetime.datetime.now()))
        response=Response("Unexpected Error Occurred - " + str(e), status=500, mimetype='application/json')
        return response

@user_routes.route('/v1/user', methods=['POST'])
def add_new_user():
    request_json=request.get_json()
    print(request_json)
    if "email" not in request_json or "first_name" not in request_json or "last_name" not in request_json or "password" not in request_json:
        response=Response("Mandatory Fields Missing", status=400, mimetype='application/json')
        return response
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email=request_json["email"]
    if(re.fullmatch(regex, email)):
        first_name=request_json["first_name"]
        last_name=request_json["last_name"]
        password=request_json["password"]
        user_service=User_service()
        return user_service.create_new_user(email=email,first_name=first_name,last_name=last_name,password=password, Response=Response)
    else:
        response=Response("Invalid Email", status=400, mimetype='application/json')
        return response

@user_routes.route('/v1/user/self', methods=['PUT'])
def update_user():
    auth_header=request.headers.get('Authorization')
    user_service = User_service()
    [username, password] = user_service.split_username_password(auth_header=auth_header)
    request_json=request.get_json()
    return user_service.update_user(request_json=request_json, username=username, password=password, Response=Response)

@user_routes.route('/v1/user/self/pic', methods=['POST'])
def add_pic():
    auth_header=request.headers.get('Authorization')
    user_service = User_service()
    [username, password] = user_service.split_username_password(auth_header=auth_header)
    if 'profilePic' not in request.files:
        response=Response("Invalid File",status=400, mimetype='application/json')
        return response
    file = request.files['profilePic']
    return user_service.upload_pic(username=username,password=password,Response=Response,file=file)

@user_routes.route('/v1/user/self/pic', methods=['GET'])
def get_pic():
    auth_header=request.headers.get('Authorization')
    user_service = User_service()
    [username, password] = user_service.split_username_password(auth_header=auth_header)
    return user_service.get_picture(username=username,password=password,Response=Response)

@user_routes.route('/v1/user/self/pic', methods=['DELETE'])
def delete_pic():
    auth_header=request.headers.get('Authorization')
    user_service = User_service()
    [username, password] = user_service.split_username_password(auth_header=auth_header)
    return user_service.delete_picture(username=username,password=password,Response=Response)