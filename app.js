document.addEventListener('DOMContentLoaded', () => {
    const processButton = document.getElementById('process-story');
    const storyInput = document.getElementById('story-input');
    const statusMessage = document.getElementById('status-message');
    const introVisual = document.getElementById('intro-visual');
    const videoDisplay = document.getElementById('video-display');

    if (processButton) {
        processButton.addEventListener('click', () => {
            const storyText = storyInput.value.trim();

            if (storyText === "") {
                statusMessage.textContent = "❌ ਕਿਰਪਾ ਕਰਕੇ ਕਹਾਣੀ ਦਾ ਪਾਠ ਦਰਜ ਕਰੋ।";
                statusMessage.style.color = "red";
                return;
            }

            // PHASE 1: STORY ANALYSIS (Thinking Node)
            statusMessage.textContent = "🧠 ਕਹਾਣੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਹੋ ਰਿਹਾ ਹੈ... (ਭਾਵਨਾਵਾਂ ਦੀ ਜਾਂਚ)";
            statusMessage.style.color = "orange";
            processButton.disabled = true;

            // Simulate AI work: Analyzing the text and creating the video assets
            setTimeout(() => {
                // PHASE 2: SYNTHESIS AND ASSEMBLY (Video Building)
                statusMessage.textContent = "🎬 ਐਨੀਮੇਸ਼ਨ ਅਤੇ ਆਵਾਜ਼ਾਂ ਬਣ ਰਹੀਆਂ ਹਨ... (Master Builder)";
                statusMessage.style.color = "yellow";
                
                // --- Display final success ---
                setTimeout(() => {
                    statusMessage.textContent = "✅ ਸੰਪੂਰਨ! ਸਟੂਡੀਓ ਪ੍ਰੋਡਕਸ਼ਨ ਤਿਆਰ।";
                    statusMessage.style.color = "lightgreen";
                    
                    // Hide the "Sat Kartar" screen and show a placeholder video
                    introVisual.style.display = 'none';
                    videoDisplay.style.display = 'block';
                    videoDisplay.innerHTML = `<p style="text-align:center; padding-top: 120px; color: white;">ਅਸਲ ਵੀਡੀਓ ਆਊਟਪੁੱਟ ਇਸੇ ਥਾਂ 'ਤੇ ਦਿਸੇਗਾ।</p>`;
                    
                    processButton.disabled = false;
                }, 4000); // 4 second assembly time

            }, 2000); // 2 second analysis time
        });
    }
    
    // Disable irrelevant buttons since this is a demonstration
    document.querySelectorAll('#visual-panel button').forEach(btn => btn.disabled = true);
    document.querySelectorAll('#audio-panel button').forEach(btn => btn.disabled = true);
    
});

