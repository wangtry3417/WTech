// ==UserScript==
// @name         l2048遊戲外掛
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  自動玩 2048 遊戲
// @author       wtech
// @match        https://sites.wtechhk.xyz/wbank/game.html
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 檢查遊戲是否開始的間隔 (毫秒)
    const GAME_START_CHECK_INTERVAL = 1000;

    // 執行自動滑動的間隔 (毫秒)
    const AUTO_SLIDE_INTERVAL = 500;

    let gameStarted = false;
    let autoPlaying = false;

    // 檢查遊戲是否已經開始，如果開始則啟動自動遊玩
    function checkGameStart() {
        if (typeof initBoard === 'function' && typeof slide === 'function' && !gameStarted) {
            gameStarted = true;
            console.log('遊戲已開始，啟動自動遊玩...');
            setTimeout(autoPlay, AUTO_SLIDE_INTERVAL); // 延遲啟動自動遊玩，給遊戲初始化時間
        } else if (!gameStarted) {
            setTimeout(checkGameStart, GAME_START_CHECK_INTERVAL); // 繼續檢查遊戲是否開始
        }
    }

    // 評估滑動方向並選擇最佳方向
    function getBestMove() {
        let bestMove = null;
        let maxScore = -1; // 初始最高分數

        const directions = ['up', 'down', 'left', 'right'];

        for (const direction of directions) {
            // 模擬滑動並計算得分
            let currentScore = evaluateMove(direction);
            if (currentScore > maxScore) {
                maxScore = currentScore;
                bestMove = direction;
            }
        }
        return bestMove;
    }

    // 模擬滑動並評估得分 (這裡的評估方式可以更精細)
    function evaluateMove(direction) {
        let boardCopy = copyBoard(); // 複製當前棋盤
        let scoreBeforeMove = score; // 記錄移動前的分數
        slide(direction); // 執行滑動 (這裡會實際修改遊戲狀態)
        let scoreAfterMove = score; // 記錄移動後的分數
        restoreBoard(boardCopy); // 還原棋盤到滑動前的狀態
        score = scoreBeforeMove; // 還原分數到滑動前，因為只是模擬評估

        // 簡單評估：合併的數值總和 + 移動後空格數量
        let moveScore = scoreAfterMove - scoreBeforeMove; // 合併數值增加的分數
        let emptyCells = countEmptyCells(); // 移動後空格數量
        return moveScore + emptyCells; // 總評分，數值越高越好
    }

    // 複製當前棋盤狀態
    function copyBoard() {
        return board.map(row => [...row]); // 使用 map 複製二維陣列
    }

    // 還原棋盤狀態
    function restoreBoard(oldBoard) {
        board = oldBoard.map(row => [...row]); // 使用 map 複製回二維陣列
        renderBoard(); // 重新渲染棋盤以反映還原的狀態
    }

    // 計算棋盤上的空格數量
    function countEmptyCells() {
        let count = 0;
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (board[i][j] === 0) {
                    count++;
                }
            }
        }
        return count;
    }

    // 自動遊玩的核心邏輯
    function autoPlay() {
        if (!gameStarted || checkGameOver()) {
            console.log('遊戲結束或尚未開始，停止自動遊玩。');
            autoPlaying = false;
            return; // 遊戲結束或未開始，停止自動遊玩
        }

        autoPlaying = true;
        const bestMoveDirection = getBestMove();

        if (bestMoveDirection) {
            console.log('自動滑動方向:', bestMoveDirection);
            slide(bestMoveDirection); // 執行最佳滑動方向
        } else {
            console.log('沒有可行的移動方向，隨機選擇一個方向。');
            const directions = ['up', 'down', 'left', 'right'];
            const randomDirection = directions[Math.floor(Math.random() * directions.length)];
            slide(randomDirection); // 隨機滑動
        }

        if (!checkGameOver()) {
            setTimeout(autoPlay, AUTO_SLIDE_INTERVAL); // 循環執行自動遊玩
        } else {
            console.log('遊戲結束，自動遊玩停止。');
            autoPlaying = false;
        }
    }


    // 啟動 userscript 時開始檢查遊戲是否開始
    checkGameStart();

})();