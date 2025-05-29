document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("chat-open-btn");
    const chatWindow = document.getElementById("chat-window");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    const chatMin = document.getElementById("chat-minimize");
    const chatExpand = document.getElementById("chat-expand");
    let expanded = false;

    btn.onclick = () => {
        chatWindow.style.display = "block";
        chatWindow.style.width = "340px";
        chatWindow.style.height = "420px";
        expanded = false;
    };
    chatSend.onclick = sendMessage;
    chatMin.onclick = () => {
        chatWindow.style.display = "none";
    };
    chatExpand.onclick = () => {
        if (!expanded) {
            chatWindow.style.width = "95vw";
            chatWindow.style.height = "90vh";
            chatWindow.style.right = "2vw";
            chatWindow.style.bottom = "2vh";
            expanded = true;
        } else {
            chatWindow.style.width = "340px";
            chatWindow.style.height = "420px";
            chatWindow.style.right = "30px";
            chatWindow.style.bottom = "90px";
            expanded = false;
        }
    };

    function sendMessage() {
        const message = chatInput.value;
        if (!message) return;
        appendMessage("user", message);
        chatInput.value = "";

        fetch('/assist/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message})
        })
        .then(resp => resp.json())
        .then(data => appendMessage("bot", data.reply))
        .catch(() => appendMessage("bot", "Помилка"));
    }

    function appendMessage(who, text) {
        const box = document.getElementById("chat-messages");
        const div = document.createElement("div");
        div.className = who;
        div.textContent = text;
        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
    }
});
