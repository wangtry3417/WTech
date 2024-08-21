/*
  事前下載定React及相關庫
  npm install react react-dom
*/

import React from 'react';
import ReactDOM from 'react-dom/client';

const comOne = () => {
  return (
     <div>
      <h1>Hello</h1>
    </div>
    );
};

const welcomeScreen = (props) => {
  return (
      <div>
      <h1>Hello {props.name}!</h1>
      <p>Welcome</p>
     </div>
    );
};

const comTwo = () => {
  return (
      <div>
      <welcomeScreen name="Ben"></welcomeScreen>
     </div>
    );
};

//root指 在html文檔中找出div id的值
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<comOne />);
const welcome = ReactDOM.createRoot(document.getElementById('weclomePlace'));
welcome.render(<comTwo />);
