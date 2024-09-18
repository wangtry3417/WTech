"""
  pip install wnet
  pip installing...
"""

"""
  wnet init
  create wnet/main.py
  create wnet/static
  create wnet/views
  create wnet/app.w
"""

"""
  wnet install -w yes -s wtps://source.wtech.net/static/wtps.zip
  C:\\Users\Destop\wnet\install.exe installing wtps://source.wtech.net/static/wtps.zip...
  installing wtps.zip
  Unzip wtps.zip
  Place into C:\\Users\Destop\wnet\*
  Running 'cd C:\\Users\Destop\wnet'
  Running file 'create_server.py'
  Done.
"""

#create_server.py
from wnet.https import App
from wnet.ssl import SSL

app = App(ssl=SSL(cer_key="key"))

def route1(req,res):
  return res.send("Hi")

app.route("/",route1)

app.run()
