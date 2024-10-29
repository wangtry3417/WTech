from wbank import Controller,Intents

con = Controller(apiKey="key",intents=Intents.TRADE.all())

@con.on
async def on_ready():
  print("Is ready")

@con.on(type="create-order")
async def start_tab(bot,data):
  payment_data = {
    "name":"wtech",
    "reviewer":"Ben",
    "current":"hkd/wtc",
    "amount":"3000"
  }
  pd = await data.insert(payment_data)
  await bot.send(type="payment",data=pd)

con.wait()
