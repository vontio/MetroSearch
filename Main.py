# -*- coding: utf-8 -*-
from MetroRouteFinder.data import getRoute
import json


def main():
    Test = 0
    if Test == 0:  # 一般使用模式——用户重复输入起终点
        while (1):
            print u"请输入城市"
            City = raw_input().decode("GBK")
            print u"请输入起点、终点"
            Request = [raw_input().decode("GBK"), raw_input().decode("GBK")]
            print json.dumps(getRoute(City, Request[0], Request[1]), ensure_ascii=False)

if __name__ == '__main__':
    main()
