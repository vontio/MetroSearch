# coding:utf-8
# 导入
from flask import render_template, flash, request, \
    jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from MetroRouteFinder import app
import json
import time
import os
import sys
from data import dataProcess, getLine, sameLine, getStation, getRoute
app.config["SECRET_KEY"] = 'Jason & Tiffany'

# Bootstrap 支持
bootstrap = Bootstrap(app)
moment = Moment(app)
# 用户时间本地化工作
List = []


@app.before_first_request
def initialization():
    for root, dirs, files in os.walk("./data"):
        for f in files:
            List.append(
                f.replace(".json", "").decode(sys.getfilesystemencoding()))


@app.route('/', methods=[u'GET'])
def index():
    return render_template('index.html', Cities=List, lista=List)


@app.route('/<string:City>/', methods=[u'GET'])
def City(City):
    if "Attention" in dataProcess("rawJson", City):
        for attention in dataProcess("rawJson", City)["Attention"]:
            flash(attention, "warning")
    return render_template('city.html', lista=List, City=City)


@app.route('/<string:City>/list/', methods=[u'GET'])
@app.route('/<string:City>/', methods=[u'POST'])
def datadealing(City):
    print u"收到请求", request.path, request.args
    a = time.clock()
    Mode = request.args["Mode"]
    k = dataProcess(Mode, City)
    print u"用了时间", time.clock() - a
    return jsonify(k if Mode != u"rawJson" else {u"rawJson": k})


@app.route('/<string:City>/Line/<string:Line>/',
           methods=[u'GET', u'POST'])
def Line(City, Line):
    return jsonify(getLine(City, Line))


@app.route('/<string:City>/Direction/<string:From>/<string:To>/',
           methods=[u'GET', u'POST'])
def sameLine2(City, From, To):
    return jsonify({"Lines": sameLine(City, From, To)})


@app.route('/<string:City>/Route/<string:From>/<string:To>/',
           methods=[u'GET', u'POST'])
def RouteSearch(City, From, To):
    print u"收到请求", request.path, request.args
    a = time.clock()
    k = getRoute(City, From, To)
    print u"用了时间", time.clock() - a
    return jsonify(k)


@app.route('/<string:City>/Location/<string:StationName>/<string:MarsLat>/<string:MarsLon>/',
           methods=[u'GET', u'POST'])
def addLocation(City, StationName, MarsLat, MarsLon):
    a = dataProcess(City=City, Mode="allStations")
    for station in a[u"Stations"]:
        if station["Name"] == StationName:
            station["MarsLat"] = MarsLat
            station["MarsLon"] = MarsLon
    file = open(u"./cache/{City}_allStations.json".format(
        City=City), "w")
    file.write(json.dumps(a))
    file.close()
    return getStationPP(City, StationName)

@app.route('/<string:City>/Station/<string:StationName>/',
           methods=[u'GET', u'POST'])
def getStationPP(City, StationName):
    return jsonify(getStation(City, StationName))
