(function () {
    const quickQuestions = ['Shipping', 'Payment', 'Returns', 'My order', 'Contact'];

    // Build the widget
    const btn = document.createElement('button');
    btn.id = 'cf-chat-btn';
    btn.setAttribute('aria-label', 'Open support chat');
    btn.innerHTML = '<i class="fas fa-comment-dots"></i>';

    const box = document.createElement('div');
    box.id = 'cf-chat-box';
    box.innerHTML = `
        <div id="cf-chat-head">
            <span>COACH FACTORY SUPPORT</span>
            <button id="cf-chat-close" aria-label="Close">&times;</button>
        </div>
        <div id="cf-chat-msgs"></div>
        <form id="cf-chat-form">
            <input id="cf-chat-input" type="text"
                   placeholder="Ask a question..." autocomplete="off">
            <button type="submit">SEND</button>
        </form>`;

    document.body.appendChild(btn);
    document.body.appendChild(box);

    const msgs = document.getElementById('cf-chat-msgs');
    const form = document.getElementById('cf-chat-form');
    const input = document.getElementById('cf-chat-input');

    function addMessage(text, who) {
        const div = document.createElement('div');
        div.className = 'cf-msg ' + who;
        div.textContent = text;
        msgs.appendChild(div);
        msgs.scrollTop = msgs.scrollHeight;
    }

    function addQuickButtons() {
        const wrap = document.createElement('div');
        wrap.className = 'cf-quick';
        quickQuestions.forEach(function (q) {
            const b = document.createElement('button');
            b.textContent = q;
            b.onclick = function () { ask(q); };
            wrap.appendChild(b);
        });
        msgs.appendChild(wrap);
        msgs.scrollTop = msgs.scrollHeight;
    }

    async function ask(text) {
        addMessage(text, 'user');
        try {
            const res = await fetch('/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            addMessage(data.reply, 'bot');
        } catch (err) {
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
        }
    }

    btn.addEventListener('click', function () {
        box.classList.toggle('open');
        if (box.classList.contains('open') && msgs.children.length === 0) {
            addMessage('Hi! How can I help you today? Pick a topic or type your question.', 'bot');
            addQuickButtons();
        }
    });

    document.getElementById('cf-chat-close').addEventListener('click', function () {
        box.classList.remove('open');
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        input.value = '';
        ask(text);
    });
})();