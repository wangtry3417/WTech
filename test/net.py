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

#app.w
#include <stdio.h>
#include <wnet.w>

set wnet of WNet() into fileStage;
set ssl of wnet.ssl.SSL(object) into fileStage;
set app of wnet.https.app(object,ssl=ssl(object,key="key")) into fileStage;

func main() {
  app.route("/",route1)
  app.wait(1000);
  app.run();
}

func route1(req,res) {
  return res.send("Hello There!.");
}

#create_server.py
from wnet.https import App
from wnet.ssl import SSL

app = App(ssl=SSL(cer_key="key"))

def route1(req,res):
  return res.send("Hi")

app.route("/",route1)

app.run()
