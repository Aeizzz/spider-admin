import json

from fetchman.pipeline.base_pipeline import ItemPipeline


class ConsolePipeline(ItemPipeline):
    def process_item(self, item):
        print(json.dumps(item))
