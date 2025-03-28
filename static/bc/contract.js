// contract.js
class Contract {
    constructor(user, reviewer, amount) {
        this.user = user;
        this.reviewer = reviewer;
        this.amount = amount;
        this.loadingElement = null;
        this.initStyles(); // 初始化樣式
        this.setupUI(); // 設置 UI
    }

    initStyles() {
        const style = document.createElement('style');
        style.innerHTML = `
            body {
                font-family: Arial, sans-serif;
                background-color: white;
                text-align: center;
            }
            #modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgba(0, 0, 0, 0.5);
            }
            #modalContent {
                background-color: white;
                margin: 15% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 400px;
                text-align: left;
                border-radius: 8px;
            }
            #loading {
                display: none;
                font-size: 16px;
                color: #61dafb;
            }
            #authorizeButton {
                background-color: #61dafb;
                color: black;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                margin-right: 10px;
            }
            #cancelButton {
                background-color: white;
                color: red;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }
        `;
        document.head.appendChild(style);
    }

    setupUI() {
        this.createModal(); // 創建模態框
        this.showModal(); // 顯示模態框
        this.createButtons(); // 創建按鈕
    }

    createModal() {
        const modal = document.createElement('div');
        modal.id = 'modal';
        modal.innerHTML = `
            <div id="modalContent">
                <h1>Transaction Details</h1>
                <p>User: <span id="user">${this.user}</span></p>
                <p>Reviewer: <span id="reviewer">${this.reviewer}</span></p>
                <p>Amount: <span id="amount">${this.amount}</span></p>
                <p id="loading">Loading...</p>
            </div>
        `;
        document.body.appendChild(modal);
    }

    showModal() {
        document.getElementById('modal').style.display = 'block';
    }

    hideModal() {
        document.getElementById('modal').style.display = 'none';
    }

    createButtons() {
        const buttonContainer = document.createElement('div');
        buttonContainer.innerHTML = `
            <button id="authorizeButton" onclick="processPayment()">Authorize Payment</button>
            <button id="cancelButton" onclick="cancelPayment()">Cancel</button>
        `;
        document.getElementById('modalContent').appendChild(buttonContainer);
    }

    async reqPayment() {
        const response = await fetch('https://sites.wtechhk.xyz/wbank/hash/transfer', {
            method: 'GET',
            headers: {
                'username': this.user,
                'reviewer': this.reviewer,
                'amount': this.amount,
            }
        });
        try {
        let res = await response.json();
        #return res.success ? res.success : res["Error-hint"];
        if (res.success) {
            const sha256Code = res.code;
            const contractAddress = this.convertToAddress(sha256Code);
            return contractAddress;
        } else {
            return res["Error-hint"];
        }
        } catch(err) {
            console.error(err);
            return null;
        }
    }

    convertToAddress(code) {
      // 取前 40 個字符以符合以太坊地址長度
      return '0x' + code.slice(0, 40);
    }

    showLoading() {
        this.loadingElement = document.getElementById('loading');
        this.loadingElement.style.display = 'block';
    }

    hideLoading() {
        if (this.loadingElement) {
            this.loadingElement.style.display = 'none';
        }
    }

    async processPayment() {
        this.showLoading();
        const statement = await this.reqPayment();
        this.hideLoading();
        this.hideModal();
        return statement;
    }

    static init(user, reviewer, amount) {
        return new Contract(user, reviewer, amount);
    }
}

// 將 Contract 類暴露給全局對象
window.Contract = Contract;
