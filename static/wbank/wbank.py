"""
 pip install wlang wlang-ext --upgrade
 ...Done!.
 wlang init && wlang-ext add -s wlang install wbank-ext
"""

from wbank import Controller
from wbank_ext import type
from json_ext import loads

app = Controller(apiKey="Key")
app._set -> type._scropes -> ["AllActions"]

@app.on -> type._create_payment
def create_payment(bot):
  result = app._request -> (app._fetch_first_user(),"ben",4000)
  return loads(result.toJson())["success"]

app.run()
