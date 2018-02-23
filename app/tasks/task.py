from app import celery
from manager import manager

@celery.task
def startSpider(namelist):
    for name in namelist:
        print(name)
        if name in manager.spider_list:
            manager.start_spider(name)
