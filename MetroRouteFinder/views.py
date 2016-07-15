# coding:utf-8
# 导入
from flask import render_template, flash, request, \
    jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from MetroRouteFinder import app
from forms import RouteForm
import os
import sys
from data import dataProcess, getLine, sameLine, getRoute
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
    print List
    return render_template('index.html', Cities=List, lista=List)


@app.route('/<string:City>/', methods=[u'GET'])
def City(City):
    if "Attention" in dataProcess("rawJson", City):
        for attention in dataProcess("rawJson", City)["Attention"]:
            flash(attention, "warning")
    form = RouteForm()
    return render_template('city.html', form=form, lista=List, City=City)


@app.route('/<string:City>/list/', methods=[u'GET'])
@app.route('/<string:City>/', methods=[u'POST'])
def datadealing(City):
    Mode = request.args["Mode"]
    k = dataProcess(Mode, City)
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
    return jsonify(getRoute(City, From, To))
