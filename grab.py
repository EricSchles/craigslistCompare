import requests
import lxml.html
import pickle
class Scraper:
    def __init__(self):
        pass
    
    def get_nynj_craigslist(self):
        ny_nj_craigslist = ["newyork","cnj","jerseyshore","newjersey","southjersey"]
        r = requests.get("https://www.craigslist.org/about/sites")
        html = lxml.html.fromstring(r.text)
        craigslists = html.xpath("//a/@href")
        links = []
        for i in craigslists:
            if "craigslist" in i:
                for area in ny_nj_craigslist:
                    if area in i:
                        if not "www" in i:
                            i = str(i)
                            links.append(i)
        with open("nynj_craigslists","w") as f:
            pickle.dump(links,f)


    def grab(self):
        
    
    
    
