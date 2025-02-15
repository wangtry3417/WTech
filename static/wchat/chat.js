let socket = io();
        const usernameInput = document.getElementById('username-input');
        const submitUsernameButton = document.getElementById('submit-username');
        const activeChannels = document.getElementById('active-channels');
        const channelListItems = document.getElementById('channel-list-items');
        const chatMessages = document.getElementById('chat-messages');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const chatContainer = document.getElementById('chat-container');
        const exitButton = document.getElementById('exit-button');
        const timeDisplayList = document.getElementById('timeList');

        let username = null;
        let room = null;

        //add time function
        function updateTime() {
            const options = { 
                year: 'numeric', month: '2-digit', day: '2-digit',
                hour: '2-digit', minute: '2-digit', second: '2-digit',
                hour12: false 
            };
            timeDisplayList.textContent = new Date().toLocaleString('zh-TW', options);
        }
        setInterval(updateTime, 1000);
        updateTime();

        const loadChatHistory = () => {
            const messages = JSON.parse(sessionStorage.getItem('chatMessages')) || [];
            messages.forEach(data => {
                const message = createMessageElement(data);
                chatMessages.appendChild(message);
            });
            chatMessages.scrollTop = chatMessages.scrollHeight;
        };

        const saveChatHistory = (messageData) => {
            const messages = JSON.parse(sessionStorage.getItem('chatMessages')) || [];
            messages.push(messageData);
            sessionStorage.setItem('chatMessages', JSON.stringify(messages));
        };

        submitUsernameButton.addEventListener('click', () => {
            username = usernameInput.value;
            if (!username) {
                alert("請輸入用戶名");
                return;
            }
            usernameInput.style.display = 'none';
            activeChannels.style.display = 'block';
            loadActiveChannels();
        });
        const allChannels = {
    "morning": ["財經群組", "政府事務發洩區","wbank客服"], // 早上顯示的頻道
    "afternoon": ["邦金國際金融","wbank客服","金融經紀Ben","閒聊區"], // 下午顯示的頻道
    "evening": ["邦金國際金融", "世遊娛樂城", "VIP888荷官", "馬會出糧區","波友區","wbank客服"], // 晚上顯示的頻道
};

       const getCurrentTimeSlot = () => {
         let localDate = new Date(); // UTC+8或本地時間
         const hours = localDate.getHours();
         setInterval(()=>{
         let localDate = new Date();
         timeDisplayList.innerHTML = localDate.toLocaleString(); // 顯示目前時間
         },1000);
           
         if (hours >= 6 && hours < 12) {
            return "morning"; // 早上 6:00 - 11:59
         } else if (hours >= 12 && hours < 18) {
            return "afternoon"; // 下午 12:00 - 17:59
         } else {
            return "evening"; // 晚上 18:00 - 5:59
         }
    };

        const loadActiveChannels = () => {
            const timeSlot = getCurrentTimeSlot();
            const channels = allChannels[timeSlot];

            channelListItems.innerHTML = ''; // 清空現有的頻道
            channels.forEach(channel => {
                const channelItem = document.createElement('div');
                channelItem.classList.add('channel-item');
                channelItem.textContent = channel;
                channelItem.addEventListener('click', () => {
                    room = channel;
                    socket.emit('joinChat', { username, room_number: room });
                    chatContainer.style.display = 'flex';
                    loadChatHistory(); // 載入聊天歷史
                });
                channelListItems.appendChild(channelItem);
            });
            if (channels.length === 0) {
                activeChannels.style.display = 'none';
            }
        };

const createMessageElement = (data) => {
    const message = document.createElement('div');
    message.classList.add('message');

    if (data.username === username) {
        message.classList.add('sent');
    } else {
        message.classList.add('received');
    }
    const timestamp = new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    if (data.type === 'text') {
        message.innerHTML = `<div class="username">${data.username}</div><div class="chat-text">${data.text}</div><div class="timestamp">${timestamp}</div>`;
    } else if (data.type === 'image') {
        message.innerHTML = `<div class="username">${data.username}</div><img src="${data.imageData}" alt="image" style="max-width: 150px"><div class="timestamp">${timestamp}</div>`;
    }

    return message;
};

        // 圖片壓縮函式
const compressImage = (imageFile, maxWidth = 800) => {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(imageFile);
        reader.onload = (event) => {
            const img = new Image();
            img.src = event.target.result;
            img.onload = () => {
                let width = img.width;
                let height = img.height;

                if (width > maxWidth) {
                    height = Math.round((height * maxWidth) / width);
                    width = maxWidth;
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                const dataUrl = canvas.toDataURL(imageFile.type, 0.7); // 0.7 是壓縮品質，可以調整
                resolve(dataUrl);
            };
        };
        reader.onerror = (error) => {
            console.error("圖片讀取錯誤:", error);
            resolve(null); // 發生錯誤時解析為 null
        };
    });
};


sendButton.addEventListener('click', async () => { // sendButton 監聽器改為 async
    const message = messageInput.value;
    const imageUpload = document.getElementById("image-upload").files[0];
    let msgType = "text";

    if (imageUpload) {
        msgType = "image";

        // 顯示 "圖片發送中..." 訊息 (視覺回饋)
        const sendingMessageElement = document.createElement('div');
        sendingMessageElement.classList.add('message', 'sent', 'sending-message'); // 加入 'sending-message' 類別方便識別
        sendingMessageElement.innerHTML = `<div class="chat-text">圖片發送中...</div>`;
        chatMessages.appendChild(sendingMessageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // 確保訊息可見

        try {
            const compressedDataUrl = await compressImage(imageUpload); // 等待圖片壓縮完成

            if (compressedDataUrl) { // 檢查壓縮是否成功
                const msgData = { username: username, imageData: compressedDataUrl, room_number: room, type: msgType, timestamp: Date.now(), mimeType: imageUpload.type };
                socket.emit('chatMessage', msgData);
                chatMessages.appendChild(createMessageElement(msgData));
                document.getElementById("image-upload").value = '';
            } else {
                // 圖片壓縮失敗的處理 (例如顯示錯誤訊息)
                alert("圖片壓縮失敗，請稍後再試。");
            }
        } catch (error) {
            console.error("圖片處理錯誤:", error);
            alert("圖片處理錯誤，請稍後再試。"); // 錯誤處理，例如顯示 alert
        } finally {
            // 無論成功或失敗，都移除 "圖片發送中..." 訊息
            chatMessages.removeChild(sendingMessageElement); // 移除載入訊息
        }


    }

    if (message) {
        const messageData = { username: username, text: message, room_number: room, type: msgType, timestamp: Date.now() };
        socket.emit('chatMessage', messageData);
        chatMessages.appendChild(createMessageElement(messageData));
        saveChatHistory(messageData);
        messageInput.value = '';
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
});

socket.on('chatMessage', (data) => {
    let msgData = {};
    msgData = data.type === "image" ?
        { username: data.username, imageData: data.imageData, type: data.type, timestamp: data.timestamp, mimeType: data.mimeType } :
        { username: data.username, text: data.text, type: data.type, timestamp: data.timestamp };
    if (data.username !== username) {
        chatMessages.appendChild(createMessageElement(msgData));
        saveChatHistory(msgData);
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
});
        exitButton.addEventListener('click', () => {
            socket.emit('leaveChat', { username, room_number: room });
            chatMessages.innerHTML = '';
            sessionStorage.removeItem('chatMessages'); // 清除訊息
            chatContainer.style.display = 'none';
            usernameInput.style.display = 'block';
            activeChannels.style.display = 'none';
        });