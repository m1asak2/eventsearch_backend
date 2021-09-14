import os
import requests
from bs4 import BeautifulSoup
from typing import List
from model.event import Event, EventTable
from domain.searchbase import SearchBase


class Connpass(SearchBase):
    def __init__(self):
        self.__domain = "https://connpass.com/search/"

    def convert(self, data: Event):
        if data.address and data.address[0]:
            address = "&" + \
                '&'.join([f"prefectures={value}" for value in data.address])
        else:
            address = ""
        start = f"&start_from={data.start_from}"
        end = f"&start_to={data.start_to}"
        keyword = "?q="
        keyword += "+".join([f"{value}" for value in data.keyword])
        # keyword = f"?q={data.keyword[0]}" + r"+" + \
        #     "+".join([f"{value}" for value in data.keyword[1:]])
        url = f"{self.__domain}{keyword}{start}{end}{address}"
        return url, data.limit

    def get(self, url, limit=100):
        res = requests.get(url)
        print(url)
        soup = BeautifulSoup(res.text, "html.parser")
        tablelist: List[EventTable] = []
        while(True):
            events = soup.select(".event_list")
            for event in events:
                # 両端の改行、タブ、空白を削除
                schedule_area = event.select_one('.event_schedule_area')
                event_detail_area = event.select_one('.event_detail_area')
                day = f"{schedule_area.select('.year')[0].text}/{schedule_area.select('.date')[0].text}"
                time = (event_detail_area.select_one('.event_label_area').select_one(".time").text).replace("~", "").replace("〜", "")
                address = event_detail_area.select_one(".icon_place").text.strip()
                title = event_detail_area.select_one(
                    ".event_title").select_one("a").text
                if event_detail_area.select_one(".series_title"):
                    group = event_detail_area.select_one(".series_title").text
                else:
                    group = ""
                img = event_detail_area.select_one(
                    '.image_link').select_one("img")['src']
                link = event_detail_area.select_one(".event_title").a.get("href")
                tablelist.append(EventTable(
                    address=address, title=title, day=day.replace("/", "-"), time=time, group=group, img=img, link=link))
                if len(tablelist) >= limit:
                    return tablelist
            if len(soup.select(".to_next")) > 0:
                next_page = soup.select_one(".to_next").a.get("href")
                url = self.__domain + next_page
                res = requests.get(url)
                soup = BeautifulSoup(res.text, "html.parser")
            else:
                return tablelist
