<?php

// 定義網站的基本信息
$title = "泓財數字銀行 WBank";
$author = "WBank";
$keywords = "WBank,wcoins,泓財,數字銀行,hsbc";
$contact_email = "wangtry3417@gmail.com";

// 定義模板內容
$content = <<<EOD
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="$author">
    <meta name="keywords" content="$keywords">
    <meta name="bot" content="index,follow">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$title</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef2f3;
            color: #333;
        }
        header {
            background: #007bff;
            color: #fff;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        nav {
            display: flex;
        }
        nav a {
            color: #fff;
            text-decoration: none;
            padding: 10px 15px;
            border-radius: 5px;
            margin-left: 10px;
            transition: background 0.3s;
        }
        nav a:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            animation: fadeIn 1s;
        }
        /* 其他 CSS 代碼 */
    </style>
</head>
<body>

<header>
    <h1>$title</h1>
    <nav>
        <a href="#home">首頁</a>
        <a href="#about">關於</a>
        <a href="/wbank">登入</a>
    </nav>
</header>

<div class="container" id="home">
    <h2>關於我們</h2>
    <p>泓財數字銀行 WBank 旗下有泓幣 wcoins。</p>
    
    <div class="feature">
        <img src="https://cdn-icons-png.flaticon.com/512/888/888871.png" alt="QR Payment Icon">
        <div>
            <strong>QR Code 付款</strong>
            <p>2-3 秒內完成付款，快速便捷。</p>
        </div>
    </div>
    
    <a href="/wbank" class="btn-login">立即登入/開戶</a>
</div>

<footer>
    <p>&copy; 2024 泓財銀行 WBank. 版權所有.</p>
    <p>聯絡方式: $contact_email</p>
</footer>

<script>
    // 這裡可以添加更多的 JavaScript 代碼
</script>

</body>
</html>
EOD;

// 輸出內容
echo $content;

?>
