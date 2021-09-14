from domain.connpass2 import Connpass
from domain.doorkeeper import Doorkeeper
from domain.searchbase import SearchBase
from model.event import Event, EventTable
from model.bases import Bases


class Factory:
    def __init__(self, target: str):
        self.strategy_dic = {
            'connpass': Connpass(),
            'doorkeeper': Doorkeeper()
        }
        self.strategy: SearchBase = self.strategy_dic[target]
        # self.base = SearchBase()

    def check_strategy(self):
        print(self.strategy.__class__.__name__)
        return self.strategy.__class__.__name__

    def get_event(self, data: Event):
        return self.strategy.get_event(data)


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
