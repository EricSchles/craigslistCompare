import requests
import lxml.html
import pickle
import grequests
import pandas as pd

class Scraper:
    def __init__(self):
        pass

    def setup(self,num_pages=2):
        craigslists= ["http://newyork.craigslist.org/","http://cnj.craigslist.org/","http://jerseyshore.craigslist.org/","http://newjersey.craigslist.org/","http://southjersey.craigslist.org/"]
        casual_encounters = []
        ads = []
        for site in craigslists:
            base = site
            site = site+"search/w4m"
            urls = []
            for i in xrange(num_pages):
                if i == 0:
                    urls.append(site)
                else:
                    urls.append(site+"?s="+str(i)+"00&")
            rs = (grequests.get(u) for u in urls)
            responses = grequests.map(rs)
            for r in responses:
                html = lxml.html.fromstring(r.text)
                links = html.xpath("//a/@href")
                for link in links:
                    if "search" in link:
                        continue
                    if "http" in  link:
                        continue
                    if "w4m" in link:
                        link = "http://"+r.url.split("/")[-3]+link
                        if not link in ads:
                            ads.append(link)
        return ads

    def parse(self,r):
        values = {}
        text = r.text.encode("ascii","ignore")
        html = lxml.html.fromstring(text)
        values["title"] = [i.text_content() for i in html.xpath('//h2[@class="postingtitle"]')]
        values["body"] = [i.text_content() for i in html.xpath('//section[@id="postingbody"]')]
        return values

    def save(self,r):
        name = "_".join(r.url.split("/")[-2:])
        text = r.text.encode("ascii","ignore")
        with open(name,"w") as f:
            f.write(text)
        
    def run(self):
        ads = self.setup()
        df = pd.DataFrame()
        rs = (grequests.get(u) for u in ads)
        responses = grequests.map(rs)
        now = time.strftime("%m_%d_%y_%H")
        folder = craigslist+now
        if not os.path.exists(folder):
            os.mkdir(folder)
        os.chdir(folder)
        if not os.path.exists("ads"):
            os.mkdir("ads")
        os.chdir("ads")
        for r in responses:
            self.save(r.text)
            df = df.append(self.parse(r),ignore_index=True)
        os.chdir("../")
        df.to_csv("craigslist_data.csv")
        
        
