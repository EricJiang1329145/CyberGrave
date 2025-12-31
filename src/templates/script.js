document.addEventListener('DOMContentLoaded', function() {
    const candle = document.getElementById('candle');
    const candleBtn = document.getElementById('candle-btn');
    const candleCount = document.getElementById('candle-count');
    const messageForm = document.getElementById('submit-message');
    const messageName = document.getElementById('message-name');
    const messageContent = document.getElementById('message-content');
    const messageList = document.getElementById('message-list');
    const musicToggle = document.getElementById('music-toggle');
    const bgMusic = document.getElementById('bg-music');

    let candleLit = false;
    let candleCountValue = parseInt(localStorage.getItem('candleCount') || '0');
    candleCount.textContent = candleCountValue;

    if (candleBtn) {
        candleBtn.addEventListener('click', function() {
            if (!candleLit) {
                candle.classList.add('lit');
                candleBtn.textContent = '熄灭烛光';
                candleLit = true;
                candleCountValue++;
                candleCount.textContent = candleCountValue;
                localStorage.setItem('candleCount', candleCountValue.toString());
            } else {
                candle.classList.remove('lit');
                candleBtn.textContent = '点亮烛光';
                candleLit = false;
            }
        });
    }

    if (messageForm) {
        messageForm.addEventListener('click', function(e) {
            e.preventDefault();

            const name = messageName.value.trim();
            const content = messageContent.value.trim();

            if (!name || !content) {
                alert('请填写姓名和留言内容');
                return;
            }

            const message = {
                name: name,
                content: content,
                time: new Date().toLocaleString('zh-CN')
            };

            let messages = JSON.parse(localStorage.getItem('messages') || '[]');
            messages.push(message);
            localStorage.setItem('messages', JSON.stringify(messages));

            displayMessage(message);

            messageName.value = '';
            messageContent.value = '';
        });
    }

    function displayMessage(message) {
        const messageItem = document.createElement('div');
        messageItem.className = 'message-item';
        messageItem.innerHTML = `
            <div class="message-name">${escapeHtml(message.name)}</div>
            <div class="message-content">${escapeHtml(message.content)}</div>
            <div class="message-time">${message.time}</div>
        `;
        messageList.appendChild(messageItem);
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function loadMessages() {
        const messages = JSON.parse(localStorage.getItem('messages') || '[]');
        messages.forEach(displayMessage);
    }

    loadMessages();

    if (musicToggle && bgMusic) {
        let musicPlaying = false;

        musicToggle.addEventListener('click', function() {
            if (musicPlaying) {
                bgMusic.pause();
                musicToggle.textContent = '🎵';
                musicPlaying = false;
            } else {
                bgMusic.play().catch(function(error) {
                    console.log('音乐播放失败:', error);
                    alert('无法播放音乐，请检查音频文件');
                });
                musicToggle.textContent = '⏸️';
                musicPlaying = true;
            }
        });
    }
});
