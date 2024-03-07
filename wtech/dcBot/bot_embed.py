from discord import Embed

def embed(*, colour=None, color=None, title=None, type='rich', url=None, description=None, timestamp=None):
  e = Embed(colour=colour,color=color,title=title,type=type,url=url,description=description,timestamp=timeslap)
  return e
