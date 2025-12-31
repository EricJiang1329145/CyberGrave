document.addEventListener('DOMContentLoaded', function() {
    const candleBtn = document.getElementById('candle-btn');
    const candleCount = document.getElementById('candle-count');
    const candleList = document.getElementById('candle-list');
    const candle = document.getElementById('candle');
    const musicToggle = document.getElementById('music-toggle');
    const bgMusic = document.getElementById('bg-music');

    // 加载蜡烛数量和列表
    loadCandles();

    // 点蜡烛按钮点击事件
    candleBtn.addEventListener('click', function() {
        const name = prompt('请输入您的姓名（可选）', '匿名');
        if (name !== null) {
            const message = prompt('请输入您的留言（可选）', '');
            if (message !== null) {
                lightCandle(name, message);
            }
        }
    });

    // 音乐开关
    musicToggle.addEventListener('click', function() {
        if (bgMusic.paused) {
            bgMusic.play();
            musicToggle.textContent = '🔊';
        } else {
            bgMusic.pause();
            musicToggle.textContent = '🎵';
        }
    });

    // 加载蜡烛数据
    function loadCandles() {
        fetch('/api/candles')
            .then(response => response.json())
            .then(data => {
                displayCandles(data);
                updateCandleCount(data.length);
            })
            .catch(error => console.error('加载蜡烛失败:', error));
    }

    // 点蜡烛
    function lightCandle(name, message) {
        fetch('/api/candles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name || '匿名',
                message: message || ''
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 点蜡烛动画
                candle.classList.add('lighting');
                setTimeout(() => {
                    candle.classList.remove('lighting');
                }, 1000);
                
                // 重新加载蜡烛列表
                loadCandles();
                
                alert('蜡烛已点亮！');
            }
        })
        .catch(error => {
            console.error('点蜡烛失败:', error);
            alert('点蜡烛失败，请重试');
        });
    }

    // 更新蜡烛数量
    function updateCandleCount(count) {
        candleCount.textContent = count;
    }

    // 显示蜡烛列表
    function displayCandles(candles) {
        candleList.innerHTML = '';
        candles.forEach(candle => {
            const candleItem = document.createElement('div');
            candleItem.className = 'candle-item';
            candleItem.innerHTML = `
                <div class="candle-icon">🕯️</div>
                <div class="candle-info">
                    <div class="candle-name">${escapeHtml(candle.name)}</div>
                    ${candle.message ? `<div class="candle-message">${escapeHtml(candle.message)}</div>` : ''}
                    <div class="candle-time">${formatTime(candle.created_at)}</div>
                </div>
            `;
            candleList.appendChild(candleItem);
        });
    }

    // HTML转义
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // 格式化时间
    function formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) {
            return '刚刚';
        } else if (diff < 3600000) {
            return Math.floor(diff / 60000) + '分钟前';
        } else if (diff < 86400000) {
            return Math.floor(diff / 3600000) + '小时前';
        } else {
            return date.toLocaleDateString('zh-CN');
        }
    }
});
