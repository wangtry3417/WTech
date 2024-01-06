from flask import Flask,render_template,jsonify,request,abort

app = Flask("WTech")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/chat",methods=["POST"])
def chat():
  username = request.form.get("user")
  return jsonify({"user":username})

@app.route("/wcoin/login")
def lo():
  return render_template("wcoin.html")

@app.route("/wcoin/client",methods=["POST"])
def client():
  user = request.form.get("user")
  pw = request.form.get("pw")
  if user == "wangtry" and pw == "003417":
    count = 200000000
    return render_template("client.html",user=user,count=count)
  elif user == "Cw1023" and pw == "1023":
    count = 25000000
    return render_template("client.html",user=user,count=count)
  else:
    return abort(405)


app.run(host="0.0.0.0",port=5000)
