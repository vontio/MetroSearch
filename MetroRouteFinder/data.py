# coding:utf-8
from werkzeug.contrib.cache import SimpleCache
import json
cache = SimpleCache()


def getLine(City, lineName):
    rawJsonFile = dataProcess({"City": City, "Mode": "rawJson"})
    for Line in rawJsonFile:
        if Line["Name"] == lineName:
            return Line
    return {}


def getStation(City, stationName):
    for Station in dataProcess({"City": City, "Mode": "allStations"})[u"Stations"]:
        if Station[u"Name"] == stationName:
            return Station
    return {}


def sameLine(City, From, To):
    Lines = []
    for Line in getStation(City, From)["Lines"]:
        if Line in getStation(City, To)["Lines"]:
            Lines.append({"Line": Line, "Distance": getDirection(City, Line, From, To)[1],
                          "Direction": getDirection(City, Line, From, To)[0]})
    return Lines


def getDirection(City, lineName, From, To):
    LineObject = getLine(City, lineName)
    fromIndex = LineObject["Stations"].index(From)
    toIndex = LineObject["Stations"].index(To)
    k = toIndex - fromIndex
    if (k == 0):
        direction = u"同站出入"
    elif u"Ring" in LineObject:
        k *= LineObject[u"Ring"]
        # Ring 如果为 1 代表自上到下为逆时针，反之为顺时针
        LineLength = len(LineObject["Stations"]) / 2
        if abs(k) < LineLength:
            direction = u"逆时针" if k > 0 else u"顺时针"
        elif abs(k) > LineLength:
            direction = u"顺时针" if k > 0 else u"逆时针"
        else:
            direction = u"您随便坐"
    else:
        direction = LineObject["Stations"][-1 if k > 0 else 0]
    return [direction, k]

def dataProcess(Mode = u"allStations", City = u"Guangzhou"):
    filename = u"{Mode}_{City}".format(Mode=Mode, City=City)
    k = cache.get(filename)
    if k is None:
        k = eval(Mode)(City)
        cache.set(filename, k, timeout=86400)
    return k

def rawJson(City):
    return json.load(open(u"./data/{City}.json".format(City=City)))


def lineColors(City):
    a = {}
    for Line in dataProcess({"City": City, "Mode": "rawJson"}):
        a[Line["Name"]] = Line[u"Color"] if u"Color" in Line else u"black"
    return a






def allStations(City):
    a = []  # 存储名称
    b = []  # 存储线路列表
    c = []
    rawJsonFile = dataProcess({"City": City, "Mode": "rawJson"})
    for Line in rawJsonFile:
        for Station in Line["Stations"]:
            if Station not in a:
                a.append(Station)
                b.append([])
                c.append([])
            b[a.index(Station)].append(Line["Name"])  # 加入线路名称
            linePosition = Line["Stations"].index(Station)
            if (linePosition >= 1):
                nextStation = Line["Stations"][linePosition - 1]
                if nextStation not in c[a.index(Station)]:
                    c[a.index(Station)].append(nextStation)
            elif ("Ring" in Line):
                nextStation = Line["Stations"][-1]
                if nextStation not in c[a.index(Station)]:
                    c[a.index(Station)].append(nextStation)
            if (linePosition < len(Line["Stations"]) - 1):
                nextStation = Line["Stations"][linePosition + 1]
                if nextStation not in c[a.index(Station)]:
                    c[a.index(Station)].append(nextStation)
            elif ("Ring" in Line):
                nextStation = Line["Stations"][0]
                if nextStation not in c[a.index(Station)]:
                    c[a.index(Station)].append(nextStation)
    allStationsList = [{u"Name": a[i], u"Lines": b[i], u"Neighbors": c[i]}
                       for i in xrange(len(a))]
    return {"Stations": allStationsList}


def InfoCardArray(City):
    Data = dataProcess({"City": City, "Mode": "rawJson"})
    InfoCard = []
    for Line in Data:
        for Station in Line[u'Stations']:
            InfoCard.append({u'Line': Line[u'Name'],
                             u'System': Line[u'System'],
                             u'Name': Station})
        if u'Ring' in Line:
            InfoCard.append({u'Line': Line[u'Name'],
                             u'System': Line[u'System'],
                             u'Name': Line[u'Stations'][0]})
    length = len(InfoCard)
    Array = [[u"无" for i in range(length)] for j in range(length)]
    for i in xrange(length):
        Array[i][i] = u"同"
    for i in xrange(length):
        for j in xrange(length):
            if (Array[i][j] == u"无"):
                if (InfoCard[i][u'Name'] == InfoCard[j][u'Name']):
                    if (InfoCard[i][u'Line'] == InfoCard[j][u'Line']):
                        Array[i][j] = u"同"  # 同站、同线——用于处理环线使用
                    elif InfoCard[i][u'System'] == InfoCard[j][u'System']:
                        Array[i][j] = u"换"  # 同站、不同线——说明是换乘站
                    else:
                        Array[i][j] = u"转"  # 同站、不同线——说明是换乘站
                elif ((InfoCard[i][u'Line'] == InfoCard[j][u'Line']) and
                      ((j == i + 1) or (i == j + 1))):
                    Array[i][j] = u"车"  # 起点较终点小1、同线，说明是相邻车站
                Array[j][i] = Array[i][j]
    for i in range(len(InfoCard)):
        InfoCard[i][u'Interchange'] = (
            Array[i].count(u"转") + Array[i].count(u"换") >= 1)
        InfoCard[i][u'Terminal'] = (
            Array[i].count(u"车") == 1 and Array[i].count(u"同") <= 1)
    return {u"InfoCard": InfoCard, u"Array": Array}

def Write_Distance(Array, Peak):
    distanceTable = {
        u"无": 10000000000000,
        u"车": 3,
        u"换": 2,
        u"同": 0,
        u"转": 4
    } if Peak else {
        u"无": 10000000000000,
        u"车": 3.3,
        u"换": 4,
        u"同": 0,
        u"转": 8
    }
    Stations_Count = len(Array)
    Distance = [[distanceTable[u"无"]
                 for j in range(Stations_Count)]
                for i in range(Stations_Count)]
    for i in range(Stations_Count):
        for j in range(Stations_Count):
            Distance[i][j] = distanceTable[Array[i][j]]
    print u"距离写入完成"
    length = Distance
    path = [[0 for j in range(Stations_Count)] for i in range(Stations_Count)]
    for k in range(Stations_Count):
        for i in range(Stations_Count):
            for j in range(Stations_Count):
                # 如果既有路径大于经过K点中转的路径
                if (length[i][j] > length[i][k] + length[k][j]):
                    length[i][j] = length[i][k] + length[k][j]  # 则将既有路径更新
                    path[i][j] = path[k][j]  # 并将路径设为K点
    print u"数据初始化完成"
    return [length, path]


def init(City=u"Guangzhou", Peak=0):
    InfoCard = dataProcess({"City": City, "Mode": "InfoCardArray"})["InfoCard"]
    Processed_Data = Write_Distance(
        dataProcess({"City": City, "Mode": "InfoCardArray"})["Array"], Peak)
    All_Length = Processed_Data[0]
    All_Path = Processed_Data[1]
    return [InfoCard, All_Length, All_Path]


def getRoute(City=u"Guangzhou", From=u"机场南", To=u"金洲", Peak=1):
    init(City, Peak)
    return [[u"机场南", u"体育西路", u"珠江新城", u"车陂南", u"金洲"], [u"机场南", u"体育西路", u"客村", u"万胜围", u"金洲"]]
