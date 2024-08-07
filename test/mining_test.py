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

#buyIn(exchange_info : str,amount : float)
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
