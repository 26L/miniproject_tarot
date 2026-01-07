// --- Constants & Config ---
const API_BASE = '/api/v1';
const SPREAD_CONFIG = {
    'one_card': { count: 1, name: '원 카드' },
    'three_card': { count: 3, name: '쓰리 카드' }
};

// --- State Management ---
const state = {
    currentStep: 'intro', // intro -> shuffle -> draw -> result
    session: null,        // { session_id, spread_config, cards }
    drawnCount: 0,
    isProcessing: false
};

// --- DOM Elements ---
const elements = {
    sections: {
        intro: document.getElementById('step-intro'),
        shuffle: document.getElementById('step-shuffle'),
        draw: document.getElementById('step-draw'),
        result: document.getElementById('step-result')
    },
    inputs: {
        question: document.getElementById('user-question'),
        spreadType: document.getElementById('spread-type')
    },
    buttons: {
        start: document.getElementById('btn-start'),
        retry: document.getElementById('btn-retry')
    },
    drawArea: {
        deck: document.getElementById('deck'),
        fanDeck: document.getElementById('fan-deck'),
        slots: document.getElementById('spread-slots'),
        count: document.getElementById('draw-count'),
        total: document.getElementById('draw-total')
    },
    resultArea: {
        cards: document.getElementById('result-cards'),
        text: document.getElementById('interpretation-text')
    }
};

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
});

function initEventListeners() {
    elements.buttons.start.addEventListener('click', handleStartReading);
    elements.buttons.retry.addEventListener('click', () => location.reload());
    // elements.drawArea.deck.addEventListener('click', handleCardDraw); // Removed for fan-out mode
}

// --- Step Transitions ---
function switchStep(stepName) {
    // Hide all sections
    Object.values(elements.sections).forEach(el => {
        el.classList.remove('active');
        setTimeout(() => {
            if (!el.classList.contains('active')) el.classList.add('hidden');
        }, 500); // Wait for fade out
    });

    // Show target section
    const target = elements.sections[stepName];
    target.classList.remove('hidden');
    // Small delay to allow display:block to apply before opacity transition
    setTimeout(() => {
        target.classList.add('active');
    }, 50);

    state.currentStep = stepName;
}

// --- Handlers ---

async function handleStartReading() {
    const question = elements.inputs.question.value.trim();
    const spreadType = elements.inputs.spreadType.value;

    if (!question) {
        alert('질문을 입력해주세요.');
        elements.inputs.question.focus();
        return;
    }

    if (state.isProcessing) return;
    state.isProcessing = true;
    elements.buttons.start.disabled = true;
    elements.buttons.start.textContent = "운명을 읽는 중...";

    try {
        // 1. API Call (Pre-draw)
        const response = await fetch(`${API_BASE}/readings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: question,
                spread_type: spreadType
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to start reading');
        }

        const data = await response.json();
        state.session = data;

        // 2. Prepare Draw Area
        prepareDrawArea(data.spread_config);

        // 3. Move to Shuffle (Auto transition)
        switchStep('shuffle');
        
        // 4. Auto-advance to Draw after animation (3s)
        setTimeout(() => {
            switchStep('draw');
            state.isProcessing = false;
        }, 3000);

    } catch (error) {
        console.error(error);
        alert(`오류가 발생했습니다: ${error.message}`);
        state.isProcessing = false;
        elements.buttons.start.disabled = false;
        elements.buttons.start.textContent = "운명의 카드 펼치기";
    }
}

function prepareDrawArea(spreadConfig) {
    const container = elements.drawArea.slots;
    container.innerHTML = ''; // Clear
    
    // Create empty slots
    spreadConfig.positions.forEach(pos => {
        const slot = document.createElement('div');
        slot.className = 'slot';
        slot.dataset.index = pos.index;
        slot.dataset.label = pos.meaning;
        slot.textContent = '?';
        container.appendChild(slot);
    });

    elements.drawArea.total.textContent = spreadConfig.card_count;
    elements.drawArea.count.textContent = '0';
    state.drawnCount = 0;

    // Render Fan-out Deck
    renderFanDeck();
}

function renderFanDeck() {
    const fanContainer = elements.drawArea.fanDeck;
    fanContainer.innerHTML = '';
    const totalCards = 78;
    const arcAngle = 120; // 각도 넓힘

    for (let i = 0; i < totalCards; i++) {
        const card = document.createElement('div');
        card.className = 'fan-card';
        
        // 각도 계산 (-60도 ~ 60도)
        const angle = (arcAngle / (totalCards - 1)) * i - (arcAngle / 2);
        card.style.transform = `rotate(${angle}deg)`;
        card.style.zIndex = i;

        card.addEventListener('click', (e) => handleCardDraw(e.target));
        fanContainer.appendChild(card);
    }
}

function handleCardDraw(cardElement) {
    if (state.currentStep !== 'draw') return;
    
    const total = state.session.spread_config.card_count;
    if (state.drawnCount >= total) return;
    if (cardElement.classList.contains('selected')) return;

    // 즉시 투명화하지 않고 애니메이션 시작 시점에 처리
    cardElement.classList.add('selected');

    // 1. Visual Effect (Card flying from its position to slot)
    const currentCardIndex = state.drawnCount;
    const targetSlot = elements.drawArea.slots.children[currentCardIndex];
    
    // Create a temporary flying card at the exact same position
    const flyer = document.createElement('div');
    flyer.className = 'card-back';
    flyer.style.position = 'fixed';
    
    const cardRect = cardElement.getBoundingClientRect();
    // 현재 회전된 상태의 각도를 유지하며 시작
    const currentTransform = cardElement.style.transform;
    
    flyer.style.width = `${cardRect.width}px`;
    flyer.style.height = `${cardRect.height}px`;
    flyer.style.left = `${cardRect.left}px`;
    flyer.style.top = `${cardRect.top}px`;
    flyer.style.zIndex = 2000;
    flyer.style.transition = 'all 0.8s cubic-bezier(0.25, 1, 0.5, 1)';
    // flyer.style.transform = currentTransform; // (Optional: 시작 시 회전 유지)

    document.body.appendChild(flyer);

    // End position (Slot)
    const slotRect = targetSlot.getBoundingClientRect();
    
    requestAnimationFrame(() => {
        flyer.style.left = `${slotRect.left}px`;
        flyer.style.top = `${slotRect.top}px`;
        flyer.style.width = `${slotRect.width}px`;
        flyer.style.height = `${slotRect.height}px`;
        flyer.style.transform = 'rotate(0deg)'; // 똑바로 정렬
    });

    // Cleanup after animation
    setTimeout(() => {
        if (document.body.contains(flyer)) document.body.removeChild(flyer);
        targetSlot.style.backgroundImage = "url('/static/cards/tarot_verso.png')";
        targetSlot.style.backgroundSize = "100% 100%";
        targetSlot.textContent = ''; 
        
        state.drawnCount++;
        elements.drawArea.count.textContent = state.drawnCount;

        if (state.drawnCount >= total) {
            setTimeout(revealResults, 800);
        }
    }, 800);
}

async function revealResults() {
    switchStep('result');
    renderResultCards();
    
    // Small delay before interpretation starts
    setTimeout(startInterpretationStream, 1500);
}

function renderResultCards() {
    const container = elements.resultArea.cards;
    container.innerHTML = '';
    
    state.session.cards.forEach((card, index) => {
        // Create Card Structure (Flip supported)
        const wrapper = document.createElement('div');
        wrapper.className = 'tarot-card';
        wrapper.style.animationDelay = `${index * 0.2}s`; // Staggered fade-in
        
        const inner = document.createElement('div');
        inner.className = 'card-inner';
        
        const front = document.createElement('div');
        front.className = 'card-front';
        // Handle image path
        // card.image_url already contains '/static/cards/...' from DB
        front.style.backgroundImage = `url('${card.image_url}')`;
        if (card.is_reversed) {
            front.style.transform = 'rotateY(180deg) rotate(180deg)'; // Flip + Reverse
        }

        const back = document.createElement('div');
        back.className = 'card-back-face';

        inner.appendChild(front);
        inner.appendChild(back);
        wrapper.appendChild(inner);
        
        // Label (Position & Name)
        const info = document.createElement('div');
        info.className = 'card-info';
        info.innerHTML = `<p><strong>${card.position_meaning}</strong></p><p>${card.name_kr}</p>`;
        info.style.color = '#fff';
        info.style.marginTop = '10px';
        info.style.textAlign = 'center';
        
        const cardContainer = document.createElement('div');
        cardContainer.style.display = 'flex';
        cardContainer.style.flexDirection = 'column';
        cardContainer.style.alignItems = 'center';
        
        cardContainer.appendChild(wrapper);
        cardContainer.appendChild(info);
        
        container.appendChild(cardContainer);

        // Trigger Flip Animation
        setTimeout(() => {
            wrapper.classList.add('flipped');
        }, 500 + (index * 300));
    });
}

async function startInterpretationStream() {
    const output = elements.resultArea.text;
    output.textContent = ''; // Clear previous
    output.innerHTML = '<span class="cursor">|</span>'; // Typing cursor

    try {
        const response = await fetch(`${API_BASE}/interpretations/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: state.session.session_id })
        });

        if (!response.ok) throw new Error('Stream connection failed');

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let fullText = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            // Parse SSE format (data: ...)
            const lines = chunk.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const content = line.slice(6); // Remove 'data: '
                    // Handle special tokens if needed
                    fullText += content;
                    output.textContent = fullText;
                    
                    // Auto scroll
                    const container = document.querySelector('.interpretation-container');
                    container.scrollTop = container.scrollHeight;
                }
            }
        }
    } catch (error) {
        console.error(error);
        output.textContent += "\n[오류가 발생하여 해석을 완료할 수 없습니다.]";
    }
}