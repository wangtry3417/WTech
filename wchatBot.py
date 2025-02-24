import socketio, os
from google import genai

# 創建 SocketIO 客戶端
sio = socketio.Client()
client = genai.Client(api_key=os.envion.get("gkey"))

# 當連接成功時的回調函數
@sio.event
def connect():
    print("Connected to the server")
    sio.emit('joinChat', { "username": "funGPT", "room_number": "wbank客服" });

# 當接收到 'chatMessage' 事件時的回調函數
@sio.on('chatMessage')
def on_chat_message(data):
    if data["type"] == "text":
        if data["text"] in "H" or data["text"] in "h" or data["text"] in "你好":
            sio.emit("chatMessage",{ "username": "funGPT", "type":"text", "text":"您好，請問有什麼可以幫忙？", "room_number": "wbank客服" });
        else:
            response = client.models.generate_content(
               model='gemini-2.0-flash', 
               contents=str(data["text"])
             )
            sio.emit("chatMessage",{ "username": "funGPT", "type":"text", "text":response.text, "room_number": "wbank客服" });

# 當斷開連接時的回調函數
@sio.event
def disconnect():
    print("Disconnected from the server")
    sio.emit('leaveChat', { "username": "funGPT", "room_number": "wbank客服" });

def run_model():
  # 連接到 Socket.IO 伺服器
  sio.connect('https://sites.wtechhk.xyz')

  # 保持程序運行以接收消息
  sio.wait()