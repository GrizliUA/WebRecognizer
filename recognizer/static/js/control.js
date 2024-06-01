function controlFeed(action) {
    fetch(`/control_feed/${action}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
        });
}