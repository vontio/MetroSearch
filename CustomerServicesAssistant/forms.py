# coding:utf-8
# 表单处理
from flask_wtf import Form
import wtforms
# 表单处理

class QuestionForm(Form):
    question = wtforms.TextField(label=u'问题')
    submit = wtforms.SubmitField(label=u'提交')

class LoginForm(Form):
    UserName = wtforms.TextField(label=u'用户名')
    Password = wtforms.PasswordField(label=u'密码')
    sbmt = wtforms.SubmitField(label=u'登录')
