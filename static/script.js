document.addEventListener("DOMContentLoaded", () => {
    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    function addMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, "user");
        userInput.value = "";

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        })
            .then((response) => response.json())
            .then((data) => {
                addMessage(data.response, "bot");
            })
            .catch((error) => {
                console.error("Error:", error);
                addMessage("Something went wrong. Please try again.", "bot");
            });
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});
