from app import celery
from manager import manager


@celery.task
def startSpider(namelist):
    for name in namelist:
        if name in manager.spider_list:
            manager.start_spider(name)


@celery.task
def start_spider_id(spider_id):
    '''
    启动单个爬虫
    :param spider_id:
    :return:
    '''
    manager.start(spider_id)
