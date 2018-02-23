from flask import current_app
import time
from .. import scheduler

def add_job():
    while True:
        print('1111111----------------1111111111111111111111')


def test():
    job = {
        'id':'rds-to-mysql-1',
        'fun':'add_job',
        'args':'',
    }
    result = current_app.apscheduler.add_job(func=__name__+':'+job['func'], id=job['id'], trigger='interval', seconds=1)
    print(result)
    print('123')
