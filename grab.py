import requests
import lxml.html
import pickle
import grequests
import pandas as pd
class Scraper:
    def __init__(self):
        pass

    def setup(self):
        craigslists= ["http://newyork.craigslist.org/","http://cnj.craigslist.org/","http://jerseyshore.craigslist.org/","http://newjersey.craigslist.org/","http://southjersey.craigslist.org/"]
        casual_encounters = []
        for site in craigslists:
            casual_encounters.append(site+"search/w4m")
        urls = []
        for site in casual_encounters:
            for i in xrange(15):
                if i == 0:
                    urls.append(site)
                else:
                    urls.append(site+"?s="+str(i)+"00&")
        rs = (grequests.get(u) for u in urls)
        responses = grequests.map(rs)
        ads = []
        for r in responses:
            html = lxml.html.fromstring(r.text)
            links = html.xpath("//a/@href")
            for link in links:
                if "w4m" in link:
                    ads.append("http://"+r.url.split("/")[-3]+link)
        return ads

    def parse(self,link):
        values = {}
        html = lxml.html.fromstring(r.text)
        title = html.xpath('//h2[@class="postingtitle"]')
        body = html.xpath('//section[@id="postingbody"]')

    def run(self):
        ads = self.setup()
        df = pd.DataFrame()
        rs = (grequests.get(u) for u in ads)
        responses = grequests.map(rs)
        for r in responses:
            self.parse(r.text)
            
