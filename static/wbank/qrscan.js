let html5QrCode;
let scanning = false;
let username = sessionStage.getItem("username");
function scan() {
    document.getElementById('qrScanner').style.display = 'flex'; // 顯示掃描框
    startScanning(); // 自動開始掃描
}

function closeScanner() {
    stopScanning(); // 停止掃描
    document.getElementById('qrScanner').style.display = 'none'; // 隱藏掃描框
}

function startScanning() {
    if (scanning) return; // 防止重複啟動掃描器

    html5QrCode = new Html5Qrcode("qr-reader");

    html5QrCode.start(
        { facingMode: "environment" }, // 使用後置相機
        {
            fps: 10, // 每秒幀數
            qrbox: 250 // 掃描框大小
        },
        (decodedText, decodedResult) => {
            // 當掃描到 QR 碼時的處理
            window.location.href="/wbank/v1/paycode?reviewer=" + "{{user}}" + "&code=" + decodedText;
            stopScanning(); // 停止掃描
        },
        (errorMessage) => {
            // 掃描失敗的處理
            console.warn(`掃描失敗: ${errorMessage}`);
        }
    ).catch(err => {
        console.error(`啟動掃描器失敗: ${err}`);
    });

    scanning = true; // 標記為正在掃描
}

function stopScanning() {
    if (html5QrCode) {
        html5QrCode.stop().then(ignore => {
            scanning = false; // 標記為不在掃描
        }).catch(err => {
            console.error(`停止掃描器失敗: ${err}`);
        });
    }
}
