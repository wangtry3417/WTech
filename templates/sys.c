#include <stdio.h>
#include "wcoin.c"

int main() {
   char network[] = Wcoin.create("Wcoin-001");
   char coins[] = Wcoin.setCoin("wcoin");
   int port = 90;
   int blockID = 779;
   Wcoin.connectSYS(0);
}
