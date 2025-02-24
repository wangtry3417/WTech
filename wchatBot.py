import socketio

# 創建 SocketIO 客戶端
sio = socketio.Client()

# 當連接成功時的回調函數
@sio.event
def connect():
    print("Connected to the server")

# 當接收到 'chatMessage' 事件時的回調函數
@sio.on('chatMessage')
def on_chat_message(data):
    pass

# 當斷開連接時的回調函數
@sio.event
def disconnect():
    print("Disconnected from the server")

# 連接到 Socket.IO 伺服器
sio.connect('https://sites.wtechhk.xyz')

# 保持程序運行以接收消息
sio.wait()