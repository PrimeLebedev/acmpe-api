from flask import Flask

app = Flask(__name__)

API_ROOT = '/api/v1'
CALENDAR_API_ROOT = API_ROOT + '/calendar'

@app.route(CALENDAR_API_ROOT + '/', methods=['GET'])
def read():
    return 'read'