from wcoins.trading import Buy,Sell
from wcoins import Exchange,data

exchange = Exchange({
  "name":"wbank",
  "apiKey":"key"
})

exchange.action(Buy(amount=10000,type="leverage"))

if exchange.market.price == 200000:
  exchange.action(Sell(amount=2000,type="markets"))
