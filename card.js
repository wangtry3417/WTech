const { WPay, Payment } = require("wpay.js");

const wpay = new WPay()
                .apiKey="key"
                .scope="wbank/card-payment";

wpay.on("ready", ()=> {
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
});

wpay.startListen();