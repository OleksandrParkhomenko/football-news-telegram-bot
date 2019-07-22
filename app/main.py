from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify

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

if __name__ == '__main__':
    app.run()
