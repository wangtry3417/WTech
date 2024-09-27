from hashlib import sha256
from random import randint

def get_auth_code(clientID,clientSecret,redirectURL):
  pass

def get_client(username,pw):
  #客戶端ID
  clientID = [str(randint(10,30)),username]
  t1 = ",".join(clientID)
  hash_clientID = sha256(t1.encode()).hexdigest()
  #客戶端密鑰
  secret = [pw,str(random(20,30))]
  t2 = ",".join(secret)
  hash_secret = sha256(t2.encode()).hexdigest()
  return hash_clientID,hash_secret
