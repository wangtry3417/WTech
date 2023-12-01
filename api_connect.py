from cryptography.fernet import Fernet
import time
import requests as req

f = open("key.key","rb")
key = f.read()


class Intents:
  def __init__(self):
    self.intents = False
  def shop(self):
    self.intents = True

class WTech:
  def __init__(self,intents : Intents):
    self.intents = intents
  def connect(self,api_key):
    fernet = Fernet(key)
    # 解密结果
    decrypted_data = fernet.decrypt(api_key)

    # 将解密后的字符串转换为列表
    original_list = eval(decrypted_data.decode())

    # 打印解密后的列表
    print("[Client] : Connect to WTech API")
    time.sleep(2)
    res = req.get(url="https://gateway.wangtry3417.repl.co/wtech/api/connect")
    print("[res] : connect to {}".format(original_list[0]))
    t = 30000
    time.sleep(t)
    return False
  def checkList(self,data,number):
    fernet = Fernet(key)
    # 解密结果
    decrypted_data = fernet.decrypt(data)

    # 将解密后的字符串转换为列表
    original_list = eval(decrypted_data.decode())

    # 打印解密后的列表
    print(original_list[number])
  def en(self,l):
    # 将列表转换为字符串
    list_string = str(l)

    # 创建 Fernet 加密器
    fernet = Fernet(key)

    # 加密字符串
    encrypted_data = fernet.encrypt(list_string.encode())

    # 打印加密后的结果
    print(encrypted_data.decode())
