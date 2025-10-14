document.addEventListener('DOMContentLoaded', () => {
    // 1. Get Main Elements
    const processButton = document.getElementById('process-story');
    const storyInput = document.getElementById('story-input');
    const statusMessage = document.getElementById('status-message');
    const visualPanel = document.getElementById('visual-panel');
    const audioPanel = document.getElementById('audio-panel');

    // 2. AGI Logic Variables
    let currentAnimation = 'walk'; // Default action
    let currentBackground = 'khu'; // Default setting

    // --- A. TOGGLE LOGIC FOR SIDE PANELS (Closing the closets) ---
    document.querySelectorAll('.toggle-btn').forEach(button => {
        button.addEventListener('click', () => {
            const panel = document.getElementById(button.dataset.panel + '-panel');
            panel.classList.toggle('closed-panel');
        });
    });
    
    // --- B. PRIMARY PROCESS BUTTON LOGIC ---
    if (processButton) {
        processButton.addEventListener('click', () => {
            const storyText = storyInput.value.trim();

            if (storyText === "") {
                statusMessage.textContent = "❌ ਕਿਰਪਾ ਕਰਕੇ ਕਹਾਣੀ ਦਾ ਪਾਠ ਦਰਜ ਕਰੋ।";
                statusMessage.style.color = "red";
                return;
            }

            // PHASE 1: AGI THINKING NODE (The Core Analysis)
            statusMessage.textContent = "🧠 ਕਹਾਣੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਹੋ ਰਿਹਾ ਹੈ... (AmritCore V5 Thinking)";
            statusMessage.style.color = "orange";
            processButton.disabled = true;

            // SIMULATION OF AGI LOGIC FOR THE FINAL REPORT
            setTimeout(() => {
                // Get current user selections from the UI (Demonstrating AGI logic linkage)
                const volume = document.getElementById('dialogue-volume').value;
                const bgPreset = document.getElementById('background-preset').value;
                
                // Final Console Output
                console.log("--- AMRTICORE V5 FINAL TASK LOAD ---");
                console.log("Story:", storyText.substring(0, 50) + '...');
                console.log("Animation Command:", currentAnimation);
                console.log("Selected Background:", bgPreset);
                console.log("Final Dialogue Volume:", volume);
                
                // PHASE 2: SYNTHESIS AND ASSEMBLY
                statusMessage.textContent = "✅ ਸਫ਼ਲ! AmritCore V5 ਅਸੈਂਬਲੀ ਪੂਰੀ ਹੋਈ।";
                statusMessage.style.color = "lightgreen";
                processButton.disabled = false;
                
            }, 3000); // 3 seconds total simulation time
        });
    }

    // --- C. INTERACTIVE CONTROL NODE LOGIC (Mapping buttons to AI commands) ---
    document.querySelectorAll('#visual-panel .control-grid button').forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            currentAnimation = action; // Update the AI's internal state
            statusMessage.textContent = `⚙️ ਕਿਰਦਾਰ ਸੈੱਟ ਹੋਇਆ: ${action.toUpperCase()} (${action === 'sit' ? 'ਸੁਰਤ ਵਿੱਚ ਜੁੜਿਆ' : 'ਹਰਕਤ ਲਈ ਤਿਆਰ'})`;
            statusMessage.style.color = "#3B82F6";
        });
    });
    
    // --- D. NEW INPUT LOGIC (Camera/File Upload) ---
    document.querySelectorAll('.upload-btn').forEach(button => {
        button.addEventListener('click', () => {
            const inputType = button.dataset.input;
            statusMessage.textContent = `📂 ${inputType.toUpperCase()} ਇਨਪੁੱਟ ਤਿਆਰ... (ਨਵੇਂ ਲੈਪਟਾਪ ਦੀ ਲੋੜ ਹੈ)`;
            statusMessage.style.color = "#FF8C00";
        });
    });
});

