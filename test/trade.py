from wcoins.trading import Buy,Sell
from wcoins import Exchange,data

exchange = Exchange({
  "name":"wbank",
  "apiKey":"key"
})

exchange.action(Buy(amount=100,type="markets"))

exchange._startTrade()
