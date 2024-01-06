from flask import Flask,render_template,jsonify,request

app = Flask("WTech")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/chat",methods=["POST"])
def chat():
  username = request.form.get("user")
  return jsonify({"user":username})


app.run(host="0.0.0.0",port=5000)
