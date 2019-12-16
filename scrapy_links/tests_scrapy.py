import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings

from multiprocessing import Process, Queue
from twisted.internet import reactor, default
import threading
import concurrent.futures
import time

#Project packages
# from testspiders.spiders.followall import FollowAllSpider
from demo_project.spiders.link_scraper import LinkScraper
from tkinter_ui import Application, tk

from helpers import get_urls_fm_csv


start = time.perf_counter()
# Get urls 
url_list = get_urls_fm_csv()
# Set Search Words
search_params = [ 'clubs', 'home', 'about' ]

def react_rest():    
    runner = CrawlerRunner(get_project_settings())
    runner.crawl(LinkScraper, url_list, search_params)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

tries = 4
# global myreactor
# myreactor = None
while tries:
    print(tries)
    tries -= 1
    try:
        
        react_rest()
        
        print('tries ', tries)
    except BaseException:
        print(BaseException)
        #reload reactor
        # from __future__ import division, absolute_import

        import sys
        del sys.modules['twisted.internet.reactor']
        from twisted.internet import selectreactor
        reactor = selectreactor.SelectReactor()
        from twisted.internet.main import installReactor
        installReactor(reactor)
        # default.install()
        # myreactor = reactor
        # reactor._startedBefore=False


# runner = CrawlerRunner(get_project_settings())
# runner.crawl(LinkScraper, url_list, search_params)
# # runner.crawl(LinkScraper, url_list, search_params)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())

# reactor.run()



class QuotesSpider(scrapy.Spider):
    name = "quates"
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            print(quote.css('span.text::text').extract_first())

# the wrapper to make it run more times
def run_spider(spider):
    def f(q):
        try:
            runner = CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

# print('first run:')
# run_spider(QuotesSpider)
# print('\nsecond run:')
# run_spider(QuotesSpider)

# q = Queue()
# def run():
#     # crawler = CrawlerProcess(get_project_settings())
#     runner = CrawlerRunner(get_project_settings())
#     # crawler.crawl(spider_name, url_list, search_params)
#     deferred = runner.crawl('LinkScraper', url_list, search_params)
#     deferred.addBoth(lambda _: reactor.stop())
#     # reactor.run() # the script will block here
#     q.put(reactor.run)

# threads = []
# if isinstance(search_params, list):
#     print(type(search_params))

# for search_param in search_params:
#     t = threading.Thread(target=run)
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()

# print(q)
# print('DONE')



# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()




#@TODO add additional settings
# settings={
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
#     "Cache-Control": "no-cache",
#     "Connection": "keep-alive",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
#     "Referer": "https://github.com/"}