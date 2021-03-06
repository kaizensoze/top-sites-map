import json
import scrapy
import subprocess
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

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
            lookup(self.hosts)

def lookup(hosts):
    data = []
    for i, host in enumerate(hosts):
        rank = i+1
        
        ip = subprocess.check_output("nslookup %s | grep 'Address' | sed -n 2p | awk '{print $2}'" % host, shell=True).strip()
        
        if ip != "":
            latlng_output = subprocess.check_output("curl -s ipinfo.io/%s" % ip, shell=True)
            latlng_json = json.loads(latlng_output)
            latlng = latlng_json['loc'].strip()
            
            address = subprocess.check_output("curl -s \"http://maps.googleapis.com/maps/api/geocode/json?latlng=%s&sensor=false\" | jq -r '.results[1] | .formatted_address'" % latlng, shell=True).strip()
        else:
            latlng = ""
            address = ""
        
        data.append({
            'rank': rank,
            'host': host,
            'ip': ip,
            'lat_lng': latlng,
            'address': address
        })
        
        print("| %s | %s | %s |" % (rank, host, address))
    
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
