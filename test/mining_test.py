from wcoins.mining import make_block,sha256,complie
from wcoins.crypto import check_address
from wcoins.time import nowTimes

wallet_address = "d08f40525e098fb04d29b0d65657cdbffaa64cbe9ca28b8b1355184bf69b03da"

def making_block(forward_block,timeslamp):
  return make_block(sha256(wallet_address)*888,forward_block,timeslamp)

def start_mining():
  if check_address(wallet_address):
    formula = complie(formula=f"{make_block(sha256(wallet_address)*897,nowTimes())+3*909}",path="/*",mode="fast")
    print(making_block(formula.toHex(),nowTimes()))
  else:
    print("Wallet invaild")

start_mining()
