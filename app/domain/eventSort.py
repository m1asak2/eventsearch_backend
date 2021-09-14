from typing import List, Dict
import re
from model.event import EventTable


def sort_date(list: List[EventTable]):
    dic: Dict[int, int] = {}
    regex_year = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    for (i, table) in enumerate(list):
        date = regex_year.search(table.day).groups()
        num: int = int(int(date[0]) * 1e4 + int(date[1]) * 1e2 + int(date[2]))
        dic[i] = num
    sortedDic = sorted(dic.items(), key=lambda x: x[1])
    res: List[EventTable] = []
    for (key, val) in sortedDic:
        res.append(list[key])
    return res


def compare_fast(ref: str, target: str):
    regex_year = re.compile(r'(\d{4})-(\d{2})-(\d{2})')

    def compare(ref: List[str], target: List[str]):
        if len(ref) < 1:
            return None
        if ref[0] == target[0]:
            return compare(ref[1:], target[1:])
        elif int(ref[0]) < int(target[0]):
            return True
        return False
    r_ref = regex_year.search(ref)
    r_target = regex_year.search(target)
    return compare(r_ref.groups(), r_target.groups())
