# coding:utf-8
import json
try:
    import cPickle as pickle
except:
    import pickle


def getLine(City, lineName):
    for Line in getRawJson(City)["Lines"]:
        if Line["Name"] == lineName:
            if "System" not in Line:
                Line["System"] = City + u"地铁"
            return Line


def getStation(City, stationName):
    for Station in dataProcess(City=City, Mode="allStations")[u"Stations"]:
        if Station[u"Name"] == stationName:
            return Station


def sameLine(City, From, To, system=u"All"):
    Lines = []
    for Line in (set(getStation(City, From)["Lines"]) &
                 set(getStation(City, To)["Lines"])):
        System = getLine(City, Line)["System"]
        if system == u"All" or System == system:
            p = getDirection(City, Line, From, To)
            Lines.append({"Line": Line,
                          "System": System,
                          "Direction": p[0],
                          "Distance": p[1],
                          "Time": p[2]})
    ClearedLine = []
    try:
        Minimum = Lines[0]["Distance"]
        for Line in Lines:
            Minimum = Line["Distance"] if (
                Minimum > Line["Distance"]) else Minimum
        for Line in Lines:
            if Line["Distance"] == Minimum:
                ClearedLine.append(Line)
        return ClearedLine
    except:
        return Lines


def timeCalculation(lO, fromIndex, toIndex, ring=0):
    dist = toIndex - fromIndex
    if (dist > 0):
        start, end = fromIndex, toIndex
    else:
        start, end = toIndex, fromIndex
    if u"Time" in lO:
        if ring == 0:
            time = sum(lO[u"Time"][start:end])
        else:
            time = (sum(lO[u"Time"][end:]) +
                    sum(lO[u"Time"][:start]))
    else:
        if ring != 0:
            dist = len(lO["Stations"]) - abs(dist)
        time = abs(dist) * (lO["AvgTime"] if u"AvgTime" in lO else 1)
    return time


def getDirection(City, lineName, From, To):
    lO = getLine(City, lineName)
    fromIndex = lO["Stations"].index(From)
    toIndex = lO["Stations"].index(To)
    k = toIndex - fromIndex
    time = 0
    if (k == 0):
        direction, time = u"同站出入", 0
    elif u"Ring" in lO:
        LineLength = len(lO["Stations"]) / 2
        k = k * lO["Ring"]  # 1 代表逆时针 反之代表顺时针
        # 这样一来 k > 0 代表逆时针方向；k < 0 代表顺时针方向
        if abs(k) < LineLength:  # 小于一半原方向
            direction = u"逆时针" if k > 0 else u"顺时针"
            time = timeCalculation(lO, fromIndex, toIndex)
            k = abs(k)
        else:  # 反之反方向
            direction = u"顺时针" if k > 0 else u"逆时针"
            time = timeCalculation(lO, fromIndex, toIndex, 1)
            k = len(lO["Stations"]) - abs(k)
    else:
        direction = lO["Stations"][-1 if toIndex > fromIndex else 0]
        time = timeCalculation(lO, fromIndex, toIndex)
        k = abs(k)
    return [direction, k, time]


def allStations(City):
    a, b, c, d = [], [], [], []  # 存储名称
    rawK = getRawJson(City)
    rawJsonFile = rawK["Lines"]
    for Line in rawJsonFile:
        LineSystem = Line[u'System'] if "System" in Line else City + u"地铁"
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
            elif ("Ring" in Line):
                nextStation = Line["Stations"][-1]
            if (linePosition < len(Line["Stations"]) - 1):
                nextStation = Line["Stations"][linePosition + 1]
            elif ("Ring" in Line):
                nextStation = Line["Stations"][0]
            if nextStation not in c[a.index(Station)]:
                c[a.index(Station)].append(nextStation)

    allStationsList = [{u"Name": a[i], u"Lines": b[i],
                        u"Neighbors": c[i], u"Systems": d[i]}
                       for i in xrange(len(a))]
    lineColors = {}
    for Line in rawJsonFile:
        lineColors[Line["Name"]] = {
            u"Color": Line[u"Color"] if u"Color" in Line else u"#000000",
            u"ShortName": (Line[u"ShortName"]
                           if u"ShortName" in Line else Line[u"Name"])
        }
    virtual = (rawK["VirtualTransfers"] if "VirtualTransfers" in rawK else [])
    transfer = []
    for s in allStationsList:
        if len(s["Systems"]) > 1:
            for a in s["Systems"]:
                for b in s["Systems"]:
                    if a != b:
                        transfer.append([s["Name"], a, b])
    return {"Stations": allStationsList,
            "Lines": lineColors,
            "VirtualTransfers": virtual,
            "Transfers": transfer}


def Write_Distance(City, Mode):
    f = u"./cache/{City}_{Mode}_DistanceArray.dat".format(City=City, Mode=Mode)
    try:
        k = pickle.load(open(f, 'rb'))
    except:
        k = Raw_Write_Distance(City, Mode)
        pickle.dump(k, open(f, "wb"), 1)
    return k


def getInfoCard(City):
    return dataProcess(City=City, Mode="InfoCardArray")["InfoCard"]


def getRawJson(City):
    return dataProcess(City=City, Mode="rawJson")


def Route_Find(Station_List, City, Mode="Normal"):
    k = Write_Distance(City, Mode)
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


def Print_Result(Station_List, City, Mode="Normal"):
    Route = Route_Find(Station_List, City, Mode)
    InfoCard = getInfoCard(City)
    Length = Route[0]
    Path = Route[1]
    CleanedPath = []
    for i in xrange(len(Path)):
        b = Path[i]
        if (Length[i] == min(Length)):
            for j in xrange(len(b)):
                b[j] = InfoCard[b[j]][u'Name']
            # 以下代码执行删除非“路线改变”车站，可直接删除
            j = len(b) - 2
            while j > 0:
                if (b[j] != b[j - 1]):
                    del b[j]
                j = j - 1
            # 以上代码执行删除非“路线改变”车站，可直接删除
            # 以下代码检测环线分界点
            j = len(b) - 2
            while j > 0:
                lista = [a["Line"]
                         for a in sameLine(City, b[j], b[j - 1])]
                listb = [a["Line"]
                         for a in sameLine(City, b[j], b[j + 1])]
                for item in lista:
                    if item in listb and "Ring" in getLine(City, item):
                        del b[j]
                        break
                j = j - 1
            # 以上代码检测环线分界点
            if b not in CleanedPath:
                CleanedPath.append(b)
    return CleanedPath


def Bulid_List(City, Route, Mode, SystemName):
    InfoCard = getInfoCard(City)
    Station_List = []
    for From in InfoCard:
        for To in InfoCard:
            if ([From[u'Name'], To[u'Name']] == Route):
                if Mode == u"一票到底":
                    if (From[u'System'] == SystemName and
                            To[u'System'] == SystemName):
                        Station_List.append(
                            [InfoCard.index(From), InfoCard.index(To)])
                else:
                    Station_List.append(
                        [InfoCard.index(From), InfoCard.index(To)])
    return Print_Result(Station_List, City, Mode)


def generateDict(Paths, City, system="All"):
    Deal = [[] for item in Paths]
    for line in Paths:
        for i in xrange(0, len(line) - 1):
            Deal[Paths.index(line)].append(
                sameLine(City, line[i], line[i + 1], system))
    return [{u"Stations": Paths[i],
             u"Lines": Deal[i]} for i in xrange(len(Paths))]


def getRoute(City, From, To):
    k = getRawJson(City)
    # b = [u"站数少", u"换乘少", u"抽象测试", u"实际测试"]
    b = [u"站数少", u"换乘少"]
    if "VirtualTransfers" in k:
        b.append(u"不出站")
    c = [(mode, mode, u"All") for mode in b]
    routes, modes, Systems = [], [], []
    for line in k["Lines"]:
        LineSystem = line[u'System'] if u'System' in line else City + u"地铁"
        if LineSystem not in Systems:
            Systems.append(LineSystem)
    if len(Systems) > 1:
        for system in Systems:
            c.append((u"一票到底", system, system))
    for item in c:
        for element in generateDict(
                Bulid_List(City, [From, To], item[0], item[1]), City, item[2]):
            if element["Lines"] != []:
                if element not in routes:
                    routes.append(element)
                    modes.append([item[1]])
                else:
                    modes[routes.index(element)].append(item[1])
    return {"Routes": routes, "Modes": modes}


def InfoCardArray(City):
    JsonFile = getRawJson(City)
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
    Array = {u"Stations": length, u"Items": {
        u"同": [], u"车": [], u"换": [], u"虚": [], u"转": []}}
    for i in xrange(length):
        for j in xrange(length):
            if (InfoCard[i][u'Name'] == InfoCard[j][u'Name']):
                if InfoCard[i][u'Line'] == InfoCard[j][u'Line']:
                    Array[u"Items"][u"同"].append((i, j))  # 同站、同线——用于处理环线使用
                elif InfoCard[i][u'System'] == InfoCard[j][u'System']:
                    Array[u"Items"][u"换"].append((i, j))  # 同站、不同线——说明是换乘站
                    InfoCard[i][u'Interchange'] = True
                else:
                    Array[u"Items"][u"转"].append((i, j))  # 同站、不同线——说明是换乘站
                    InfoCard[i][u'Interchange'] = True
            elif ((InfoCard[i][u'Line'] == InfoCard[j][u'Line']) and
                    ((j == i + 1) or (i == j + 1))):
                Array[u"Items"][u"车"].append((i, j))  # 起点较终点小1、同线，说明是相邻车站

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
                    Array[u"Items"][u"换"].remove((s, t))
                    Array[u"Items"][u"换"].remove((t, s))
                    Array[u"Items"][u"虚"].append((s, t))
                    Array[u"Items"][u"虚"].append((t, s))
    for i in xrange(length):
        count1 = 0
        for element in Array[u"Items"][u"车"]:
            if element[0] == i:
                count1 += 1
        if count1 == 1:
            count1 == 0
            for element in Array[u"Items"][u"同"]:
                if element[0] == i:
                    count1 += 1
            if count1 <= 1:
                InfoCard[i][u'Terminal'] = True
    return {u"InfoCard": InfoCard, u"Array": Array}


def Raw_Write_Distance(City, Mode):
    ConfigFile = json.load(open("./config.json"))["Mode"]
    if Mode in ConfigFile:
        distanceTable = ConfigFile[Mode]
    elif Mode[-2:] == u"测试":
        distanceTable = ConfigFile[u"测试"]
    else:
        distanceTable = ConfigFile[u"普通"]
    Array = dataProcess(City=City, Mode="InfoCardArray")["Array"]
    Stations_Count = Array["Stations"]
    Distance = [[ConfigFile[u"无"]
                 for j in range(Stations_Count)]
                for i in range(Stations_Count)]
    for item in Array[u"Items"][u"同"]:
        Distance[item[0]][item[1]] = ConfigFile[u"同"]
    for item in Array[u"Items"][u"车"]:
        rawd = getDistance(City, min(item[0], item[1]))
        Distance[item[0]][item[1]] = (
            rawd if (rawd >= 0 and Mode != u"抽象测试") else ConfigFile[u"车"])
    for item in Array[u"Items"][u"换"]:
        Distance[item[0]][item[1]] = distanceTable[u"换"]
    for item in Array[u"Items"][u"转"]:
        Distance[item[0]][item[1]] = ConfigFile[u"无"] if (
            Mode == u"一票到底") else distanceTable[u"转"]
    for item in Array[u"Items"][u"虚"]:
        Distance[item[0]][item[1]] = ConfigFile[u"无"] if (
            Mode == u"不出站") else distanceTable[u"换"]
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


def getDistance(City, id):
    item = getInfoCard(City)[id]
    Line = getLine(City, item["Line"])
    if "Time" in Line:
        index = Line["Stations"].index(item["Name"])
        Name = Line["Time"][index]
    else:
        Name = Line["AverageTime"] if u"AverageTime" in Line else -1
    return Name


def dataProcess(Mode=u"InfoCardArray", City=u"Guangzhou"):
    if Mode != "rawJson":
        filename = u"./cache/{City}_{Mode}.json".format(
            City=City, Mode=Mode)
        try:
            k = json.load(open(filename))
        except:
            k = eval(Mode)(City)
            file = open(filename, "w")
            file.write(json.dumps(k))
            file.close()
    else:
        k = json.load(open(u"./data/{City}.json".format(City=City)))
    return k
