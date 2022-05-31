import requests
from bs4 import BeautifulSoup
import pandas as pd

class Ad():
    def __init__(self, ad_no, position, employer, location, date_pub, date_ad, date_res, status, link_res, link_ad):
        self.ad_no = ad_no
        self.position = position
        self.employer = employer
        self.location = location
        self.date_pub = date_pub
        self.date_ad = date_ad
        self.date_res = date_res
        self.status = status
        self.link_res = link_res
        self.link_ad = link_ad

    def add(self, ads):
        ads.append(Ad(self.ad_no, self.position, self.employer, self.location, self.date_pub, self.date_ad, self.date_res, self.status, self.link_res, self.link_ad))

def mth_change(month):
    table = {
    "stycznia": "01",   "lutego": "02",
    "marca": "03",       "kwietnia": "04",
    "maja": "05",           "czerwca": "06",
    "lipca": "07",       "sierpnia": "08",
    "września": "09",  "października": "10",
    "listopada": "11", "grudnia": "12"
    }
    month_replaced = table[month]
    return month_replaced

URL = "https://nabory.kprm.gov.pl/wyniki-naborow?AdResult%5BpagesCnt%5D=20&AdResult%5BisAdvancedMode%5D=&AdResult%5Bsort%5D=1&AdResult%5Bid%5D=&AdResult%5Bid_institution%5D=&AdResult%5Bid_institution_position%5D="

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

ads = []

listing = soup.find_all("a", class_="single")

for listing in listing:
    ad_no = listing.find_next("span", class_="id")
    job_pos = listing.find_next("strong", class_="title")
    job_empl = listing.find_next("b")
    job_loc = job_empl.find_next("b")
    date_pub = job_loc.find_next("b")
    link_res = "https://nabory.kprm.gov.pl"+listing["href"]
    page = requests.get(link_res)
    soup = BeautifulSoup(page.content, "html.parser")
    link_ad = soup.find("a", class_="btn btn-b")
    link_ad = "https://nabory.kprm.gov.pl"+link_ad["href"]
    date_ad = soup.find("div", class_="box bor")
    day = date_ad.find_next("strong")
    day = day.get_text()
    month = date_ad.find_next("p")
    year = month.find_next("p")
    year = year.get_text()
    month = mth_change(month.text.strip())
    date_added = day + "." + month + "." + year
    date_res = date_ad.find_next("div", class_="box bor")
    day = date_res.find_next("strong")
    day = day.get_text()
    month = date_res.find_next("p")
    year = month.find_next("p")
    year = year.get_text()
    month = mth_change(month.text.strip())
    date_resulted = day + "." + month + "." + year
    status = soup.find("strong", class_="c")
    status = status.get_text(" ")
    Ad.add((Ad(ad_no.text.strip(), job_pos.text.strip(), job_empl.text.strip(), job_loc.text.strip(), date_pub.text.strip(), date_added, date_resulted, status, link_res, link_ad)), ads)



# for ad in ads:
#     print(ad.ad_no, ad.position, ad.employer, ad.location, ad.date_pub, ad.date_ad, ad.date_res, ad.status, ad.link_res, ad.link_ad)

df = pd.DataFrame([t.__dict__ for t in ads])
print(df)