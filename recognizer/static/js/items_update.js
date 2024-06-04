function fetchIdentifiedItems() {
    fetch('/get_identified_items/')
        .then(response => response.json())
        .then(data => {
            const identifiedHistoryList = document.getElementById('identified-list');
            identifiedHistoryList.innerHTML = '';

            data.identified_items.forEach(record => {
                const recordTime = record.time;
                const items = record.data;

                const formattedItems = formatItems(items);

                const li = document.createElement('li');
                li.textContent = `${recordTime} - ${formattedItems}`;
                identifiedHistoryList.appendChild(li);
            });
        });
}

function formatItems(items) {
    let formattedItems = '';

    for (const item in items) {
        if (items[item] !== 0) { // Виводимо лише, якщо кількість не дорівнює 0
            const itemName = item.charAt(0).toUpperCase() + item.slice(1); // Перший символ у верхньому регістрі
            formattedItems += `${itemName}: ${items[item]}, `; // Додано кількість предметів
        }
    }

    formattedItems = formattedItems.slice(0, -2); // Видаляємо останню кому

    return formattedItems;
}

setInterval(fetchIdentifiedItems, 1000);
