
def chat(p):
  res = {
    "Hello" : "Hi!That's a good day",
    "Hi" : "Hi!That's a good day",
    "Who are you?" : "I am making by W Tech API",
    "Who are you" : "I am making by W Tech API",
    
  }
  for q , a in res.items():
    prompt = input(p)
    return prompt
    if prompt == q:
      return a
    else:
      print("Error for chat")
    

def start_in(user_prompt):
  return chat(user_prompt)

def login(token):
  if len(token) == 84 and type(token) == str:
    return start_in()
  else:
    print("token wrong")
    
