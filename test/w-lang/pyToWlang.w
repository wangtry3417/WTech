#include <stdio.h>
#include <string.h>
#include <object.h>
#include <cLangtoW.w>

set main() into mainStage();
set pyFunc() into fileStage();
set output(object) into fileStage()&&pyFunc();

func pyFunc() {
   set o of output()
}


func main() {
  
}
