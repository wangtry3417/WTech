#mining.py
from wcoins.mining import make_block,sha256,complie
from wcoins.crypto import check_address
from wcoins.time import nowTimes

wallet_address = "d08f40525e098fb04d29b0d65657cdbffaa64cbe9ca28b8b1355184bf69b03da"

def making_block(forward_block,timeslamp):
  return make_block(sha256(wallet_address)*888,forward_block,timeslamp)

def start_mining():
  if check_address(wallet_address):
    formula = complie(formula=f"{make_block(sha256(wallet_address)*897,nowTimes())+3*909}",path="/*",mode="fast")
    print(making_block(formula.toHex(),nowTimes()))
  else:
    print("Wallet invaild")

start_mining()

#trade.py
from wcoins.trade import buyIn,sellOut
from wcoins import Exchange,timeWait

exchange = Exchange(name="WBank",apiKey="api-key")
exchange.init()
timeWait(3000)

#buyIn(exchange_info : wcoins.Exchange,amount : float)
buyIn(exchange,amount=300).toBuy()
timeWait(2000)

sellOut(exchange,amount=100).toSell()
timeWait(2000)

#tradeBot.py
from wbank.trade import Bot,complier
from wbank.wcoins import data
from wtech.ai.math import *

class tradeBot(Bot):
  def __init__(self):
    self.coinName = "wcoins"
    self.symbol = "WTC"
    self.mode = "simple"
    self.data = complie(data,mode="json-list",format="wcoins-**/")
    super().__init__(self)
  def start(self):
    statement = random(type="list",data="['buy','sell']")
    return complier(statement=statement,followData=self.data,rules=True)
  def has_troubles(self):
    return complier(statement="cancel-all",followData=self.data,rules=True)

bot = tradeBot(apiKey="api-key")
bot.start()

#chatapi.py
import wchat
from wchat.slash import Commands

client = wchat.Client(intents=wchat.Intents.all())
slash = Commands(prefix="/",client=client)

@client.on("connect")
#on_connect(c : Client,msg=None)
async def on_connect(c):
  await c.prepare()
  print("Bot is online")

@client.on("on_message")
#on_message(c : Client,msg : Message,tts=None,system_message=None...)
async def on_message(c,msg):
  if msg.content == "Ping":
    await c.message.send("Pong")

@slash.cmds("createChannel",options=wchat.slash.options(type="input",name="Channel name",description="Enter the channel name",require=True))
async def createChannel(ctx : wchat.slash.Context):
  await ctx.create(type="channel",name=wchat.slash.find_option("Channel name")) #建立通訊通道
  await ctx.reply("Created channel")

client.run(apiKey="api-key")

#cin.py
from wcoins.blockchain import createChain,addressSetup,nodeSetup
from wcoins.payment import p2p
from wcoins import Rules


class blockChain(createChain):
  def __init__(self):
    self.coinName = "cat-coins",
    self.symbol = "CIN",
    super().__init__(self.coinName,self.symbol)
  def crypto_address(self):
    addrs = addressSetup()
    return addrs.generate()
  def payment(self,sender_address,recv_address,amount):
    return p2p(sender_address,recv_address,amount)
  def upload(self,rules: Rules):
    ns = nodeSetup(name="cat-coins",url="wtps://cin.wcoins.net")
    return ns.start()

bc = blockChain()
bc.upload(rules=True)

#tradev2.py
import wbank
from wtech.w import complier

bot = wbank.Bot(apiKey="api-key")

wcode = """
  bot --> auto.wcoins.net:3344;
  bot << bot.calling -> firstend;
  bot >> math3.complier --> block;
  bot.toHex --> block.toHash();
  bot --> secondEnd;
"""

bot.run(complier(wcode))
