# -*- coding: utf-8 -*-
from MetroRouteFinder.data import getRoute
def main():
    Test = 0
    if Test == 0:  # 一般使用模式——用户重复输入起终点
        while (1):
            
            print u"请输入城市"
            City = raw_input().decode("GBK")
            print u"请输入起点、终点"
            Request = [raw_input().decode("GBK"), raw_input().decode("GBK")]
            getRoute(City, Request[0], Request[1])
    else:
        if Test == 1:  # 测试模式1：计算所有外延节点之间的相互路径
            Station_List = []
            for From in InfoCard:
                if (From['Terminal'] == 1 and
                        From['Interchange'] == 0):
                    for To in InfoCard:
                        if (To['Terminal'] == 1 and
                                To['Interchange'] == 0):
                            Station_List.append(
                                [InfoCard.index(From), InfoCard.index(To)])
        Print_Result(Station_List,All_Length,InfoCard,All_Path, 1)

if __name__ == '__main__':
    main()
