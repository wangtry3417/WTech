const { WPay, Payment, Session } = require("wpay.js");

const wpay = new WPay()
                .apiKey="key"
                .scope="wbank/card-payment";
const session = new Session();
session.add("user", "wbank-username")
session.add("pw", "login-password")

wpay.on("ready", ()=> {
  wpay.emit("loginWbank");
});
wpay.on("loginWbank", ()=> {
  wpay.request(url="wbank/internal-login", formData={ user: session.select("user"), pw: session.select("pw") }, csrfToken="wpay/wbank-csrf-token")
  // 請求過後，客戶端與WBank server有紀錄
  wpay.emit("paymentCreate");
});
wpay.on("paymentCreate", ()=> {
  let pm = Payment(wpay, {
      cardNumber: "xxxxx",
      password: "xxxxx",
      accessKey: wpay.apiKey,
      reviewer: "benchan",
      amount: 1000,
      currency: "HKD"
    });
  wpay.redirect("wbank/cardPayment",method="PATCH",pm);
  wpay.closeConnect();
  session.clear();
});

wpay.startListen();