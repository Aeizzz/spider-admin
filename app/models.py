from datetime import datetime
from flask import g
from . import db





class DataBase():
    def __init__(this):
        pass

    def save(this):
        db.session.add(this)
        db.session.commit()

    def delete(this):
        db.session.delete(this)
        db.session.commit()


class Logs(db.Model, DataBase):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    spider_id = db.Column(db.String(30))
    date = db.Column(db.Date, default=datetime.now())
    status = db.Column(db.Boolean, default=False)
    count = db.Column(db.Integer, default=0)

    def __init__(self, spider_id, status=False, count=0):
        self.spider_id = spider_id
        self.status = status
        self.count = count
        self.date = datetime.now()
