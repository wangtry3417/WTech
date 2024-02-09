from wcoins.trading import Bot
from wcoins.trade import trading,comhex,payment_method


bot = Bot(
    name="",
    intents="trading"
    ).starter()
    
@bot.event(event_type="create_order")
async def create(complier : bot.Compliter):
    price = 2300
    coins = "Wcoins"
    wcoin_trader = comhex(price=price,coin_name=coins,using_crypto="hash-function")
    await complier.complex(wcoin_trader)
    
@bot.event(event_type="trading")
async def trade(complier : bot.hashTrade):
    hash = ""
    #payment_method :
    #["card","crypto","paypal","wpay"]
    payment = payment_method[0]
    wcoin_trader = hashTrade(hash).toPay(payment)
    await complier.hashPay(wcoin_trader)
    
bot.run()
