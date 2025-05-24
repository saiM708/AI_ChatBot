const chatMessages = document.getElementById('chatMessages');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');

    function appendMessage(text, sender) {
      const msgDiv = document.createElement('div');
      msgDiv.className = 'message ' + sender;
      msgDiv.textContent = text;
      chatMessages.appendChild(msgDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (!message) return;

      appendMessage(message, 'user');
      chatInput.value = '';
      chatInput.disabled = true;

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        });
        const data = await response.json();
        if (response.ok) {
          appendMessage(data.response || 'No response from AI.', 'bot');
        } else {
          appendMessage('Error: ' + (data.error || 'Unknown error'), 'bot');
        }
      } catch (error) {
        appendMessage('Error: ' + error.message, 'bot');
      } finally {
        chatInput.disabled = false;
        chatInput.focus();
      }
    });