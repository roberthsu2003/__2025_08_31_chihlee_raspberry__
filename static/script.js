document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const controlButtons = document.querySelectorAll('.control-btn');

    // 導覽列開關
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // 設備控制按鈕
    controlButtons.forEach(button => {
        button.addEventListener('click', () => {
            const deviceId = button.dataset.device;
            const deviceCard = document.getElementById(deviceId);
            const statusSpan = deviceCard.querySelector('.status');

            if (deviceId === 'light-1') {
                if (statusSpan.textContent === '關閉') {
                    statusSpan.textContent = '開啟';
                    statusSpan.style.color = '#27ae60';
                    button.textContent = '關閉';
                    button.classList.add('on');
                } else {
                    statusSpan.textContent = '關閉';
                    statusSpan.style.color = '#e74c3c';
                    button.textContent = '開啟';
                    button.classList.remove('on');
                }
            } else if (deviceId === 'door-lock-1') {
                if (statusSpan.textContent === '上鎖') {
                    statusSpan.textContent = '解鎖';
                    statusSpan.style.color = '#27ae60';
                    button.textContent = '上鎖';
                    button.classList.add('on');
                } else {
                    statusSpan.textContent = '上鎖';
                    statusSpan.style.color = '#e74c3c';
                    button.textContent = '解鎖';
                    button.classList.remove('on');
                }
            }
            // 這裡可以添加發送請求到後端的邏輯
            console.log(`設備 ${deviceId} 狀態已更新`);
        });
    });

    // 模擬溫度感測器數據更新
    const tempSensor = document.getElementById('temp-sensor-1');
    if (tempSensor) {
        const temperatureSpan = tempSensor.querySelector('.temperature');
        setInterval(() => {
            const randomTemp = (Math.random() * 5 + 20).toFixed(1); // 20.0 - 25.0
            temperatureSpan.textContent = `${randomTemp}°C`;
        }, 5000); // 每 5 秒更新一次
    }
});