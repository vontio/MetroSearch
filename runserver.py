# -*- coding: utf-8 -*-
"""
This script runs the Management application using a development server.
"""

from os import environ
import webbrowser
from MetroRouteFinder import app

if __name__ == '__main__':
    DEBUG = environ.get("SVR_DEBUG", False)
    HOST = environ.get('SVR_HOST', '0.0.0.0')
    PORT = 63876
    DEBUG = True
    context = ("C:\users\jason\JasonLee.test.crt", "C:\users\jason\JasonLee.test.key")
    webbrowser.open("https://localhost:{p}".format(p=PORT), new=0, autoraise=True)
    app.run(HOST, PORT, debug=DEBUG, ssl_context=context)