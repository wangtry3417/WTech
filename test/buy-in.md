# 如何購入泓幣？
購入泓幣(wcoins) 有兩大方式。
 - 1:平台購入
 - 2:API Auto-buy-in
   
1:平台購入 ：
用戶可以透過W Coins官網或crypto transfer購入W Coins.同時，亦可透過Robux購買泓幣。

2:
以下將有教學。


# -------------
# 泓幣自動程式交易

第一步：下載wcoins.py
```
 pip install wcoins-wtech
```
第二步：setUp bot
``` python
  bot = Bot(
    name="",
    intents="trading"
    ).starter()
```
第三步：建立賬單
``` python
@bot.event(event_type="create_order")
async def create(complier : bot.Compliter):
    price = 2300
    coins = "Wcoins"
    wcoin_trader = comhex(price=price,coin_name=coins,using_crypto="hash-function")
    await complier.complex(wcoin_trader)
```
第四步：付款交易
``` python
@bot.event(event_type="trading")
async def trade(complier : bot.hashTrade):
    hash = ""
    #payment_method :
    #["card","crypto","paypal","wpay"]
    payment = payment_method[0]
    wcoin_trader = hashTrade(hash).toPay(payment)
    await complier.hashPay(wcoin_trader)
```
第五步：運行交易機器人
``` python
  bot.run()
```

# ----------
# 泓幣的起源地
泓幣（W Coins）由泓技WTech開創。
