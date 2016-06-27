# coding:utf-8
# 导入
from flask import render_template, flash, request, \
    redirect, url_for, jsonify, Response
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from MetroRouteFinder import app
from forms import RouteForm
from data import dataProcess, getLine, sameLine, getRoute
app.config["SECRET_KEY"] = 'Jason & Tiffany'

# Bootstrap 支持
bootstrap = Bootstrap(app)
# Bootstrap 支持
# 用户时间本地化工作
moment = Moment(app)
# 用户时间本地化工作


@app.route('/', methods=[u'GET'])
def index():
    form = RouteForm()
    try:
        City = request.args[u"City"]
    except:
        City = u"Guangzhou"
    results = []
    return render_template('city.html', form=form, results=results, City=City)


@app.route('/', methods=[u'POST'])
@app.route('/list/', methods=[u'GET'])
def datadealing():
    Mode = request.args["Mode"]
    City = request.args["City"]
    return jsonify(dataProcess(Mode=Mode, City=City))


@app.route('/getLine/', methods=[u'GET', u'POST'])
def Line():
    try:
        City = request.args[u"City"]
        lineName = request.args[u"lineName"]
    except:
        City = u"Guangzhou"
        lineName = u"1"
    return jsonify(getLine(City, lineName))


@app.route('/sameLine/', methods=[u'GET', u'POST'])
@app.route('/getDirection/', methods=[u'GET', u'POST'])
def sameLine2():
    try:
        City = request.args[u"City"]
        From = request.args[u"from"]
        To = request.args[u"to"]
        return jsonify({"Lines": sameLine(City, From, To)})
    except:
        return jsonify({"Lines": sameLine(u"Guangzhou", u"公园前", u"东山口")})

@app.route('/Route/', methods=[u'GET', u'POST'])
def RouteSearch():
    try:
        City = request.args[u"City"]
        From = request.args[u"from"]
        To = request.args[u"to"]
        Peak = request.args[u"peak"]
        return jsonify({"Routes": getRoute(City, From, To, Peak)})
    except:
        return jsonify({"Routes": getRoute()})
