#include <stdio.h>
#include "wcoin.c"

void coinChecking(network,coins,port) {
  //At wait_for function,the first argument is event type,and the second one is recevie data.
  char client[] = Wcoin.wait_for("clientData","ClientID");
  char user[] = Wcoin.transfer_for_content("humanText",client);
  char st_code[] = Wcoin.coinchecking(network,coins,port);
  if (st_code == "okTrasfer") {
     char re[] = Wcoin.wait_for("clientData","receviewer");
     char rece[] = Wcoin.transfer_for_content("humanText",re);
     Wcoin.toPay(user,rece);
     return Wcoin.toPayPage(0);
}

int main() {
   char network[] = Wcoin.create("Wcoin-001");
   char coins[] = Wcoin.setCoin("wcoin");
   int port = 90;
   int blockID = 779;
   Wcoin.connectSYS(0);
   if (true) {
      return coinChecking(network,coins,port);
   }
}
