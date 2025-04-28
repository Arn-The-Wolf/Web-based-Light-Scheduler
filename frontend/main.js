const ws = new WebSocket('ws://localhost:8765'); // Adjust port if needed

const form = document.getElementById('schedule-form');
const statusDiv = document.getElementById('status');

ws.onopen = () => {
    statusDiv.textContent = 'Connected to scheduler server.';
};
ws.onclose = () => {
    statusDiv.textContent = 'Disconnected from server.';
};
ws.onerror = (err) => {
    statusDiv.textContent = 'WebSocket error.';
};
ws.onmessage = (msg) => {
    statusDiv.textContent = msg.data;
};

form.onsubmit = (e) => {
    e.preventDefault();
    const onTime = document.getElementById('on-time').value;
    const offTime = document.getElementById('off-time').value;
    if (!onTime || !offTime) {
        statusDiv.textContent = 'Please enter both ON and OFF times.';
        return;
    }
    const payload = { on: onTime, off: offTime };
    ws.send(JSON.stringify(payload));
    statusDiv.textContent = 'Schedule sent!';
};
