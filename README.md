Civil Engineering Visual Library
A two-image teaching tool for civil engineering onboarding. Every slide pairs a real-world view with a CAD view (or before/after, plan/section, etc.) and supports voice narration so trainers can talk viewers through what they’re seeing.

## Public viewer (GitHub Pages, testing)

**Live viewer:** https://rodgers-consulting-inc.github.io/RodgersWay_VisualPlaybook/

That URL loads the **read-only app** (`index.html`). Pages must be turned on for this repo (Settings → Pages → branch `main`, folder `/ (root)`). If you see a 404, Pages is off or hasn’t finished building yet (often within a minute of a push).

**Editor:** there is intentionally no polished “secret” Pages URL—you can still open it locally (see below) at `http://localhost:…/editor.html`. Do not rely on obscurity for confidentiality; assume anyone with the link can open it until you add real auth.


## What's in this repo

```
├── index.html          # Public viewer (read-only)
├── editor.html        # Authoring tool (autosaves to this browser via localStorage)
├── assets/
│   └── shared.js      # Shared schema/helpers (viewer + editor)
├── data/
│   └── library.json   # Modules, slides (v2 blocks), narration paths
├── media/
│   ├── images/
│   ├── audio/
│   └── video/         # Present when you Publish slides that include video blocks
└── README.md
```


## Running locally (recommended for collaborators)

The viewer **loads** `data/library.json` with `fetch`. The editor **Loads** from the same path and uses `assets/shared.js`. **Opening `index.html` or `editor.html` as `file://` often breaks** those requests. Use a tiny HTTP server from the **repo root**.

### Option A — Python

```bash
cd RodgersWay_VisualPlaybook
python -m http.server 8080
```

Then:

- **Viewer:** http://localhost:8080/  (or `http://localhost:8080/index.html`)
- **Editor:** http://localhost:8080/editor.html  

Stop with `Ctrl+C`.

### Option B — Node (no install beyond Node)

```bash
cd RodgersWay_VisualPlaybook
npx --yes serve -p 8080
```

Open the URLs shown in the terminal (same `/` and `/editor.html` paths).

### Option C — VS Code

Install **Live Server**, open this folder, then “Open with Live Server” from `index.html` or browse to `/editor.html` on the port it chooses.

---

## Workflow for collaborators (content + quick UI tweaks)

1. Clone and stay on **`main`** (or the branch your team agrees is current).
2. Pull before you start: `git pull`.
3. Start a **local server** (above) from the project root—not by double‑clicking the HTML files.
4. Edit **content** in the **editor** (`/editor.html`). Work **autosaves in that browser profile** (`localStorage`). Use **Backup** sometimes to download JSON as a safety copy.
5. Preview the **viewer** at `/` to see what learners see.
6. When a batch is ready, use **Publish** in the editor: it downloads a **zip** with `data/library.json` and `media/` laid out for git.
7. Unzip **into your clone** (replace `data/` and `media/` as needed), then commit and push:

   ```bash
   git add .
   git commit -m "Update training library content"
   git push
   ```

8. Wait for GitHub Pages to refresh (~1 minute), then hard-refresh the **public viewer** link above (`Ctrl+Shift+R` / `Cmd+Shift+R`).

**Load from repo:** In the editor, **Load** re-reads `data/library.json` from the running server (**discards unsaved browser draft**)—use after a colleague pushed new content / after you switched branches.


## Publish updates via zip (still the shipped path until cloud publish exists)

Steps 6–8 above replace “magic deploy”: there is **no automatic push from the browser** yet; Publish produces files you merge into git.

When you Publish, the bundle reorganizes assets for git:

- Images → `media/images/` like `<slide-id>-A.png`
- Audio → `media/audio/` like `<slide-id>.webm`
- Video blocks (when used) → `media/video/`
- `data/library.json` points at paths (no huge base64 in the exported JSON)


## First-time setup (repository + Pages)

Clone this repo:

```bash
git clone https://github.com/Rodgers-Consulting-Inc/RodgersWay_VisualPlaybook.git
cd RodgersWay_VisualPlaybook
```

Enable **GitHub Pages** on GitHub:

- Repo **Settings → Pages → Build and deployment**.
- Source: **Deploy from a branch**.
- Branch: **`main`**, folder **`/ (root)`**, Save.

The site URL should match:

**https://rodgers-consulting-inc.github.io/RodgersWay_VisualPlaybook/**


## Using the editor

### Adding images

Click an image slot (or drag a file onto it). Use **Teach → Image A / Image B type** dropdowns for labels (real-world vs CAD, etc.).

### Recording narration

**Voice** tab → **Record** (microphone permission once). Follow the narration script hints in the panel. **Stop** when done—or upload `.mp3` / `.wav` / `.m4a`.

### Teaching scaffold

**Teach** tab: five answers that appear in the viewer as “Teaching notes” after narration.

### Organizing slides

Toolbar: reorder, duplicate, delete. Sidebar: **+ ADD** modules.

### Backups

**Backup** downloads the full JSON—keep copies if browser storage might be cleared.

### Editor URL note

Treat `editor.html` as a **draft studio** (`noindex` in metadata). Prefer **localhost** during development.


## Troubleshooting

**Viewer or editor doesn’t load data**

- Serve from **localhost** as above, not raw `file://`.

**GitHub Pages 404**

- Confirm `index.html` is at the repo root and Pages is enabled on `main`.

**Publish / “storage full”**

- `localStorage` is small; Publish more often or use Backup, compress media, shorten narrations.

**Changes don’t appear on Pages**

- Check Actions; force-refresh the viewer URL.


## License / use

Internal training material for Rodgers Consulting.  
Creating communities with clients who share our values.
