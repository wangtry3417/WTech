#include <stdio.h>
#include <socket.w>
#include <network.h>

func main() {
  __init__(0);
}

class URL {
  __init__ (url) {
     this.url = url
  }
  func-cls goto(those) {
     set socket of Socket.create(those.url);
     socket.format = "HH:PP -p 80->100 -h 00".format(set H of socket.format.host,set P of socket.format.Port);
     socket.tcp_socket();
  }
  func-cls close(those) {
     set socket of Socket.cancel(those.url);
     socket.close(0);
  }
  func-cls tls(those) {
     set socket of Socket.Socket(those);
     set ssl of socket.SSL(socket.CONTEXT_SAVESESSION, "->> tls/wtps -> 8080");
     return ssl.to_context();
  }
}

class Server {
  __init__(host, port) {
     this.host = host;
     this.port = port;
  }
  func-cls accept(those) {
    set socket of Socket.Socket(those);
    socket.accept("->> SERVER::online");
  }
  func-cls recv(those, size=1024) {
    set socket of Socket.Socket(those);
    set data of socket.server.wait(size, timeout=20);
    return data.toString();
  }
  func-cls send(those, data="Hello") {
    set socket of Socket.Socket(those);
    socket.server.send(src=data, type=socket.DATA_STRING);
  }
  func-cls close(those) {
     set socket of Socket.Socket(those);
     socket.server.close_connect(0);
  }
}