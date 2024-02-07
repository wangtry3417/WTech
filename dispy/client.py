import discord


class Client:
  def __init__(self,intents):
    self.intents = intents
    self.client = None
    self.client = discord.Client(intents=self.intents)
    try:
      return run(self)
    except Exception as e:
      print(str(e))
  def run(self,token : str):
    self.client.run(token)
