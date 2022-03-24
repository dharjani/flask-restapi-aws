from flask import Flask
from routes.healthcheck_routes import healthcheck_routes
from routes.user_routes import user_routes
import os
from dotenv import load_dotenv

load_dotenv()

rds_host = os.getenv('RDS_HOST')
rds_db = os.getenv('RDS_DB')
rds_user = os.getenv('RDS_USERNAME')
rds_pwd = os.getenv('RDS_PWD')
conn_string = 'mysql+pymysql://' + str(rds_user) + ':' + str(rds_pwd) + '@' + str(rds_host) + '/' + str(rds_db)

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  conn_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)

app.register_blueprint(healthcheck_routes)
app.register_blueprint(user_routes)

if __name__=='__main__':
    app.run('0.0.0.0', port=8080)