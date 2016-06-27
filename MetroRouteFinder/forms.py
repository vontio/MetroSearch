# coding:utf-8
# 表单处理
from flask_wtf import Form
import wtforms
# 表单处理


class RouteForm(Form):
    fromInput = wtforms.TextField(label=u'从')
    toInput = wtforms.TextField(label=u'到')
    submit = wtforms.SubmitField(label=u'提交')
