import json
import uuid
import datetime
import bcrypt
import base64
import boto3
import os
from models.Images import Images
from models.Users import Users, db
from models.Logs import Logs

S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")
S3_SECRET = os.getenv("S3_SECRET_ACCESS_KEY")
S3_URL_PREFIX = os.getenv("S3_URL_PREFIX")

class User_service():
    def __init__(self) -> None:
        pass

    def create_log(self, api_name, api_type, log_type,log_message,create_date):
        new_log=Logs(api_name=api_name,api_type=api_type,log_type=log_type,log_message=log_message,create_date=create_date)
        db.session.add(new_log)
        db.session.commit()
    
    def split_username_password(self,auth_header):
        auth_token=base64.b64decode(auth_header[6:])
        auth_token=auth_token.decode("utf-8")
        return auth_token.split(':')

    def get_user(self, username, password, Response):
        user=Users.query.filter_by(email=username).first()
        if user==None:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
        password_hash=user.password
        if bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8")):
            response_payload={"id":user.id,"email":user.email,"first_name":user.first_name,"last_name":user.last_name,"account_updated":user.account_updated, "account_created":user.account_created}
            response=Response(json.dumps(response_payload), status=200, mimetype='application/json')
            return response
        else:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
    
    def create_new_user(self, email, password, first_name, last_name, Response):
        hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        account_created_datetime=datetime.datetime.now()
        account_updated_datetime=datetime.datetime.now()
        account_created=account_created_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        account_updated=account_updated_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        uid=str(uuid.uuid4())
        try:
            new_user=Users(email=email,first_name=first_name,last_name=last_name,password=hashed_password.decode("utf-8"),account_created=account_created,account_updated=account_updated,id=uid)
            db.session.add(new_user)
            db.session.commit()
            response_payload={"id":uid,"email":email,"first_name":first_name,"last_name":last_name,"account_created":account_created,"account_updated":account_updated}
            response=Response(json.dumps(response_payload), status=200, mimetype='application/json')
            return response
        except Exception as e:
            response=Response("Email already exists", status=400, mimetype='application/json')
            return response

    def update_user(self, request_json, username, password, Response):
        user=Users.query.filter_by(email=username).first()
        password_hash=user.password
        if user==None:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
        if bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8")):
            if "first_name" in request_json:
                first_name=request_json["first_name"]
                user.first_name=first_name
            if "last_name" in request_json:
                last_name=request_json["last_name"]
                user.last_name=last_name
            if "password" in request_json:
                password=request_json["password"]
                hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
                user.password=hashed_password.decode("utf-8")
            account_updated_datetime=datetime.datetime.now()
            account_updated=account_updated_datetime.strftime("%m/%d/%Y, %H:%M:%S")
            user.account_updated=account_updated
            db.session.commit()
            response_payload={"id":user.id,"email":user.email,"first_name":user.first_name,"last_name":user.last_name,"account_created":user.account_created,"account_updated":user.account_updated}
            response=Response(json.dumps(response_payload), status=200, mimetype='application/json')
            #response=Response(status=204, mimetype='application/json')
            return response
        else:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
    
    def upload_pic(self, username, password, Response, file):
        user=Users.query.filter_by(email=username).first()
        password_hash=user.password
        if user==None:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
        if bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8")):
            try:
                s3 = boto3.resource('s3',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET)
                BUCKET = S3_BUCKET
                s3filename = file.filename
                s3url = str(S3_BUCKET) + "/" + user.id + "/" + s3filename
                print(s3url)
                image = Images.query.filter_by(user_id=user.id).first()
                now=datetime.datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                if image==None:
                    object=s3.Object(BUCKET,user.id+"/"+s3filename)
                    object.put(Body=file)

                    image=Images(filename=s3filename,upload_date=dt_string,user_id=user.id,id=str(uuid.uuid4()),url=s3url)
                    db.session.add(image)
                    db.session.commit()
                    
                else:
                    s3.Object(BUCKET,user.id+"/" + image.filename).delete()
                    object=s3.Object(BUCKET,user.id+"/"+s3filename)
                    object.put(Body=file)

                    image.filename=s3filename
                    image.upload_date=dt_string
                    image.url=s3url
                    db.session.commit()

                response_payload={"id":image.id, "user_id":image.user_id, "file_name":image.filename, "upload_date":image.upload_date, "url":image.url}
                response=Response(json.dumps(response_payload),status=200,mimetype='application/json')
                return response
            except Exception as e:
                user_service=User_service()
                user_service.create_log(api_name='/v1/user/self/pic', api_type='POST', log_type='Error', log_message=str(e), create_date= str(datetime.datetime.now()))
                response=Response("Unauthorized S3 Access", status=401, mimetype='application/json')
                return response
        else:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
    
    def get_picture(self, username,password,Response):
        user=Users.query.filter_by(email=username).first()
        password_hash=user.password
        if user==None:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
        if bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8")):
            try:
                image=Images.query.filter_by(user_id=user.id).first()
                if image==None:
                    response_payload={"status":"No image found for the user"}
                else:
                    response_payload={"file_name":image.filename, "id":image.id, "url":image.url, "upload_date":image.upload_date, "user_id":image.user_id}
                response=Response(json.dumps(response_payload),status=200,mimetype='application/json')
                return response
            except Exception as e:
                user_service=User_service()
                user_service.create_log(api_name='/v1/user/self/pic', api_type='GET', log_type='Error', log_message=str(e), create_date= str(datetime.datetime.now()))
                response=Response("Unauthorized Database Access", status=401, mimetype='application/json')
                return response
        else:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
    
    def delete_picture(self,username,password,Response):
        user=Users.query.filter_by(email=username).first()
        password_hash=user.password
        if user==None:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response
        if bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8")):
            try:
                image=Images.query.filter_by(user_id=user.id).first()
                if image==None:
                    response=Response("Image not found for user",status=404, mimetype="application/json")
                else:
                    s3 = boto3.resource('s3',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET)
                    BUCKET = S3_BUCKET
                    s3.Object(BUCKET,user.id+"/"+image.filename).delete()
                    Images.query.filter_by(user_id=user.id).delete()
                    db.session.commit()
                    response=Response(status=204, mimetype='application/json')
                return response
            except Exception as e:
                user_service=User_service()
                user_service.create_log(api_name='/v1/user/self/pic', api_type='DELETE', log_type='Error', log_message=str(e), create_date= str(datetime.datetime.now()))
                response=Response("Unauthorized Database Access", status=401, mimetype='application/json')
                return response
        else:
            response=Response("Unauthorized", status=401, mimetype='application/json')
            return response

                
       