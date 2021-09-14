from model.event import Event, EventTable
from typing import List
import os
from bs4 import BeautifulSoup
import requests
import datetime
from domain.searchbase import SearchBase
import re


class Doorkeeper(SearchBase):
    def __init__(self):
        self.__domain = "http://api.doorkeeper.jp/events/"

    def convert(self, data: Event):
        if data.address and data.address[0]:
            tmp = [f"prefecture={value}" if value != "online" and value is str else ""
                   for value in data.address]
            address = "&" + \
                '&'.join(tmp)
            if address == "&":
                address = ""
        else:
            address = ""
        start = f"&since={data.start_from}"
        end = f"&until={data.start_to}"
        # limit = f"&page={data.limit}"
        sort = "&sort=starts_at"
        keyword = "?q="
        keyword += "+".join([f"{value}" for value in data.keyword])
        url = f"{self.__domain}{keyword}{start}{end}{address}{sort}"
        print(url)
        return url, data.limit

    def get(self, url, limit=0):
        events: list = requests.get(url).json()

        tablelist: List[EventTable] = []
        for i, dic in enumerate(events):
            if not (i < limit):
                break
            res: dict = dic["event"]
            title = res["title"]
            address = 'オンライン' if res["address"] is None else res["address"]
            img = res["banner"] if "banner" in res else ""
            link = res["public_url"]
            res = requests.get(link)
            soup = BeautifulSoup(res.text, "html.parser")
            info_date: str = soup.select_one('.community-event-info-date').text.strip()
            day, time = self.get_date(info_date)
            group: str = soup.select_one('.community-header-info').select_one('.community-title').select_one('a').text
            tablelist.append(EventTable(
                address=address, title=title, day=day, time=time, group=group, img=img, link=link))
        return tablelist

    def get_date(self, date: str):
        regex_year = re.compile(r'\d{4}-\d{2}-\d{2}')
        regex_time = re.compile(r'\d{2}:\d{2}')
        if not regex_year.search(date):
            date = datetime.datetime.strptime(date.split("-")[0], '%a, %d %b %Y %H:%M ').strftime('%Y-%m-%d %H:%M')
        return regex_year.search(date).group(0), regex_time.search(date).group(0)
