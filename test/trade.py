from wcoins.trading import Buy,Sell
from wcoins import Exchange,data

exchange = Exchange({
  "name":"wbank",
  "apiKey":"key"
})

exchange.action(Buy(amount=30,type="markets"))

for d in data:
  print(d["open"])
  print(d["close"])
  print(d["high"])
