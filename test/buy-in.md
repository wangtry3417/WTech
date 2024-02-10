
# 泓幣自動程式交易

第一步：下載pip3
```
 pkg install wcoins-wtech
```
第二步：setUp bot
``` python
  bot = Bot(
    name="",
    intents="trading"
    ).starter()
```

``` python
@bot.event(event_type="create_order")
async def create(complier : bot.Compliter):
    price = 2300
    coins = "Wcoins"
    wcoin_trader = comhex(price=price,coin_name=coins,using_crypto="hash-function")
    await complier.complex(wcoin_trader)
```
