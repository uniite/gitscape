ws = new WebSocket("ws://localhost:8000");
ws.onopen = function() {
    console.log("Opened");
    wsCommand("git", "branches")
}
ws.onmessage = function(msg) {
    wsCallback(JSON.parse(msg.data));
}

function wsCommand(controller, action) {
    sendObj({
        controller: controller,
        action: action,
        args: Array.prototype.slice.call(arguments, 2)
    });
}

function sendObj(obj) {
    ws.send(JSON.stringify(obj));
}
