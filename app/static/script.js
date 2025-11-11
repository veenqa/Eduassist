document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const sendButton = document.getElementById('send-button');

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });

    sendButton.addEventListener('click', function() {
        sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('user', message);
        userInput.value = '';

        // Show loading indicator
        const loadingId = addMessage('bot', 'Thinking...');
        
        // Send message to server
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Remove loading message
            removeMessage(loadingId);
            
            if (data.error) {
                addMessage('bot', '❌ ' + data.error);
            } else if (data.response) {
                // Properly format the response with line breaks
                const formattedResponse = data.response.replace(/\n/g, '<br>');
                addMessage('bot', formattedResponse, true);
            } else {
                addMessage('bot', '❌ No response received from server.');
            }
        })
        .catch(error => {
            removeMessage(loadingId);
            console.error('Error:', error);
            addMessage('bot', '❌ Sorry, there was an error processing your request. Please try again.');
        });
    }

    function addMessage(sender, text, isHTML = false) {
        const messageDiv = document.createElement('div');
        const messageId = 'msg-' + Date.now();
        messageDiv.id = messageId;
        messageDiv.className = `message ${sender}-message`;
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        
        if (isHTML) {
            textDiv.innerHTML = text;
        } else {
            textDiv.textContent = text;
        }
        
        messageDiv.appendChild(textDiv);
        chatBox.appendChild(messageDiv);
        
        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
        
        return messageId;
    }

    function removeMessage(messageId) {
        const messageElement = document.getElementById(messageId);
        if (messageElement) {
            messageElement.remove();
        }
    }

    // Focus on input when page loads
    userInput.focus();
});