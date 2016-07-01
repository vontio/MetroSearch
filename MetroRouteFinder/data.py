# coding:utf-8
from werkzeug.contrib.cache import SimpleCache
import json
cache = SimpleCache()


def dataProcess(Mode=u"InfoCardArray", City=u"Guangzhou"):
    filename = u"./cache/{City}_{Mode}.json".format(
        City=City, Mode=Mode)
    if Mode != "rawJson":
        try:
            k = json.load(open(filename))
            # print u"命中" + filename
        except:
            k = eval(Mode)(City)
            file = open(filename, "w")
            file.write(json.dumps(k))
            file.close()
            # print u"未命中" + filename
        return k
    else:
        return json.load(open(u"./data/{City}.json".format(City=City)))


def getLine(City, lineName):
    rawJsonFile = dataProcess(City=City, Mode="rawJson")["Lines"]
    for Line in rawJsonFile:
        if Line["Name"] == lineName:
            Line["System"] = City + u"地铁"
            return Line
    return {}


def getStation(City, stationName):
    for Station in dataProcess(City=City, Mode="allStations")[u"Stations"]:
        if Station[u"Name"] == stationName:
            return Station
    return {}


def sameLine(City, From, To, Mode=u"All"):
    Lines = []
    # print From, To
    # print getStation(City, From)
    for Line in getStation(City, From)["Lines"]:
        if Line in getStation(City, To)["Lines"]:
            if Mode != u"All":
                if getLine(City, Line)["System"] == Mode:
                    Lines.append({"Line": Line,
                                  "System": getLine(City,Line)["System"],
                                  "Distance": getDirection(City, Line, From, To)[1],
                                  "Direction": getDirection(City, Line, From, To)[0]})
            else:
                Lines.append({"Line": Line,
                              "System": getLine(City, Line)["System"],
                              "Distance": getDirection(City, Line, From, To)[1],
                              "Direction": getDirection(City, Line, From, To)[0]})
    # return Lines
    ClearedLine = []
    Minimum = Lines[0]["Distance"]
    for Line in Lines:
        Minimum = Line["Distance"] if (Minimum > Line["Distance"]) else Minimum
    for Line in Lines:
        if Line["Distance"] == Minimum:
            ClearedLine.append(Line)
    return ClearedLine


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
        k = min(abs(k), len(LineObject["Stations"]) - abs(k))
    else:
        direction = LineObject["Stations"][-1 if k > 0 else 0]
    return [direction, abs(k)]


def lineColors(City):
    a = {}
    for Line in dataProcess(City=City, Mode="rawJson")["Lines"]:
        a[Line["Name"]] = {u"Color": Line[u"Color"] if u"Color" in Line else u"",
                           u"ShortName": Line[u"ShortName"] if u"ShortName" in Line else Line[u"Name"]}
    return a


def allStations(City):
    a = []  # 存储名称
    b = []  # 存储线路列表
    c = []
    d = []
    rawJsonFile = dataProcess(City=City, Mode="rawJson")["Lines"]
    for Line in rawJsonFile:
        try:
            LineSystem = Line[u'System']
        except:
            LineSystem = City + u"地铁"
        for Station in Line["Stations"]:
            if Station not in a:
                a.append(Station)
                b.append([])
                c.append([])
                d.append([])
            if Line["Name"] not in b[a.index(Station)]:
                b[a.index(Station)].append(Line["Name"])  # 加入线路名称
            if LineSystem not in d[a.index(Station)]:
                d[a.index(Station)].append(LineSystem)  # 加入线路名称
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
    allStationsList = [{u"Name": a[i], u"Lines": b[i], u"Neighbors": c[i], u"Systems": d[i]}
                       for i in xrange(len(a))]
    return {"Stations": allStationsList}


def InfoCardArray(City):
    JsonFile = dataProcess(City=City, Mode="rawJson")
    Data = JsonFile["Lines"]
    InfoCard = []
    for Line in Data:
        try:
            LineSystem = Line[u'System']
        except:
            LineSystem = City + u"地铁"
        for Station in Line[u'Stations']:
            InfoCard.append({u'Line':   Line[u'Name'],
                             u'System': LineSystem,
                             u'Name':   Station})
        if u'Ring' in Line:
            InfoCard.append({u'Line':   Line[u'Name'],
                             u'System': LineSystem,
                             u'Name':   Line[u'Stations'][0]})
    length = len(InfoCard)
    Array = [[(u"无" if i != j else u"同") for i in range(length)]
             for j in range(length)]
    for i in xrange(length):
        for j in xrange(length):
            if (Array[i][j] == u"无"):
                if (InfoCard[i][u'Name'] == InfoCard[j][u'Name']):
                    if InfoCard[i][u'Line'] == InfoCard[j][u'Line']:
                        Array[i][j] = u"同"  # 同站、同线——用于处理环线使用
                    elif InfoCard[i][u'System'] == InfoCard[j][u'System']:
                        Array[i][j] = u"换"  # 同站、不同线——说明是换乘站
                    else:
                        Array[i][j] = u"转"  # 同站、不同线——说明是换乘站
                elif ((InfoCard[i][u'Line'] == InfoCard[j][u'Line']) and
                      ((j == i + 1) or (i == j + 1))):
                    Array[i][j] = u"车"  # 起点较终点小1、同线，说明是相邻车站
                Array[j][i] = Array[i][j]

    def getStationID(Name, Line):
        for station in InfoCard:
            if station["Name"] == Name and Line == station["Line"]:
                return InfoCard.index(station)
    try:
        for item in JsonFile["VirtualTransfers"]:
            Array[getStationID(item[0], item[1])][
                getStationID(item[0], item[2])] = u"虚"
            Array[getStationID(item[0], item[2])][
                getStationID(item[0], item[1])] = u"虚"
    except:
        a = 0
    for i in range(len(InfoCard)):
        InfoCard[i][u'Interchange'] = (
            Array[i].count(u"转") + Array[i].count(u"虚") + Array[i].count(u"换") >= 1)
        InfoCard[i][u'Terminal'] = (
            Array[i].count(u"车") == 1 and Array[i].count(u"同") <= 1)
    return {u"InfoCard": InfoCard, u"Array": Array}


def Write_Distance(City, Mode):
    # filename = u"DistanceArray_{Peak}{SJT}{City}".format(City=City, Peak=Peak,SJT=SJT)
    filename = u"./cache/DistanceArray_{Mode}_{City}.json".format(City=City, Mode=Mode)
    try:
        k = json.load(open(filename))
        # print u"命中" + filename
    except:
        k = Raw_Write_Distance(City, Mode)
        file = open(filename, "w")
        file.write(json.dumps(k))
        file.close()
        # print u"未命中" + filename

    # k = cache.get(filename)
    # if k is None:
    #     k = Raw_Write_Distance(City, Peak, SJT)
    #     cache.set(filename, k, timeout=86400)
    #     print u"距离缓存未命中"
    # else:
    #     print u"距离缓存命中"
    return k


def Raw_Write_Distance(City, Mode):
    ConfigFile = json.load(open("./config.json"))["Mode"]
    if Mode in ConfigFile:
        distanceTable = ConfigFile[Mode]
    else:
        distanceTable = ConfigFile[u"普通"]
    Array = dataProcess(City=City, Mode="InfoCardArray")["Array"]
    InfoCard = dataProcess(City=City, Mode="InfoCardArray")["InfoCard"]
    Stations_Count = len(Array)
    Distance = [[distanceTable[u"无"]
                 for j in range(Stations_Count)]
                for i in range(Stations_Count)]
    for i in range(Stations_Count):
        for j in range(Stations_Count):
            if (Array[i][j] == u"虚"):
                Distance[i][j] = distanceTable[
                    u"无"] if (Mode == u"不出站") else distanceTable[u"换"]
            elif (Array[i][j] == u"转") and (Mode == u"一票到底"):
                Distance[i][j] = distanceTable[u"无"]
            else:
                Distance[i][j] = distanceTable[Array[i][j]]
    # print u"距离写入完成"
    length = Distance
    path = [[i for j in range(Stations_Count)] for i in range(Stations_Count)]
    for k in range(Stations_Count):
        for i in range(Stations_Count):
            for j in range(Stations_Count):
                # 如果既有路径大于经过K点中转的路径
                if (length[i][j] > length[i][k] + length[k][j]):
                    length[i][j] = length[i][k] + length[k][j]  # 则将既有路径更新
                    path[i][j] = path[k][j]  # 并将路径设为K点
    # print u"数据初始化完成"
    return [length, path]


def getInfoCard(City):
    return dataProcess(City=City, Mode="InfoCardArray")["InfoCard"]


def getArray(City, Mode="Normal"):
    return Write_Distance(City, Mode)


def Route_Find(Station_List, City, Mode="Normal"):
    InfoCard = getInfoCard(City)
    k = getArray(City, Mode)
    All_Length = k[0]
    All_Path = k[1]
    Length = []
    Path = []
    for b in Station_List:
        List = [b[1]]
        k = b[1]
        while (k != b[0]):
            k = All_Path[b[0]][k]
            List.append(k)
        Length.append(All_Length[b[0]][b[1]])
        Path.append(List[::-1])
    return [Length, Path]


def VirtualTransfers(City):
    try:
        virtual = dataProcess(City=City, Mode="rawJson")["VirtualTransfers"]
    except:
        virtual = []
    transfer = []
    for station in dataProcess(City=City, Mode="allStations")["Stations"]:
        if len(station["Systems"]) > 1:
            for systema in station["Systems"]:
                for systemb in station["Systems"]:
                    if systema != systemb:
                        transfer.append([station["Name"], systema, systemb])
    return {"VirtualTransfers": virtual,
            "Transfers": transfer,
            "VirtualTransfersRemind": u"出站换乘"}

def Print_Result(Station_List, City, Mode="Normal"):
    Route = Route_Find(Station_List, City, Mode)
    InfoCard = getInfoCard(City)
    Length = Route[0]
    Path = Route[1]
    CleanedPath = []
    for i in xrange(len(Length)):
        for j in xrange(len(Path[i])):
            Path[i][j] = InfoCard[Path[i][j]][u'Name']
        if (Length[i] == min(Length)):
            # 以下代码执行删除非“路线改变”车站，可直接删除
            j = len(Path[i]) - 2
            while j > 0:
                if (Path[i][j] != Path[i][j - 1]):
                    del Path[i][j]
                j = j - 1
            # 以上代码执行删除非“路线改变”车站，可直接删除
            if Path[i] not in CleanedPath:
                CleanedPath.append(Path[i])
    # print u"建立路线完成"
    return CleanedPath


def Bulid_List(City, Route, Mode, SystemName):
    InfoCard = getInfoCard(City)
    Station_List = []
    for From in InfoCard:
        for To in InfoCard:
            if ([From[u'Name'], To[u'Name']] == Route):
                if Mode == u"一票到底":
                    if From[u'System'] == SystemName and To[u'System'] == SystemName:
                        Station_List.append(
                            [InfoCard.index(From), InfoCard.index(To)])
                else:
                    Station_List.append(
                        [InfoCard.index(From), InfoCard.index(To)])
    return Print_Result(Station_List, City, Mode)


def generateDict(Paths, City, Mode="All"):
    Deal = [[] for item in Paths]
    for line in Paths:
        for i in xrange(0, len(line) - 1):
            Deal[Paths.index(line)].append(
                sameLine(City, line[i], line[i + 1], Mode))
    return [{u"Stations": Paths[i], u"Lines": Deal[i]} for i in xrange(len(Paths))]


def getRoute(City, From, To):
    routes = []
    modes = []
    b = [u"站数少", u"换乘少"]
    if "VirtualTransfers" in dataProcess("rawJson", City):
        b.append(u"不出站")
    for mode in b:
        a = generateDict(Bulid_List(City, [From, To], mode, " "), City)
        for element in a:
            if element not in routes:
                routes.append(element)
                modes.append([mode])
            else:
                modes[routes.index(element)].append(mode)
    Systems = []
    rawJsonFile = dataProcess("rawJson", City)["Lines"]
    for line in rawJsonFile:
        try:
            LineSystem = Line[u'System']
        except:
            LineSystem = City + u"地铁"
        if LineSystem not in Systems:
            Systems.append(LineSystem)
    if len(Systems) > 1:
        for system in Systems:
            a = generateDict(
                Bulid_List(City, [From, To], u"一票到底", system), City, system)
            print a
            for element in a:
                if element["Lines"] != []:
                    if element not in routes:
                        routes.append(element)
                        modes.append([system])
                    else:
                        modes[routes.index(element)].append(system)
    return {"Routes": routes, "Modes": modes}
