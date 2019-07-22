from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
from werkzeug.contrib.fixers import ProxyFix

import bot

app = Flask(__name__)
sslify = SSLify(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.get_json()
        bot.bot(response)
        return jsonify(response)

    return '<h1>Bot welcomes you</h1>'

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run()
