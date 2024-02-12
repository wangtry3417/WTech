from requests import *
from wtech.jumpWeb.autoMode import goto,thingsTransfer

url = "https://wcoins.wtech.net"

class wcoins:
  def __init__(self):
    self.network = "WC-01929"
    self.port = 9088
    self.user = "root"
    self.pw = "Wt392928@)m2ksm28"
    self.secret = None
  def get_secret(self):
    if self.user == "root":
      res = get(url=f"{url}/api/get_secret",auth=("wtech001",9087)).json()
      secret = res["save-password"]
      real_secret = secret[1]
      return real_secret
    else:
      return False
  def startTrade(self):
    res = get(url="https://wc0001.wcoins.net:8888").json()
    for re in res:
      price = re[1]
      math1 = get(url="https://ai.wtech.net/api/v1/wcoins?query=math",data={"price" : price).json()
      if math1["ans"] > 10:
        return goto("wtps://wcoin.wtech.net","wtps",9087)
      else:
        return thingsTransfer("wtps://wcoin.wtech.net","wtps",9088",data={"complie_data":math1["ans"]})
