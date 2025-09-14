
Amrit-core - Naam Tone Studio (prototype)
Files:
 - index.html
 - styles.css
 - app.js
 - manifest.json
 - sw.js (service worker for offline cache)
 - icons/icon-192.svg, icon-512.svg

How to run locally:
1) Put these files in a web server root (or use a simple local server).
   - e.g. on macOS / iPad with a web server app, or using Python locally:
     python3 -m http.server 8000
   - then open http://localhost:8000 in your browser.
2) To publish on GitHub Pages:
   - Create a repository and push these files to the main branch.
   - Enable GitHub Pages (Settings → Pages → Deploy from branch → main / root).
   - After a minute you'll get a site URL to open.
3) To install on iPad/iPhone:
   - Open the site in Safari → Share → Add to Home Screen.

Notes:
 - The "Record" button uses MediaRecorder and will save a short webm audio file.
 - This is a small starter PWA and "Naam Tone Studio" for testing and demo.
