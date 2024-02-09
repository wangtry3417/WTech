from wcoins.trading import Bot
from wcoins.trade import tradPrice


bot = Bot(
    name="",
    intents="trading"
    ).starter()
    
class WcoinPrice(tradPrice):
    def __init__(self):
        self.url = None
        super(WcoinPrice,self).__init__()
    def prinPrice(self):
        self.coins = "Wcoins"
        self.clientID = "Ws-101828"
        self.url = f"https://wcoin.wtech.net/data/{self.coins}/{clientID}"
        return self.url

bot.run(
   event=WcoinPrice().printPrice,
   need_re_prin=True
   )