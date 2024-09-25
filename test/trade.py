from wcoins.trading import Buy,Sell
from wcoins import Exchange,data

exchange = Exchange({
  "name":"wbank",
  "apiKey":"key"
})

exchange.action(Buy(amount=10000,type="leverage"))

if exchange.market.price == 200000:
  exchange.action(Sell(amount=2000,type="markets"))

# 要下載泓式語法
# pip install wlang-ext wlang
# wlang init && wlang start-detect

from wcoins.trading import Buy,Sell
from wcoins import Exchange,data

exchange = Exchange({
  "name":"wbank",
  "apiKey":"key"
})

exchange.action(exchange.Action -> type.buy -> Buy(amount=10000,type="leverage"))
