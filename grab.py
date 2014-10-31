import requests
import lxml.html
import pickle

class Scraper:
    def __init__(self):
        pass

    def grab(self):
        craigslists= ["http://newyork.craigslist.org/","http://cnj.craigslist.org/","http://jerseyshore.craigslist.org/","http://newjersey.craigslist.org/","http://southjersey.craigslist.org/"]
        casual_encounters = []
        for site in craigslists:
            casual_encounters.append(site+"search/w4m")
        indexed_sites = []
        for site in casual_encounters:
            for i in xrange(15):
                if i == 0:
                    indexed_sites.append(site)
                else:
                    indexed_sites.append(site+"?s="+str(i)+"00&")
        
    
