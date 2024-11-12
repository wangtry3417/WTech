from wbank import Controller

app = Controller(apiKey="Key")
app._set_scropes = ["AllActions"]

result = app._request(target="transfer/hash",args={"username":app._refer_username,"reviewer":"ben","amount":"100"}).toRequest()
if result._status_code == 200:
  if result.toJson()["success"]:
    print("轉帳成功")
  else:
    print(result.toJson()["Error-hint"])
else:
  print("不行")
