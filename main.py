from flask import Flask,render_template,jsonify,request,abort,url_for,redirect
from cryptography.fernet import Fernet
import hashlib
import os
import paypalrestsdk
import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import smtplib
import stripe
import datetime
import requests
from email.mime.text import MIMEText
#from nltk.stem import WordNetLemmatizer
#from nltk.book import *

stripe.api_key = 'sk_test_51L2HC2J0QjqOTdOCHZxTbi3deVcbYNQhuvExH1thqeLvB7pbMiCHtapDTP5S64TKAkJpqsOkAm2uBNVBmhMpO9Jl00vFoU1QNJ'

class AIModules:
  def __init__(self,text):
    self.text = text
  def think(self):
    #nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('all-corpora')
    nltk.download('popular')
    #tokens = word_tokenize(self.text)  # 分词
    #tokens = [token.lower() for token in tokens]  # 转换为小写
    #tokens = [token for token in tokens if token.isalpha()]  # 仅保留字母字符
    #tokens = [token for token in tokens if token not in stopwords.words("english")]  # 去除停用
    response = self.text
    return response

app = Flask("WTech")

paypalrestsdk.configure({
  'mode': 'sandbox', 
  'client_id': 'ASK8RjfrdCzGvCQRDvnfa321S_5OBGMK4KDGac5PreKf6NU-0d0MUPPrYe_S-fq4tcoHN22P8Nz4xZs3',
  'client_secret': 'EB1-tdfv74XcCxkdDWjueV19ePB4Wf8uMKwdhE2robSWQF21i6nC6pm57zzVARTzJ03ah6X4ARc1GhBQ'
})

def hash_value(user):
  u = user.encode()
  sha = hashlib.sha256(u).hexdigest()
  return sha

@app.route("/")
def index():
  return render_template("wtechHome.html")

def generate_data():
    data = []
    for i in range(31):
        data.append({
            'date': f'2024-01-{i+1}',
            'price': random.randint(180, 3000000)
        })
    return data

current_datetime = datetime.datetime.now()

@app.route('/data')
def data():
    global current_datetime
    
    data = []
    for i in range(31):
        data.append({
            'date': current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'price': random.randint(180, 3000000)
        })
        current_datetime += datetime.timedelta(seconds=1)  # 每次递增1秒
    
    return jsonify(data)

@app.route("/wtech/staff")
def wtechStaff():
  return render_template("wtechStaff.html")

@app.route("/wtech/v2/checkuser",methods=["GET","POST"])
def wtechCheckUser():
  email = request.form.get("email")
  return render_template("wtechDash.html",email=email)

@app.route("/wtech/v2/automail",methods=["GET"])
def send_auto_mail():
  email = str(request.args.get("email"))
  subject = str(request.args.get("subject"))
  content = str(request.args.get("content"))
  msg = MIMEText(content,"plain","utf-8")
  msg["To"] = email
  msg["From"] = "1245server@gmail.com"
  msg["Subject"] = subject
  s = smtplib.SMTP("smtp.gmail.com",587)
  s.starttls()
  s.login("1245server@gmail.com","jvbswpfesugcqazw")
  #send_data = f"Subject: {subject} \n\n {content}"
  s.sendmail("1245server@gmail.com",[email],msg.as_string())
  return jsonify({"status" : "Sent!","status_code" : 200})

@app.route('/wtech/upload', methods=['POST'])
def upload_file():
   username = request.form.get("username")
   file = request.files.get("file")
   res = requests.post(url="https://133afc38-12b6-4a64-a3ca-93921fd8559d-00-17y66hwk67wlv.sisko.replit.dev/upload",data={"username":username,"file":file})
   try:
     return res.content
   except:
     return "Upload error"

@app.route("/wtech/about")
def wtechAbout():
  return render_template("wtechAbout.html")

@app.route("/wtech/v2/discordUser",methods=["GET","POST"])
def wtechDCUser():
  code = request.args.get("code")
  data = {
        'client_id': 1188619676671037530,
        'client_secret': 'SNnZshi6sgXkTfoNyGAswV_KfGCIdB0h',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://wtech-5o6t.onrender.com/wtech/v2/checkuser',
    }
  headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
  response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
  response_json = response.json()
  access_token = response_json.get('access_token')
  user_info = requests.get(
    'https://discord.com/api/users/@me', 
    headers={'Authorization': f'Bearer {access_token}'}
).json()
  email = user_info.get('email')
  return jsonify({
    "user" : email
  })

@app.route("/chat",methods=["POST"])
def chat():
  username = request.form.get("user")
  return jsonify({"user":username})

@app.route("/wcoin/sys")
def wsys():
  return render_template("sys.c")

@app.route("/wcoin/sk/ok")
def skDone():
  return render_template("skdone.html")
#wcoin
@app.route("/wcoin/shop")
def cshop():
  return render_template("cshop.html")

@app.route("/api/v1/chat/<code>",methods=["GET","POST"])
def chatCode(code : str):
  prompt = request.form.get("prompt")
  if code == "WTech1028":
    ai = AIModules(prompt)
    response = ai.think()
    return jsonify({
       "Human-prompt" : prompt,
       "gen-prompt" : response,
       "Using module" : "FunGPT modules"
    })
  elif code == "WTech192828":
    ai = AIModules(prompt)
    response = ai.think()
    return jsonify({
       "Human-prompt" : prompt,
       "gen-prompt" : response,
       "Using module" : "FunGPT modules"
    })
  else:
    return jsonify({"Invaild code" : "Message not found"})

@app.route("/wtech/home",methods=["GET","POST","PATCH","DELETE","PUT"])
def wtechHome():
  return render_template("wtechHome.html")

@app.route("/wtech/server")
def wtechSer():
  return render_template("wtechServer.html")

@app.route("/wcoin/login")
def lo():
  return render_template("wcoin.html")

@app.route("/wcoin/sk/transfer")
def skLoad():
  return render_template("sk.html")

@app.route("/wcoin/sk/buy/info",methods=["GET"])
def sk():
  count = int(request.args.get("price"))
  try:
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'hkd',
                    'unit_amount': count*10,
                    'product_data': {
                        'name': 'W Coins'
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='/wcoin/sk/ok',
        cancel_url='/wcoin/sys',
    )
  except Exception as e:
    return str(e)

  return render_template("skdone.html")

@app.route("/wtech/product")
def wtechProduct():
  return render_template("wtechProduct.html")


@app.route("/wtech/v2/sms",methods=["GET"])
def emailSms():
  email = request.args.get("email")
  code = random.randint(1001,9999)
  subject = "Don't reply this mail"
  content = f"""
  Dear User,
     Hey, this is the auto-mail, the code is : {code}

  Best wishes,
  W Tech Inc. technical department
  """
  s = smtplib.SMTP("smtp.gmail.com",587)
  s.starttls()
  s.login("1245server@gmail.com","jvbswpfesugcqazw")
  send_data = f"Subject: {subject} \n\n {content}"
  s.sendmail("1245server@gmail.com",email,send_data)
  return jsonify({"block":"true","code":code,"status":"Email sent!"})

@app.route("/wtech/v2/mailservice",methods=["GET"])
def wtechEmail():
  email = request.args.get("email")
  msg = MIMEText("""
尊敬的企業用戶，
您好！我是 自動電郵程式，我們泓技科技的代表，非常榮幸能與您聯繫。我們的目標是幫助您的企業實現自我創新和自動化，以提高服務質量並最大化業務效益。
我們的專業團隊已經開發了一系列服務，包括泓幣(WCoins)、電腦遊戲販售、Fungpt-turbo智能AI服務等。
我們的自動化服務 FunGPT 是我們的首款聊天AI，儘管由於託管問題已經停止服務，但我們的Fungpt-turbo已經準備就緒，期待為您的業務創造價值。只要註冊用戶，您即可體驗到我們的智能服務。
透過我們的電郵服務，我們更確保能即時與您聯絡，為您在面對任何問題或需求時提供所需要的即時支援。
我們認為，透過我們的產品和服務，我們能夠協助您的企業實現更高的生產率和效率。我們相信自動化和創新是未來的方向，並將堅持不懈地為我們的客戶提供最前沿的科技服務。
如果您希望進一步了解我們的產品和服務，或者需要任何協助，請隨時透過回復此電郵與我們聯繫，我們將非常樂意為您提供幫助。
謝謝您的時間。期待迎接挑戰，與您共同建立自動化的未來！

官方網站：https://wtech-5o6t.onrender.com

順祝商祺
泓技技術團隊敬上
  ""","plain","utf-8")
  msg["Subject"] = "泓技科技-引領您的企業自動化轉型之旅"
  msg["From"] = "1245server@gmail.com"
  msg["To"] = email
  s = smtplib.SMTP("smtp.gmail.com",587)
  s.starttls()
  s.login("1245server@gmail.com","jvbswpfesugcqazw")
  #send_data = f"Subject: {subject} \n\n {content}"
  s.sendmail("1245server@gmail.com",[email],msg.as_string())
  return jsonify({"block":"true","status":"Email sent!"})

@app.route("/wtech/stock/chi")
def stock():
  return render_template("stock.html")

@app.route("/wcoin/client",methods=["POST"])
def client():
  user = request.form.get("user")
  pw = request.form.get("pw")
  url = "https://wtech-5o6t.onrender.com/data"
  res = requests.get(url=url).json()
  if user == "wangtry" and pw == "003417":
    count = 20000
    last_json = res[-1]
    first_json = res[0]
    last_price = last_json["price"]
    first_price = first_json["price"]
    for r in res:
      price = r["price"]
      if int(str(last_price)[-1]) >= int(str(first_price)[0]):
        cp = int(str(last_price)[-1]) - int(str(first_price)[0])
        count *= cp
      else:
        count -= 1000
    return render_template("client.html",user=user,count=count)
  elif user == "Cw1023" and pw == "1023":
    count = 25000000
    return render_template("client.html",user=user,count=count)
  elif user == "li-chen" and pw == "Abcd1234":
    count = 200.01
    return render_template("block.html",user=user)
  else:
    return abort(405)

@app.route("/wcoin/wcm")
def wcm():
  return render_template("wcm.html")

@app.route("/wcoin/wcm/<clientID>/<MType>")
def wcmConnect(clientID : str,MType : str):
  if clientID == "Sdcygc6766" and MType == "WM107":
    return jsonify({
        "clientID" : clientID,
        "name" : MType,
        "BlockClain id" : 51,
    })
  else:
    return jsonify({"Error 404":"Client-info not found"})

@app.route("/wcoin/pay")
def wpay_coin():
  return render_template("coin.html")

@app.route("/wcoin/pay/paypal",methods=["GET"])
def paypal_coins():
  count = request.args.get("price")
  place = request.args.get("country")
  paym = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
          "payment_method": "paypal"
      },
      "redirect_urls": {
          "return_url": url_for("paySuccess"),
          "cancel_url": url_for("wtechLogin")
      },
      "transactions": [{
          "amount": {
              "total": count,
              "currency": place
          },
          "description": "For Wcoins"
      }]
    })
  if paym.create():
    for link in paym.links:
      if link.method == "REDIRECT":
        redirect_url = link.href
        return redirect(redirect_url)
  else:
    return jsonify({
      "msg" : "Invaild payment method!"
    })
#ssksk
@app.route("/wtech/v2/login")
def wtechLogin():
  return render_template("wtechLogin.html")

@app.route("/wcoin/pay/success")
def paySuccess():
  return render_template("paySuccess.html")

@app.route("/wcoin/mining/starter",methods=["GET","POST"])
def miningSt():
  MKey = request.args.get("MKey")
  if MKey == "Wc-12901929Kall":
    return render_template("stMining.html")
  else:
    return jsonify({"Invaild key":"Cannot find machine"})

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

@app.route("/wtech/api/v1/login",methods=["GET"])
def checkUser():
  clientID = str(request.args.get("clientID"))
  user = request.form.get("user")
  pw = request.form.get("pw")
  if clientID == "00001":
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

@app.route("/wcoin/sell")
def sellCoin():
  return render_template("sell.html")

@app.route("/wcoin/sell/real")
def real():
  rate = random.randint(489,1000)
  return render_template("real.html",rate=rate)

@app.route("/wcoin/sell/crypto")
def crypto():
  rate = random.randint(489,1000)
  return render_template("crypto.html",rate=rate)

@app.route("/crypto/transfer/done")
def cryptoDone():
  return jsonify({"Done":"Successfully transfer! Please wait!"})

@app.route("/wcoin/transfer/cash",methods=["GET"])
def cashTransfer():
  email = request.args.get("mail")
  subject = "Client request : withdraw cash"
  content = """
  Dear Client,
     Hey, It is auto-mail,it will have staff to help you.

  Best wishes,
  W Tech Inc. technical department
  """
  s = smtplib.SMTP("smtp.gmail.com",587)
  s.starttls()
  s.login("1245server@gmail.com","jvbswpfesugcqazw")
  send_data = f"Subject: {subject} \n\n {content}"
  s.sendmail("1245server@gmail.com",email,send_data)
  return render_template("serverMail.html")

@app.route("/wcoins/mining/info")
def chAdd():
  rate = random.randint(489,1000)
  return render_template("mining.html",rate=rate)

@app.route("/wcoin/transfer/crypto",methods=["GET"])
def transferCrypto():
  address = request.form.get("address")
  amout = request.form.get("amout")
  if True:
    return render_template("cryptoTran.html",address=address,amout=amout)
  else:
    return jsonify({"Error 405":"Invaild infomation"})

@app.route("/style/css/simple")
def style():
  return render_template("style.css")

app.run(host="0.0.0.0",port=5000)
