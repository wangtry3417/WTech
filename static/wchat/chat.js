const socket = io();
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
            //message.classList.add('message', data.type);
            message.classList.add('message');

            // 根據消息來源設置類別
            if (data.username === username) {
                message.classList.add('sent'); // 自己的消息
            } else {
                message.classList.add('received'); // 對方的消息
            }
            const timestamp = new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            if (data.type === 'text') {
                message.innerHTML = `<div class="username">${data.username}</div><div class="chat-text">${data.text}</div><div class="timestamp">${timestamp}</div>`;
            } else if (data.type === 'image') {
                message.innerHTML = `<div class="username">${data.username}</div><img src="${data.imageUrl}" alt="image" style="max-width: 100%; border-radius: 8px;"><div class="timestamp">${timestamp}</div>`;
            }

            return message;
        };

        sendButton.addEventListener('click', () => {
            const message = messageInput.value;
            if (message) {
                const messageData = { username:username, text: message, room_number: room, type: "text", timestamp: Date.now() };
                socket.emit('chatMessage', messageData);
                chatMessages.appendChild(createMessageElement(messageData));
                saveChatHistory(messageData); // 儲存聊天歷史
                messageInput.value = '';
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        });

        socket.on('chatMessage', (data) => {
            const messageData = { username:data.username, text: data.text, type: data.type, timestamp: data.timestamp}; // 根據類型設置
            if (data.username !== username) {
              chatMessages.appendChild(createMessageElement(messageData));
              saveChatHistory(messageData); // 儲存聊天歷史
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