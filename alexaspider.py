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
        data = []
        for i, host in enumerate(self.hosts):
            print(i, host)
            
            ip = subprocess.check_output("ping -c 1 %s | grep '64 bytes from ' | awk '{print $4}' | cut -d ':' -f1" % host, shell=True).strip()
            
            latlng_output = subprocess.check_output("curl ipinfo.io/%s" % ip, shell=True)
            latlng_json = json.loads(latlng_output)
            latlng = latlng_json['loc'].strip()
            
            data.append({
                'host': host,
                'ip': ip,
                'loc': latlng
            })
        
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    
