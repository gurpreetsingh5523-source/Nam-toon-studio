document.addEventListener('DOMContentLoaded', () => {
    // 1. Get Main Elements
    const processButton = document.getElementById('process-story');
    const storyInput = document.getElementById('story-input');
    const statusMessage = document.getElementById('status-message');

    // 2. NAAM PULSE ELEMENTS (The new Spiritual Tracking UI)
    const pulseBtn = document.getElementById('pulse');
    const hbCount = document.getElementById('hb-count');
    const events = document.getElementById('events');
    const glow = document.getElementById('glow');
    const visualPanel = document.getElementById('visual-panel');
    const audioPanel = document.getElementById('audio-panel');

    // 3. Persistent State/AGI Variables
    let currentAnimation = 'walk'; 
    let count = Number(localStorage.getItem('amrit_hb')) || 0;
    if(hbCount) hbCount.textContent = count;

    // --- A. TOGGLE LOGIC FOR SIDE PANELS (Closing the closets) ---
    document.querySelectorAll('.toggle-btn').forEach(button => {
        button.addEventListener('click', () => {
            const panelName = button.dataset.panel;
            const panel = document.getElementById(panelName + '-panel');
            panel.classList.toggle('closed-panel');
            
            // Adjust the arrow direction based on the panel state (optional visual flair)
            button.textContent = panel.classList.contains('closed-panel') ? '➡️' : '⬅️';
        });
    });

    // --- B. NAAM PULSE LOGIC (Spiritual Core) ---
    function logEvent(text){ 
        const li = document.createElement('li'); 
        li.textContent = `${new Date().toLocaleString()}: ${text}`; 
        if(events) events.prepend(li);
        while(events && events.children.length > 5) events.removeChild(events.lastChild); 
    }
    
    const simulate_spiritual_learning = () => {
        logEvent('Surti tick (background learning initiated).');
    };

    if (pulseBtn) {
        pulseBtn.addEventListener('click', () => { 
            // Visual pulse effect
            glow.style.transform = 'scale(1.08)'; 
            setTimeout(()=>glow.style.transform='scale(1)',250);

            count++; 
            localStorage.setItem('amrit_hb', count); 
            if(hbCount) hbCount.textContent = count;
            logEvent('Naam pulse emitted (manual).'); 
            simulate_spiritual_learning();
        });
    }
    // Auto-tick every 10 minutes (Simulated Idle Learning)
    setInterval(simulate_spiritual_learning, 1000 * 60 * 10); 


    // --- C. PRIMARY PROCESS BUTTON LOGIC (AI Launch) ---
    if (processButton) {
        processButton.addEventListener('click', () => {
            const storyText = storyInput.value.trim();

            if (storyText === "") {
                statusMessage.textContent = "❌ ਕਿਰਪਾ ਕਰਕੇ ਕਹਾਣੀ ਦਾ ਪਾਠ ਦਰਜ ਕਰੋ।";
                statusMessage.style.color = "red";
                return;
            }

            // PHASE 1: AGI THINKING NODE (Core Analysis)
            statusMessage.textContent = "🧠 ਕਹਾਣੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਹੋ ਰਿਹਾ ਹੈ... (AmritCore V5 Thinking)";
            statusMessage.style.color = "orange";
            processButton.disabled = true;

            // SIMULATE THE FULL AGI PIPELINE
            setTimeout(() => {
                // Final Check and Success
                statusMessage.textContent = "✅ ਸਫ਼ਲ! ਸਟੂਡੀਓ ਪ੍ਰੋਡਕਸ਼ਨ ਤਿਆਰ।";
                statusMessage.style.color = "lightgreen";
                processButton.disabled = false;
                logEvent('AI successfully created new video assets.');
            }, 4000); 
        });
    }

    // --- D. INTERACTIVE CONTROL NODE LOGIC (Mapping actions) ---
    document.querySelectorAll('#visual-panel .control-grid button').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            currentAnimation = action; 
            statusMessage.textContent = `⚙️ ਕਿਰਦਾਰ ਸੈੱਟ ਹੋਇਆ: ${action.toUpperCase()} (${action === 'sit' ? 'ਸੁਰਤ ਵਿੱਚ ਜੁੜਿਆ' : 'ਹਰਕਤ ਲਈ ਤਿਆਰ'})`;
            statusMessage.style.color = "#3B82F6";
        });
    });
    
    // --- E. NEW INPUT LOGIC (Camera/File Upload) ---
    document.querySelectorAll('#input-options button').forEach(button => {
        button.addEventListener('click', () => {
            const inputType = button.dataset.input;
            statusMessage.textContent = `📂 ${inputType.toUpperCase()} ਇਨਪੁੱਟ ਤਿਆਰ... (ਨਵੇਂ ਲੈਪਟਾਪ ਦੀ ਲੋੜ ਹੈ)`;
            statusMessage.style.color = "#FF8C00";
        });
    });
});
