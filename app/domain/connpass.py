import os
import requests
import datetime
from dateutil.relativedelta import relativedelta
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
# from model.event import Event
domain = "https://connpass.com/api/v1/event/"
key = "python"
keyword = f"?keyword={key}"


search = f"{domain}{keyword}"


class SearchBase(metaclass=ABCMeta):
    def __init_value(self):
        pass

    @abstractmethod
    def convert(self, dic: dict):
        '''
        取得先に合わせて型変換
        '''
        pass

    @abstractmethod
    def get(self, url):
        pass

    def get_event(self, dic: dict):
        self.__init_value()
        url = self.convert(dic)
        print(url)
        data = self.get(url)
        return self.terminate(data)

    # @abstractmethod
    def terminate(self, data):
        return data

    def day(self, month=None):
        res = datetime.date.today()
        if month:
            res += relativedelta(months=month)
        return res.strftime('%Y%m%d')

    def set_key(self, dic: dict, key: str, head: str, default=""):
        default = default if default == "" else f"{head}{default}"
        return f"{head}{dic[key]}" if key in dic else default


class Connpass(SearchBase):
    def __init__(self):
        self.__domain = "https://connpass.com/api/v1/event/"

    def convert(self, dic: dict):
        address = self.set_key(dic, "address", "&keyword_or=")
        start = self.set_key(dic, "start", "&ym=", self.day())
        end = self.set_key(dic, "end", "&ymd=", self.day(6))
        count = self.set_key(dic, "count", "&count=", 10)
        # 開催日時順
        order = self.set_key(dic, "order", "&order=", 1)
        keyword = f"?keyword={dic['key']}"
        url = f"{self.__domain}{keyword}{address}{order}{count}"
        return url
    # def convertRaw(self,):

    def get(self, url):
        # events = requests.get(url).json()["events"]
        events = requests.get(
            "https://connpass.com/api/v1/event/?keyword=python&keyword_or=osaka,=online&order=1").json()["events"]
        print(len(events))
        events = requests.get(
            "https://connpass.com/api/v1/event/?keyword=python&keyword=osaka&order=1").json()["events"]
        print(len(events))

        res = requests.get(
            "https://connpass.com/search/?q=python&start_from=2021/01/18&start_to=2021/07/05&prefectures=osaka&selectItem=osaka")
        soup = BeautifulSoup(res.text, "html.parser")
        events = soup.find()
        print(len(events))
        # print(events)
        for lst in events:
            print(f'{lst["title"]},{lst["started_at"]},{lst["address"]}')


class Doorkeeper(SearchBase):
    def __init__(self):
        self.__domain = "http://api.doorkeeper.jp/events/"

    def convert(self, dic: dict):
        address = self.set_key(dic, 'address', "&prefecture_id=")
        start = self.set_key(dic, 'start', "&since=", self.day())
        keyword = f"?q={dic['key']}" if dic["key"] != "" else ""
        url = self.__domain
        if keyword != "":
            url += f"{keyword}{address}{start}"
        print(url)
        return url

    def get(self, url):
        events = requests.get(url).json()
        print(type(events))
        # print(events)
        for dic in events:
            print(dic["event"]["title"])


class Factory:
    def __init__(self, strategy: SearchBase):
        self.strategy = strategy()
        print(strategy)
        # self.base = SearchBase()

    def check_strategy(self):
        print(self.strategy.__class__.__name__)
        return self.strategy.__class__.__name__

    def get_event(self, dic: dict):
        return self.strategy.get_event(dic)


# def main():
#   a = Connpass()
#   b = {"key": "python", "address": "osaka"}
#   # print(b)
#   # res = a.get(a.convert(b))
#   # print(res)

#   fac = Factory(Connpass)
#   print(fac.get_event(b))
#   # print(fac.check_strategy())


# if __name__ == "__main__":
#   main()
