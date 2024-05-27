from .http import *
import socket

class network(object):
  def __init__(self,hostname,port):
    self.socketOnj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.hostname = "0.0.0.0"
    self.port = port
    self.username = None
    self.password = None
  def run(self,host=self.hostname,port : int):
    self.socketOnj.bind((self.hostname,port))
    self.socketOnj.listen(5)
    while True:
      cs,address = self.socketOnj.accept()
      with open("userIP.txt","a+") as fp:
        fp.write(f"New client IP : {address}")
        print("Connected")
  def send_data(self,things : str):
    self.socketOnj.send(things.encode())
    print("Sent!")
  def disconnect(self):
    self.socketOnj.close()
