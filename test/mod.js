const { GameManager } = require("wplay.js");

const gm = new GameManager()
               .name="VM-mod"
               .gameName="GTL-1";
gm.setKey("F2")

gm.on("connect",(player,game)=> {
   game.emit("welcome","歡迎加入");
   game.ui.new(position="left-top", callback=uiBuilder);
});
const uiBuilder = (player,game,screen) => {
  screen.ui.add(inputType="text-button",fontColor=gm.color.rgb(255,255,255), fontValue="生命值不變",callback=lifeRemote);
  screen.ui.add(inputType="text-button",fontColor=gm.color.rgb(255,255,255), fontValue="等級上升500",callback=RPRemote)
};
const lifeRemote = (player,game) => {
  game.remote(player.life.setValue(100),forever=true);
};
const RPRemote = (player,game) => {
  game.remote(player.level.increaseValue(500),forever=false);
};
