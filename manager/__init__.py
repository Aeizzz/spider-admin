from processor.blog import spider
from .spider_manager import SpiderManager

manager = SpiderManager()
manager.set_spider(spider)

