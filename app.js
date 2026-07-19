document.addEventListener('DOMContentLoaded', () => {
    // 1. DOM Elements
    const pulseBtn = document.getElementById('pulse');
    const glow = document.getElementById('glow');
    const hbCount = document.getElementById('hb-count');
    const eventsList = document.getElementById('events');
    const statusMessage = document.getElementById('status-message');
    const storyInput = document.getElementById('story-input');
    const processButton = document.getElementById('process-story');
    const consoleBox = document.getElementById('console-box');
    const consoleLogs = document.getElementById('console-logs');

    // Preset & Preview Monitors
    const backgroundPromptInput = document.getElementById('background-prompt-input');
    const generateSceneBtn = document.getElementById('generate-scene-btn');
    const bgUploadInput = document.getElementById('bg-upload-input');
    const bgUploadBtn = document.getElementById('bg-upload-btn');
    const previewScreen = document.getElementById('preview-screen');
    const avatarContainer = document.getElementById('avatar-container');
    const subtitleBubble = document.getElementById('subtitle-bubble');
    const sfxOverlay = document.getElementById('sfx-overlay');
    const videoPlayer = document.getElementById('video-player');
    const introVisual = document.getElementById('intro-visual');



    // Sidebar Panels
    const characterPanel = document.getElementById('character-panel');
    const sidebarCharacterList = document.getElementById('sidebar-character-list');
    const addTrackBtnSidebar = document.getElementById('add-track-btn-sidebar');

    // Inspector Panel elements
    const blockInspector = document.getElementById('block-inspector');
    const noSelectionMessage = document.getElementById('no-selection-message');
    const inspectorCharacter = document.getElementById('inspector-character');
    const inspectorText = document.getElementById('inspector-text');
    const inspectorVolume = document.getElementById('inspector-volume');
    const inspectorPan = document.getElementById('inspector-pan');
    const inspectorStartTime = document.getElementById('inspector-start-time');
    const deleteBlockBtn = document.getElementById('delete-block-btn');

    // Recording buttons (inspector)
    const blockMicRecordBtn = document.getElementById('block-mic-record-btn');
    const blockMicStopBtn = document.getElementById('block-mic-stop-btn');

    // Block Storyboard image buttons (inspector)
    const blockImageUploadInput = document.getElementById('block-image-upload-input');
    const blockImageUploadBtn = document.getElementById('block-image-upload-btn');
    const blockImagePreviewContainer = document.getElementById('block-image-preview-container');
    const blockImagePreviewThumb = document.getElementById('block-image-preview-thumb');
    const blockImageFilenameLabel = document.getElementById('block-image-filename-label');
    const blockImageClearBtn = document.getElementById('block-image-clear-btn');

    // Global Recording toolbar elements
    const globalMicRecordBtn = document.getElementById('global-mic-record-btn');
    const globalMicStopBtn = document.getElementById('global-mic-stop-btn');
    const globalRecTrack = document.getElementById('global-rec-track');

    // AI Script elements
    const aiGenerateBtn = document.getElementById('ai-generate-btn');
    const aiPrompt = document.getElementById('ai-prompt');
    const aiTheme = document.getElementById('ai-theme');
    const aiModel = document.getElementById('ai-model');

    // AI assets creation controls
    const aiCharPrompt = document.getElementById('ai-char-prompt');
    const aiCharGenerateBtn = document.getElementById('ai-char-generate-btn');

    // AI Post-Production controls
    const aiVoiceCloning = document.getElementById('ai-voice-cloning');
    const aiSubtitleGeneration = document.getElementById('ai-subtitle-generation');
    const aiAudioEnhancement = document.getElementById('ai-audio-enhancement');
    const aiColorGrading = document.getElementById('ai-color-grading');

    // Timeline Workspace controls
    const playBtn = document.getElementById('play-btn');
    const stopBtn = document.getElementById('stop-btn');
    const rewindBtn = document.getElementById('rewind-btn');
    const zoomSlider = document.getElementById('zoom-slider');
    const loadDemoBtn = document.getElementById('load-demo-btn');
    const addBlockBtn = document.getElementById('add-block-btn');
    const clearTimelineBtn = document.getElementById('clear-timeline-btn');
    const currentPlaycode = document.getElementById('current-playcode');
    const totalDurationcode = document.getElementById('total-durationcode');
    const workspaceEl = document.getElementById('timeline-workspace-el');
    const scrollingRuler = document.getElementById('scrolling-ruler');
    const playhead = document.getElementById('playhead');
    const timelineTracksContainer = document.getElementById('timeline-tracks-container');
    const sfxSelector = document.getElementById('sfx-selector');

    // 2. Generic Editor State
    let registeredTracks = [
        { name: 'Scene Background', type: 'background' },
        { name: 'Krishna', type: 'character' },
        { name: 'Sultan', type: 'character' },
        { name: 'Dialogues', type: 'dialogue' },
        { name: 'Text Overlay', type: 'text' },
        { name: 'Transitions', type: 'transition' },
        { name: 'SFX', type: 'sfx' },
        { name: 'BGM', type: 'bgm' }
    ];

    let timelineData = [
        { id: '1', character: "Krishna", text: "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਨੈਮ ਟੂਨ ਸਟੂਡੀਓ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ!", volume: 1.0, pan: 0.0, start_time: 1.0, duration: 4.5 }
    ];

    let selectedBlockId = null;
    let pixelsPerSecond = 40;
    let maxProjectDuration = 60.0;
    let playheadTime = 0.0;
    let isPlaying = false;
    let compiledVideoLoaded = false;
    let animationFrameId = null;
    let lastFrameTime = 0;
    let audioCtx = null;
    const audioCache = {};

    // Keyframes storage (e.g. trackKeyframes[trackName] = [{time: 0, volume: 1.0}])
    const trackKeyframes = {};

    // Mute/Solo/Volume states (dynamically updated)
    const mutedTracks = {};
    const soloTracks = {};
    const trackVolumes = {
        'Scene Background': 1.0,
        'Krishna': 0.8,
        'Sultan': 0.8,
        'Dialogues': 0.8,
        'Text Overlay': 1.0,
        'Transitions': 1.0,
        'SFX': 0.8,
        'BGM': 0.8
    };

    let mediaRecorder = null;
    let audioChunks = [];

    // --- SYSTEM DIAGNOSTICS LOG ---
    function logEvent(msg) {
        const li = document.createElement('li');
        const now = new Date();
        li.textContent = `[${now.toLocaleTimeString()}] ${msg}`;
        eventsList.appendChild(li);
        eventsList.scrollTop = eventsList.scrollHeight;
    }

    async function updateSystemStatus() {
        try {
            const res = await fetch('/api/status');
            if (res.ok) {
                const data = await res.json();
                logEvent(`System: ${data.status} | Cache Size: ${data.cache_size_bytes} bytes | GPU: ${data.gpu_available ? 'ARM GPU Active' : 'CPU Mode'}`);
            }
        } catch (e) {
            console.log("Status fetch failed", e);
        }
    }
    updateSystemStatus();
    setInterval(updateSystemStatus, 15000);

    // Toggle panels logic
    document.querySelectorAll('.toggle-btn').forEach(button => {
        button.addEventListener('click', () => {
            const panelName = button.dataset.panel;
            const panel = document.getElementById(panelName + '-panel');
            panel.classList.toggle('closed-panel');
            button.textContent = panel.classList.contains('closed-panel') ? '➡️' : '⬅️';
        });
    });

    // Naam Pulse simulator
    let count = Number(localStorage.getItem('amrit_hb')) || 0;
    if(hbCount) hbCount.textContent = count;
    if (pulseBtn) {
        pulseBtn.addEventListener('click', () => { 
            glow.style.transform = 'scale(1.08)'; 
            setTimeout(() => glow.style.transform = 'scale(1)', 250);
            count++; 
            localStorage.setItem('amrit_hb', count); 
            if(hbCount) hbCount.textContent = count;
            logEvent('Pulse simulated.'); 
        });
    }

    // --- TIME FORMATTING ---
    function formatTimecode(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        const centis = Math.floor((seconds % 1) * 100);
        
        const pad = (num) => String(num).padStart(2, '0');
        return `${pad(mins)}:${pad(secs)}.${pad(centis)}`;
    }

    // --- RULER RENDERING ---
    function renderRuler() {
        scrollingRuler.innerHTML = '';
        const interval = pixelsPerSecond < 25 ? 10 : (pixelsPerSecond < 60 ? 5 : 2);
        for (let t = 0; t <= maxProjectDuration; t += interval) {
            const marker = document.createElement('div');
            marker.className = 'ruler-marker';
            marker.style.left = `${t * pixelsPerSecond}px`;
            marker.textContent = `${Math.floor(t / 60)}m ${t % 60}s`;
            scrollingRuler.appendChild(marker);
        }
    }

    // --- PRE-LOAD AUDIO CLIPS ---
    async function loadAudioClip(block) {
        if (block.character === 'SFX' || block.character === 'BGM') {
            const audioPath = `/audio/${block.text}.wav`;
            if (!audioCache[block.id]) {
                const aud = new Audio(audioPath);
                aud.loop = (block.character === 'BGM');
                audioCache[block.id] = aud;
            }
            return;
        }

        if (block.audio_file) {
            if (!audioCache[block.id]) {
                audioCache[block.id] = new Audio(`/media/audio/recordings/${block.id}.wav`);
            }
            return;
        }

        try {
            const cacheKey = `${block.character}_${block.text}`;
            const res = await fetch(`/api/preview_tts?character=${encodeURIComponent(block.character)}&text=${encodeURIComponent(block.text)}`);
            if (res.ok) {
                const data = await res.json();
                if (!audioCache[block.id] || audioCache[block.id].dataset.textKey !== cacheKey) {
                    const aud = new Audio(data.url);
                    aud.dataset.textKey = cacheKey;
                    audioCache[block.id] = aud;
                }
            }
        } catch (e) {
            console.log("Failed to load TTS preview clip for block:", block.id, e);
        }
    }

    function preloadAllAudio() {
        timelineData.forEach(block => loadAudioClip(block));
    }

    // --- DYNAMIC TRACK & SIDEBAR GENERATION ---
    function renderTrackLanes() {
        timelineTracksContainer.innerHTML = '';
        
        registeredTracks.forEach(track => {
            const laneEl = document.createElement('div');
            laneEl.className = 'track-lane';
            laneEl.id = `track-lane-${track.name}`;

            // Build Track header labels
            const labelEl = document.createElement('div');
            labelEl.className = 'track-label';
            labelEl.style.display = 'flex';
            labelEl.style.justifyContent = 'space-between';
            labelEl.style.alignItems = 'center';

            const nameSpan = document.createElement('span');
            nameSpan.style.fontSize = '0.8rem';
            nameSpan.textContent = track.name;

            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'track-actions';
            actionsDiv.style.display = 'flex';
            actionsDiv.style.gap = '4px';

            // Mute Button
            const muteBtn = document.createElement('button');
            muteBtn.className = 'track-mute-btn';
            muteBtn.textContent = mutedTracks[track.name] ? '🔇' : '🔊';
            if (mutedTracks[track.name]) muteBtn.classList.add('active-mute');
            muteBtn.style.background = 'none';
            muteBtn.style.border = 'none';
            muteBtn.style.cursor = 'pointer';
            muteBtn.style.fontSize = '0.85rem';
            muteBtn.title = 'Mute';
            muteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                mutedTracks[track.name] = !mutedTracks[track.name];
                muteBtn.textContent = mutedTracks[track.name] ? '🔇' : '🔊';
                muteBtn.classList.toggle('active-mute', mutedTracks[track.name]);
                logEvent(`Track ${track.name} Muted: ${mutedTracks[track.name]}`);
            });

            // Solo Button
            const soloBtn = document.createElement('button');
            soloBtn.className = 'track-solo-btn';
            soloBtn.textContent = '⭐';
            if (soloTracks[track.name]) {
                soloBtn.classList.add('active-solo');
                soloBtn.style.filter = 'none';
            } else {
                soloBtn.style.filter = 'grayscale(1)';
            }
            soloBtn.style.background = 'none';
            soloBtn.style.border = 'none';
            soloBtn.style.cursor = 'pointer';
            soloBtn.style.fontSize = '0.85rem';
            soloBtn.title = 'Solo';
            soloBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                soloTracks[track.name] = !soloTracks[track.name];
                soloBtn.classList.toggle('active-solo', soloTracks[track.name]);
                soloBtn.style.filter = soloTracks[track.name] ? 'none' : 'grayscale(1)';
                logEvent(`Track ${track.name} Soloed: ${soloTracks[track.name]}`);
            });

            // Track Volume Slider
            const volSlider = document.createElement('input');
            volSlider.type = 'range';
            volSlider.min = '0';
            volSlider.max = '100';
            volSlider.value = Math.round((trackVolumes[track.name] !== undefined ? trackVolumes[track.name] : 0.8) * 100);
            volSlider.style.width = '45px';
            volSlider.style.height = '4px';
            volSlider.style.background = '#4b5563';
            volSlider.style.outline = 'none';
            volSlider.style.borderRadius = '2px';
            volSlider.style.cursor = 'pointer';
            volSlider.style.padding = '0';
            volSlider.style.margin = '0 2px';
            volSlider.title = `Volume: ${volSlider.value}%`;
            volSlider.addEventListener('input', (e) => {
                const val = parseFloat(e.target.value) / 100;
                trackVolumes[track.name] = val;
                volSlider.title = `Volume: ${e.target.value}%`;
            });

            // Keyframe Button (💎)
            const keyframeBtn = document.createElement('button');
            keyframeBtn.className = 'track-keyframe-btn';
            keyframeBtn.innerHTML = '💎';
            keyframeBtn.style.background = 'none';
            keyframeBtn.style.border = 'none';
            keyframeBtn.style.cursor = 'pointer';
            keyframeBtn.style.fontSize = '0.75rem';
            keyframeBtn.style.padding = '0';
            keyframeBtn.style.opacity = '0.6';
            keyframeBtn.title = 'Add Volume Keyframe';

            const hasKf = trackKeyframes[track.name] && trackKeyframes[track.name].some(kf => Math.abs(kf.time - playheadTime) < 0.25);
            if (hasKf) {
                keyframeBtn.style.opacity = '1';
                keyframeBtn.style.textShadow = '0 0 8px #60a5fa';
            }

            keyframeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (!trackKeyframes[track.name]) {
                    trackKeyframes[track.name] = [];
                }
                const curTime = Math.round(playheadTime * 10) / 10;
                const curVol = trackVolumes[track.name] !== undefined ? trackVolumes[track.name] : 0.8;
                
                const existingIdx = trackKeyframes[track.name].findIndex(kf => Math.abs(kf.time - curTime) < 0.25);
                if (existingIdx !== -1) {
                    trackKeyframes[track.name][existingIdx].volume = curVol;
                    logEvent(`Updated volume keyframe at ${curTime}s to ${Math.round(curVol * 100)}% for track: ${track.name}`);
                } else {
                    trackKeyframes[track.name].push({ time: curTime, volume: curVol });
                    logEvent(`Added volume keyframe at ${curTime}s to ${Math.round(curVol * 100)}% for track: ${track.name}`);
                }
                trackKeyframes[track.name].sort((a, b) => a.time - b.time);

                keyframeBtn.style.opacity = '1';
                keyframeBtn.style.textShadow = '0 0 8px #60a5fa';
                statusMessage.textContent = `💎 Volume Keyframe added at ${curTime}s!`;
                statusMessage.style.color = "#60a5fa";
            });

            actionsDiv.appendChild(muteBtn);
            actionsDiv.appendChild(soloBtn);
            actionsDiv.appendChild(volSlider);
            actionsDiv.appendChild(keyframeBtn);

            // Delete Track button (Only for custom character tracks)
            if (track.type === 'character') {
                const delBtn = document.createElement('button');
                delBtn.textContent = '❌';
                delBtn.style.background = 'none';
                delBtn.style.border = 'none';
                delBtn.style.cursor = 'pointer';
                delBtn.style.fontSize = '0.75rem';
                delBtn.title = 'Delete Track';
                delBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (confirm(`Delete character track "${track.name}" and all its timeline blocks?`)) {
                        registeredTracks = registeredTracks.filter(t => t.name !== track.name);
                        timelineData = timelineData.filter(b => b.character !== track.name);
                        logEvent(`Removed character track: ${track.name}`);
                        rebuildEditorUI();
                    }
                });
                actionsDiv.appendChild(delBtn);
            }

            labelEl.appendChild(nameSpan);
            labelEl.appendChild(actionsDiv);

            // Blocks container inside track lane
            const blocksContainer = document.createElement('div');
            blocksContainer.className = 'track-blocks';
            blocksContainer.id = `blocks-container-${track.name}`;
            blocksContainer.style.position = 'relative';
            blocksContainer.style.height = '100%';
            blocksContainer.style.flexGrow = '1';

            laneEl.appendChild(labelEl);
            laneEl.appendChild(blocksContainer);
            timelineTracksContainer.appendChild(laneEl);
        });
    }

    function renderSidebarCharacters() {
        sidebarCharacterList.innerHTML = '';
        
        registeredTracks.filter(t => t.type === 'character').forEach(track => {
            const item = document.createElement('div');
            item.className = 'sidebar-char-item';

            const nameSpan = document.createElement('span');
            nameSpan.className = 'sidebar-char-name';
            nameSpan.textContent = track.name;

            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'sidebar-char-actions';

            const uploadBtn = document.createElement('button');
            uploadBtn.className = 'char-upload-small-btn';
            uploadBtn.textContent = '📷 Character Pic';
            uploadBtn.addEventListener('click', () => {
                const fileInput = document.createElement('input');
                fileInput.type = 'file';
                fileInput.accept = 'image/*';
                fileInput.addEventListener('change', async (e) => {
                    const file = e.target.files[0];
                    if (!file) return;
                    logEvent(`Uploading avatar for ${track.name}...`);
                    const formData = new FormData();
                    formData.append('file', file);
                    try {
                        const res = await fetch(`/api/upload_character?character_name=${encodeURIComponent(track.name)}`, {
                            method: 'POST',
                            body: formData
                        });
                        if (res.ok) {
                            logEvent(`Avatar loaded successfully for character "${track.name}"!`);
                            updateInteractiveMonitor();
                        }
                    } catch (err) {
                        logEvent(`Avatar upload failed.`);
                    }
                });
                fileInput.click();
            });

            actionsDiv.appendChild(uploadBtn);
            item.appendChild(nameSpan);
            item.appendChild(actionsDiv);
            sidebarCharacterList.appendChild(item);
        });
    }

    function updateSelectDropdowns() {
        // Rec track dropdown
        globalRecTrack.innerHTML = '';
        registeredTracks.filter(t => t.type === 'character').forEach(track => {
            const opt = document.createElement('option');
            opt.value = track.name;
            opt.textContent = track.name;
            globalRecTrack.appendChild(opt);
        });

        // Inspector dropdown
        inspectorCharacter.innerHTML = '';
        registeredTracks.forEach(track => {
            const opt = document.createElement('option');
            opt.value = track.name;
            opt.textContent = track.name;
            inspectorCharacter.appendChild(opt);
        });
    }

    function rebuildEditorUI() {
        renderTrackLanes();
        renderSidebarCharacters();
        updateSelectDropdowns();
        renderTimeline();
    }

    // Add track triggers
    if (addTrackBtnSidebar) {
        addTrackBtnSidebar.addEventListener('click', () => {
            const name = prompt("Enter new character track name:");
            if (name) {
                const cleanName = name.trim().replace(/[^a-zA-Z0-9\s-_]/g, '');
                if (!cleanName) return;
                if (registeredTracks.some(t => t.name.toLowerCase() === cleanName.toLowerCase())) {
                    alert("Track already exists!");
                    return;
                }
                registeredTracks.push({ name: cleanName, type: 'character' });
                logEvent(`Created new character track: ${cleanName}`);
                rebuildEditorUI();
            }
        });
    }

    // --- TIMELINE RENDERING LOOP ---
    function renderTimeline() {
        // Clear old blocks inside lanes
        registeredTracks.forEach(track => {
            const container = document.getElementById(`blocks-container-${track.name}`);
            if (container) container.innerHTML = '';
        });

        let maxTime = 12.0;
        timelineData.forEach(block => {
            const end = block.start_time + block.duration;
            if (end > maxTime) maxTime = end;
        });
        maxProjectDuration = Math.max(60.0, Math.ceil(maxTime + 10.0));
        
        const workspaceWidth = (maxProjectDuration * pixelsPerSecond) + 120;
        workspaceEl.style.width = `${workspaceWidth}px`;
        
        renderRuler();
        updatePlayheadUI();

        timelineData.forEach(block => {
            const container = document.getElementById(`blocks-container-${block.character}`);
            if (!container) return; // Track might have been deleted

            const blockEl = document.createElement('div');
            blockEl.className = 'timeline-block';
            if (block.id === selectedBlockId) {
                blockEl.classList.add('active-block');
            }

            if (block.character === 'SFX') {
                blockEl.classList.add('sfx-block');
            } else if (block.character === 'BGM') {
                blockEl.classList.add('bgm-block');
            }

            const blockLeft = block.start_time * pixelsPerSecond;
            const blockWidth = block.duration * pixelsPerSecond;

            blockEl.style.left = `${blockLeft}px`;
            blockEl.style.width = `${blockWidth}px`;

            const icon = block.audio_file ? '🎙️' : (block.character === 'SFX' || block.character === 'BGM' ? '🎵' : '🗣️');
            blockEl.innerHTML = `<span class="block-title">${icon} ${block.character}: ${block.text}</span>`;

            const resizeHandle = document.createElement('div');
            resizeHandle.className = 'resize-handle';
            blockEl.appendChild(resizeHandle);

            blockEl.addEventListener('mousedown', (e) => {
                e.stopPropagation();
                selectBlock(block.id);
                const isResize = e.target.classList.contains('resize-handle');
                initDrag(e, block, isResize ? 'resize' : 'move');
            });

            container.appendChild(blockEl);
        });

        preloadAllAudio();
        totalDurationcode.textContent = formatTimecode(maxTime);
        updateInteractiveMonitor();
    }

    // --- SELECTION & INSPECTOR ---
    function selectBlock(id) {
        selectedBlockId = id;
        const block = timelineData.find(b => b.id === id);

        if (block) {
            blockInspector.style.display = 'block';
            noSelectionMessage.style.display = 'none';

            inspectorCharacter.value = block.character;
            inspectorText.value = block.text;
            inspectorVolume.value = Math.round(block.volume * 100);
            inspectorPan.value = Math.round(block.pan * 100);
            inspectorStartTime.value = block.start_time;

            if (block.image_file && blockImagePreviewThumb && blockImageFilenameLabel && blockImagePreviewContainer) {
                blockImagePreviewThumb.src = block.image_file;
                blockImageFilenameLabel.textContent = block.image_file.split('/').pop();
                blockImagePreviewContainer.style.display = 'flex';
            } else if (blockImagePreviewContainer) {
                blockImagePreviewContainer.style.display = 'none';
            }
        } else {
            blockInspector.style.display = 'none';
            noSelectionMessage.style.display = 'block';
        }

        document.querySelectorAll('.timeline-block').forEach(el => {
            el.classList.remove('active-block');
        });
        renderTimeline();
    }

    inspectorCharacter.addEventListener('change', (e) => {
        const block = timelineData.find(b => b.id === selectedBlockId);
        if (block) {
            block.character = e.target.value;
            markTimelineAsModified();
            renderTimeline();
            logEvent(`Speaker mapping modified: ${block.character}`);
        }
    });

    inspectorText.addEventListener('input', (e) => {
        const block = timelineData.find(b => b.id === selectedBlockId);
        if (block) {
            block.text = e.target.value;
            if (block.character !== 'SFX' && block.character !== 'BGM') {
                block.duration = Math.max(1.5, Math.min(10.0, e.target.value.length / 6.0));
            }
            markTimelineAsModified();
            renderTimeline();
        }
    });

    inspectorVolume.addEventListener('input', (e) => {
        const block = timelineData.find(b => b.id === selectedBlockId);
        if (block) {
            block.volume = parseFloat(e.target.value) / 100;
            markTimelineAsModified();
        }
    });

    inspectorPan.addEventListener('input', (e) => {
        const block = timelineData.find(b => b.id === selectedBlockId);
        if (block) {
            block.pan = parseFloat(e.target.value) / 100;
            markTimelineAsModified();
        }
    });

    inspectorStartTime.addEventListener('change', (e) => {
        const block = timelineData.find(b => b.id === selectedBlockId);
        if (block) {
            let t = parseFloat(e.target.value);
            if (isNaN(t) || t < 0) t = 0;
            block.start_time = Math.round(t * 10) / 10;
            e.target.value = block.start_time;
            markTimelineAsModified();
            renderTimeline();
        }
    });

    deleteBlockBtn.addEventListener('click', () => {
        if (!selectedBlockId) return;
        timelineData = timelineData.filter(b => b.id !== selectedBlockId);
        if (audioCache[selectedBlockId]) {
            audioCache[selectedBlockId].pause();
            delete audioCache[selectedBlockId];
        }
        markTimelineAsModified();
        selectedBlockId = null;
        selectBlock(null);
        logEvent('Timeline block removed.');
    });

    addBlockBtn.addEventListener('click', () => {
        let nextStart = 0.0;
        if (timelineData.length > 0) {
            const maxEnd = Math.max(...timelineData.map(b => b.start_time + b.duration));
            nextStart = Math.round(maxEnd * 10) / 10;
        }

        const firstChar = registeredTracks.find(t => t.type === 'character');
        if (!firstChar) {
            alert("Please add a character track first!");
            return;
        }

        const newBlock = {
            id: Date.now().toString(),
            character: firstChar.name,
            text: "New Dialogue Block",
            volume: 1.0,
            pan: 0.0,
            start_time: nextStart,
            duration: 3.0
        };
        markTimelineAsModified();
        timelineData.push(newBlock);
        selectBlock(newBlock.id);
        logEvent('Dialogue block added.');
    });

    // Helper to switch preview to draft when timeline changes
    function markTimelineAsModified() {
        if (compiledVideoLoaded) {
            compiledVideoLoaded = false;
            stopPlayback();
            videoPlayer.style.display = 'none';
            videoPlayer.src = '';
            introVisual.style.display = 'flex';
            introVisual.style.opacity = '1';
            logEvent("Timeline edited. Preview monitor switched to Draft compositing mode.");
        }
    }

    if (loadDemoBtn) {
        loadDemoBtn.addEventListener('click', () => {
            stopPlayback();
            
            registeredTracks = [
                { name: 'Krishna', type: 'character' },
                { name: 'Sultan', type: 'character' },
                { name: 'SFX', type: 'sfx' },
                { name: 'BGM', type: 'bgm' }
            ];

            timelineData = [
                { id: 'demo_1', character: "Krishna", text: "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਸੁਲਤਾਨਾ! ਕੀ ਹਾਲ ਚਾਲ ਨੇ?", volume: 1.0, pan: -0.2, start_time: 1.0, duration: 4.0 },
                { id: 'demo_2', character: "SFX", text: "peacock", volume: 0.8, pan: 0.5, start_time: 2.0, duration: 3.0 },
                { id: 'demo_3', character: "Sultan", text: "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਭਰਾਵਾ, ਸਭ ਵਧੀਆ! ਤੂੰ ਦੱਸ, ਖੂਹ 'ਤੇ ਕਿਵੇਂ ਗੇੜਾ ਮਾਰਿਆ?", volume: 1.0, pan: 0.2, start_time: 5.5, duration: 5.5 },
                { id: 'demo_4', character: "BGM", text: "flute", volume: 0.25, pan: 0.0, start_time: 0.0, duration: 12.0 }
            ];
            
            markTimelineAsModified();
            selectedBlockId = 'demo_1';
            rebuildEditorUI();
            selectBlock(selectedBlockId);
            logEvent('Demo timeline template loaded successfully.');
        });
    }

    clearTimelineBtn.addEventListener('click', () => {
        stopPlayback();
        markTimelineAsModified();
        timelineData = [];
        selectedBlockId = null;
        selectBlock(null);
        logEvent('Timeline cleared.');
    });

    zoomSlider.addEventListener('input', (e) => {
        pixelsPerSecond = parseInt(e.target.value);
        renderTimeline();
    });

    // --- DRAG / RESIZE LOGIC ---
    let dragBlock = null;
    let dragMode = null;
    let dragStartX = 0;
    let initialStart = 0;
    let initialDuration = 0;

    function initDrag(e, block, mode) {
        dragBlock = block;
        dragMode = mode;
        dragStartX = e.clientX;
        initialStart = block.start_time;
        initialDuration = block.duration;

        document.addEventListener('mousemove', handleDrag);
        document.addEventListener('mouseup', endDrag);
    }

    function handleDrag(e) {
        if (!dragBlock) return;
        const deltaX = e.clientX - dragStartX;
        const timeDelta = deltaX / pixelsPerSecond;

        if (dragMode === 'move') {
            let newStart = initialStart + timeDelta;
            if (newStart < 0) newStart = 0;
            dragBlock.start_time = Math.round(newStart * 10) / 10;
            if (dragBlock.id === selectedBlockId) {
                inspectorStartTime.value = dragBlock.start_time;
            }
        } else if (dragMode === 'resize') {
            let newDuration = initialDuration + timeDelta;
            if (newDuration < 0.5) newDuration = 0.5;
            dragBlock.duration = Math.round(newDuration * 10) / 10;
        }
        renderTimeline();
    }

    function endDrag() {
        document.removeEventListener('mousemove', handleDrag);
        document.removeEventListener('mouseup', endDrag);
        dragBlock = null;
        dragMode = null;
        markTimelineAsModified();
        logEvent('Block bounds updated.');
    }

    // --- PLAYHEAD SCRUBBING ---
    scrollingRuler.addEventListener('mousedown', (e) => {
        scrub(e);
        document.addEventListener('mousemove', scrub);
        document.addEventListener('mouseup', endScrub);
    });

    function scrub(e) {
        const rect = scrollingRuler.getBoundingClientRect();
        const offsetX = e.clientX - rect.left;
        playheadTime = Math.max(0, offsetX / pixelsPerSecond);
        
        if (compiledVideoLoaded) {
            videoPlayer.currentTime = playheadTime;
        } else {
            Object.values(audioCache).forEach(aud => {
                aud.pause();
                aud.currentTime = 0;
            });
        }

        updatePlayheadUI();
        updateInteractiveMonitor();
    }

    function endScrub() {
        document.removeEventListener('mousemove', scrub);
        document.removeEventListener('mouseup', endScrub);
        logEvent(`Playhead scrubbed to ${playheadTime.toFixed(2)}s`);
    }

    function updatePlayheadUI() {
        playhead.style.left = `${(playheadTime * pixelsPerSecond) + 120}px`;
        currentPlaycode.textContent = formatTimecode(playheadTime);
    }

    // --- DYNAMIC PREVIEW MONITOR SYNCHRONIZER (GENERIC) ---
    function updateInteractiveMonitor() {
        // 1. Update background preset image based on prompt input
        const promptText = (backgroundPromptInput ? backgroundPromptInput.value : "").toLowerCase();
        let imageFile = 'khu.jpg';
        if (promptText.includes('custom_bg') || promptText.includes('images/custom_bg')) {
            const cleanUrl = promptText.split('?')[0];
            imageFile = cleanUrl.split('/').pop();
        } else if (promptText.includes('talab') || promptText.includes('pond') || promptText.includes('ਤਲਾਬ')) {
            imageFile = 'talab.jpg';
        } else if (promptText.includes('field') || promptText.includes('khet') || promptText.includes('ਖੇਤ') || promptText.includes('wheat')) {
            imageFile = 'field.jpg';
        }
        previewScreen.style.backgroundImage = `url('images/${imageFile}')`;

        // 2. Identify active dialogue and SFX blocks
        let activeDialogue = null;
        let activeSFX = null;

        timelineData.forEach(block => {
            const isInside = (playheadTime >= block.start_time && playheadTime <= block.start_time + block.duration);
            if (isInside) {
                if (block.character === 'SFX') {
                    activeSFX = block;
                } else if (block.character !== 'BGM') {
                    activeDialogue = block;
                }
            }
        });

        // 2b. Overlay block storyboard image if defined
        if (activeDialogue && activeDialogue.image_file) {
            previewScreen.style.backgroundImage = `url('${activeDialogue.image_file}')`;
        }

        // 3. Render Avatars dynamically based on speaking state
        if (activeDialogue) {
            const name = activeDialogue.character;
            avatarContainer.innerHTML = `
                <div class="toon-avatar-wrapper active-speaker" style="display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 110px; height: 110px; border-radius: 50%; border: 3px solid #fbbf24; box-shadow: 0 0 25px rgba(251,191,36,0.8); background: #111827; display: flex; align-items: center; justify-content: center; overflow: hidden; animation: speaker-bounce 0.5s infinite alternate;">
                        <img src="images/${name.toLowerCase()}.jpg" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                        <span style="display: none; color: #fbbf24; font-size: 2.2rem; font-weight: 800;">${name[0].toUpperCase()}</span>
                    </div>
                    <span style="color: white; font-weight: 600; font-size: 0.85rem; margin-top: 5px; background: rgba(0,0,0,0.6); padding: 2px 8px; border-radius: 10px;">${name}</span>
                </div>
            `;
        } else {
            avatarContainer.innerHTML = '';
        }

        // 4. Update Subtitles Bubble
        if (activeDialogue) {
            subtitleBubble.textContent = `${activeDialogue.character}: "${activeDialogue.text}"`;
            subtitleBubble.style.display = 'block';
        } else {
            subtitleBubble.style.display = 'none';
        }

        // 5. Update SFX Overlays
        if (activeSFX) {
            sfxOverlay.innerHTML = `🔊 SFX: ${activeSFX.text.toUpperCase()}`;
            sfxOverlay.style.display = 'flex';
        } else {
            sfxOverlay.style.display = 'none';
        }
    }

    const bgPresets = ['Village Well (ਤੂਤਾਂ ਵਾਲਾ ਖੂਹ)', 'Village Pond (ਪਿੰਡ ਦਾ ਤਲਾਬ)', 'Wheat Field (ਕਣਕ ਦਾ ਖੇਤ)'];
    let currentBgIndex = 0;

    if (backgroundPromptInput) {
        backgroundPromptInput.addEventListener('input', updateInteractiveMonitor);
    }
    if (generateSceneBtn) {
        generateSceneBtn.addEventListener('click', updateInteractiveMonitor);
    }



    // Interpolated volume between keyframes helper
    function getInterpolatedVolume(trackName, time) {
        const kfs = trackKeyframes[trackName];
        const defaultVol = trackVolumes[trackName] !== undefined ? trackVolumes[trackName] : 0.8;
        if (!kfs || kfs.length === 0) {
            return defaultVol;
        }
        if (time <= kfs[0].time) {
            return kfs[0].volume;
        }
        if (time >= kfs[kfs.length - 1].time) {
            return kfs[kfs.length - 1].volume;
        }
        for (let i = 0; i < kfs.length - 1; i++) {
            const k1 = kfs[i];
            const k2 = kfs[i + 1];
            if (time >= k1.time && time <= k2.time) {
                const ratio = (time - k1.time) / (k2.time - k1.time);
                return k1.volume + ratio * (k2.volume - k1.volume);
            }
        }
        return defaultVol;
    }

    // Mute / Solo check helper
    function isTrackAllowedToPlay(trackName) {
        if (mutedTracks[trackName]) return false;
        const anySoloActive = Object.values(soloTracks).some(v => v === true);
        if (anySoloActive) {
            return soloTracks[trackName] === true;
        }
        return true;
    }

    // --- BROWSER PLAYBACK SCHEDULER ---
    function startPlayback() {
        if (isPlaying) return;
        isPlaying = true;
        playBtn.textContent = '⏸️ Pause';
        lastFrameTime = performance.now();
        
        if (compiledVideoLoaded) {
            videoPlayer.play().catch(e => console.log("Video playback deferred", e));
        } else {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
        }

        animationFrameId = requestAnimationFrame(playbackLoop);
        logEvent('Playback started.');
    }

    function pausePlayback() {
        if (!isPlaying) return;
        isPlaying = false;
        playBtn.textContent = '⏯️ Play';
        cancelAnimationFrame(animationFrameId);
        
        if (compiledVideoLoaded) {
            videoPlayer.pause();
        } else {
            Object.values(audioCache).forEach(aud => aud.pause());
        }
        logEvent('Playback paused.');
    }

    function stopPlayback() {
        pausePlayback();
        playheadTime = 0.0;
        updatePlayheadUI();
        updateInteractiveMonitor();
        
        if (compiledVideoLoaded) {
            videoPlayer.pause();
            videoPlayer.currentTime = 0;
        } else {
            Object.values(audioCache).forEach(aud => {
                aud.pause();
                aud.currentTime = 0;
            });
        }
        logEvent('Playback stopped.');
    }

    function playbackLoop(now) {
        if (!isPlaying) return;

        if (compiledVideoLoaded) {
            playheadTime = videoPlayer.currentTime;
            if (videoPlayer.ended) {
                stopPlayback();
                return;
            }
            updatePlayheadUI();
            updateInteractiveMonitor();
        } else {
            const delta = (now - lastFrameTime) / 1000;
            lastFrameTime = now;
            
            const oldTime = playheadTime;
            playheadTime += delta;
            
            let maxTime = 12.0;
            timelineData.forEach(block => {
                const end = block.start_time + block.duration;
                if (end > maxTime) maxTime = end;
            });
            if (playheadTime > maxTime) {
                stopPlayback();
                return;
            }

            updatePlayheadUI();
            updateInteractiveMonitor();

            // Audio Trigger Scheduler
            timelineData.forEach(block => {
                const aud = audioCache[block.id];
                if (!aud) return;

                const allowed = isTrackAllowedToPlay(block.character);

                if (oldTime <= block.start_time && playheadTime > block.start_time) {
                    if (allowed) {
                        const masterVol = getInterpolatedVolume(block.character, playheadTime);
                        aud.volume = block.volume * masterVol;
                        aud.currentTime = 0;
                        aud.play().catch(e => console.log("Audio trigger deferred", e));
                    } else {
                        aud.volume = 0;
                    }
                }
                
                if (oldTime < block.start_time + block.duration && playheadTime >= block.start_time + block.duration) {
                    aud.pause();
                }
            });
        }

        animationFrameId = requestAnimationFrame(playbackLoop);
    }

    playBtn.addEventListener('click', () => {
        if (isPlaying) {
            pausePlayback();
        } else {
            startPlayback();
        }
    });

    stopBtn.addEventListener('click', stopPlayback);
    rewindBtn.addEventListener('click', () => {
        playheadTime = 0.0;
        updatePlayheadUI();
        updateInteractiveMonitor();
        Object.values(audioCache).forEach(aud => {
            aud.pause();
            aud.currentTime = 0;
        });
    });

    // --- AI SCRIPT GENERATOR (GENERIC INTERFACE) ---
    if (aiGenerateBtn) {
        aiGenerateBtn.addEventListener('click', async () => {
            const promptVal = aiPrompt.value.trim();
            const themeVal = aiTheme.value;

            statusMessage.textContent = "🧠 AI generating story script...";
            statusMessage.style.color = "#a855f7";
            aiGenerateBtn.disabled = true;
            logEvent(`AI script request sent for theme: ${themeVal}`);

            try {
                const res = await fetch('/api/generate_script', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        prompt: promptVal,
                        theme: themeVal,
                        model: aiModel ? aiModel.value : "Offline Templates"
                    })
                });

                if (res.ok) {
                    const data = await res.json();
                    
                    // Keep timeline data structure mapping, translate track lanes if they don't exist
                    timelineData = data.timeline;
                    
                    // Add characters dynamically if missing from script response
                    timelineData.forEach(b => {
                        if (!registeredTracks.some(t => t.name === b.character)) {
                            registeredTracks.push({ name: b.character, type: 'character' });
                        }
                    });

                    markTimelineAsModified();
                    storyInput.value = timelineData.map(b => `${b.character}: ${b.text}`).join('\n');
                    rebuildEditorUI();

                    if (timelineData.length > 0) {
                        selectedBlockId = timelineData[0].id;
                        selectBlock(selectedBlockId);
                    } else {
                        selectedBlockId = null;
                        selectBlock(null);
                    }

                    statusMessage.textContent = "✅ AI Script loaded on timeline!";
                    statusMessage.style.color = "#10b981";
                    logEvent('Script loaded.');
                } else {
                    const errData = await res.json();
                    statusMessage.textContent = "❌ AI Generation failed.";
                    statusMessage.style.color = "#ef4444";
                }
            } catch (err) {
                statusMessage.textContent = "❌ Server connection failure.";
                statusMessage.style.color = "#ef4444";
            } finally {
                aiGenerateBtn.disabled = false;
            }
        });
    }

    // --- TIMELINE EXPORT & COMPILATION ---
    if (processButton) {
        processButton.addEventListener('click', async () => {
            if (timelineData.length === 0) {
                statusMessage.textContent = "❌ Please add dialogue blocks first.";
                statusMessage.style.color = "#ef4444";
                return;
            }

            statusMessage.textContent = "🧠 Processing MoviePy compilation...";
            statusMessage.style.color = "#fbbf24";
            processButton.disabled = true;
            consoleBox.style.display = "block";
            consoleLogs.textContent = "🚀 Compiling video using dynamic track compositions...\n";

            try {
                const payload = {
                    timeline: timelineData.map(b => ({
                        character: b.character,
                        text: b.text,
                        volume: b.volume * (trackVolumes[b.character] !== undefined ? trackVolumes[b.character] : 0.8),
                        pan: b.pan,
                        start_time: b.start_time,
                        audio_file: b.audio_file || null,
                        image_file: b.image_file || null
                    })),
                    background_preset: backgroundPromptInput ? backgroundPromptInput.value : "khu",
                    sfx_preset: sfxSelector.value,
                    ducking: aiAudioEnhancement ? aiAudioEnhancement.checked : true,
                    mastering: true,
                    voice_cloning: aiVoiceCloning ? aiVoiceCloning.checked : true,
                    subtitles: aiSubtitleGeneration ? aiSubtitleGeneration.checked : true,
                    color_grading: aiColorGrading ? aiColorGrading.value : "Standard",
                    keyframes: trackKeyframes
                };

                const res = await fetch('/api/process_timeline', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (res.ok) {
                    const data = await res.json();
                    consoleLogs.textContent = data.logs;
                    introVisual.style.opacity = '0';
                    setTimeout(() => {
                        introVisual.style.display = 'none';
                        videoPlayer.style.display = 'block';
                        videoPlayer.controls = false;
                        videoPlayer.src = `${data.video_url}?t=${new Date().getTime()}`;
                        videoPlayer.load();
                        
                        compiledVideoLoaded = true;
                        playheadTime = 0.0;
                        updatePlayheadUI();
                        updateInteractiveMonitor();
                        
                        startPlayback();
                    }, 500);

                    statusMessage.textContent = "✅ Compilation success!";
                    statusMessage.style.color = "#10b981";
                    logEvent('Movie exported.');
                } else {
                    const errData = await res.json();
                    consoleLogs.textContent += `\n❌ Error: ${errData.detail || 'Internal server error'}`;
                    statusMessage.textContent = "❌ Compiler failed.";
                    statusMessage.style.color = "#ef4444";
                }
            } catch (err) {
                consoleLogs.textContent += `\n❌ Request Error: ${err.message}`;
                statusMessage.textContent = "❌ Server error.";
                statusMessage.style.color = "#ef4444";
            } finally {
                processButton.disabled = false;
            }
        });
    }

    // --- VOICE RECORDING HELPER ---
    async function startRecordingFlow() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };
        mediaRecorder.start();
        logEvent("Recording voiceover stream...");
    }

    async function stopRecordingAndUpload(blockId, callback) {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') return;
        
        mediaRecorder.onstop = async () => {
            statusMessage.textContent = "💾 Uploading audio file...";
            statusMessage.style.color = "#fbbf24";
            
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('block_id', blockId);
            formData.append('file', audioBlob, `rec_${blockId}.wav`);

            try {
                const uploadRes = await fetch('/api/upload_recording', {
                    method: 'POST',
                    body: formData
                });
                if (uploadRes.ok) {
                    const data = await uploadRes.json();
                    callback(data);
                } else {
                    const errData = await uploadRes.json();
                    alert(`Upload failed: ${errData.detail}`);
                }
            } catch (err) {
                alert("Upload connection failure");
            }
        };
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }

    // A. Inspector Block recording listeners
    if (blockMicRecordBtn && blockMicStopBtn) {
        blockMicRecordBtn.addEventListener('click', async () => {
            if (!selectedBlockId) return;
            try {
                await startRecordingFlow();
                blockMicRecordBtn.disabled = true;
                blockMicStopBtn.disabled = false;
                statusMessage.textContent = "🔴 Recording block-specific voiceover...";
                statusMessage.style.color = "#ef4444";
            } catch (err) {
                alert("Microphone stream failed!");
            }
        });

        blockMicStopBtn.addEventListener('click', async () => {
            blockMicRecordBtn.disabled = false;
            blockMicStopBtn.disabled = true;
            await stopRecordingAndUpload(selectedBlockId, (data) => {
                const block = timelineData.find(b => b.id === selectedBlockId);
                if (block) {
                    block.audio_file = data.audio_file;
                    audioCache[block.id] = new Audio(data.url);
                    audioCache[block.id].load();
                    logEvent(`Saved mic override for block: ${block.id}`);
                    statusMessage.textContent = "✅ Voiceover saved!";
                    statusMessage.style.color = "#10b981";
                    renderTimeline();
                }
            });
        });
    }

    // B. Global record buttons
    if (globalMicRecordBtn && globalMicStopBtn) {
        globalMicRecordBtn.addEventListener('click', async () => {
            try {
                await startRecordingFlow();
                globalMicRecordBtn.disabled = true;
                globalMicStopBtn.disabled = false;
                statusMessage.textContent = "🔴 Recording custom global voiceover clip...";
                statusMessage.style.color = "#ef4444";
            } catch (err) {
                alert("Microphone stream failed!");
            }
        });

        globalMicStopBtn.addEventListener('click', async () => {
            globalMicRecordBtn.disabled = false;
            globalMicStopBtn.disabled = true;
            
            const transcript = prompt("Type script dialogue spoken:", "Hello!");
            if (!transcript) {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
                logEvent("Recording aborted.");
                statusMessage.textContent = "🔴 Recording aborted.";
                statusMessage.style.color = "#fbbf24";
                return;
            }

            const tempBlockId = 'rec_' + Date.now();
            await stopRecordingAndUpload(tempBlockId, (data) => {
                const newBlock = {
                    id: tempBlockId,
                    character: globalRecTrack.value,
                    text: transcript,
                    volume: 1.0,
                    pan: 0.0,
                    start_time: Math.round(playheadTime * 10) / 10,
                    duration: 3.5,
                    audio_file: data.audio_file
                };
                timelineData.push(newBlock);
                audioCache[newBlock.id] = new Audio(data.url);
                audioCache[newBlock.id].load();
                
                logEvent(`Created mic block at ${newBlock.start_time}s on ${newBlock.character} track.`);
                statusMessage.textContent = "✅ Voiceover block inserted!";
                statusMessage.style.color = "#10b981";
                selectBlock(newBlock.id);
            });
        });
    }

    // --- AI BRAINSTORMING CHAT CONTROLLERS ---
    const switchMonitorBtn = document.getElementById('switch-monitor-btn');
    const aiChatBoard = document.getElementById('ai-chat-board');
    const chatMessagesContainer = document.getElementById('chat-messages-container');
    const chatInputField = document.getElementById('chat-input-field');
    const chatVoiceBtn = document.getElementById('chat-voice-btn');
    const chatSendBtn = document.getElementById('chat-send-btn');

    let chatHistory = [
        { role: 'ai', content: "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਏ.ਆਈ. ਕਹਾਣੀਕਾਰ ਹਾਂ। ਅੱਜ ਅਸੀਂ ਕਿਸ ਵਿਸ਼ੇ 'ਤੇ ਕਹਾਣੀ ਬਣਾਈਏ? ਤੁਸੀਂ ਮਾਈਕ੍ਰੋਫੋਨ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਮੇਰੇ ਨਾਲ ਗੱਲ ਵੀ ਕਰ ਸਕਦੇ ਹੋ!" }
    ];

    function renderChatMessages() {
        if (!chatMessagesContainer) return;
        chatMessagesContainer.innerHTML = '';
        chatHistory.forEach(msg => {
            const bubble = document.createElement('div');
            bubble.className = `chat-bubble ${msg.role}`;
            bubble.textContent = msg.content;
            chatMessagesContainer.appendChild(bubble);
        });
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }

    // Toggle Preview Monitor vs AI Chat Room
    if (switchMonitorBtn && aiChatBoard) {
        switchMonitorBtn.addEventListener('click', () => {
            const isVisible = aiChatBoard.style.display !== 'none';
            if (isVisible) {
                aiChatBoard.style.display = 'none';
                switchMonitorBtn.textContent = '💬 Brainstorm Chat';
                switchMonitorBtn.style.background = 'linear-gradient(135deg, #a855f7, #7e22ce)';
                switchMonitorBtn.style.color = 'white';
            } else {
                stopPlayback();
                aiChatBoard.style.display = 'flex';
                switchMonitorBtn.textContent = '📺 Preview Monitor';
                switchMonitorBtn.style.background = 'rgba(255,255,255,0.08)';
                switchMonitorBtn.style.color = '#e5e7eb';
                renderChatMessages();
            }
        });
    }

    async function sendChatMessage(text) {
        if (!text.trim()) return;
        
        chatHistory.push({ role: 'user', content: text });
        renderChatMessages();
        chatInputField.value = '';

        chatHistory.push({ role: 'ai', content: "ਏ.ਆਈ ਵਿਚਾਰ ਕਰ ਰਿਹਾ ਹੈ... 🧠" });
        renderChatMessages();

        try {
            const res = await fetch('/api/chat_brainstorm', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    chat_history: chatHistory.slice(0, -1),
                    current_timeline: timelineData,
                    model: aiModel ? aiModel.value : "Offline Templates"
                })
            });

            chatHistory.pop();

            if (res.ok) {
                const data = await res.json();
                chatHistory.push({ role: 'ai', content: data.reply });
                
                if (data.timeline && Array.isArray(data.timeline)) {
                    timelineData = data.timeline;
                    markTimelineAsModified();
                    
                    timelineData.forEach(b => {
                        if (!registeredTracks.some(t => t.name === b.character)) {
                            registeredTracks.push({ name: b.character, type: 'character' });
                        }
                    });
                    
                    storyInput.value = timelineData.map(b => `${b.character}: ${b.text}`).join('\n');
                    rebuildEditorUI();
                    
                    chatHistory.push({ role: 'system', content: "🔔 [ਸਿਸਟਮ]: ਟਾਈਮਲਾਈਨ ਸਕ੍ਰਿਪਟ ਅਪਡੇਟ ਹੋ ਗਈ ਹੈ!" });
                }
            } else {
                chatHistory.push({ role: 'ai', content: "ਮਾਫ਼ ਕਰਨਾ, ਸਰਵਰ ਨਾਲ ਸੰਪਰਕ ਕਰਨ ਵਿੱਚ ਅਸਫਲ।" });
            }
        } catch (err) {
            chatHistory.pop();
            chatHistory.push({ role: 'ai', content: "ਨੈੱਟਵਰਕ ਵਿੱਚ ਸਮੱਸਿਆ ਆਈ ਹੈ।" });
        }
        renderChatMessages();
    }

    if (chatSendBtn && chatInputField) {
        chatSendBtn.addEventListener('click', () => {
            sendChatMessage(chatInputField.value);
        });
        chatInputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendChatMessage(chatInputField.value);
            }
        });
    }

    // --- PUNJABI SPEECH RECOGNITION (WEB SPEECH API) ---
    let recognition = null;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.lang = 'pa-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            chatVoiceBtn.textContent = '🎤 ਸੁਣ ਰਿਹਾ...';
            chatVoiceBtn.style.background = '#dc2626';
            logEvent("Punjabi speech recognition listening...");
        };

        recognition.onresult = (e) => {
            const transcript = e.results[0][0].transcript;
            chatInputField.value = transcript;
            logEvent(`Recognized speech: "${transcript}"`);
            sendChatMessage(transcript);
        };

        recognition.onerror = () => {
            logEvent("Speech recognition encountered an error.");
        };

        recognition.onend = () => {
            chatVoiceBtn.textContent = '🎤 ਮਾਈਕ';
            chatVoiceBtn.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
        };

        if (chatVoiceBtn) {
            chatVoiceBtn.addEventListener('click', () => {
                recognition.start();
            });
        }
    } else {
        if (chatVoiceBtn) {
            chatVoiceBtn.title = "Web Speech API not supported in this browser";
            chatVoiceBtn.addEventListener('click', () => {
                alert("Speech recognition is only supported in Google Chrome / WebKit browsers.");
            });
        }
    }

    // --- CUSTOM BACKGROUND PHOTO UPLOADER ---
    if (bgUploadBtn && bgUploadInput) {
        bgUploadBtn.addEventListener('click', () => {
            bgUploadInput.click();
        });

        bgUploadInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            statusMessage.textContent = "📤 Uploading custom background image...";
            statusMessage.style.color = "#fbbf24";
            
            const formData = new FormData();
            formData.append('file', file);

            try {
                const res = await fetch('/api/upload_background', {
                    method: 'POST',
                    body: formData
                });

                if (res.ok) {
                    const data = await res.json();
                    if (backgroundPromptInput) {
                        backgroundPromptInput.value = `${data.url}?t=${Date.now()}`;
                    }
                    statusMessage.textContent = "✅ Custom background uploaded!";
                    statusMessage.style.color = "#10b981";
                    logEvent("Custom background photo updated.");
                    updateInteractiveMonitor();
                } else {
                    statusMessage.textContent = "❌ Background upload failed.";
                    statusMessage.style.color = "#ef4444";
                }
            } catch (err) {
                statusMessage.textContent = "❌ Server upload error.";
                statusMessage.style.color = "#ef4444";
            }
        });
    }

    // --- DIALOGUE BLOCK CUSTOM STORYBOARD PHOTO UPLOADER ---
    if (blockImageUploadBtn && blockImageUploadInput) {
        blockImageUploadBtn.addEventListener('click', () => {
            blockImageUploadInput.click();
        });

        blockImageUploadInput.addEventListener('change', async (e) => {
            if (!selectedBlockId) return;
            const file = e.target.files[0];
            if (!file) return;

            statusMessage.textContent = "📤 Uploading storyboard image for block...";
            statusMessage.style.color = "#fbbf24";

            const formData = new FormData();
            formData.append('file', file);

            try {
                const res = await fetch(`/api/upload_block_image?block_id=${selectedBlockId}`, {
                    method: 'POST',
                    body: formData
                });

                if (res.ok) {
                    const data = await res.json();
                    const block = timelineData.find(b => b.id === selectedBlockId);
                    if (block) {
                        block.image_file = `${data.url}?t=${Date.now()}`;
                        markTimelineAsModified();
                        
                        if (blockImagePreviewThumb && blockImageFilenameLabel && blockImagePreviewContainer) {
                            blockImagePreviewThumb.src = block.image_file;
                            blockImageFilenameLabel.textContent = file.name;
                            blockImagePreviewContainer.style.display = 'flex';
                        }
                        
                        statusMessage.textContent = "✅ Storyboard photo saved for block!";
                        statusMessage.style.color = "#10b981";
                        logEvent(`Uploaded custom storyboard frame for block: ${selectedBlockId}`);
                        updateInteractiveMonitor();
                    }
                } else {
                    statusMessage.textContent = "❌ Block image upload failed.";
                    statusMessage.style.color = "#ef4444";
                }
            } catch (err) {
                statusMessage.textContent = "❌ Server upload error.";
                statusMessage.style.color = "#ef4444";
            }
        });
    }

    if (blockImageClearBtn) {
        blockImageClearBtn.addEventListener('click', () => {
            if (!selectedBlockId) return;
            const block = timelineData.find(b => b.id === selectedBlockId);
            if (block) {
                delete block.image_file;
                markTimelineAsModified();
                if (blockImagePreviewContainer) {
                    blockImagePreviewContainer.style.display = 'none';
                }
                statusMessage.textContent = "🗑️ Block storyboard photo cleared.";
                statusMessage.style.color = "#fbbf24";
                logEvent(`Cleared custom storyboard frame for block: ${selectedBlockId}`);
                updateInteractiveMonitor();
            }
        });
    }

    // --- AI CHARACTER CREATOR GENERATOR EVENT ---
    if (aiCharGenerateBtn && aiCharPrompt) {
        aiCharGenerateBtn.addEventListener('click', async () => {
            const promptVal = aiCharPrompt.value.trim();
            if (!promptVal) {
                alert("Please enter a character prompt description!");
                return;
            }

            const charName = prompt("Enter a name for the new AI character:", "Simran");
            if (!charName) return;

            statusMessage.textContent = "🎨 AI is painting your character...";
            statusMessage.style.color = "#fbbf24";
            aiCharGenerateBtn.disabled = true;

            try {
                const res = await fetch('/api/generate_character', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: promptVal,
                        name: charName
                    })
                });

                if (res.ok) {
                    const data = await res.json();
                    
                    if (!registeredTracks.some(t => t.name === data.character_name)) {
                        registeredTracks.push({ name: data.character_name, type: 'character' });
                    }
                    trackVolumes[data.character_name] = 0.8;
                    
                    statusMessage.textContent = `✅ AI Character "${data.character_name}" created!`;
                    statusMessage.style.color = "#10b981";
                    logEvent(`AI Character created: ${data.character_name}`);
                    aiCharPrompt.value = '';
                    
                    rebuildEditorUI();
                } else {
                    statusMessage.textContent = "❌ Character generation failed.";
                    statusMessage.style.color = "#ef4444";
                }
            } catch (err) {
                statusMessage.textContent = "❌ Server error generating character.";
                statusMessage.style.color = "#ef4444";
            } finally {
                aiCharGenerateBtn.disabled = false;
            }
        });
    }

    // Initial boot
    rebuildEditorUI();
    renderChatMessages();
});
