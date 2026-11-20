"use strict";

const $ = (id) => document.getElementById(id);
const backgrounds = {field: "Fields", khu: "Village well", talab: "Pond"};
const portraits = {sant_kaur: "Sant Kaur", sultan: "Sultan", krishna: "Krishna"};
const types = /^(image\/(png|jpeg|webp)|video\/(mp4|webm|quicktime)|audio\/(wav|x-wav|mpeg|mp4|ogg|webm))$/;
const categories = {
  sources: ["Source overview", ""],
  script: ["Script & media", "Paste narration or write a script"],
  clips: ["Clip assembly", "Enter a shot list, then assign imported clips"],
  presenter: ["Presenter", "Enter presenter narration"],
  animation: ["Animation", "Enter storyboard beats"]
};
const initial = {
  project: "ਪਿੰਡ ਦੀ ਪਹਿਲੀ ਸਵੇਰ", ratio: "16:9", voice: "", captions: true, category: "sources",
  sources: [{id: "notes", name: "ਕਹਾਣੀ ਦੇ ਨੋਟ", text: "ਸੰਤ ਕੌਰ ਸਵੇਰੇ ਖੇਤਾਂ ਵੱਲ ਤੁਰਦੀ ਹੈ। ਖੂਹ ਕੋਲ ਉਸ ਦੀ ਮੁਲਾਕਾਤ ਸੁਲਤਾਨ ਨਾਲ ਹੁੰਦੀ ਹੈ। ਦੋਵੇਂ ਪਿੰਡ ਲਈ ਪਾਣੀ ਬਚਾਉਣ ਦਾ ਰਾਹ ਸੋਚਦੇ ਹਨ।", enabled: true}],
  assets: [],
  scenes: [
    {title: "ਸਵੇਰ ਦੀ ਰੌਸ਼ਨੀ", script: "ਸੰਤ ਕੌਰ ਖੇਤਾਂ ਵਿਚੋਂ ਲੰਘੀ। ਕਣਕ ਦੀਆਂ ਬੱਲੀਆਂ ਉੱਤੇ ਤ੍ਰੇਲ ਚਮਕ ਰਹੀ ਸੀ।", background: "field", reference: "notes", duration: 6},
    {title: "ਖੂਹ ਕੋਲ ਮੁਲਾਕਾਤ", script: "ਸੁਲਤਾਨ ਨੇ ਆਖਿਆ, “ਆਓ, ਪਿੰਡ ਲਈ ਪਾਣੀ ਬਚਾਉਣ ਦਾ ਰਾਹ ਲੱਭੀਏ।”", background: "khu", reference: "notes", duration: 7, transition: "fade"},
    {title: "ਪਾਣੀ ਦੀ ਸਾਂਝ", script: "ਤਲਾਬ ਕੰਢੇ ਬੈਠ ਕੇ ਦੋਵੇਂ ਪਿੰਡ ਦੀ ਅਗਲੀ ਸਵੇਰ ਬਾਰੇ ਸੋਚਣ ਲੱਗੇ।", background: "talab", reference: "notes", duration: 8, motion: "push"}
  ]
};
const localId = /^[a-f0-9]{32}$/;
const sceneId = () => crypto.randomUUID().replaceAll("-", "");
const blank = () => ({id: sceneId(), title: "Untitled scene", script: "", reference: "", quote: "", duration: 5,
  background: "", actor: "", footage: "", generated: "", audio: "", motion: "still", transition: "cut",
  videoModel: "", videoPrompt: "", videoShape: "landscape", videoFrames: "33", videoSeed: ""});
const fileLimit = 18 * 1024 ** 2;
const storageKey = "naam-toon-production-v1";
const buttons = [...document.querySelectorAll("[data-category]")];
const edit = {"scene-title": "title", "scene-script": "script", reference: "reference",
  duration: "duration", background: "background", footage: "footage", actor: "actor",
  audio: "audio", motion: "motion", transition: "transition"};

function normalize(data) {
  if (typeof data?.project !== "string" || !Array.isArray(data.assets) || !Array.isArray(data.sources)
      || !Array.isArray(data.scenes) || data.scenes.length < 1 || data.scenes.length > 30) {
    throw Error("Choose a Naam Toon project file with 1–30 scenes.");
  }
  const ids = new Set();
  const assets = data.assets.map(({id, name, url}) => {
    const match = /^data:([^;]+);base64,([A-Za-z0-9+/=]+)$/.exec(url);
    if (!match || !types.test(match[1]) || !/^[\w-]{1,80}$/.test(id) || ids.has(id)
        || Object.hasOwn(backgrounds, id) || Object.hasOwn(portraits, id)) throw Error("Invalid project media.");
    ids.add(id);
    return {id, name: String(name), url, mime: match[1]};
  });
  const sources = data.sources.map(({id, name, text, enabled}) => {
    if (typeof id !== "string" || typeof text !== "string" || typeof name !== "string") throw Error("Invalid project source.");
    return {id, name, text, enabled: enabled !== false};
  });
  const sceneIds = new Set();
  const scenes = data.scenes.map((entry) => {
    if (typeof entry?.title !== "string" || typeof entry.script !== "string"
        || !Number.isInteger(entry.duration) || entry.duration < 1 || entry.duration > 120) {
      throw Error("Invalid scene title, narration or duration.");
    }
    const result = {...blank()};
    for (const key of Object.keys(result)) {
      if (typeof result[key] === typeof entry[key]) result[key] = entry[key];
    }
    if (!localId.test(result.id) || sceneIds.has(result.id)) result.id = sceneId();
    sceneIds.add(result.id);
    if (!localId.test(result.generated)) result.generated = "";
    for (const key of ["background", "actor", "footage", "audio"]) {
      const mediaType = {background: "image", actor: "image", footage: "video", audio: "audio"}[key];
      const builtins = {background: backgrounds, actor: portraits}[key] || {};
      if (!Object.hasOwn(builtins, result[key]) &&
          !assets.some((item) => item.id === result[key] && item.mime.startsWith(mediaType + "/"))) result[key] = "";
    }
    if (!sources.some((item) => item.id === result.reference)) result.reference = "";
    if (!result.reference) result.quote = "";
    return result;
  });
  return {...initial, project: data.project, ratio: ["16:9", "9:16", "1:1"].includes(data.ratio) ? data.ratio : "16:9",
    voice: ["en", "pa"].includes(data.voice) ? data.voice : "", captions: data.captions !== false,
    category: Object.hasOwn(categories, data.category) ? data.category : "sources", assets, sources, scenes};
}

let project = normalize(initial);
try {
  const saved = localStorage.getItem(storageKey);
  if (saved) project = normalize(JSON.parse(saved));
} catch {}
let selected = 0;
let locationSeconds = 0;
let animationFrame = 0;
let draft = null;
let available = {models: [], missing: [], voices: {}};
let previousStoryboard = null;
let revision = 0;
let storageWarning = false;
let videoModels = [];
let videoJobs = [];
let videoSubmitting = false;
let videoPoll = null;
const say = (words) => { $("status").textContent = words; };

function save() {
  revision += 1;
  try {
    localStorage.setItem(storageKey, JSON.stringify(project));
    storageWarning = false;
  } catch {
    if (!storageWarning) say("Browser storage is full. Save a project file to keep these edits.");
    storageWarning = true;
  }
}

function options(node, values, current) {
  node.replaceChildren(...values.map(([key, title, disabled]) => {
    const option = new Option(title, key);
    option.disabled = Boolean(disabled);
    return option;
  }));
  if (values.some(([key]) => key === current)) node.value = current;
}

const media = (type) => project.assets.filter(({mime}) => mime.startsWith(type + "/")).map(({id, name}) => [id, name]);
const url = (id) => {
  if (Object.hasOwn(backgrounds, id) || Object.hasOwn(portraits, id)) return "/assets/" + id + ".webp";
  return project.assets.find((asset) => asset.id === id)?.url || "";
};
const total = () => project.scenes.reduce((sum, item) => sum + item.duration, 0);
const startOf = (index) => project.scenes.slice(0, index).reduce((sum, item) => sum + item.duration, 0);

function categoryView() {
  const [name, prompt] = categories[project.category];
  $("input-heading").textContent = name;
  $("source-tools").hidden = project.category !== "sources";
  $("brief-label").hidden = project.category === "sources";
  $("brief").placeholder = prompt;
  for (const button of buttons) button.setAttribute("aria-pressed", String(button.dataset.category === project.category));
  modelView();
}

function modelView() {
  const current = $("model").value;
  const local = project.category === "sources" ? "Exact excerpts · local" : "Script splitter · local";
  const unavailable = project.category === "presenter"
      ? [["avatar", "Lip-sync model · unavailable (no provider)", true]]
      : available.models.length ? [] : [["offline", "Ollama · unavailable (no completion models)", true]];
  options($("model"), [["local", local], ...available.models.map((name) => [name, name + " · Ollama"]), ...unavailable], current);
  modelHelp();
}

function modelHelp() {
  const local = $("model").value === "local";
  $("language").disabled = local || project.category === "sources";
  $("focus-label").hidden = local && project.category !== "sources";
  const text = local ? "Keeps the wording and language of your input."
    : project.category === "sources" ? "Ollama selects excerpts. Scene narration uses the quoted source text."
    : "Runs the selected text model through local Ollama.";
  const capability = {clips: " Assign imported or generated video to each shot.", presenter: " Uses a still portrait and optional audio.",
    animation: " Uses still-image motion and fades."}[project.category] || "";
  $("model-help").textContent = text + capability;
}

function sourceView() {
  const elements = project.sources.map((source) => {
    const detail = document.createElement("details");
    const summary = document.createElement("summary");
    summary.textContent = source.name;
    const check = document.createElement("input");
    check.type = "checkbox";
    check.checked = source.enabled;
    check.onchange = () => { source.enabled = check.checked; save(); };
    const label = document.createElement("label");
    label.className = "check";
    label.append(check, "Include in drafting");
    const sample = document.createElement("p");
    sample.textContent = source.text;
    detail.append(summary, label, sample);
    return detail;
  });
  $("sources").replaceChildren(...elements);
}

function setVisual(id, value) {
  const element = $(id);
  const src = value.startsWith("/video-clips/") ? value : url(value);
  element.hidden = !src;
  if (src && element.getAttribute("src") !== src) element.src = src;
  if (!src && element.hasAttribute("src")) element.removeAttribute("src");
}

function monitor() {
  const item = project.scenes[selected];
  const t = Math.max(0, locationSeconds - startOf(selected));
  const shape = {"9:16": "portrait", "1:1": "square"}[project.ratio] || "";
  $("stage").className = "stage " + shape;
  setVisual("background-view", item.footage || item.generated ? "" : item.background);
  setVisual("footage-view", item.generated ? "/video-clips/" + item.generated : item.footage);
  setVisual("actor-view", item.actor);
  const video = $("footage-view");
  if (!video.hidden && video.readyState >= 1 && Number.isFinite(video.duration) && video.duration > 0) {
    const desired = t % video.duration;
    if (Math.abs(video.currentTime - desired) > 0.08) video.currentTime = desired;
  }
  $("background-view").style.transform = item.motion === "push" ? "scale(" + (1 + 0.11 * t / item.duration) + ")" : "";
  const opacity = item.transition === "fade" ? Math.min(1, t / 0.35, (item.duration - t) / 0.35) : 1;
  $("stage").style.filter = "brightness(" + Math.max(0, opacity) + ")";
  $("caption-view").hidden = !project.captions;
  $("stage-title").textContent = item.title;
  $("stage-text").textContent = item.script;
  $("seek").max = total();
  $("seek").value = locationSeconds;
  $("time").value = locationSeconds.toFixed(1) + " / " + total() + " s";
}
$("footage-view").addEventListener("loadedmetadata", monitor);

function inspector() {
  const item = project.scenes[selected];
  options($("reference"), [["", "No linked source"], ...project.sources.map(({id, name}) => [id, name])], item.reference);
  options($("background"), [["", "Solid background"], ...Object.entries(backgrounds), ...media("image")], item.background);
  options($("actor"), [["", "No presenter"], ...Object.entries(portraits), ...media("image")], item.actor);
  const generated = videoJobs.filter(({state}) => state === "ready")
    .map(({id, model_name, seed}) => ["gen:" + id, "Generated · " + model_name + " · " + seed]);
  if (item.generated && !generated.some(([value]) => value === "gen:" + item.generated)) {
    generated.unshift(["gen:" + item.generated, "Linked generated clip · " + item.generated.slice(0, 8)]);
  }
  options($("footage"), [["", "No video clip"], ...media("video"), ...generated],
    item.generated ? "gen:" + item.generated : item.footage);
  options($("audio"), [["", "Use project voice or clip audio"], ...media("audio")], item.audio);
  for (const [id, field] of Object.entries(edit)) if (field !== "footage") $(id).value = item[field];
  const source = project.sources.find(({id}) => id === item.reference);
  $("quote").hidden = !source;
  $("quote").textContent = source ? item.quote || source.text.slice(0, 240) : "";
  $("scene-number").textContent = (selected + 1) + " / " + project.scenes.length;
  $("earlier").disabled = selected === 0;
  $("later").disabled = selected === project.scenes.length - 1;
  $("remove").disabled = project.scenes.length === 1;
  $("duplicate").disabled = $("add-scene").disabled = project.scenes.length >= 30;
  generationView(true);
}

function timeline() {
  const lane = $("timeline");
  const scroll = lane.scrollLeft;
  const nodes = project.scenes.map((item, index) => {
    const button = document.createElement("button");
    button.setAttribute("aria-current", String(index === selected));
    const thumbnail = document.createElement("img");
    thumbnail.alt = "";
    const src = url(item.background || item.actor);
    if (src) { thumbnail.src = src; button.append(thumbnail); }
    const title = document.createElement("span");
    title.textContent = item.title || "Untitled scene";
    const seconds = document.createElement("small");
    seconds.className = "muted";
    seconds.textContent = item.duration + " s" + (item.footage || item.generated ? " · clip" : "");
    button.append(title, seconds);
    button.onclick = () => pick(index);
    return button;
  });
  lane.replaceChildren(...nodes);
  lane.scrollLeft = scroll;
}

function redraw() { inspector(); timeline(); monitor(); }
function stop() {
  if (animationFrame) cancelAnimationFrame(animationFrame);
  animationFrame = 0;
  $("play").textContent = "Play storyboard";
}
function storyboard() {
  $("result").pause();
  $("result").hidden = true;
  $("stage").hidden = false;
  $("show-storyboard").hidden = true;
  $("monitor-kind").textContent = "Storyboard preview";
}
function pick(index) {
  stop();
  storyboard();
  selected = index;
  locationSeconds = startOf(index);
  redraw();
}
function seek(time) {
  locationSeconds = Math.max(0, Math.min(total(), time));
  let index = project.scenes.findIndex((item, i) => startOf(i) + item.duration > locationSeconds);
  if (index < 0) index = project.scenes.length - 1;
  if (selected !== index) {
    selected = index;
    inspector();
    timeline();
  }
  monitor();
}
function repeat() {
  if (animationFrame) { stop(); return; }
  storyboard();
  if (locationSeconds >= total()) seek(0);
  const origin = performance.now() - locationSeconds * 1000;
  $("play").textContent = "Pause storyboard";
  const step = (now) => {
    seek((now - origin) / 1000);
    if (locationSeconds < total()) animationFrame = requestAnimationFrame(step);
    else stop();
  };
  animationFrame = requestAnimationFrame(step);
}

for (const [id, field] of Object.entries(edit)) {
  const control = $(id);
  control.addEventListener(control.matches("textarea, input:not([type=number])") ? "input" : "change", () => {
    const item = project.scenes[selected];
    item[field] = field === "duration" ? Math.max(1, Math.min(120, Math.round(Number(control.value) || 1))) : control.value;
    if (field === "footage") {
      item.generated = control.value.startsWith("gen:") ? control.value.slice(4) : "";
      if (item.generated) item.footage = "";
    }
    if (field === "reference") item.quote = "";
    stop();
    storyboard();
    if (field === "duration") locationSeconds = startOf(selected);
    if (field === "reference" || field === "duration") inspector();
    timeline();
    monitor();
    save();
  });
}
for (const button of buttons) button.onclick = () => {
  project.category = button.dataset.category;
  if (project.category === "clips") $("generate-clip").open = true;
  discard();
  categoryView();
  save();
};

function addSource(name, text) {
  const cleaned = text.trim();
  if (!cleaned) throw Error("Enter source text first.");
  if (cleaned.length > 60000 || project.sources.length >= 32) throw Error("Use up to 32 sources, each up to 60,000 characters.");
  project.sources.push({id: crypto.randomUUID(), name: name.trim().slice(0, 160) || "Untitled source", text: cleaned, enabled: true});
  sourceView();
  inspector();
  save();
}
$("add-source").onclick = () => {
  try {
    addSource($("source-name").value, $("source-text").value);
    $("source-name").value = $("source-text").value = "";
  } catch (error) { say(error.message); }
};
$("source-files").onchange = async (event) => {
  for (const file of event.target.files) {
    try {
      if (file.size > 240000) throw Error("Text file exceeds the source limit.");
      addSource(file.name, await file.text());
    } catch (error) { say(error.message); }
  }
  event.target.value = "";
};
$("media-files").onchange = async (event) => {
  for (const file of event.target.files) {
    try {
      if (!types.test(file.type) || file.size > fileLimit) throw Error("Unsupported type or media file over 18 MB.");
      const data = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(Error("Could not read media."));
        reader.readAsDataURL(file);
      });
      const bytes = project.assets.reduce((sum, item) => sum + item.url.length, data.length);
      if (bytes > 29 * 1024 ** 2) throw Error("Project exceeds the combined media limit.");
      project.assets.push({id: crypto.randomUUID(), name: file.name, mime: file.type, url: data});
      save();
    } catch (error) { say(error.message); }
  }
  event.target.value = "";
  mediaView();
  inspector();
};
function mediaView() {
  $("media-list").textContent = project.assets.length ? project.assets.map(({name}) => name).join(" · ") : "No imported media";
}

async function api(route, data) {
  const request = data === undefined ? undefined : {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)};
  const response = await fetch(route, request);
  const result = await response.json();
  if (!response.ok) throw Error(result.error || "Studio request failed.");
  return result;
}
function discard() { draft = null; $("draft-review").hidden = true; }
$("draft").onclick = async () => {
  const button = $("draft");
  const category = project.category;
  const model = $("model").value;
  const previous = revision;
  button.disabled = true;
  discard();
  say("Drafting with " + (model === "local" ? "the local planner" : model) + "…");
  try {
    const outcome = await api("/api/plan", {
      category, model, text: $("brief").value, format: $("format").value, language: $("language").value,
      focus: $("focus").value, sources: project.sources.filter((source) => source.enabled)
    });
    if (revision !== previous || category !== project.category) {
      say("The project changed while drafting. Draft again to use the latest inputs.");
      return;
    }
    draft = outcome.scenes;
    $("draft-scenes").replaceChildren(...draft.map((scene) => {
      const item = document.createElement("li");
      item.textContent = scene.title + " — " + scene.script;
      return item;
    }));
    $("draft-review").hidden = false;
    say(draft.length + " draft scenes ready for review.");
  } catch (error) { say(error.message); }
  finally { button.disabled = false; }
};

function adopt(append) {
  if (!draft) return;
  const next = append ? project.scenes.concat(draft) : draft;
  if (next.length > 30) { say("A storyboard supports up to 30 scenes."); return; }
  const position = append ? project.scenes.length : 0;
  rememberStoryboard();
  project.scenes = normalize({...project, scenes: next}).scenes;
  discard();
  pick(position);
  save();
  if (!storageWarning) say("Draft added to the storyboard.");
}
$("apply-draft").onclick = () => adopt(true);
$("replace-draft").onclick = () => adopt(false);
$("discard-draft").onclick = discard;
$("model").onchange = modelHelp;
function rememberStoryboard() {
  previousStoryboard = {scenes: project.scenes.map((item) => ({...item})), selected};
  $("undo").disabled = false;
}
$("undo").onclick = () => {
  if (!previousStoryboard) return;
  project.scenes = previousStoryboard.scenes;
  pick(previousStoryboard.selected);
  previousStoryboard = null;
  $("undo").disabled = true;
  save();
};
$("add-scene").onclick = () => { rememberStoryboard(); project.scenes.push(blank()); pick(project.scenes.length - 1); save(); };
$("duplicate").onclick = () => { rememberStoryboard(); project.scenes.splice(selected + 1, 0, {...project.scenes[selected], id: sceneId()}); pick(selected + 1); save(); };
$("remove").onclick = () => { rememberStoryboard(); project.scenes.splice(selected, 1); pick(Math.min(selected, project.scenes.length - 1)); save(); };
function move(change) {
  rememberStoryboard();
  const [item] = project.scenes.splice(selected, 1);
  project.scenes.splice(selected + change, 0, item);
  pick(selected + change);
  save();
}
$("earlier").onclick = () => move(-1);
$("later").onclick = () => move(1);
$("play").onclick = repeat;
$("seek").oninput = () => { stop(); storyboard(); seek(Number($("seek").value)); };
$("show-storyboard").onclick = storyboard;
$("project-name").oninput = () => { project.project = $("project-name").value; save(); };
for (const field of ["ratio", "voice", "captions"]) $(field).onchange = () => {
  project[field] = field === "captions" ? $(field).checked : $(field).value;
  storyboard();
  monitor();
  save();
};
$("save-project").onclick = () => {
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([JSON.stringify(project, null, 2)], {type: "application/json"}));
  link.download = "naam-toon-project.json";
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 3000);
};
for (const button of document.querySelectorAll("[data-pick]")) button.onclick = () => $(button.dataset.pick).click();
$("new-project").onclick = () => {
  if (!confirm("Start a blank project? Save a project file first if you need a copy.")) return;
  project = normalize({...initial, project: "Untitled project", sources: [], scenes: [blank()]});
  discard();
  refresh();
  save();
  say("New project started.");
};
$("restore").onchange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    if (file.size > 32 * 1024 ** 2) throw Error("Project file exceeds 32 MB.");
    project = normalize(JSON.parse(await file.text()));
    discard();
    refresh();
    save();
    if (!storageWarning) say("Opened " + project.project);
  } catch (error) { say(error.message); }
  event.target.value = "";
};

$("render").onclick = async () => {
  const button = $("render");
  button.disabled = true;
  stop();
  const original = revision;
  say("Preparing render…");
  try {
    const {job} = await api("/api/render", project);
    let task;
    do {
      task = await api("/api/jobs/" + job);
      say(task.message);
      if (task.state === "running") await new Promise((resolve) => setTimeout(resolve, 450));
    } while (task.state === "running");
    if (task.state !== "ready") throw Error(task.message);
    $("result").src = task.url;
    $("result").hidden = false;
    $("stage").hidden = true;
    $("show-storyboard").hidden = false;
    $("download").href = task.url;
    $("download").hidden = false;
    $("monitor-kind").textContent = "Rendered MP4";
    const {width, height, seconds} = task.info;
    say("MP4 verified · " + width + " × " + height + " · " + seconds.toFixed(1) + " s"
      + (original !== revision ? " · rendered before your latest edits" : ""));
  } catch (error) { say("Render failed. " + error.message); }
  finally { button.disabled = false; }
};

function outputView() {
  const voices = [["", "Imported audio or silence"], ...[["en", "English"], ["pa", "Punjabi"]]
    .map(([code, language]) => [code, language + " · " + (available.voices[code] || "unavailable"), !available.voices[code]])];
  options($("voice"), voices, project.voice);
}

const generationFields = {"video-model": "videoModel", "video-prompt": "videoPrompt",
  "video-shape": "videoShape", "video-frames": "videoFrames", "video-seed": "videoSeed"};

function activeVideoJob() {
  return videoJobs.find(({state}) => state === "queued" || state === "submitting");
}

function generationView(resetFields = false) {
  const item = project.scenes[selected];
  if (resetFields) {
    for (const [id, key] of Object.entries(generationFields)) {
      if (id !== "video-model") $(id).value = item[key];
    }
    options($("video-model"), [["", "Choose a video model"], ...videoModels.map((model) => [
      model.id, model.name + (model.available ? " · local" : " · unavailable"), !model.available
    ])], item.videoModel);
  }
  const model = videoModels.find(({id}) => id === $("video-model").value);
  const ready = model?.available;
  $("queue-video").disabled = !ready || !item.videoPrompt.trim() || videoSubmitting || Boolean(activeVideoJob());
  $("video-model-help").textContent = ready
    ? "Text to video · " + model.fps + " fps · " + (Number(item.videoFrames) / model.fps).toFixed(1) + " s"
    : model?.reason || [...new Set(videoModels.map(({name, reason}) => reason && name + ": " + reason))]
      .filter(Boolean).join(" · ") || "Choose a model installed in local ComfyUI.";
  const jobs = videoJobs.filter((job) => job.scene === item.id);
  $("video-history").replaceChildren(...jobs.map((job) => {
    const row = document.createElement("div");
    row.className = "stack";
    const label = document.createElement("p");
    label.className = "muted";
    label.textContent = job.model_name + " · seed " + job.seed + " · " + job.message;
    row.append(label);
    if (job.state === "ready") {
      const rowActions = document.createElement("div");
      rowActions.className = "row";
      const use = document.createElement("button");
      use.textContent = "Use in scene";
      use.disabled = item.generated === job.id;
      use.onclick = () => {
        rememberStoryboard();
        item.generated = job.id;
        item.footage = "";
        pick(selected);
        save();
      };
      const download = document.createElement("a");
      download.className = "button";
      download.href = "/video-clips/" + job.id;
      download.download = "naam-toon-clip-" + job.seed + ".mp4";
      download.textContent = "Download clip";
      rowActions.append(use, download);
      row.append(rowActions);
    }
    return row;
  }));
}

for (const [id, key] of Object.entries(generationFields)) {
  $(id).oninput = () => {
    project.scenes[selected][key] = $(id).value;
    save();
    generationView();
  };
}

async function refreshVideo() {
  const [{models}, {jobs}] = await Promise.all([api("/api/video-models"), api("/api/video-jobs")]);
  videoModels = models;
  videoJobs = jobs;
  inspector();
  scheduleVideo();
}

function scheduleVideo() {
  clearTimeout(videoPoll);
  const current = activeVideoJob();
  if (!current) return;
  videoPoll = setTimeout(async () => {
    try {
      const job = await api("/api/video-jobs/" + current.id);
      videoJobs = videoJobs.map((entry) => entry.id === job.id ? job : entry);
      $("video-status").textContent = job.message;
      inspector();
    } catch (error) {
      $("video-status").textContent = error.message;
    }
    scheduleVideo();
  }, 2500);
}

$("check-video-models").onclick = async () => {
  const button = $("check-video-models");
  button.disabled = true;
  try {
    await refreshVideo();
    $("video-status").textContent = "Model availability refreshed.";
  } catch (error) {
    $("video-status").textContent = error.message;
  } finally {
    button.disabled = false;
  }
};

$("queue-video").onclick = async () => {
  const item = project.scenes[selected];
  videoSubmitting = true;
  generationView();
  $("video-status").textContent = "Submitting to local ComfyUI…";
  try {
    const job = await api("/api/video-jobs", {
      scene: item.id, model: item.videoModel, prompt: item.videoPrompt,
      frames: Number(item.videoFrames), shape: item.videoShape,
      seed: item.videoSeed === "" ? null : Number(item.videoSeed)
    });
    videoJobs.unshift(job);
    $("video-status").textContent = job.message;
    scheduleVideo();
  } catch (error) {
    $("video-status").textContent = error.message;
  } finally {
    videoSubmitting = false;
    generationView();
  }
};

function refresh() {
  previousStoryboard = null;
  $("undo").disabled = true;
  for (const id of ["brief", "focus", "source-name", "source-text"]) $(id).value = "";
  $("project-name").value = project.project;
  $("ratio").value = project.ratio;
  $("captions").checked = project.captions;
  $("download").hidden = true;
  categoryView();
  mediaView();
  sourceView();
  outputView();
  pick(0);
}
refresh();
refreshVideo().catch((error) => { $("video-status").textContent = error.message; });
api("/api/models").then((found) => {
  available = found;
  modelView();
  outputView();
  if (available.missing.length) say("Rendering requires " + available.missing.join(", ") + ".");
}).catch((error) => say("Model inventory unavailable. " + error.message));
