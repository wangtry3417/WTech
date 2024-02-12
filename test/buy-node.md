泓幣(wcoins) 有兩大方式。
 - 1:平台購入
 - 2:API Auto-buy-in
   
1:平台購入 ：
用戶可以透過W Coins官網或crypto transfer購入W Coins.同時，亦可透過Robux購買泓幣。

2:
以下將有教學。


# -------------
# 泓幣自動程式交易

第一步：下載wcoins.js
```
 npm i wcoin-wtech
```
第二步：setUp bot
``` node
  const { Bot,Trader,Intents } = require("wcoin.js");

  const trader = new Trader();
  const bot = new Bot()
              .name=""
              .intents=Intents.TRADING;
```
第三步：建立賬單
``` node
  bot.on("create-order", async (complier) => {
     const trade = trader.createOrder("user","user",200);
  await complier.tradOrder(trade.toHash());
});
```
第四步：付款交易
``` node
  bot.on("payment", async (complier) => {
     const trade = trader.createOrder("user","user",200);
  const payment = trader.payment = "card";
  await complier.trade(trade.toHash(),payment).toPay();
});
```
第五步：運行交易機器人
``` node
  bot.run();
```

# ----------
# 泓幣的起源地
泓幣（W Coins）由泓技WTech開創。
