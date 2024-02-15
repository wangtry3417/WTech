from requests import *

def get_web_text(url,form_data=None,json_type_data=None):
  res = get(url=url,json=json_type_data,data=form_data)
  return res.text

def get_web_for_json(url,form_data=None,json_type_data=None):
  res = get(url=url,json=json_type_data,data=form_data).json()
  try:
    return res
  except:
    return "Error: Cannot read the url json data!"
