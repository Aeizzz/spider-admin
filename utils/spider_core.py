#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import time
import traceback
import types
import uuid

from fetchman.downloader.http.spider_request import Request
from fetchman.downloader.requests_downloader import RequestsDownLoader
from fetchman.downloader.selenium_downloader import SeleniumDownLoader
from fetchman.pipeline.pipe_item import pipeItem
from fetchman.scheduler.queue import PriorityQueue
from fetchman.settings import default_settings
from fetchman.utils import FetchManLogger
from fetchman.utils.httpobj import urlparse_cached


def _priority_compare(r1, r2):
    return r2.priority - r1.priority


def _priority_compare_key(item):
    return item.priority


class SpiderCore(object):
    def __init__(self, processor=None, downloader=None, use_proxy=False, scheduler=None, batch_size=None,
                 time_sleep=None, test=False):
        # 用于测试,爬取成功第一个以后结束
        self.test = test
        self._processor = processor
        FetchManLogger.init_logger(processor.spider_id)
        self._host_regex = self._get_host_regex()
        self._spider_status = 'stopped'
        self._pipelines = {}
        self._time_sleep = time_sleep
        if time_sleep:
            self._batch_size = 0
        else:
            if isinstance(downloader, SeleniumDownLoader):
                self._batch_size = default_settings.DRIVER_POOL_SIZE - 1
            else:
                if batch_size:
                    self._batch_size = batch_size - 1
                else:
                    self._batch_size = 9
        self._spider_id = processor.spider_id
        self._process_count = 0

        if not downloader:
            self._downloader = RequestsDownLoader(use_proxy=use_proxy)
        elif isinstance(downloader, SeleniumDownLoader):
            self._downloader = downloader
            self._batch_size = default_settings.DRIVER_POOL_SIZE - 1
        else:
            self._downloader = downloader

        if not scheduler:
            self._queue = PriorityQueue(self._processor)
        else:
            self._queue = scheduler

    def create(self, processor):
        self._processor = processor
        return self

    def set_scheduler(self, scheduler):
        self._queue = scheduler
        return self

    def set_downloader(self, downloader):
        self._downloader = downloader
        if isinstance(downloader, SeleniumDownLoader):
            self._batch_size = default_settings.DRIVER_POOL_SIZE - 1
        return self

    def set_pipeline(self, pipeline=None, pipeline_name=None, ):
        if not pipeline_name:
            pipeline_name = str(uuid.uuid1())
        self._pipelines[pipeline_name] = pipeline
        return self

    def stop(self):
        if self._spider_status == 'stopped':
            FetchManLogger.logger.info("STOP %s SUCCESS" % self._spider_id)
            return
        elif self._spider_status == 'stopping':
            while self._spider_status == 'stopping':
                pass
        elif self._spider_status == 'start':
            self._spider_status = 'stopping'
            while self._spider_status == 'stopping':
                pass

    def start(self):
        try:
            FetchManLogger.logger.info("START %s SUCCESS" % self._spider_id)
            self._spider_status = 'start'
            # 启动爬虫记录日志
            self._queue = PriorityQueue(self._processor)
            if not self._processor.start_requests:
                self._processor.init_start_requests()
            for start_request in self._processor.start_requests:
                if self._should_follow(start_request):
                    start_request.duplicate_remove = False
                    self._queue.push(start_request)
                    FetchManLogger.logger.info("start request:" + str(start_request))
            for batch in self._batch_requests():
                print(batch)
                if len(batch) > 0:
                    self._crawl(batch)
                    if self.test:
                        if self._process_count > 0:
                            return
                if self._spider_status == 'stopping':
                    break
            # 循环结束，记录停止日志

            self._spider_status = 'stopped'
            FetchManLogger.logger.info("STOP %s SUCCESS" % self._spider_id)
        except Exception:
            FetchManLogger.logger.info("%s -- Exception -- Stopped -- %s" % (self._spider_id, traceback.format_exc()))
            self._spider_status = 'stopped'

    def restart(self):
        self._queue = PriorityQueue(self._processor)
        self._queue.clear()
        self.start()

    def _batch_requests(self):
        batch = []
        count = 0
        while True:
            count += 1
            temp_request = self._queue.pop()
            if temp_request:
                if not temp_request.callback:
                    temp_request.callback = self._processor.process
                batch.append(temp_request)
            if len(batch) > self._batch_size or count > self._batch_size:
                if sys.version_info < (3, 0):
                    batch.sort(_priority_compare)
                else:
                    batch.sort(key=_priority_compare_key, reverse=True)
                if len(batch) > 0:
                    yield batch
                else:
                    break
                batch = []
                count = 0

    def _crawl(self, batch):
        responses = self._downloader.download(batch)
        if self._time_sleep:
            time.sleep(self._time_sleep)
        for response in responses:
            callback = response.request.callback(response)
            if isinstance(callback, types.GeneratorType):
                pipe = self._queue.get_pipe()
                for item in callback:
                    if isinstance(item, Request):
                        # logger.info("push request to queue..." + str(item))
                        if self._should_follow(item):
                            self._queue.push_pipe(item, pipe)
                    else:
                        if isinstance(item, pipeItem):
                            # 如果返回对象是pipeItem，则用对应的pipeline处理
                            self._process_count += 1
                            for pipename in item.pipenames:
                                if pipename in self._pipelines:
                                    self._pipelines[pipename].process_item(item.result)
                            if self.test:
                                if self._process_count > 0:
                                    return
                        else:
                            # 如果返回对象不是pipeItem，则默认用每个pipeline处理
                            self._process_count += 1
                            for pipeline in self._pipelines.itervalues():
                                pipeline.process_item(item)
                            if self.test:
                                if self._process_count > 0:
                                    return
                pipe.execute()
            elif isinstance(callback, Request):
                # logger.info("push request to queue..." + str(back))
                if self._should_follow(callback):
                    self._queue.push(callback)
            elif isinstance(callback, pipeItem):
                # 如果返回对象是pipeItem，则用对应的pipeline处理
                self._process_count += 1
                for pipename in callback.pipenames:
                    if pipename in self._pipelines:
                        self._pipelines[pipename].process_item(callback.result)
            else:
                # 如果返回对象不是pipeItem，则默认用每个pipeline处理
                self._process_count += 1
                for pipeline in self._pipelines.itervalues:
                    pipeline.process_item(item)
                if self.test:
                    if self._process_count > 0:
                        return

    def _should_follow(self, request):
        regex = self._host_regex
        # hostname can be None for wrong urls (like javascript links)
        host = urlparse_cached(request).hostname or ''
        return bool(regex.search(host))

    def _get_host_regex(self):
        """Override this method to implement a different offsite policy"""
        allowed_domains = getattr(self._processor, 'allowed_domains', None)
        if not allowed_domains:
            return re.compile('')  # allow all by default
        regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in allowed_domains if d is not None)
        return re.compile(regex)
