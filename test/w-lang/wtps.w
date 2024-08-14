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
}
