const { GameManager } = require("wplay.js");

const gm = new GameManager()
               .name="VM-mod"
               .gameName="GTL-1";

gm.on("connect",(player,game)=> {
   game.emit("welcome","歡迎加入");
   game.ui.new(position="left-top", callback=uiBuilder);
});
const uiBuilder = (player,game,screen) => {
  ui.add(inputType="text-button",fontColor=gm.color.rgb(255,255,255), fontValue="生命值不變",callback=null);
  ui.add(inputType="text-button",fontColor=gm.color.rgb(255,255,255), fontValue="選單2",callback=null)
};
const lifeRemote = (player,game) => {
  game.remote(player.life.setValue(100),forever=true);
};
