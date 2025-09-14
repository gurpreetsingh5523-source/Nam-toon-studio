
// Simple Naam Tone Studio using WebAudio + MediaRecorder for download
let ctx, osc, gainNode, dest, mediaRec;
const freq = document.getElementById('freq');
const vol = document.getElementById('vol');
const wave = document.getElementById('wave');
const playBtn = document.getElementById('play');
const stopBtn = document.getElementById('stop');
const recordBtn = document.getElementById('record');
const status = document.getElementById('status');
const preview = document.getElementById('preview');
const freqVal = document.getElementById('freqVal');
const volVal = document.getElementById('volVal');

freq.addEventListener('input', ()=> freqVal.textContent = freq.value);
vol.addEventListener('input', ()=> volVal.textContent = vol.value);

function ensureContext(){
  if(!ctx){
    ctx = new (window.AudioContext || window.webkitAudioContext)();
  }
}

playBtn.addEventListener('click', async ()=>{
  ensureContext();
  osc = ctx.createOscillator();
  gainNode = ctx.createGain();
  osc.type = wave.value;
  osc.frequency.value = Number(freq.value);
  gainNode.gain.value = Number(vol.value);
  osc.connect(gainNode);
  gainNode.connect(ctx.destination);
  // also connect to a MediaStreamDestination for recording
  dest = ctx.createMediaStreamDestination();
  gainNode.connect(dest);
  osc.start();
  playBtn.disabled = true;
  stopBtn.disabled = false;
  status.textContent = "ਚਲ ਰਿਹਾ ਹੈ…";
});

stopBtn.addEventListener('click', ()=>{
  if(osc){
    try{ osc.stop(); } catch(e){}
    osc.disconnect();
    gainNode.disconnect();
    playBtn.disabled = false;
    stopBtn.disabled = true;
    status.textContent = "ਰੁਕਿਆ ਹੋਇਆ।";
  }
});

recordBtn.addEventListener('click', async ()=>{
  ensureContext();
  // If nothing playing, create a short sample to record
  if(!dest){
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = wave.value;
    o.frequency.value = Number(freq.value);
    g.gain.value = Number(vol.value);
    o.connect(g);
    const d = ctx.createMediaStreamDestination();
    g.connect(d);
    o.start();
    const mr = new MediaRecorder(d.stream);
    const chunks=[];
    mr.ondataavailable = e => chunks.push(e.data);
    mr.onstop = ()=>{
      const blob = new Blob(chunks, {type: 'audio/webm'});
      preview.src = URL.createObjectURL(blob);
      preview.style.display = "block";
      const a = document.createElement('a');
      a.href = preview.src;
      a.download = 'naam-tone.webm';
      a.click();
    };
    mr.start();
    setTimeout(()=>{
      mr.stop();
      o.stop();
    }, 2000);
    return;
  }
  mediaRec = new MediaRecorder(dest.stream);
  const chunks = [];
  mediaRec.ondataavailable = e => chunks.push(e.data);
  mediaRec.onstop = ()=>{
    const blob = new Blob(chunks, {type: 'audio/webm'});
    preview.src = URL.createObjectURL(blob);
    preview.style.display = "block";
    const a = document.createElement('a');
    a.href = preview.src;
    a.download = 'naam-tone.webm';
    a.click();
  };
  mediaRec.start();
  status.textContent = "Recording... 3s";
  setTimeout(()=>{
    mediaRec.stop();
    status.textContent = "Recording saved.";
  }, 3000);
});

// Service worker registration for offline
if('serviceWorker' in navigator){
  navigator.serviceWorker.register('/sw.js').then(()=>{
    console.log('SW registered');
  }).catch(()=>{});
}
