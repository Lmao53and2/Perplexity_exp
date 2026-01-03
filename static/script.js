const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const thinking = document.getElementById('thinking');
const taskList = document.getElementById('task-list');
const pdfUpload = document.getElementById('pdf-upload');
const pdfStatus = document.getElementById('pdf-status');

let pdfText = "";

// Anime.js animation for messages
function animateMessage(el) {
    anime({
        targets: el,
        translateY: [20, 0],
        opacity: [0, 1],
        easing: 'easeOutExpo',
        duration: 800
    });
}

function addMessage(role, content) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerText = content;
    chatHistory.appendChild(div);
    animateMessage(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function handleSend() {
    const message = userInput.value.trim();
    if (!message) return;

    const provider = document.getElementById('provider-select').value;
    const apiKey = document.getElementById('api-key-input').value;
    const modelMap = {
        "OpenAI": "gpt-4o",
        "Groq": "llama-3.3-70b-versatile",
        "Perplexity": "sonar-pro"
    };

    addMessage('user', message);
    userInput.value = '';
    
    // Show thinking with animation
    anime({
        targets: thinking,
        opacity: 1,
        duration: 300,
        easing: 'linear'
    });

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                provider,
                model: modelMap[provider],
                api_key: apiKey,
                pdf_text: pdfText
            })
        });

        const data = await response.json();
        
        // Hide thinking
        anime({
            targets: thinking,
            opacity: 0,
            duration: 300,
            easing: 'linear'
        });

        if (data.content) {
            addMessage('ai', data.content);
            updateTasks(message, provider, modelMap[provider], apiKey);
        } else {
            addMessage('ai', "Error: " + (data.detail || "Unknown error"));
        }
    } catch (err) {
        console.error(err);
        addMessage('ai', "Failed to connect to backend.");
    }
}

async function updateTasks(message, provider, model, api_key) {
    try {
        const res = await fetch('/extract-tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, provider, model, api_key })
        });
        const data = await res.json();
        data.tasks.forEach(task => {
            const li = document.createElement('li');
            li.innerText = task;
            taskList.appendChild(li);
            anime({
                targets: li,
                translateX: [-20, 0],
                opacity: [0, 1],
                duration: 500
            });
        });
    } catch (e) {}
}

pdfUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    pdfStatus.innerText = "Processing...";
    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('/upload-pdf', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        pdfText = data.text;
        pdfStatus.innerText = "PDF Loaded ✅";
    } catch (err) {
        pdfStatus.innerText = "Upload failed ❌";
    }
});

sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});
