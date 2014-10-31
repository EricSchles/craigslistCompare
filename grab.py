import requests
import lxml.html
import pickle
import grequests

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
        for r in responses:
            
                    
