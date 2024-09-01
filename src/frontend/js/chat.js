const allMailsElement = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendMessageButton = document.getElementById('send-message');
const loading = document.getElementById('loading');

sendMessageButton.addEventListener('click', async () => {
    if (sendMessageButton.disabled) {
        return;
    }

    sendMessageButton.disabled = true;
    sendMessageButton.innerHTML = '<span class="loading loading-small"></span>';

    const message = messageInput.value;
    if (message) {
        allMailsElement.innerHTML += `<div class="message right blue">${message}</div>`;
        messageInput.value = '';

        res = await sendMessage(message);

        if (res) {
            allMailsElement.innerHTML += `<div class="message">${res}</div>`;
        }

        sendMessageButton.disabled = false;
        sendMessageButton.innerHTML = 'Send';
    } else {
        sendMessageButton.disabled = false;
        sendMessageButton.innerHTML = 'Send';
    }
});

messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessageButton.click();
    }
});

async function sendMessage(message) {
    const _res = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: message
        })
    });

    const _json = await _res.json();

    if (_res.ok && _json.success) {
        return _json.response;
    }

    return "Error";
}

async function init() {
    loading.style.display = 'block';
    await fetch('/api/chat/init', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    loading.style.display = 'none';
    document.querySelector("section").classList.remove("hidden");
}

init();