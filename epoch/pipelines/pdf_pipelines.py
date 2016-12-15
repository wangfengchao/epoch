# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import scrapy

class PdfdownloadPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        item['file_paths'] = file_paths
        return item