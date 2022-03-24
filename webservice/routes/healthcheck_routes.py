import imp


import os
import json
import datetime
from service.user_service import User_service
from flask import Blueprint, Response

S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")
S3_SECRET = os.getenv("S3_SECRET_ACCESS_KEY")
S3_URL_PREFIX = os.getenv("S3_URL_PREFIX")
RDS_USERNAME=os.getenv("RDS_USERNAME")
RDS_PWD=os.getenv("RDS_PWD")
RDS_DB=os.getenv("RDS_DB")
RDS_HOST=os.getenv("RDS_HOST")

healthcheck_routes=Blueprint('healthcheck_routes',__name__)

@healthcheck_routes.route('/healthz',methods = ['GET'])
def index():
    response=Response('{"status":"service is up and running"}', status=200, mimetype='application/json')
    return response

@healthcheck_routes.route('/envvar',methods = ['GET'])
def env_varibales():
    try:
        env_var = {"S3_BUCKET" : str(S3_BUCKET), "S3_KEY" : str(S3_KEY), "S3_SECRET" : str(S3_SECRET), "S3_URL_PREFIX" : str(S3_URL_PREFIX), "RDS_USERNAME" : str(RDS_USERNAME), "RDS_PWD" : str(RDS_PWD), "RDS_DB" : str(RDS_DB), "RDS_HOST" : str(RDS_HOST)}
        response=Response(json.dumps(env_var), status=200, mimetype='application/json')
        return response
    except Exception as e:
        user_service=User_service()
        user_service.create_log(api_name='/v1/user/self', api_type='GET', log_type='Error', log_message=str(e), create_date= str(datetime.datetime.now()))
        response=Response("Unexpected Error Occurred - " + str(e), status=500, mimetype='application/json')
        return response
