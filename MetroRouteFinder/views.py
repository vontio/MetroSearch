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
@app.route('/<string:City>/', methods=[u'GET'])
def index(City=u"Guangzhou"):
    form = RouteForm()
    results = []
    return render_template('city.html', form=form, results=results, City=City)

@app.route('/<string:City>/list/', methods=[u'GET'])
@app.route('/<string:City>/', methods=[u'POST'])
def datadealing(City=u"Guangzhou"):
    Mode = request.args["Mode"]
    k = dataProcess(Mode, City)
    return jsonify(k if Mode != u"rawJson" else {u"rawJson":k})

@app.route('/<string:City>/Line/', methods=[u'GET', u'POST'])
@app.route('/<string:City>/Line/<string:Line>/', methods=[u'GET', u'POST'])
def Line(City = u"Guangzhou", Line=u"1"):
    return jsonify(getLine(City, Line))


@app.route('/<string:City>/Direction/<string:From>/<string:To>/', methods=[u'GET', u'POST'])
def sameLine2(City = u"Guangzhou", From=u"体育西路", To=u"广州东站"):
    return jsonify({"Lines": sameLine(City, From, To)})

@app.route('/<string:City>/Route/<string:From>/<string:To>/', methods=[u'GET', u'POST'])
def RouteSearch(City = u"Guangzhou", From=u"体育西路", To=u"广州东站"):
    return jsonify(getRoute(City, From, To))
