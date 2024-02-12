#include <stdio.h>
// head filer


set main() into mainStage;
set network(object) into fileStage;
set name into fileStage typeof string;
// set <function.name> into fileStage;

class network {
  __init__ (name,user,pw) {
      this.name = user;
      this.user = user;
      this.pw = pw;
 }
 func-cls pwDisplay (those) {
     if (those.user == "wt") {
        those.pw = 9009;
        return those.pw;
   }
}
}

func main() {
  prinConsole("Hello World!");
  name = "wt";
  set net of network(object,name=None,user=name,pw=None).pwPisplay();
  return toString(net);
}

/*
  result:
  9009
*/
