from flask import Flask,render_template,jsonify,request,abort
from cryptography.fernet import Fernet
import hashlib
import psycopg2
import os

app = Flask("WTech")

def hash_value(user):
  u = user.encode()
  sha = hashlib.sha256(u).hexdigest()
  return sha

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

@app.route("/wcoin/api/v1/checkUser",methods=["GET"])
def mining():
  user = request.args.get("user")
  if user == "wangtry":
    user_hash = hash_value(user=user)
    return jsonify({
       "user" : user,
       "user-api-key" : user_hash,
       "balance-on-decimal" : 200000000
    })
  elif user == "Cw1023":
    user_hash = hash_value(user=user)
    return jsonify({
       "user" : user,
       "user-api-key" : user_hash,
       "balance-on-decimal" : 25000000
    })
  else:
    return jsonify({"Invaild user":"Please correctly input!"})

@app.route("/wcoin/create/account")
def create():
  return render_template("new.html")

@app.route("/wcoin/api/v1/new_client",methods=["GET"])
def cre():
    clientID = request.args.get("clientID")
    intents = request.args.get("intents")
    fname = request.form.get("fname")
    id = request.form.get("id")
    user = request.form.get("user")
    pw = request.form.get("pw")
    with open("user.txt","a+") as f:
        fo = f"""
         User full-name: {fname}, \n
         User id: {id} \n
         --------------- \n
        """
        f.write(fo)
    return render_template("tr.html")
    
@app.route("/work/login")
def worker():
  return render_template("worker.html")

@app.route("/wtech/api/v1/login",method=["GET"])
def checkUser():
  clientID = request.args.get("clientID")
  user = request.form.get("user")
  pe = request.form.get("pw")
  if clientID = "00001":
    if user == "wangtry" and pw == "003417":
      return "success"
    else:
      return abort(502)
  else:
    return jsonify({"Invaild clientID":"Client is not verified!"})

@app.route("/wcoin/buy",methods=["GET"])
def buy():
  user = request.args.get("user")
  if user == "wangtry":
    count = 200000000
    l = [user,count]
    list_string = str(l)
    fernet = Fernet("DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q=")
    address = fernet.encrypt(list_string.encode()).decode()
    return render_template("buy.html",address=address)
  elif user == "Cw1023":
    count = 25000000
    l = [user,count]
    list_string = str(l)
    fernet = Fernet("DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q=")
    address = fernet.encrypt(list_string.encode()).decode()
    return render_template("buy.html",address=address)
  else:
    return abort(502)



app.run(host="0.0.0.0",port=5000)
