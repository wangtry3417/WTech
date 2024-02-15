from tkinter import tk,Button

class Window:
  def __init__(self,title):
    self.window = Tk()
    self.window.title = title
  def show(self):
    self.window.mainloop()
  def create_btn(self,text,callback):
    button = Button(self.window,text=text,command,callback)
    button.pack()
    
