from flask import Flask,render_template,jsonify,request,abort,url_for,redirect,make_response,send_file
from flask_cors import CORS
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
import psycopg2
import numpy
import re
import pyqrcode
from io import BytesIO
import base64
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import pytz
from discord import Bot,Embed,Option
import discord
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

CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

auth = HTTPBasicAuth()

users = {
    "wangtry": generate_password_hash("Chan1234#"),
    "wtech": generate_password_hash("wtechStaff1234#"),
    "wtechpass001": generate_password_hash("Asswfcx24166456#"),
    "wtechpass002": generate_password_hash("Assxct656654#")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@auth.error_handler
def unauthorized():
    # return make_response(jsonify({'error': 'Unauthorized access'}), 401)
    return make_response("沒有授權訪問",401)

conn = psycopg2.connect(database="wbank", user="root", 
password="r7wPtW1z6ltgw4oW8hW6qeIzJacfgwCM", host="dpg-cop0h6779t8c73fimlm0-a.singapore-postgres.render.com", 
port=5432)

"""
paypalrestsdk.configure({
  'mode': 'sandbox', 
  'client_id': 'ASK8RjfrdCzGvCQRDvnfa321S_5OBGMK4KDGac5PreKf6NU-0d0MUPPrYe_S-fq4tcoHN22P8Nz4xZs3',
  'client_secret': 'EB1-tdfv74XcCxkdDWjueV19ePB4Wf8uMKwdhE2robSWQF21i6nC6pm57zzVARTzJ03ah6X4ARc1GhBQ'
})
"""

paypalrestsdk.configure({
  'mode': 'live', 
  'client_id': 'AZsh7JUNnTOO2eYLuwhfwMltWUUCcDS--qf2TzNVDCvlDK20lhbUrbRXYfZgfJEaDskmPi5nmssIQWme',
  'client_secret': 'ELlPg1idvYkNyzL1nBip5r2qL-fLBhHUpuz_aFQUD6OC7D1AlYj7qxPislk8_0igdkcp0afgPw2O5K0a'
})

def hash_value(user):
  u = user.encode()
  sha = hashlib.sha256(u).hexdigest()
  return sha

@app.errorhandler(500)
def error_server(e):
  return jsonify({
    "status" : "server error",
    "status_code(https)" : 500,
    "status_code(wtps)" : 407,
    "server hint" : "carefully and try again!",
    "error_detail" : str(e)
  })

@app.route("/")
def index():
  x_forwarded_for = request.headers.get('X-Forwarded-For')
  if x_forwarded_for:
    user_ip = x_forwarded_for.split(',')[0]
  else:
    user_ip = request.remote_addr
    
  res = requests.get(f"https://ipinfo.io/{user_ip}?token=f5bcbfedf78b27").json()
  if "bogon" not in res:
    if res["country"] == "TW":
      return redirect("/wtech/bockweb?place=tw")
    else:
      return render_template("wtechHome.html")
  else:
    return abort(502)

@app.route("/wtech/chat")
def wtechChat():
  return render_template("wtechChat.html")
  
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

@app.route("/wtech/bockweb",methods=["GET"])
def webCheckIsBlock():
  place = str(request.args.get("place"))
  if place == "tw":
    country = "中華民國（台灣)"
    return render_template("wtechBlock.html",country=country)
  elif place == "us":
    country = "United Status"
    return render_template("wtechBlockEn.html",country=country)
    
@app.route("/wtech/v2/staff")
def wtechVStaff():
  return render_template("StaffLogin.html")

@app.route("/wtech/staff")
def wtechStaff():
  return render_template("wtechStaff.html")

@app.route("/wtech/v2/discord/bot")
def wtech_discord_bot():
  token = request.headers.get("token")
  bot = discord.Bot()
  @bot.event
  async def on_ready():
     print("ok")
  @bot.slash_command()
  async def about(ctx):
    e = Embed(title="about me",description="""Hello, I am made by wtech inc.
              The link: http://wtechhk.xyz"
              """)
    await ctx.respond(embed=e)

  @bot.slash_command(description="To google search",options=[Option(str,description="query",name="query")])
  async def ggogle_search(ctx,query):
    res = req.get(url=f"https://google.com/search?q={query}").content
    await ctx.respond(res)
    if not token:
        return jsonify({"Error": "Please enter a token!"})
    else:
      if len(token) > 20:
        while True:
          try:
            bot.run(token)
          except Exception as e:
            return jsonify({"Error":e})
          return "ok"
      else:
          return jsonify({"Token Error" : "Bot token invaild!"})
  

@app.route("/wtech/v2/staffDashboard",methods=["POST"])
def wtechStaffDB():
  user = str(request.form.get("user"))
  pw = int(request.form.get("pw"))
  ## 允許python執行postgresql語法
  with conn.cursor() as cur:
    
    ## SQL語法
    sql = "SELECT * From Staff;"

    ## 執行sql語法
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
      if row[0] == user and row[1] == pw :
        position = row[2]
        return render_template("staffDB.html",user=user,position=position)
      return jsonify({"Invaild input" : "Cannot find this user in WTech staff database","Your enter user" : user,"Your enter pw" : pw})


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
  s = smtplib.SMTP("smtpout.secureserver.net",465)
  s.starttls()
  s.login("tech-support@wtechhk.xyz","WTech1234#")
  #send_data = f"Subject: {subject} \n\n {content}"
  s.sendmail("tech-support@wtechhk.xyz",[email],msg.as_string())
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

@app.route("/wtech/v2/cryptoList")
def wtechCryptoListDe():
  phase = request.headers.get("crypto-List")
  key = "DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q="
  fernet = Fernet(key)
  # 解密结果
  decrypted_data = fernet.decrypt(phase)

  # 将解密后的字符串转换为列表
  adrs = eval(decrypted_data.decode())
  return jsonify({
   "Crypto-text" : phase,
   "Decrypted-result" : adrs
  })

@app.route("/wtech/v2/wtps")
def wtechWtps():
  url = str(request.args.get("url"))
  urll = re.split("://|:|/",url)
  domains = [
    "wcoins.wtech.net",
    "wtech.net"
  ]
  if urll[0] == "wtps":
    for domain in domains:
      if urll[1] == domain:
        if domain == "wcoins.wtech.net":
          if urll[2] == "3301":
            pass
          elif urll[2] == "3305":
            if urll[3] == "mining":
              points = int(request.args.get("value"))
              return redirect("http://wtechhk.xyz/cw1023/startMining.html")
            else:
              abort(503)
          else:
            return "Wtech network has not found this port of it."
        elif domain == "wtech.net":
          return redirect("/")
        else:
          return jsonify({"Wtech error" : "Cannot read this domain"})
      else:
        return jsonify({"Wtech error" : "Cannot read this domain"})
  else:
    return "Cannot load wtps://"

@app.route("/wcoins/v3/miner",methods=["POST"])
def wtechWcoinsMining():
  user = request.form.get("miner_place")
  cur = conn.cursor()
  cur.execute(f"SELECT * FROM wcoins_mining_place where {user}")
  rows = cur.fetchall()
  for row in rows:
    return render_template("wbankMiner.html",user=user)
  return "找不到wcoins礦池"
    
@app.route("/wcoin/v2/mining")
def wtechMiningWcoins():
  address = request.headers.get("User-wallet")
  key = "DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q="
  fernet = Fernet(key)
  # 解密结果
  decrypted_data = fernet.decrypt(address)

  # 将解密后的字符串转换为列表
  adrs = eval(decrypted_data.decode())
  res = requests.get(url="https://wtech-5o6t.onrender.com/data").json()
  pr = []
  for item in res:
    pr.append(item["price"])
  np_prices = numpy.array(pr)
  fmat = ((adrs[1]*np_prices.mean())/np_prices.min())*2
  data = ["wtps://wcoins.wtech.net:3305/mining",fmat]
  # 将列表转换为字符串
  list_string = str(data)

  # 创建 Fernet 加密器
  fernet = Fernet(key)

  # 加密字符串
  encrypted_data =  fernet.encrypt(list_string.encode())
  token = encrypted_data.decode()
  run_times = 0
  while run_times <= 10:
    run_times += 1
    return f"Mining value : {fmat} \n Ready address : {token}"
    res = requests.get(url="https://wtech-5o6t.onrender.com/data").json()
    pr = []
    for item in res:
      pr.append(item["price"])
      np_prices = numpy.array(pr)
      fmat = ((adrs[1]*np_prices.mean())/np_prices.min())*2
  return "Um... seem like error"

@app.route("/wtech/about")
def wtechAbout():
  x_forwarded_for = request.headers.get('X-Forwarded-For')
  if x_forwarded_for:
    user_ip = x_forwarded_for.split(',')[0]
  else:
    user_ip = request.remote_addr
    
  res = requests.get(f"https://ipinfo.io/{user_ip}?token=f5bcbfedf78b27").json()
  if "bogon" not in res:
    if res["country"] == "TW":
      return redirect("/wtech/bockweb?place=tw")
    else:
      return render_template("wtechAbout.html")
  else:
    return abort(502)

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

@app.route("/wtech/v2/bankDB",methods=["GET","POST"])
def wtech_bank_db():
  url = request.args.get("redirectURL")
  if url != "":
    user = request.form.get("user")
    pw = request.form.get("pw")
    cur = conn.cursor()
    cur.execute(f"select * from wbankwallet where Username='{user}'")
    rows = cur.fetchall()
    for row in rows:
      if pw == row[2]:
        username = row[0]
        balance = row[1]
        redirect_res = redirect(url,code=302)
        res = make_response(redirect_res)
        res.set_cookie("username",username)
        res.set_cookie("balance",balance)
        return res
        return redirect(url)
      return abort(503)
  else:
    return "Cannot find redirect URL!."

@app.route("/wtech/wcoins/card")
def wtech_wcoins_card():
  return render_template("wcoins_card.html")

@app.route("/wbank/v1/record")
def wbank_read_record():
    user = request.headers.get("user")
    cur = conn.cursor()
    cur.execute(f"select * from wbankrecord where username='{user}'")
    rows = cur.fetchall()
    result = []
    for row in rows:
        record = {
            "user" : row[0],
            "action" : row[1],
            "time" : row[2]
        }
        result.append(record)
    return jsonify(result)

@app.route("/wtech/v2/transfer")
def wtech_transfer():
  code = request.args.get("code")
  key = "DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q="
  fernet = Fernet(key)
  # 解密结果
  decrypted_data = fernet.decrypt(code)

  # 将解密后的字符串转换为列表
  data = eval(decrypted_data.decode())
  cur = conn.cursor()
  cur.execute(f"select * from wbankwallet where Username='{data[0]}'")
  rows = cur.fetchall()
  for row in rows:
    if row[1] < 0:
      return jsonify({"message":"Your account have not balance!."}) , 500
    elif row[1] < data[2]:
      return jsonify({"message":"Your account have not any balance!."}) , 500
    else:
      cur.execute(f"""UPDATE wbankwallet
SET balance={row[1]-data[2]}
WHERE username='{data[0]}'""")
      conn.commit()
      bl = f"由 {data[0]} 轉帳 {data[2]} 給 {data[1]}"
      tz = pytz.timezone('Asia/Taipei')
      # 取得當前的 UTC 時間
      utc_time = datetime.datetime.now(pytz.timezone('UTC'))
      # 轉換 UTC 時間到 UTC+8 時區
      local_time = utc_time.astimezone(tz)
      cur.execute(f"INSERT INTO wbankrecord (username, action, time) VALUES ('{data[1]}', '{bl}', '{local_time}');")
      conn.commit()
      cur.execute(f"select * from wbankwallet where Username='{data[1]}'")
      cols = cur.fetchall()
      for col in cols:
        cur.execute(f"""UPDATE wbankwallet
SET balance={col[1]+data[2]}
WHERE username='{col[0]}'""")
        conn.commit()
        prompt = f"""
     轉帳方： {data[0]}
     收款方： {col[0]}
     金額: {data[2]}
     狀態：成功✅
    """
        data = {
        "embeds": [
        {
            "title": "Wcoins 轉帳通知",
            "description": prompt,
            "color": 65280,  # You can use hex color codes, this one is for blue
        }
    ]
    }
      r = requests.post(url="https://discord.com/api/webhooks/1236986187793829930/OBBvTByDyP-fvcVKI40D51UpaN5wU5HOjeHtxdiwh40-b09-gVj-jmoLcdPwlLs0-M2x",json=data)
      return jsonify({"Good news":"Success to transfer"})
  return "Cannot transfer it! check your code arg."

@app.route("/wtech/v2/createOrder")
def wtech_create_order():
  user = request.headers.get("Username")
  reviewer = request.headers.get("reviewer")
  count = int(request.headers.get("Value"))
  #redirect_url = request.args.get("redirectURL")
  code = [user,reviewer,count]
  key = "DUBWKuYEugUex8ynVKm-7ctcUmwaV0u0JpzLkoka8_Q="
  list_string = str(code)

  # 创建 Fernet 加密器
  fernet = Fernet(key)

  # 加密字符串
  encrypted_data =  fernet.encrypt(list_string.encode())
  token = encrypted_data.decode()
  return jsonify({"code" : token})

@app.route("/wp",methods=["GET","POST"])
def wp_user_db():
  user = request.form.get("username")
  pw = request.form.get("password")
  cur = conn.cursor()
  try:
    cur.execute("select * from worldplay")
    rows = cur.fetchall()
    for row in rows:
      if user == row[0]:
        balance = row[1]
        return render_template("worldPlay.html",user=user,balance=balance)
    return "Somethings is wrong!."
  except psycopg2.Error as e:
    conn.rollback()
    return f"Error: {e}"

@app.route("/wp/buyIn")
def wp_buyIn():
  user = request.headers.get("name")
  balance = int(request.headers.get("balance"))
  cur = conn.cursor()
  cur.execute(f"UPDATE worldplay set balance={balance} where username='{user}'")
  conn.commit()
  return jsonify({"Done":"Almost Done!."})

class Game:
    def __init__(self):
        self.reset()
    def reset(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.player_chips = 100  # 讓玩家在開始時有100個籌碼
        self.bet = 10  # 預設的下注籌碼為10
    def deal_card(self):
        return self.deck.pop() if self.deck else self.reset()
    def bet(self, amount):
        self.bet = amount
    def hit(self):
        self.player_hand.append(self.deal_card())
    def stand(self):
        while sum(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
        player_won, dealer_won = self.check_win()
        # 如果玩家贏了，他會贏得一定比例的賭金
        if player_won:
            self.player_chips += self.bet * 2
    def get_player_hand(self):
        return self.player_hand
    def get_dealer_hand(self):
        return self.dealer_hand
    def check_win(self):
        player_score = sum(self.get_player_hand())
        dealer_score = sum(self.get_dealer_hand())
        player_won = dealer_won = False
        if player_score > 21:
            dealer_won = True
        elif dealer_score > 21:
            player_won = True
        elif player_score > dealer_score:
            player_won = True
        elif dealer_score > player_score:
            dealer_won = True
        return player_won, dealer_won
    def all_in(self):
        self.bet(self.player_chips)
      
# 創建遊戲實例
game = Game()

@app.route("/wp/luck")
def wp_luck():
  user = request.headers.get("user")
  try:
    cur = conn.cursor()
    cur.execute("select * from worldplay")
    rows = cur.fetchall()
    for row in rows:
      if user == row[0]:
        balance = row[1]
        s1 = random.randint(101,13690876)
        cur = conn.cursor()
        cur.execute(f"UPDATE worldplay set balance='{s1}' where username='{user}'")
        conn.commit()
        return jsonify({"result":s1})
    return "Somethings is wrong!."
  except psycopg2.Error as e:
    conn.rollback()
    return f"Error: {e}"

@app.route("/wp/luck/start")
def wp_luck_start():
  user = request.args.get("user")
  try:
    cur = conn.cursor()
    cur.execute("select * from worldplay")
    rows = cur.fetchall()
    for row in rows:
      if user == row[0]:
        balance = row[1]
        return render_template("goodLuck.html",balance=balance,user=user)
    return "Somethings is wrong!."
  except psycopg2.Error as e:
    conn.rollback()
    return f"Error: {e}"

@app.route("/wp/twoOne/start")
def wp_game_start():
  user = request.args.get("user")
  try:
    cur = conn.cursor()
    cur.execute("select * from worldplay")
    rows = cur.fetchall()
    for row in rows:
      if user == row[0]:
        balance = row[1]
        # 初始化遊戲
        game.reset()
        # 發牌
        player_hand = [game.deal_card(), game.deal_card()]
        dealer_hand = [game.deal_card(), game.deal_card()]
        return render_template("twoOne.html",player_hand=player_hand,dealer_hand=dealer_hand,balance=balance,user=user)
    return "Somethings is wrong!."
  except psycopg2.Error as e:
    conn.rollback()
    return f"Error: {e}"

@app.route('/hit', methods=['POST'])
def hit():
    user = request.headers.get("user")
    game.hit()
    cur = conn.cursor()
    cur.execute(f"select * from worldplay where username='{user}'")
    rows = cur.fetchall()
    for row in rows:
      cur = conn.cursor()
      cur.execute(f"UPDATE worldplay set balance='{int(row[1]) + 200}' where username='{user}'")
      conn.commit()
    return jsonify({'player_hand': game.get_player_hand(), 'player_won': game.check_win()})
@app.route('/stand', methods=['POST'])
def stand():
    user = request.headers.get("user")
    game.stand()
    cur = conn.cursor()
    cur.execute(f"select * from worldplay where username='{user}'")
    rows = cur.fetchall()
    for row in rows:
      cur = conn.cursor()
      cur.execute(f"UPDATE worldplay set balance='{int(row[1]) - 200}' where username='{user}'")
      conn.commit()
    return jsonify({'dealer_hand': game.get_dealer_hand(), 'dealer_won': game.check_win()})

# 對玩家下注
@app.route('/bet', methods=['POST'])
def bet():
    user = request.headers.get("user")
    bet_amount = request.form['bet_amount']
    cur = conn.cursor()
    cur.execute(f"select * from worldplay where username='{user}'")
    rows = cur.fetchall()
    for row in rows:
      cur = conn.cursor()
      cur.execute(f"UPDATE worldplay set balance='{int(row[1]) - int(bet_amount)}' where username='{user}'")
      conn.commit()
      #game.bet(int(bet_amount))  # 調用下注方法
      return jsonify({'bet': game.bet, 'balance': int(row[1]) - int(bet_amount)})
      
# 玩家全下
@app.route('/bet_all', methods=['POST'])
def bet_all():
    user = request.headers.get("user")
    cur = conn.cursor()
    cur.execute(f"select * from worldplay where username='{user}'")
    rows = cur.fetchall()
    for row in rows:
      cur = conn.cursor()
      cur.execute(f"UPDATE worldplay set balance='{int(row[1]) - int(row[1])}' where username='{user}'")
      conn.commit()
      #game.bet(game.player_chips)  # 將所有籌碼下注
      return jsonify({'bet': game.bet, 'balance': int(row[1]) - int(row[1])})

@app.route("/wbank")
def wbank():
  return render_template("wbank.html")

@app.route("/wbank/transfer")
def wbank_transfer():
  return render_template("wbankTransfer.html")

@app.route("/wbank/new_client")
def wbank_new_client():
  return render_template("newWbank.html")

@app.route("/wbank/v1/paypal")
def wbank_paypal():
  user = request.args.get("user")
  count = float(request.args.get("amount"))
  paym = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
          "payment_method": "paypal"
      },
      "redirect_urls": {
          "return_url": f"/wbank/v1/paypal/done?user={user}&amount={count}",
          "cancel_url": "/wbank"
      },
      "transactions": [{
          "amount": {
              "total": count,
              "currency": "HKD"
          },
          "description": "WCoins payment"
      }]
    })
  if paym.create():
    for link in paym.links:
        if link.rel == "approval_url":
            # Convert to str to avoid google appengine unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            return redirect(approval_url)
            print("Redirect for approval: %s" % (approval_url))
  else:
    return jsonify({
      "msg" : "Invaild payment method!."
    })
    
@app.route("/wtech/stock/lookUp")
def wtech_stock_lookUp():
  cur = conn.cursor()
  cur.execute(f"select * from goods")
  rows = cur.fetchall()
  goods_list = []
  for row in rows:
    data = {
      "name" : row[0],
      "number" : row[1],
      "stock" : row[2],
      "status" : row[3]
    }
    goods_list.append(data)
  return jsonify(goods_list)

@app.route("/wtech/stock/add",methods=["GET","POST"])
def wtech_stock_add():
  good_name = request.form.get("good_name")
  amount = int(request.form.get("amount"))
  good_number = "WT-" + str(random.randint(10199,901829))
  cur = conn.cursor()
  cur.execute(f"INSERT INTO goods (good_name,good_number,stock,status) VALUES ('{good_name}','{good_number}',{amount},'入貨中')")
  conn.commit()
  return redirect("http://wtranfer.wtechhk.xyz")

@app.route("/wtech/stock/changeStatus",methods=["GET","POST"])
def wtech_stock_change_status():
  good_number = request.form.get("good_number")
  status = request.form.get("status")
  if status == "inside":
    statement = "入貨中"
    cur = conn.cursor()
    cur.execute(f"UPDATE goods set status='{statement}' where good_number='{good_number}'")
    conn.commit()
    return redirect("http://wtranfer.wtechhk.xyz")
  elif status == "in-here":
    statement = "存倉中"
    cur = conn.cursor()
    cur.execute(f"UPDATE goods set status='{statement}' where good_number='{good_number}'")
    conn.commit()
    return redirect("http://wtranfer.wtechhk.xyz")
  elif status == "outside":
    statement = "出貨中"
    cur = conn.cursor()
    cur.execute(f"UPDATE goods set status='{statement}' where good_number='{good_number}'")
    conn.commit()
    return redirect("http://wtranfer.wtechhk.xyz")
  else:
    return redirect("http://wtranfer.wtechhk.xyz")

@app.route("/wtech/stock/change",methods=["GET","POST","DELETE"])
def wtech_stock_change():
  if request.method == "GET":
    good_number = request.args.get("good_number")
    cur = conn.cursor()
    cur.execute(f"DELETE from goods where good_number='{good_number}'")
    conn.commit()
    return redirect("http://wtranfer.wtechhk.xyz")
  elif request.method == "POST":
    good_number = request.args.get("good_number")
    good_count = int(request.args.get("c"))
    cur = conn.cursor()
    cur.execute(f"UPDATE goods set stock={good_count} where good_number='{good_number}'")
    conn.commit()
    return redirect("http://wtranfer.wtechhk.xyz")
  else:
    return abort(405)
  
@app.route("/wtech/v1/discordBuyin")
def discord_buy_in():
  user = request.args.get("user")
  count = request.args.get("amount")
  m = request.args.get("m")
  prompt = f"""
     用戶： {user}
     金額: {count}
     使用ATM機的名稱: {m}
    """
  data = {
        "embeds": [
        {
            "title": "Wcoins ATM 買入通知",
            "description": prompt,
            "color": 65280,  # You can use hex color codes, this one is for blue
        }
    ]
    }
  r = requests.post(url="https://discord.com/api/webhooks/1236986178792853544/CuqsxhTUbZW6QgVAuyg23fU1FpkavEcEwsvpaMqA4jbdaYjQyUEFiFzV85jQhXNWNTzA",json=data)
  return jsonify({"Ok":"Done"})

@app.route("/wtech/v1/checkServer")
def wtech_check_server_status():
  url = "https://api.render.com/v1/services/srv-cnepnida73kc73ctk59g/deploys?limit=20"

  headers = {
    "accept": "application/json",
    "authorization": "Bearer rnd_2eC5ILwF6FNYRugb9D3vOITXAqXK"
  }

  response = requests.get(url, headers=headers).json()
  res = response[0]
  update_server_date = res["deploy"]["commit"]["createdAt"]
  server_now_status = res["deploy"]["status"]
  if server_now_status == "live":
    prompt = """
     主機目前的狀態：上線運行中 🟢
    """
    data = {
        "embeds": [
        {
            "title": "主機狀況",
            "description": prompt,
            "color": 65280,  # You can use hex color codes, this one is for blue
        }
    ]
    }
    r = requests.post(url="https://discord.com/api/webhooks/1229314452189347910/GTqIUYZLHSywjU27PC-1FTthxVJcRvzT5BsD2iLAGTipwQ-lipMZXxxH936M0JhTm5JF",json=data)
    return jsonify({
    "update_date" : update_server_date,
    "status" : server_now_status
    })
  else:
    prompt = """
     主機目前的狀態：發生錯誤或已為關閉狀態 🔴
    """
    data = {
        "embeds": [
        {
            "title": "主機狀況",
            "description": prompt,
            "color": 16711680,  # You can use hex color codes, this one is for blue
        }
    ]
    }
    r = requests.post(url="https://discord.com/api/webhooks/1229314452189347910/GTqIUYZLHSywjU27PC-1FTthxVJcRvzT5BsD2iLAGTipwQ-lipMZXxxH936M0JhTm5JF",json=data)
    return jsonify({
    "update_date" : update_server_date,
    "status" : server_now_status
    })

@app.route("/wbank/hash/createOrder")
def wbank_hash_order():
  user = request.headers.get("Username")
  reviewer = request.headers.get("reviewer")
  count = int(request.headers.get("Value"))
  cur = conn.cursor()
  cur.execute(f"select username,balance from wbankwallet where username='{user}'")
  rows = cur.fetchall()
  for row in rows:
    if row[1] >= count:
      text1 = [row[0],reviewer,str(row[1])]
      t1 = ",".join(text1)
      hash1 = hashlib.sha256(t1.encode()).hexdigest()
      return jsonify({"Your order hash-value":hash1})
  return "Somethings input data is wrong!."

@app.route("/wbank/v1/paycode")
def wbank_sell_payCode():
  code = request.args.get("code")
  cur = conn.cursor()
  cur.execute("select username,balance from wbankwallet")
  rows = cur.fetchall()
  for row in rows:
    user = row[0]
    balance = row[1]
    text1 = [user,str(balance)]
    t1 = ",".join(text1)
    hash1 = hashlib.sha256(t1.encode()).hexdigest()
    if code == hash1:
      return render_template("wbankPayment.html",user=user,balance=balance)
  return "Cannot assign the user detail!."

@app.route("/wbank/buyCoins")
def wbank_buyCoind():
  user = request.args.get("user")
  fromer = "wtech-wcoins-m1"
  cur = conn.cursor()
  cur.execute(f"select username,balance from wbankwallet where username='{user}'")
  rows = cur.fetchall()
  for row in rows:
    if user == row[0]:
      text1 = [row[0],str(row[1]),fromer]
      t1 = ",".join(text1)
      hash1 = hashlib.sha256(t1.encode()).hexdigest()
      wallet_address = f"https://wtech-5o6t.onrender.com/wbank/v1/rece?code={hash1}"
      # 生成 QR 碼
      qr = pyqrcode.create(wallet_address)
      # 使用 BytesIO 創建一個在記憶體中的臨時檔案
      temp = BytesIO()
      # 保存 QR 碼圖像到臨時檔案
      qr.svg(temp,scale=8)
      qr_bytes = temp.getvalue()
      qr_b64 = base64.b64encode(qr_bytes).decode('ascii')
      # 使用 send_file 將 QR 碼圖像傳輸到前端
      return render_template("wbankSell.html", img=qr_b64)
  return "Cannot assign the user detail!."

@app.route("/wbank/v1/rece")
def wbank_receCoins():
  code = request.args.get("code")
  cur = conn.cursor()
  cur.execute("select username,balance from wbankwallet")
  rows = cur.fetchall()
  for row in rows:
    user = row[0]
    balance = row[1]
    fromer = "wtech-wcoins-m1"
    text1 = [user,str(balance),fromer]
    t1 = ",".join(text1)
    hash1 = hashlib.sha256(t1.encode()).hexdigest()
    if code == hash1:
      return render_template("wbankGet.html",user=user,balance=balance,fromer=fromer)
  return "Cannot assign the user detail!."

@app.route("/wbank/sellCoins")
def wbank_sellCoins():
  user = request.args.get("user")
  cur = conn.cursor()
  cur.execute(f"select username,balance from wbankwallet where username='{user}'")
  rows = cur.fetchall()
  for row in rows:
    if user == row[0]:
      text1 = [row[0],str(row[1])]
      t1 = ",".join(text1)
      hash1 = hashlib.sha256(t1.encode()).hexdigest()
      wallet_address = f"https://wtech-5o6t.onrender.com/wbank/v1/paycode?code={hash1}"
      # 生成 QR 碼
      qr = pyqrcode.create(wallet_address)
      # 使用 BytesIO 創建一個在記憶體中的臨時檔案
      temp = BytesIO()
      # 保存 QR 碼圖像到臨時檔案
      qr.svg(temp,scale=8)
      qr_bytes = temp.getvalue()
      qr_b64 = base64.b64encode(qr_bytes).decode('ascii')
      # 使用 send_file 將 QR 碼圖像傳輸到前端
      return render_template("wbankSell.html", img=qr_b64)
  return "Cannot assign the user detail!."

@app.route("/wbank/v1/mining")
def wbank_mining():
  user = request.args.get("user")
  url = request.args.get("poolURL")
  return render_template("wbankMining.html",user=user,url=url)

@app.route("/wbank/v1/done")
@auth.login_required
def wbank_done():
  user = request.args.get("user")
  count = request.args.get("amount")
  return render_template("wbankDone.html",user=user,count=count)

@app.route("/wbank/v1/paypal/done")
def wbank_paypal_done():
  user = request.args.get("user")
  count = request.args.get("amount")
  return render_template("wbankRe.html",user=user,count=count)

@app.route("/wbank/v1/createUser",methods=["POST"])
def wbank_into_user():
  user = request.form.get("user")
  pw = request.form.get("pw")
  email = request.form.get("email")
  cur = conn.cursor()
  cur.execute(f"INSERT INTO wbankwallet (username, balance, password, verify) VALUES ('{user}', '0', '{pw}','no')")
  conn.commit()
  cur = conn.cursor()
  cur.execute(f"select username,balance,verify from wbankwallet where username='{user}'")
  rows = cur.fetchall()
  for row in rows:
    if user == row[0]:
      text1 = [str(user),"true"]
      t1 = ",".join(text1)
      hash1 = hashlib.sha256(t1.encode()).hexdigest()
      content = f"""
   Hello There,
   This is your verify-link: https://wtech-5o6t.onrender.com/wbank/verify?code={hash1}
      """
      msg = MIMEText(content,"plain","utf-8")
      msg["To"] = email
      msg["From"] = "verify@wtechhk.xyz"
      msg["Subject"] = "Verify your account"
      s = smtplib.SMTP("mail.wtechhk.xyz",587)
      s.login("verify@wtechhk.xyz","WTechStaff1234#")
      #send_data = f"Subject: {subject} \n\n {content}"
      s.sendmail("verify@wtechhk.xyz",[email],msg.as_string())
      return redirect("http://bank.wtechhk.xyz")
  return "Cannot do that!."

@app.route("/wbank/verify")
def wbank_verify():
  code = request.args.get("code")
  cur = conn.cursor()
  cur.execute("select username,balance,verify from wbankwallet")
  rows = cur.fetchall()
  for row in rows:
    user = row[0]
    balance = row[1]
    verify = row[2]
    text1 = [user,"true"]
    t1 = ",".join(text1)
    hash1 = hashlib.sha256(t1.encode()).hexdigest()
  if code == hash1:
    cur = conn.cursor()
    cur.execute(f"UPDATE wbankwallet set verify='yes' where username='{user}'")
    conn.commit()
    return "你的帳號已成功驗證"
  return "無法驗證用戶信息，或者可能哈希值(hash-value)有誤，請聯繫我們。再一次致歉令您受到困擾🙏🥹！。"

@app.route("/wbank/client",methods=["POST"])
def wbank_client():
  user = request.form.get("user")
  pw = request.form.get("pw")
  cur = conn.cursor()
  cur.execute("select * from wbankwallet")
  rows = cur.fetchall()
  error_message = "找不到該用戶"
  for row in rows:
    if user == row[0]:
      if row[3] == "no":
        error_message = "你的帳號尚末驗證，請先查看你的電郵。"
        break
      elif pw != row[2]:
        error_message = "密碼不正確"
        break
      else: 
        balance = row[1]
        return render_template("wbankClient.html",user=user,balance=balance)
  return error_message

@app.route("/wbank/recordPage")
def wbank_record_page_v2():
  user = request.args.get("user")
  return render_template("wbankRecordPage.html",user=user)

@app.route("/wbank/fps")
def wbank_fps():
  user = request.args.get("user")
  return render_template("wbankFPS.html",user=user)

@app.route("/wtech/v2/wbank/auth",methods=["GET","POST"])
def wbank_login():
  user = request.form.get("user")
  pw = request.form.get("pw")
  if user != "":
    cur = conn.cursor()
    cur.execute("select * from wbankwallet")
    rows = cur.fetchall()
    for row in rows:
      if user == row[0]:
        if pw == row[3]:
          return redirect("http://bank.wtechhk.xyz/db.html")
        return "Password is invaild"
    return "Cannot find the user!."
  else:
    return jsonify({"Error":"Cannot provided null username"})

@app.route("/wtech/v2/checkBalance")
@auth.login_required
def user_balance():
  user = request.args.get("username")
  if user != "":
    cur = conn.cursor()
    cur.execute("select * from wbankwallet")
    rows = cur.fetchall()
    for row in rows:
      if user == row[0]:
        return jsonify({
         "Username" : user,
         "Balance" : row[1]
        })
    return "Cannot find the user!."
  else:
    return jsonify({"Error":"Cannot provided null username"})

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
  
"""
@app.route("/wcoin/sk/buy/info",methods=["GET"])
def sk():
  count = int(request.args.get("price"))
  try:
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'HKD',
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
"""

@app.route("/wtech/product")
def wtechProduct():
  x_forwarded_for = request.headers.get('X-Forwarded-For')
  if x_forwarded_for:
    user_ip = x_forwarded_for.split(',')[0]
  else:
    user_ip = request.remote_addr
    
  res = requests.get(f"https://ipinfo.io/{user_ip}?token=f5bcbfedf78b27").json()
  if "bogon" not in res:
    if res["country"] == "TW":
      return redirect("/wtech/bockweb?place=tw")
    else:
      return render_template("wtechProduct.html")
  else:
    return abort(502)


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
        if link.rel == "approval_url":
            # Convert to str to avoid google appengine unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            return redirect(approval_url)
            print("Redirect for approval: %s" % (approval_url))
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
