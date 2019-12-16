import scrapy

from link_scraper.items import LinkScraperItem
from link_scraper.pipelines import ErrorHandler



class LinkScraper(scrapy.Spider):
    handle_httpstatus_list = [404, 403, 500]
    name= 'LinkScraper'
    

    # def __init__(self):
    #     self.start_urls = ['https://brownsville.org/members/brownsville-public-library/']
    #     self.search_params = ['home']

    def __init__(self, urls: list, search_params: list):
        self.log_created = False    
        self.start_urls = urls
        self.search_params = search_params
        
   
    def parse_httpbin(self, response):
        if response.status != 200:
            print(f"ERROR\t\tin: {response.url} \t Response: {response.status}")            
            ErrorHandler(self.log_created).err_log(response)
            self.log_created = True
            
        # if isinstance(search_params, list):
        for search_param in self.search_params:
            if search_param !='':
                items= LinkScraperItem().fields
                items['link']= response.xpath(f"//a[contains(translate(@href,  'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{search_param}' )]/@href").get()
                items['url']= response.url
                if items['link']:
                    print(f"FOUND - {search_param}\tin: {response.url}")
                yield items

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)

    # def parse_httpbin(self, response):
    #     self.logger.error('Got successful response from {}'.format(response.url))
    #     # do something useful now

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        # self.logger.error(repr(failure))
        # response = failure.value.response
        # print(f" Error in: .\nDESCR: {failure}")
       
       # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            print('HttpError on %s', response.url, response.status)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            print('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            print('TimeoutError on %s', request.url)