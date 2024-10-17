from trydb import DB

db = DB(database="./database.tb")

class User(db.Model):
  __tablename__ = "users"
  def __init__(self,username,email,pw):
    self.username = username
    self.email = email
    self.pw = pw

# Add record
"""
  If TryDB command:
  Insert <table.name> -> field1,field2... -> "value1","value2"...;
"""
user1 = User(username="Ben",email="ben@gmail.com",pw="1234")
user1.session.add(user1)
user1.session.commit()

users = User.query.filter_by(username="Ben").find_first()
print(users.username)

# Complier command
query1 = db.session.addCode("""
  using <table> , select field -> where <condition>;
""")
db.session.commit()
print(query.toResult())
