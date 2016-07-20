# -*- coding: utf-8 -*-
import numpy, sys
from processing import dataProcess

def InfoCardArray(City):
    JsonFile = dataProcess(City=City, Mode="rawJson")
    InfoCard = []
    for Line in JsonFile["Lines"]:
        LineSystem = Line[u'System'] if "System" in Line else City + u"地铁"
        for Station in Line[u'Stations']:
            InfoCard.append({u'Line': Line[u'Name'],
                             u'System': LineSystem,
                             u'Name': Station})
        if u'Ring' in Line:
            InfoCard.append({u'Line': Line[u'Name'],
                             u'System': LineSystem,
                             u'Name': Line[u'Stations'][0]})
    length = len(InfoCard)
    Array = {u"Stations": length, u"Items":{u"同": [], u"车": [], u"换": [], u"虚": [], u"转": []}}
    for i in xrange(length):
        for j in xrange(length):
            if (InfoCard[i][u'Name'] == InfoCard[j][u'Name']):
                if InfoCard[i][u'Line'] == InfoCard[j][u'Line']:
                    Array[u"Items"][u"同"].append((i,j))  # 同站、同线——用于处理环线使用
                elif InfoCard[i][u'System'] == InfoCard[j][u'System']:
                    Array[u"Items"][u"换"].append((i,j))  # 同站、不同线——说明是换乘站
                    InfoCard[i][u'Interchange'] = True
                else:
                    Array[u"Items"][u"转"].append((i,j))  # 同站、不同线——说明是换乘站
                    InfoCard[i][u'Interchange'] = True
            elif ((InfoCard[i][u'Line'] == InfoCard[j][u'Line']) and
                    ((j == i + 1) or (i == j + 1))):
                Array[u"Items"][u"车"].append((i,j))  # 起点较终点小1、同线，说明是相邻车站

    def getStationID(Name, Line):
        a = []
        for s in InfoCard:
            if (s["Name"] == Name and Line == s["Line"]):
                a.append(InfoCard.index(s))
        return a
    
    if "VirtualTransfers" in JsonFile:
        for item in JsonFile["VirtualTransfers"]:
            stationa = getStationID(item[0], item[1])
            stationb = getStationID(item[0], item[2])
            for s in stationa:
                for t in stationb:
                    Array[u"Items"][u"换"].remove((s,t))
                    Array[u"Items"][u"换"].remove((t,s))
                    Array[u"Items"][u"虚"].append((s,t))
                    Array[u"Items"][u"虚"].append((t,s))
    for i in xrange(length):
        count1 = 0
        for element in Array[u"Items"][u"车"]:
            if element[0] == i:
                count1+=1
        if count1 == 1:
            count1 == 0
            for element in Array[u"Items"][u"同"]:
                if element[0] == i:
                    count1+=1
            InfoCard[i][u'Terminal'] = (count1 <= 1)
        else:
            InfoCard[i][u'Terminal'] = False
    return {u"InfoCard": InfoCard, u"Array": Array}


def Raw_Write_Distance(City, Mode):
    ConfigFile = json.load(open("../config.json"))["Mode"]
    distanceTable = ConfigFile[Mode if Mode in ConfigFile else u"普通"]
    Array = dataProcess(City=City, Mode="InfoCardArray")["Array"]
    Stations_Count = Array["Stations"]
    Distance = numpy.array([[distanceTable[u"无"]
                 for j in range(Stations_Count)]
                 for i in range(Stations_Count)])
    for item in Array[u"Items"][u"同"]:
        Distance[item[0]][item[1]] = distanceTable[u"同"]
    for item in Array[u"Items"][u"车"]:
        Distance[item[0]][item[1]] = distanceTable[u"车"]
    for item in Array[u"Items"][u"换"]:
        Distance[item[0]][item[1]] = distanceTable[u"换"]
    for item in Array[u"Items"][u"转"]:
        Distance[item[0]][item[1]] = distanceTable[u"无"] if (Mode == u"一票到底") else distanceTable[u"转"]
    for item in Array[u"Items"][u"虚"]:
        Distance[item[0]][item[1]] = distanceTable[u"无"] if (Mode == u"不出站") else distanceTable[u"换"]
    length = Distance
    path = [[i for j in range(Stations_Count)] for i in range(Stations_Count)]
    for k in range(Stations_Count):
        for i in range(Stations_Count):
            for j in range(Stations_Count):
                # 如果既有路径大于经过K点中转的路径
                if (length[i][j] > length[i][k] + length[k][j]):
                    length[i][j] = length[i][k] + length[k][j]  # 则将既有路径更新
                    path[i][j] = path[k][j]  # 并将路径设为K点
    return [length, path]