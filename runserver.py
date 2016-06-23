"""
This script runs the Management application using a development server.
"""

from os import environ
from CustomerServicesAssistant import app

if __name__ == '__main__':
    DEBUG = environ.get("SVR_DEBUG", False)
    HOST = environ.get('SVR_HOST', '0.0.0.0')
    # try:
    #     PORT = int(environ.get('SVR_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    PORT = 48482
    DEBUG = True
    app.run(HOST, PORT, debug = DEBUG)
