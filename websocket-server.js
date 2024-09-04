const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', ws => {
    console.log('Client connected');

    ws.on('close', () => {
        console.log('Client disconnected');
    });

    // Send updates when new donations are made
    setInterval(() => {
        // You would replace this with actual data fetching from your database
        const donorData = JSON.stringify({
            donors: [
                { name: "Guguloth Praveen", amount: **** },
                { name: "Guguloth Vijaya", amount: *** },
                { name: "unknown person", amount: 500 }
            ]
        });
        ws.send(donorData);
    }, 5000); // every 5 seconds
});

console.log('WebSocket server is running on ws://localhost:8080');
