# coding:utf-8
from flask_wtf import Form
import wtforms
class RouteForm(Form):
    fromInput = wtforms.TextField(label=u'从')
    toInput = wtforms.TextField(label=u'到')
    submit = wtforms.SubmitField(label=u'提交')