# 统一管理爬虫

# 管理引入头，防止重复引入
from fetchman.pipeline.pipe_item import pipeItem # 爬虫数据管道
from fetchman.processor.base_processor import BaseProcessor # 爬虫基础框架，继承基础类
from fetchman.downloader.http.spider_request import Request # 爬虫请求
from fetchman.utils.decorator import check # 爬虫日志

# 管理自己的pip管道，引用pipeline包下的所有,将所有pipeline文件引入到自己的__init__.py文件下
from pipeline import *


# 引入需要的工具
from bs4 import BeautifulSoup as bs
import json


