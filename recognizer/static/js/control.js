let intervalId;  // Зберігає ідентифікатор інтервалу

function controlFeed(action) {
    fetch(`/control_feed/${action}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
            if (action === 'pause') {  // Якщо це дія "пауза", зупиніть оновлення списку
                clearInterval(intervalId);
            } else if (action === 'resume') {  // Якщо це дія "відновити", поновіть оновлення списку
                intervalId = setInterval(fetchIdentifiedItems, 1000);
            }
        });
}
