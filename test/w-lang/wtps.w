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
     socket.tcp_socket();
  }
  func-cls close(those) {
     set socket of Socket.cancel(those.url);
     socket.close(0);
  }
}
