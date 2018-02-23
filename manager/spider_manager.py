import threading


class SpiderManager(object):
    def __init__(self):
        self.spider_list = dict()

    # 增加一个爬虫
    def set_spider(self, spider):
        self.spider_list[spider._spider_id] = spider

    # 启动一个爬虫
    def start_spider(self, spider_id):
        if self.spider_list[spider_id]._spider_status == "stopped":
            thread = threading.Thread(target=self.spider_list[spider_id].start)
            thread.setDaemon(False)
            thread.start()

    # 停止一个爬虫
    def stop_spider(self, spider_id):
        self.spider_list[spider_id].stop()

    # 删除一个爬虫
    def delete_spider(self, spider_id):
        self.spider_list.pop(spider_id)

    # 获取一个spider
    def get_spider_detail(self, spider_id):
        spider = self.spider_list[spider_id]
        return spider

    def start(self,spider_id):
        '''
        非多线程启动爬虫
        :param spider_id:
        :return:
        '''
        if self.spider_list[spider_id]._spider_status == 'stopped':
            self.spider_list[spider_id].start()

