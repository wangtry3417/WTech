from flask import *
import socketio

app = Flask(__name__)

server = socketio.Server()

@app.route("/")
def index():
  return render_template("index.html")

server.run(app,host="0.0.0.0",port="8080")
app.run(host="0.0.0.0")
