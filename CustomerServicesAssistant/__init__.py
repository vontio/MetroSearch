# coding:utf-8
"""
The flask application package.
"""
from flask import Flask
app = Flask(__name__)

import CustomerServicesAssistant.views
import CustomerServicesAssistant.forms