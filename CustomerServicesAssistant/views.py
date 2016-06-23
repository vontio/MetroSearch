# coding:utf-8
# 导入
from flask import render_template, flash, request, redirect, url_for, jsonify, Response
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from CustomerServicesAssistant import app
from datetime import datetime
from search   import search
from forms    import QuestionForm
app.config["SECRET_KEY"] = 'Jason & Tiffany'

# Bootstrap 支持
bootstrap = Bootstrap(app)
# Bootstrap 支持
# 用户时间本地化工作
moment = Moment(app)
# 用户时间本地化工作

@app.route('/', methods = [u'GET', u'POST'])
def index():
    form = QuestionForm()
    if request.method == "POST":
        results = search(form.question.data)
    else:
        results = []
    return render_template('index.html', form=form, results=results)

@app.route('/ajax', methods = [u'GET', u'POST'])
def index_json():
    form = QuestionForm()
    if request.method == "POST":
        return jsonify({u"key": form.question.data, u"results": search(form.question.data)})
    else:
        return render_template("ajax.html")
