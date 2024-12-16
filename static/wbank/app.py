"""
pip install freeapp wlang
"""
"""
wlang --upgrade
freeapp init
create app.py
create app.pyc
"""
from freeapp import View
from freeapp.views import Text,Button

class myAppView(View):
    __appname__ = "wbank"
    type.templatesURL -> "https://tps.wtech.net/wbank?id=109192s"
    type.automode -> True
    
app = myAppView()
app.wait()

"""
freeapp -upload app.py -> app.pkg
"""

# IOS (need xcode)
"""
freeapp -type ios -target app.pkg
loading...
change app.pkg to complie *.swift ...
---->-----
--------->
Done!.
"""
# Android (need JDK&ADK)
"""
freeapp -mode JDK&ADK -target true
freeapp -type apk -target app.pkg
loading...
change app.pkg to app.aab
complie your app file
---->------
---------->
building process
--->------------
--------->------
complie and change to .dex
------------->--
--------------->
Done!.
"""