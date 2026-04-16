from flask import Flask
from flask import request,jsonify
from threading import Thread
import logging

# ロガーの取得
werkzeug_logger = logging.getLogger("werkzeug")
# レベル変更
werkzeug_logger.setLevel(logging.ERROR)


app = Flask("")

@app.route("/")
def main():
    return "Bot is alive!"

@app.route("/host", methods=["POST"])
def return_guild():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(res='error'),400
    print(request.json)
    return jsonify(res='ok')
    

def run():
    app.run("0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
