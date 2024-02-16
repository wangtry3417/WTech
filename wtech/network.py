from .http import *
from flask import *

class network(app):
  def __init__(self):
    super().__init__(import_name="wtech.001")
  def index(self):
    return jsonify({"Hello" : "There"})
  def netOne(self):
    return jsonify({"Network1" : "wtps://wtech.net:51"})

def connect():
  net = network()
  net.route("/")(net.index)
  net.route("/wtech/network")(net.netOne)

  net.run(host="0.0.0.0",port=5162)
