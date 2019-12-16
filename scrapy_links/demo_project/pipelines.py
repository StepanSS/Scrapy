# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DemoProjectPipeline(object):

    def __init__(self):
        with open('res.csv', 'w') as f:
            f.write("BASE-LINK, match_URL")
        

    def process_item(self, item, spider):
        if item.get('link'):
            with open('res.csv', 'a') as f:
                f.write(f"\n{item['url']}, {item['link']}")
        return item

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

