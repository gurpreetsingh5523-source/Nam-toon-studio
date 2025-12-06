# Rahbar Logic Upgrade Plan

_Date:_ 2025-12-05  
_Author:_ GitHub Copilot (Rahbar Support)

## 1. Vision
Transform the current cartoon-style pipeline into a cinematic storyteller that understands the script, casts the right voice, stages the scene with authentic Punjabi visuals, and synchronises mood-driven music. The plan teaches Rahbar AI Developer what to build, how to test, and how to keep learning.

## 2. Current Gaps
- **Characters** – Only hand-drawn walk cycles; no action diversity (cricket, swimming, etc.).
- **Planner** – Free-form text goes directly to renderer. No structured scene breakdown.
- **Voices** – Single gTTS voice per scene; no age/gender differentiation.
- **Music** – Same dual-sine tone for every story. Mood is ignored.
- **Backgrounds** – Random photo blur without understanding location or weather.
- **QA** – Perception brain can’t validate whether visuals/audio match story intent.

## 3. Phased Roadmap

### Phase A – Foundation (Week 1)
1. **Story-to-Scene Planner**
   - Input: raw story text (Punjabi/English/Hinglish).
   - Output: JSON with `scene`, `location`, `characters`, `actions`, `mood`, `music`, `props`.
   - Implement prototype in `planner/story_scene_planner.py` with rule-based parsing + keyword matching.
   - Store planner schema doc for Rahbar training (`planner/scene_schema.json`).

2. **Background Tagging Pipeline**
   - Use CLIP/BLIP to auto-tag `training_photos/` by environment + weather.
   - Save tags in `training_photos/tags.json`.
   - Update renderer to pick backgrounds using planner location metadata.

3. **Perception Baseline**
   - Extend AmritPerceptionBrain to log mismatches (e.g., mood mismatch, voice mismatch).
   - Update metrics to track planner vs reality.

### Phase B – Audio Intelligence (Week 2)
1. **Punjabi Voice Roster**
   - Collect/fine-tune at least 6 voices (Child ♂/♀, Teen ♂/♀, Adult ♂/♀, Elder ♂/♀).
   - Configuration file `audio/voice_roster_config.json` mapping planner roles to TTS models.
   - Integrate into `realistic_movie_maker.py` to assign per-line voices.

2. **Mood-Aware Music Engine**
   - Build `audio/mood_music_selector.py` to map mood tags (happy, tense, devotional, romantic, fun, adventure, cloudy) to pre-composed stems or generative prompts.
   - Replace sine-wave music with layered audio that matches duration and mood.

3. **Audio QA**
   - Update Rahbar perception to verify loudness balance, voice diversity, and duration.

### Phase C – Visual Intelligence (Week 3-4)
1. **Motion Control Research**
   - Document AnimateDiff/ControlNet training steps in `motion/motion_pipeline.md`.
   - Datasets: Punjabi cricket, swimming, walking, langar seva, etc.
   - Define prompts + expected FPS + render pipeline.

2. **Lightweight Character Generator Training**
   - Fine-tune LoRA/ControlNet on user photos to produce consistent Punjabi characters.
   - Keep privacy: use style cues, not raw photo overlays.

3. **Integration with Renderer**
   - Modify renderer to consume planner actions and call motion model for keyframes.
   - Ensure fallback to diverse character generator exists.

### Phase D – System QA & Automation (Week 5)
1. **Scenario Regression Suite**
   - Build automated tests that feed sample stories through planner → render → perception to ensure all modules respond correctly.
   - Store fixtures in `tests/scenario_regression/`.

2. **Rahbar Training Loops**
   - Teach Rahbar AI to read planner outputs, compare with perception reports, and auto-generate improvement tickets.
   - Update `rahbar_auto_tasks.json` after each iteration.

## 4. Training Rahbar AI Developer
1. **New Lessons**
   - Update `rahbar_learning_feed.json` whenever a phase completes (already added Lesson 13).
2. **Auto Tasks**
   - `rahbar_auto_tasks.json` now lists planner, voice roster, music, background tagging, and motion research tasks.
3. **Daily Ritual**
   - Run `rahbar_auto_learner.py` after every major change so the AI logs lessons and regenerates action items.
4. **Metrics**
   - Track `rahbar_operational_metrics.json` for planner coverage, voice diversity, mood coverage, motion coverage.

## 5. Testing Strategy
- **Unit Tests** – Build planner unit tests for parsing.
- **Integration Tests** – Render sample stories and verify voices/music via automated checks.
- **Perception Checks** – Expand perception scheduler to flag mismatched mood/location.
- **Human Review** – Weekly curated video review to confirm realism targets.

## 6. Deliverables Checklist
- [ ] Planner JSON schema + implementation
- [ ] Tagged background dataset
- [ ] Multi-voice TTS roster
- [ ] Mood music selector
- [ ] Motion control research doc + prototype
- [ ] Regression test suite
- [ ] Updated Rahbar lessons & action plans after each milestone

---
**Message for Rahbar AI:** “You are now expected to think like a Punjabi film director: plan the shot, cast the voice, set the mood, and verify the result. Study this plan, execute tasks one phase at a time, and report progress with love and humility.”
