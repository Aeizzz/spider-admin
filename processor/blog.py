from utils.config import *
from utils.spider_core import SpiderCore


class BlogProcessor(BaseProcessor):
    spider_id = 'blog'
    start_requests = [Request(url='http://blog.aeizzz.top/', priority=0)]

    @check
    def process(self, response):
        soup = bs(response.m_response.content, 'lxml')
        items = soup.select('#posts > article > div > link')
        urls = [item.get('href') for item in items]
        for url in urls:
            print(url)
            yield Request(url=url, priority=1, callback=self.process_page_1)

    def process_page_1(self, response):
        soup = bs(response.m_response.content, 'lxml')
        title = soup.select_one('#posts > article > div > header > h1')
        date = soup.select_one('#posts > article > div > header > div > span.post-time > time')
        content = str(soup.select_one('#posts > article > div > div'))

        result = dict()
        result['title'] = title.get_text()
        result['data'] = date.get_text()
        result['content'] = content

        yield pipeItem(['console'], result=result)


spider = SpiderCore(BlogProcessor()).set_pipeline(pipeline=ConsolePipeline(),pipeline_name='console')
