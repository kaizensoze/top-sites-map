import json
import scrapy
import subprocess

class AlexaTopGlobalSpider(scrapy.Spider):
    name = 'alexatopglobalspider'
    start_urls = ['http://www.alexa.com/topsites']
    
    def parse(self, response):
        hosts = []
        for site_listing in response.css('li.site-listing'):
            host = site_listing.css('p.desc-paragraph a ::text').extract_first()
            hosts.append(host)
        
        host_to_ip = {}
        ip_to_latlng = {}
        for host in hosts:
            ip = subprocess.check_output("ping -c 1 %s | grep '64 bytes from ' | awk '{print $4}' | cut -d ':' -f1" % host, shell=True)
            host_to_ip[host] = ip.strip()
            
            json_text = subprocess.check_output("curl ipinfo.io/%s" % ip, shell=True)
            latlng_json = json.loads(json_text)
            latlng = latlng_json['loc']
            ip_to_latlng[ip] = latlng.strip()
        
        # write to json
        with open('data.json', 'w') as outfile:
            out = []
            for host in hosts:
                out.append({
                    'host': host,
                    'ip': host_to_ip[host],
                    'loc': ip_to_latlng[ip]
                })
            json.dump(out, outfile)
