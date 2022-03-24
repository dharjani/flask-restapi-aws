from . import db

class Users(db.Model):
    __tablename__='Users'
    email=db.Column(db.String(),primary_key=True)
    first_name=db.Column(db.String(),primary_key=False)
    last_name=db.Column(db.String(),primary_key=False)
    password=db.Column(db.String(),primary_key=False)
    account_created=db.Column(db.String(), primary_key=False)
    account_updated=db.Column(db.String(),primary_key=False)
    id=db.Column(db.String(),primary_key=False)

    def __init__(self,email,first_name,last_name,password,account_created,account_updated,id):
        self.email=email
        self.first_name=first_name
        self.last_name=last_name
        self.password=password
        self.account_created=account_created
        self.account_updated=account_updated
        self.id=id
