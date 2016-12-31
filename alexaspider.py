import json
import scrapy
import subprocess

class AlexaTopGlobalSpider(scrapy.Spider):
    name = 'alexatopglobalspider'
    start_urls = ['http://www.alexa.com/topsites']
    hosts = []
    
    def parse(self, response):
        for site_listing in response.css('li.site-listing'):
            host = site_listing.css('p.desc-paragraph a ::text').extract_first()
            self.hosts.append(host)
        
        next_page = response.css('a.next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        else:
            self.export()
    
    def export(self):
        with open('tophosts.txt', 'w') as f:
            f.write('\n'.join(self.hosts))
        f.close()
