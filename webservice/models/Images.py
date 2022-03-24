from . import db

class Images(db.Model):
    __tablename__='Images'
    filename=db.Column(db.String(),primary_key=False)
    upload_date=db.Column(db.String(),primary_key=False)
    user_id=db.Column(db.String(),primary_key=False)
    url=db.Column(db.String(), primary_key=False)
    id=db.Column(db.String(),primary_key=True)

    def __init__(self,filename,upload_date,user_id,url,id):
        self.filename=filename
        self.upload_date=upload_date
        self.user_id=user_id
        self.url=url
        self.id=id
