#include <stdio.h>
#include <ui.w>
#include <ui.h>
#include <file.w>
#include <file.h>

set fm of File.Manager();
set screen of UI.Screen();
set RGB of screen.color;

func main() {
  set template of screen.simpleUI("""
   \H VM Mod \H \n
   \h This is Roblox Mod in w-lang \h \n
    \p -------- \p
    \n
    \*content*\
  """);
   screen.list(template.content,listOne=screen.list.add(text="High-Jump",color=RGB(255,255,255),callback=Jump()));
};

func Jump(screen,player) {
  player.jumpTo(0,player.height+1,0);
}
