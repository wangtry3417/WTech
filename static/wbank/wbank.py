from web4 import Provider

provider = Provider(url="https://gateway.wbank.net:5678")
con = provider.connection()

@provider.on("connect")
def on_handle_connect(conn,msg):
 if msg["status"] == "ok":
  conn.emit("connected",{"payer":"Ben"})

if con.recv(255).toString() == "payer::Ben,reviewer::bangjin,amount::400;":
 con.post(data=con.recv(255).toString(),havePage=True).render()
