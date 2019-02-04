'''
    Notest:
'''

from flask import Flask
from rest_api import *
import os

app = Flask(__name__)

app.register_blueprint(api)

'''
@app.route("/")
def hello():
    return "Hello World!"
'''

if __name__ == "__main__":
    
    app.config['city'] = 'Toronto'
    
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host= host, port = port, use_reloader = False)