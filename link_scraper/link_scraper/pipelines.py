# -*- coding: utf-8 -*-
import json
from urllib.parse import urlsplit, urlunsplit

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class LinkScraperPipeline(object):

    def __init__(self):
        with open('res.csv', 'w') as f:
            f.write("BASE-LINK, match_URL")
        

    def process_item(self, item, spider):
        if item.get('link'):
            with open('res.csv', 'a') as f:
                f.write(f"\n{item['url']}, {item['link']}")
        return item

class LinkScraperPipelineSorted(object):

    def open_spider(self, spider):
        self.res_dict = {}
        self.file_sorted = open('res_sorted.csv', 'w')
        self.file_sorted.write("URL_ID, BASE_LINK, MATCH_URL")

    def close_spider(self, spider):
        for key, value in sorted(self.res_dict.items()):
            line = f"""\n{value['item_id']}, {value['item_url']}, {value['item_link']}"""
            # print(value)
            self.file_sorted.write(line)
        self.file_sorted.close()

    def process_item(self, item, spider):
        if item['link']:
            item_id = item['url_id']
            item_url = item['url']
            item_link = item['link']
            item_link = self._build_full_link(item_link, item_url)
            item_link = self._filter_external_links(item_link, item_url)
            if item_link:
                self.res_dict[item_id] = {  'item_id': item_id,
                                            'item_url': item_url, 
                                            'item_link': item_link }
        return item
    
    def _build_full_link(self, link, base_link):
        """ Add base URL if required.
            Return full URL.
        """
        if 'http' not in link:
            split_url = urlsplit(base_link)
            root_url = f'{split_url.scheme}://{split_url.netloc}'
            link = root_url + link
        return link
    
    def _filter_external_links(self, link, base_link):
        """ Filter all external link. Return `False` if link is external."""
        split_url = urlsplit(base_link)
        if split_url.netloc in link:
            return link
        else:
            return False


class ErrorHandler(object):

    def __init__(self, file_created):
        if not file_created:
            with open('errors.csv', 'w') as f:
                f.write("BASE-LINK, Response Status")

    def err_log(self, response):
        if response.url:
            with open('errors.csv', 'a') as f:
                f.write(f"\n{response.url}, {response.status}")
        return response

