import hashlib
# 一些常用工具
import uuid
from datetime import datetime

from pytz import timezone


class Tools(object):
    def getMD5(self, text):
        '''
        生成md5
        :param text: 输入的内容
        :return: md5
        '''
        m = hashlib.md5()
        m.update(text.encode('UTF-8'))
        return m.hexdigest()

    def getUUID(self):
        '''
        生成64位uuid
        :return:
        '''
        s_uuid = str(uuid.uuid5(uuid.uuid4(), ''))
        l_uuid = s_uuid.split('-')
        return ''.join(l_uuid)

    def getTime(self):
        '''
        获取当前时区的时间
        :return:
        '''
        ZH = timezone('Asia/Shanghai')
        return datetime.now(ZH)


tool = Tools()
