const API_BASE = '/api/reading';
let sessionId = null;
let selectedCards = [];

async function startReading() {
    const question = document.getElementById('user-question').value;
    if (!question) {
        alert("질문을 입력해주세요!");
        return;
    }

    // UI Change: Show Shuffle
    switchSection('step-draw');

    try {
        // 1. Shuffle Request
        const shuffleRes = await fetch(`${API_BASE}/shuffle`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        const sessionData = await shuffleRes.json();
        sessionId = sessionData.session_id;

        // Simulate Shuffle Delay (Visual Effect)
        await new Promise(r => setTimeout(r, 1500));

        // 2. Draw Cards Request
        const drawRes = await fetch(`${API_BASE}/draw`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                session_id: sessionId, 
                spread_type: "three_card" 
            })
        });
        const drawData = await drawRes.json();
        selectedCards = drawData.cards;

        // Show Results
        showResults(selectedCards, question);

    } catch (error) {
        console.error("Error:", error);
        alert("오류가 발생했습니다. 다시 시도해주세요.");
        location.reload();
    }
}

function showResults(cards, question) {
    switchSection('step-result');
    const container = document.getElementById('cards-container');
    container.innerHTML = '';

    // Render Cards
    cards.forEach((card, index) => {
        const cardEl = document.createElement('div');
        cardEl.className = 'tarot-card';
        // Delay animation for each card
        cardEl.style.animationDelay = `${index * 0.3}s`;
        
        const orientationText = card.is_reversed ? "역방향" : "정방향";
        const positions = ["과거", "현재", "미래"];
        
        cardEl.innerHTML = `
            <div class="card-position">${positions[index] || index+1}</div>
            <img src="${card.image_url}" class="card-img ${card.is_reversed ? 'reversed' : ''}" alt="${card.name_kr}">
            <div class="card-info">
                <strong>${card.name_kr}</strong><br>
                <small>${orientationText}</small>
            </div>
        `;
        container.appendChild(cardEl);
    });

    // Start AI Interpretation Stream
    streamInterpretation(question);
}

async function streamInterpretation(question) {
    const outputDiv = document.getElementById('interpretation-text');
    outputDiv.innerText = "AI가 카드를 읽고 있습니다...\n";

    try {
        const response = await fetch(`${API_BASE}/interpret/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                question: question,
                spread_type: "three_card",
                selected_cards: selectedCards
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;
            
            // Process SSE data lines
            const lines = buffer.split('\n\n');
            buffer = lines.pop(); // Keep incomplete line in buffer

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const jsonStr = line.slice(6);
                    try {
                        const data = JSON.parse(jsonStr);
                        if (data.status === 'done') return;
                        if (data.chunk) {
                            outputDiv.innerHTML += data.chunk; // Append text
                            // Auto scroll to bottom
                            outputDiv.scrollTop = outputDiv.scrollHeight; 
                        }
                    } catch (e) {
                        console.error('JSON Parse Error', e);
                    }
                }
            }
        }

    } catch (e) {
        outputDiv.innerText += "\n[연결 오류 발생]";
    }
}

function switchSection(id) {
    document.querySelectorAll('section').forEach(el => {
        el.classList.remove('active');
        el.classList.add('hidden');
    });
    const target = document.getElementById(id);
    target.classList.remove('hidden');
    target.classList.add('active');
}
