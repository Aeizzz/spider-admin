from flask import jsonify, request, Blueprint

from manager import manager
from ..tasks.task import startSpider,start_spider_id

api = Blueprint('api', __name__, url_prefix='/api')

from app.models import Logs


@api.route('/')
def info():
    log = Logs(spider_id='asdasd')
    log.save()
    return jsonify({})


# 启动某个爬虫
@api.route('/start')
def start_spider():
    spider_id = request.args['spider_id']
    data = dict()
    if manager.get_spider_detail(spider_id)._spider_status == 'start':
        data['code'] = 1
        data['msg'] = 'error'
        data['spider_id'] = spider_id
        return jsonify(data)
    start_spider_id.apply_async(args=[spider_id])
    data = dict()
    data['code'] = 0
    data['msg'] = 'success'
    data['spider_id'] = spider_id
    return jsonify(data)


@api.route('/stop')
def stop_spider():
    spider_id = request.args['spider_id']
    manager.stop_spider(request.args['spider_id'])
    data = dict()
    data['code'] = 0
    data['msg'] = 'success'
    data['spider_id'] = spider_id
    return jsonify(data)


# 获取单个爬虫的信息
def get_spider_detail(spider_id):
    spider = manager.get_spider_detail(spider_id)
    data = dict()
    data['spider_id'] = spider_id
    data['spider_name'] = spider._processor.spider_id
    data['status'] = spider._spider_status
    data['count'] = spider._process_count
    return data


# 展示所有爬虫的信息，返回json
@api.route('/show')
def show():
    spider_id = request.args['spider_id']
    if spider_id:
        data = get_spider_detail(spider_id)
        data_re = dict()
        data_re['spiders'] = [data]
        data_re['code'] = 0
        return jsonify(data_re)
    list = manager.spider_list
    datalist = []

    for key, value in list.items():
        data = dict()
        data['spider_id'] = key
        data['spider_name'] = value._processor.spider_id
        data['status'] = value._spider_status
        data['count'] = value._process_count
        datalist.append(data)
    # print(datalist)
    data_re = dict()
    data_re['spiders'] = datalist
    data_re['code'] = 0
    return jsonify(data_re)


@api.route('/timing', methods=['POST', 'GET'])
def celery():
    '''
    post 设置定时任务，name任务名称，list任务列表，time时间
    get 获取已经设置的定时任务
    :return:
    '''
    if request.method == 'POST':
        name_list = request.form.getlist('list')
        startSpider.apply_async(args=[name_list])
        return jsonify({'code': 0, 'msg': 'success'})
    elif request.method == 'GET':
        pass

@api.route('/add_job',methods=['POST','GET'])
def add_job():
    name_list = request.form.getlist('list')
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    hour = request.form.get('hour')
    minute = request.form.get('minute')

    pass



