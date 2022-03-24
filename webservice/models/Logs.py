from . import db

class Logs(db.Model):
    __tablename__='Logs'
    LogId=db.Column(db.Integer(),primary_key=True)
    api_name=db.Column(db.String(),primary_key=False)
    api_type=db.Column(db.String(),primary_key=False)
    log_type=db.Column(db.String(),primary_key=False)
    log_message=db.Column(db.String(),primary_key=False)
    create_date=db.Column(db.String(), primary_key=False)

    def __init__(self,api_name,api_type,log_type,log_message,create_date):
        self.api_name=api_name
        self.api_type = api_type
        self.log_type=log_type
        self.log_message=log_message
        self.create_date=create_date
