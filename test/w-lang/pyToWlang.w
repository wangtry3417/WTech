#include <stdio.h>
#include <string.h>
#include <object.h>
#include <cLangtoW.w>

set main() into mainStage();
set pyFunc() into fileStage();
set output(object) into fileStage()&&pyFunc();

func pyFunc(prompt) {
   set o of output(object);
   o.print(those,name="pyFunc",prompt=prompt,None**);
}


func main() {
  if (prinConsole(None).values(object):prefer(prm="print")) {
     return puFunc(prompt : toString(prinConsole(None).values(object):prefer(prm="print")));
  }
}
