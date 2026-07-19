from fastapi import FastAPI, HTTPException, Form, UploadFile, File
import httpx
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import hashlib
from gtts import gTTS
import shutil
import subprocess
import os
import sys
import psutil
import platform

app = FastAPI(title="Nam Toon Studio Backend", description="FastAPI Server for Punjabi Script-to-Video Engine")

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/images", StaticFiles(directory=os.path.join(BASE_DIR, "images")), name="images")
app.mount("/audio", StaticFiles(directory=os.path.join(BASE_DIR, "audio")), name="audio")

from typing import List
import json

class StoryRequest(BaseModel):
    story: str
    background_preset: str = "khu"
    sfx_preset: str = "birds"
    ducking: bool = True
    mastering: bool = True

class TimelineDialogueItem(BaseModel):
    character: str
    text: str
    volume: float = 1.0
    pan: float = 0.0
    start_time: float = 0.0
    audio_file: str = None
    image_file: str = None

class TimelineRequest(BaseModel):
    timeline: List[TimelineDialogueItem]
    background_preset: str = "khu"
    sfx_preset: str = "birds"
    ducking: bool = True
    mastering: bool = True
    voice_cloning: bool = True
    subtitles: bool = True
    color_grading: str = "Standard"
    keyframes: dict = {}

class ScriptGenerateRequest(BaseModel):
    prompt: str = ""
    theme: str = "Friendship"
    model: str = "Offline Templates"

@app.get("/")
def read_root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/styles.css")
def read_css():
    return FileResponse(os.path.join(BASE_DIR, "styles.css"))

@app.get("/app.js")
def read_js():
    return FileResponse(os.path.join(BASE_DIR, "app.js"))

@app.get("/manifest.json")
def read_manifest():
    return FileResponse(os.path.join(BASE_DIR, "manifest.json"))

@app.get("/sw.js")
def read_sw():
    return FileResponse(os.path.join(BASE_DIR, "sw.js"))

@app.get("/icon-192.svg")
def read_icon192():
    return FileResponse(os.path.join(BASE_DIR, "icon-192.svg"))

@app.get("/icon-512.svg")
def read_icon512():
    return FileResponse(os.path.join(BASE_DIR, "icon-512.svg"))

@app.get("/media/AmritCore_FINAL_STUDIO_LAUNCH.mp4")
def get_final_video():
    path = os.path.join(BASE_DIR, "AmritCore_FINAL_STUDIO_LAUNCH.mp4")
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Video file not generated yet")

@app.post("/api/process_story")
async def process_story(
    story: str = Form(...),
    background_preset: str = Form("khu"),
    sfx_preset: str = Form("birds"),
    ducking: bool = Form(True),
    mastering: bool = Form(True)
):
    try:
        # 1. Write story to novel.txt
        novel_path = os.path.join(BASE_DIR, "novel.txt")
        with open(novel_path, "w", encoding="utf-8") as f:
            f.write(story)

        logs = []
        logs.append("📝 Story successfully saved to novel.txt")

        # 2. Run colab/novel_pipeline.py
        python_exec = os.path.join(BASE_DIR, ".venv", "bin", "python")
        if not os.path.exists(python_exec):
            # fallback to global python if virtualenv python isn't found
            python_exec = sys.executable

        logs.append(f"⚙️ Running novel pipeline with: {python_exec}")
        run_pipeline = subprocess.run(
            [python_exec, os.path.join("colab", "novel_pipeline.py")],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        logs.append(run_pipeline.stdout)
        if run_pipeline.stderr:
            logs.append(f"Warnings/Errors: {run_pipeline.stderr}")

        if run_pipeline.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Novel pipeline execution failed: {run_pipeline.stderr}")

        # 3. Resolve background path
        bg_image_filename = f"{background_preset}.jpg"
        bg_image_path = os.path.join(BASE_DIR, "images", bg_image_filename)
        if not os.path.exists(bg_image_path):
            bg_image_path = os.path.join(BASE_DIR, "images", "scene_base.png")

        logs.append(f"🖼️ Resolved background image path: {bg_image_path}")

        # 4. Build builder CLI command
        builder_args = [
            python_exec,
            os.path.join("colab", "master_builder.py"),
            "--scenes", os.path.join("colab", "scenes.json"),
            "--background", bg_image_path,
            "--sfx-preset", sfx_preset
        ]
        if ducking:
            builder_args.append("--duck")
        if mastering:
            builder_args.append("--master")
        builder_args.append("--verbose")

        logs.append(f"🎬 Compiling video clip with: {' '.join(builder_args)}")
        run_builder = subprocess.run(
            builder_args,
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        logs.append(run_builder.stdout)
        if run_builder.stderr:
            logs.append(f"Compiler details: {run_builder.stderr}")

        if run_builder.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Master builder execution failed: {run_builder.stderr}")

        final_video_path = os.path.join(BASE_DIR, "AmritCore_FINAL_STUDIO_LAUNCH.mp4")
        if not os.path.exists(final_video_path):
            raise HTTPException(status_code=500, detail="Compiler succeeded, but AmritCore_FINAL_STUDIO_LAUNCH.mp4 was not created")

        logs.append("🏆 Production compiler success! Video is ready for launch.")
        combined_logs = "\n".join(logs)

        return {
            "status": "success",
            "video_url": "/media/AmritCore_FINAL_STUDIO_LAUNCH.mp4",
            "logs": combined_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process_timeline")
async def process_timeline(request: TimelineRequest):
    try:
        # Convert timeline list to scenes.json format
        scenes_data = {
            "voice_cloning": request.voice_cloning,
            "subtitles": request.subtitles,
            "color_grading": request.color_grading,
            "keyframes": request.keyframes,
            "scenes": [
                {
                    "scene_id": "timeline_scene",
                    "title": "Timeline Scene",
                    "dialogues": [
                        {
                            "character": item.character,
                            "text": item.text,
                            "volume": item.volume,
                            "pan": item.pan,
                            "start_time": item.start_time,
                            "audio_file": item.audio_file,
                            "image_file": item.image_file
                        }
                        for item in request.timeline
                    ]
                }
            ]
        }
        
        # Save to colab/scenes.json
        scenes_path = os.path.join(BASE_DIR, "colab", "scenes.json")
        with open(scenes_path, "w", encoding="utf-8") as f:
            json.dump(scenes_data, f, ensure_ascii=False, indent=2)

        logs = []
        logs.append("📝 Timeline configurations written to colab/scenes.json")

        # Resolve background path based on custom prompt keyword or custom uploaded image
        bg_prompt = request.background_preset.lower()
        bg_image_filename = "khu.jpg"
        if "custom_bg" in bg_prompt or "custom" in bg_prompt:
            if os.path.exists(os.path.join(BASE_DIR, "images", "custom_bg.jpg")):
                bg_image_filename = "custom_bg.jpg"
            elif os.path.exists(os.path.join(BASE_DIR, "images", "custom_bg.png")):
                bg_image_filename = "custom_bg.png"
        elif "talab" in bg_prompt or "pond" in bg_prompt or "ਤਲਾਬ" in bg_prompt:
            bg_image_filename = "talab.jpg"
        elif "field" in bg_prompt or "khet" in bg_prompt or "ਖੇਤ" in bg_prompt or "wheat" in bg_prompt:
            bg_image_filename = "field.jpg"

        bg_image_path = os.path.join(BASE_DIR, "images", bg_image_filename)
        if not os.path.exists(bg_image_path):
            bg_image_path = os.path.join(BASE_DIR, "images", "scene_base.png")

        logs.append(f"🖼️ Resolved background image path: {bg_image_path}")

        # Run master_builder
        python_exec = os.path.join(BASE_DIR, ".venv", "bin", "python")
        if not os.path.exists(python_exec):
            python_exec = sys.executable

        builder_args = [
            python_exec,
            os.path.join("colab", "master_builder.py"),
            "--scenes", scenes_path,
            "--background", bg_image_path,
            "--sfx-preset", request.sfx_preset
        ]
        if request.ducking:
            builder_args.append("--duck")
        if request.mastering:
            builder_args.append("--master")
        builder_args.append("--verbose")

        logs.append(f"🎬 Compiling video clip with: {' '.join(builder_args)}")
        run_builder = subprocess.run(
            builder_args,
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        logs.append(run_builder.stdout)
        if run_builder.stderr:
            logs.append(f"Compiler details: {run_builder.stderr}")

        if run_builder.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Master builder execution failed: {run_builder.stderr}")

        final_video_path = os.path.join(BASE_DIR, "AmritCore_FINAL_STUDIO_LAUNCH.mp4")
        if not os.path.exists(final_video_path):
            raise HTTPException(status_code=500, detail="Compiler succeeded, but AmritCore_FINAL_STUDIO_LAUNCH.mp4 was not created")

        logs.append("🏆 Production compiler success! Video is ready for launch.")
        combined_logs = "\n".join(logs)

        return {
            "status": "success",
            "video_url": "/media/AmritCore_FINAL_STUDIO_LAUNCH.mp4",
            "logs": combined_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate_script")
async def generate_script(req: ScriptGenerateRequest):
    templates = {
        "Friendship": [
            { "character": "Krishna", "text": "ਸੁਲਤਾਨਾ, ਕਦੇ ਸੋਚਿਆ ਈ, ਆਪਾਂ ਵੀ ਕਦੀ ਸ਼ਹਿਰ ਜਾਈਏ?" },
            { "character": "Sultan", "text": "ਕ੍ਰਿਸ਼ਨਾ, ਮੈਂ ਤਾਂ ਏਸੇ ਪਿੰਡ ਵਿੱਚ ਖੁਸ਼ ਆਂ। ਆਪਣੀ ਦੋਸਤੀ ਕਾਇਮ ਰਹੇ, ਹੋਰ ਕੀ ਚਾਹੀਦਾ।" },
            { "character": "Krishna", "text": "ਦੋਸਤੀ ਤਾਂ ਹਮੇਸ਼ਾ ਰਹੇਗੀ ਯਾਰ, ਪਰ ਸ਼ਹਿਰ ਜਾ ਕੇ ਕੁਝ ਵੱਡਾ ਕਰਾਂਗੇ!" },
            { "character": "Sultan", "text": "ਚੱਲ ਜੇ ਤੇਰੀ ਇਹੀ ਇੱਛਾ ਹੈ, ਤਾਂ ਮੈਂ ਵੀ ਤੇਰੇ ਨਾਲ ਤਿਆਰ ਹਾਂ।" }
        ],
        "Farmer & AI": [
            { "character": "Sultan", "text": "ਕ੍ਰਿਸ਼ਨਾ, ਆਹ ਨਵਾਂ ਟਰੈਕਟਰ ਤਾਂ ਆਪਣੇ ਆਪ ਖੇਤ ਵਾਹ ਰਿਹਾ ਏ!" },
            { "character": "Krishna", "text": "ਹਾਂ ਸੁਲਤਾਨਾ, ਇਹ ਏ.ਆਈ ਟਰੈਕਟਰ ਏ, ਇਹ ਸਾਡਾ ਸਮਾਂ ਤੇ ਮਿਹਨਤ ਬਚਾਉਂਦਾ ਏ।" },
            { "character": "Sultan", "text": "ਵਾਹ! ਬਾਬੇ ਨਾਨਕ ਦੀ ਮਿਹਰ ਨਾਲ ਤਕਨਾਲੋਜੀ ਵੀ ਬਰਕਤ ਪਾ ਰਹੀ ਏ।" },
            { "character": "Krishna", "text": "ਬਿਲਕੁਲ, ਹੁਣ ਅਸੀਂ ਹੋਰ ਲੋਕਾਂ ਦੀ ਸੇਵਾ ਲਈ ਵੱਧ ਸਮਾਂ ਕੱਢ ਸਕਦੇ ਹਾਂ।" }
        ],
        "Selfless Service": [
            { "character": "Sant Kaur", "text": "ਪੁੱਤਰ ਕ੍ਰਿਸ਼ਨਾ, ਗਰੀਬਾਂ ਦੀ ਸੇਵਾ ਹੀ ਸਭ ਤੋਂ ਵੱਡਾ ਧਰਮ ਹੈ।" },
            { "character": "Krishna", "text": "ਜੀ ਮਾਂ, ਮੈਂ ਅੱਜ ਪਿੰਡ ਦੇ ਸਾਂਝੇ ਲੰਗਰ ਲਈ ਰਸਦ ਲੈ ਕੇ ਆਇਆ ਹਾਂ।" },
            { "character": "Sant Kaur", "text": "ਰੱਬ ਤੈਨੂੰ ਤੰਦਰੁਸਤੀ ਬਖ਼ਸ਼ੇ ਪੁੱਤ, ਸੇਵਾ ਵਿੱਚ ਹੀ ਸੱਚਾ ਆਨੰਦ ਹੈ।" },
            { "character": "Krishna", "text": "ਮਾਂ, ਜਿੰਨੀ ਦੇਰ ਸਵਾਸ ਹਨ, ਮੈਂ ਨਿਮਰਤਾ ਨਾਲ ਸੇਵਾ ਕਰਦਾ ਰਹਾਂਗਾ।" }
        ]
    }

    dialogue_list = None

    if req.prompt and req.model != "Offline Templates":
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                ollama_url = "http://localhost:11434/api/generate"
                prompt_text = (
                    f"Write a short dialogue script in Punjabi language between two characters: Krishna and Sultan (or Sant Kaur). "
                    f"Keep it to exactly 4 dialogue lines. Format the output strictly as a JSON array of objects with keys 'character' and 'text'. "
                    f"Do not include any other markdown, headers, or explanations. "
                    f"Theme/Concept: {req.theme}. Prompt details: {req.prompt}."
                )
                
                res = await client.post(ollama_url, json={
                    "model": req.model,
                    "prompt": prompt_text,
                    "stream": False,
                    "format": "json"
                })
                
                if res.status_code == 200:
                    data = res.json()
                    response_text = data.get("response", "")
                    dialogue_list = json.loads(response_text)
                    if isinstance(dialogue_list, dict) and "dialogues" in dialogue_list:
                        dialogue_list = dialogue_list["dialogues"]
        except Exception as e:
            print(f"Ollama call failed for model {req.model}, fallback to template:", e)

    if not dialogue_list or not isinstance(dialogue_list, list):
        theme_key = req.theme
        if theme_key not in templates:
            theme_key = "Friendship"
        dialogue_list = templates[theme_key]

    timeline = []
    current_time = 0.0
    for idx, d in enumerate(dialogue_list):
        char = d.get("character", "Krishna")
        text = d.get("text", "")
        duration = max(2.0, min(5.0, len(text) / 6.0))
        start_time = round(current_time, 1)
        
        timeline.append({
            "id": f"gen_{idx}_{idx}",
            "character": char,
            "text": text,
            "volume": 1.0,
            "pan": -0.2 if char == "Krishna" else 0.2,
            "start_time": start_time,
            "duration": duration
        })
        current_time += duration + 0.5

    return {"status": "success", "timeline": timeline}

class ChatBrainstormRequest(BaseModel):
    message: str
    chat_history: list
    current_timeline: list
    model: str

@app.post("/api/chat_brainstorm")
async def chat_brainstorm(req: ChatBrainstormRequest):
    """Handles conversational AI story brainstorming and automatic script generation."""
    reply = "ਵਾਹ, ਬਹੁਤ ਵਧੀਆ ਵਿਚਾਰ ਹੈ! ਤੁਸੀਂ ਟਾਈਮਲਾਈਨ 'ਤੇ ਬਲਾਕਾਂ ਨੂੰ ਐਡਜਸਟ ਕਰਕੇ ਜਾਂ ਡਾਇਲਾਗ ਐਡੀਟਰ ਵਿੱਚ ਸਿੱਧਾ ਬਦਲਾਅ ਕਰਕੇ ਸੁਧਾਰ ਕਰ ਸਕਦੇ ਹੋ।"
    updated_timeline = None

    # 1. Ollama Call if model is selected
    if req.message and req.model != "Offline Templates":
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                ollama_url = "http://localhost:11434/api/generate"
                prompt_text = (
                    f"You are a Creative Storytelling Assistant for Punjabi animation movies. "
                    f"The user wants to brainstorm or edit their story.\n"
                    f"User message: '{req.message}'\n"
                    f"Current Story Script Blocks (as JSON array):\n{json.dumps(req.current_timeline, ensure_ascii=False)}\n\n"
                    f"Reply in friendly Punjabi language, discussing their feedback. "
                    f"If the user wants to add, modify, or rewrite dialogues/blocks, you MUST generate the updated script blocks list. "
                    f"Format your response strictly as a JSON object with two keys:\n"
                    f"1. 'reply': Your conversational response in Punjabi.\n"
                    f"2. 'updated_timeline': (optional) A JSON array of the revised timeline blocks, matching the structure: [{{'character': 'CharName', 'text': 'Dialogue text'}}].\n"
                    f"Do not include any other explanations, markdown wrappers, or HTML tags outside the raw JSON object."
                )
                
                res = await client.post(ollama_url, json={
                    "model": req.model,
                    "prompt": prompt_text,
                    "stream": False,
                    "format": "json"
                })
                
                if res.status_code == 200:
                    data = res.json()
                    response_text = data.get("response", "")
                    parsed = json.loads(response_text)
                    reply = parsed.get("reply", reply)
                    updated_timeline = parsed.get("updated_timeline", None)
        except Exception as e:
            print(f"Ollama brainstorm call failed: {e}")

    # 2. Smart Offline Rule Fallback
    if not updated_timeline and req.message:
        msg_lower = req.message.lower()
        if "raju" in msg_lower or "simran" in msg_lower:
            reply = "ਮੈਂ ਤੁਹਾਡੇ ਸੁਝਾਅ ਮੁਤਾਬਕ ਨਵੇਂ ਕਿਰਦਾਰਾਂ (Raju/Simran) ਨਾਲ ਟਾਈਮਲਾਈਨ ਸਕ੍ਰਿਪਟ ਅਪਡੇਟ ਕਰ ਦਿੱਤੀ ਹੈ! ਹੁਣ ਤੁਸੀਂ ਐਡੀਟਰ ਵਿੱਚ ਇਸਨੂੰ ਸੁਧਾਰ ਸਕਦੇ ਹੋ।"
            updated_timeline = [
                { "character": "Raju", "text": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਸਿਮਰਨ, ਕਿਵੇਂ ਚੱਲ ਰਹੀ ਹੈ ਕਹਾਣੀ?" },
                { "character": "Simran", "text": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਰਾਜੂ, ਸਭ ਵਧੀਆ! ਅਸੀਂ ਏ.ਆਈ ਨਾਲ ਨਵੀਂ ਮੂਵੀ ਬਣਾ ਰਹੇ ਹਾਂ।" }
            ]
        elif "peacock" in msg_lower or "ਮੋਰ" in msg_lower or "ਆਵਾਜ਼" in msg_lower:
            reply = "ਮੈਂ ਕਹਾਣੀ ਵਿੱਚ ਮੋਰ ਦੀ ਆਵਾਜ਼ (peacock SFX) ਜੋੜ ਦਿੱਤੀ ਹੈ ਤਾਂ ਜੋ ਮਾਹੌਲ ਹੋਰ ਵਧੀਆ ਲੱਗੇ!"
            updated_timeline = list(req.current_timeline)
            # Add SFX block at the end
            max_start = max([b.get('start_time', 0.0) + b.get('duration', 3.0) for b in updated_timeline]) if updated_timeline else 0.0
            updated_timeline.append({
                "character": "SFX",
                "text": "peacock",
                "start_time": round(max_start, 1),
                "duration": 3.0
            })
        elif "clear" in msg_lower or "ਸਾਫ਼" in msg_lower:
            reply = "ਮੈਂ ਟਾਈਮਲਾਈਨ ਸਾਫ਼ ਕਰ ਦਿੱਤੀ ਹੈ, ਹੁਣ ਨਵੀਂ ਕਹਾਣੀ ਸ਼ੁਰੂ ਕਰੋ!"
            updated_timeline = []

    # 3. Format timeline structures if updated
    formatted_timeline = None
    if updated_timeline is not None:
        import time
        formatted_timeline = []
        current_time = 0.0
        for idx, d in enumerate(updated_timeline):
            char = d.get("character", "Krishna")
            text = d.get("text", "")
            duration = d.get("duration")
            if not duration:
                duration = max(2.0, min(5.0, len(text) / 6.0))
            
            formatted_timeline.append({
                "id": f"chat_gen_{idx}_{int(time.time())}",
                "character": char,
                "text": text,
                "volume": 1.0,
                "pan": -0.2 if idx % 2 == 0 else 0.2,
                "start_time": round(current_time, 1),
                "duration": round(duration, 1)
            })
            current_time += duration + 0.5

    return {
        "status": "success",
        "reply": reply,
        "timeline": formatted_timeline
    }

@app.get("/api/preview_tts")
def preview_tts(character: str, text: str):
    try:
        # Create hash key based on text content
        hash_input = f"{character}_{text}".encode("utf-8")
        hash_key = hashlib.md5(hash_input).hexdigest()
        
        # Audio cache directory inside audio folder
        cache_dir = os.path.join(BASE_DIR, "audio", "cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        filename = f"{hash_key}.mp3"
        cached_file_path = os.path.join(cache_dir, filename)
        
        # Synthesize using gTTS if cache misses
        if not os.path.exists(cached_file_path):
            tts = gTTS(text, lang='pa')
            tts.save(cached_file_path)
            
        return {
            "status": "success",
            "url": f"/audio/cache/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload_recording")
async def upload_recording(block_id: str = Form(...), file: UploadFile = File(...)):
    try:
        recordings_dir = os.path.join(BASE_DIR, "audio", "recordings")
        os.makedirs(recordings_dir, exist_ok=True)
        
        ext = os.path.splitext(file.filename)[1]
        if not ext:
            ext = ".wav"
            
        filename = f"{block_id}{ext}"
        file_path = os.path.join(recordings_dir, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "status": "success",
            "url": f"/audio/recordings/{filename}",
            "audio_file": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
def get_system_status():
    """Return platform and resource details."""
    cpu_percent = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "status": "Online",
        "cpu_usage": f"{cpu_percent}%",
        "ram_usage": f"{ram.percent}%",
        "disk_free": f"{disk.free // (1024**3)} GB free",
        "platform": platform.system(),
        "arch": platform.machine()
    }

@app.post("/api/upload_character")
async def upload_character(character_name: str, file: UploadFile = File(...)):
    """Allows uploading custom character portrait to images folder."""
    images_dir = os.path.join(BASE_DIR, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    safe_name = "".join(c for c in character_name.lower() if c.isalnum() or c in ("-", "_"))
    ext = os.path.splitext(file.filename)[1]
    if not ext:
        ext = ".jpg"
    
    filename = f"{safe_name}{ext}"
    target_path = os.path.join(images_dir, filename)
    try:
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {
            "status": "success", 
            "filename": filename, 
            "url": f"/images/{filename}",
            "character_name": character_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/upload_background")
async def upload_background(file: UploadFile = File(...)):
    """Allows uploading a custom background image."""
    images_dir = os.path.join(BASE_DIR, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    ext = os.path.splitext(file.filename)[1]
    if not ext:
        ext = ".jpg"
    filename = f"custom_bg{ext}"
    target_path = os.path.join(images_dir, filename)
    try:
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {
            "status": "success",
            "url": f"/images/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Background upload failed: {str(e)}")

@app.post("/api/upload_block_image")
async def upload_block_image(block_id: str, file: UploadFile = File(...)):
    """Allows uploading a custom storyboard frame photo for a specific block."""
    cache_dir = os.path.join(BASE_DIR, "images", "cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    ext = os.path.splitext(file.filename)[1]
    if not ext:
        ext = ".png"
    filename = f"{block_id}{ext}"
    target_path = os.path.join(cache_dir, filename)
    try:
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {
            "status": "success",
            "url": f"/images/cache/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Block image upload failed: {str(e)}")

class CharacterGenerateRequest(BaseModel):
    prompt: str
    name: str

@app.post("/api/generate_character")
async def generate_character(req: CharacterGenerateRequest):
    """Simulates AI character generation based on text prompt and saves preset avatar."""
    images_dir = os.path.join(BASE_DIR, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    safe_name = "".join(c for c in req.name.lower() if c.isalnum() or c in ("-", "_"))
    filename = f"{safe_name}.jpg"
    target_path = os.path.join(images_dir, filename)
    
    src_avatar = os.path.join(images_dir, "krishna.jpg")
    try:
        if os.path.exists(src_avatar):
            shutil.copy2(src_avatar, target_path)
        else:
            # Create a simple placeholder
            from PIL import Image
            img = Image.new('RGB', (200, 200), color='#2563eb')
            img.save(target_path)
            
        return {
            "status": "success",
            "character_name": req.name,
            "url": f"/images/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
