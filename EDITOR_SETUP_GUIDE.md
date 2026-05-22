# RodgersWay Visual Playbook — Editor Setup Guide

**Who this is for:** Anyone who needs to add, edit, or update slides in the Visual Playbook — no coding experience required.

**What you'll end up with:** A working copy of the project on your computer, a local web server running, and the editor open in your browser so you can create and update content.

---

## Table of Contents

1. [What You're Setting Up (and Why)](#1-what-youre-setting-up-and-why)
2. [Create a GitHub Account](#2-create-a-github-account)
3. [Get Access to the Repository](#3-get-access-to-the-repository)
4. [Install Git Bash (Windows)](#4-install-git-bash-windows)
5. [Install Python](#5-install-python)
6. [Download (Clone) the Project Files](#6-download-clone-the-project-files)
7. [Start the Local Web Server](#7-start-the-local-web-server)
8. [Open the Editor in Your Browser](#8-open-the-editor-in-your-browser)
9. [Making and Saving Edits](#9-making-and-saving-edits)
10. [Publishing Your Changes to GitHub](#10-publishing-your-changes-to-github)
11. [Your Daily Editing Routine](#11-your-daily-editing-routine)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. What You're Setting Up (and Why)

The Visual Playbook is a website that lives on **GitHub** — a cloud service that stores files and tracks every change ever made to them. The public viewer is always online at:

> https://rodgers-consulting-inc.github.io/RodgersWay_VisualPlaybook/

The **editor**, however, is not something you run in the cloud — it runs on **your own computer**. This is intentional: it keeps drafts private and gives you full control before anything goes public.

Here is the overall flow:

```
Your Computer                          GitHub (cloud)
─────────────────────────────          ──────────────────────────
 Git Bash  ──── clone ──────────────►  Repository (file storage)
 Python server  (runs locally)                │
 Browser ─► editor.html  (edit)               │
           ─► Publish zip (download)          │
 Git Bash  ──── push ──────────────────────►  Repository updated
                                              │
                                    GitHub Pages builds live site
                                              ▼
                                    Public viewer updated (~1 min)
```

You need four free tools:

| Tool | What it does |
|------|-------------|
| **GitHub account** | Identifies you so you can push changes |
| **Git Bash** | Command-line tool to download and upload files |
| **Python** | Runs a tiny local web server so the editor works correctly |
| **A web browser** | Where you actually use the editor (Chrome or Edge recommended) |

---

## 2. Create a GitHub Account

> Skip this step if you already have a GitHub account.

1. Open your browser and go to **https://github.com**
2. Click **Sign up** in the top-right corner.
3. Enter your **email address** and click **Continue**.
4. Create a **password** (at least 15 characters or 8 characters with mixed types). Click **Continue**.
5. Choose a **username** (e.g., `jane-rodgers`). Click **Continue**.
6. Answer whether you want product updates and click **Continue**.
7. Complete the **puzzle** to verify you're human.
8. Click **Create account**.
9. GitHub will send a **verification email**. Open that email and click the link (or type the 8-digit code).
10. On the "Tell us about yourself" screen, you can skip/answer however you like. Click **Continue**.
11. Choose the **Free** plan when prompted.

**You now have a GitHub account.** Write down your username and password somewhere safe.

---

## 3. Get Access to the Repository

The project files are stored in a **private repository** (a folder on GitHub). You need to be invited before you can download or upload anything.

**Send your GitHub username to the repository owner** (your manager or the person who shared this guide with you). They will add you as a **collaborator**.

You will receive an email from GitHub with the subject line:
> *"You have been invited to collaborate on Rodgers-Consulting-Inc/RodgersWay_VisualPlaybook"*

1. Open that email.
2. Click the big **"View invitation"** button.
3. On the GitHub page that opens, click **Accept invitation**.
4. You now have access to the repository.

---

## 4. Install Git Bash (Windows)

> **Mac users:** Skip to Step 5 — Git is already installed on macOS. Open the **Terminal** app (search for "Terminal" in Spotlight) wherever this guide says "open Git Bash."

Git Bash gives you a command-line window that can talk to GitHub.

1. Go to **https://git-scm.com/downloads**
2. Click **Download for Windows**. The download starts automatically.
3. Open the downloaded file (it will be named something like `Git-2.xx.x-64-bit.exe`).
4. Click **Yes** when Windows asks if you want to allow the app to make changes.
5. Read the license and click **Next**.
6. **Installation location** — leave the default and click **Next**.
7. **Components screen** — leave all defaults checked and click **Next**.
8. **Start Menu folder** — leave default, click **Next**.
9. **Default editor** — change this to **"Use Notepad as Git's default editor"** (easier for beginners), then click **Next**.
10. **Initial branch name** — select **"Let Git decide"** and click **Next**.
11. **PATH environment** — select **"Git from the command line and also from 3rd-party software"** (usually the second option). Click **Next**.
12. All remaining screens — leave every option at its default and keep clicking **Next**.
13. On the final screen, click **Install**.
14. When it finishes, click **Finish**.

**Test it worked:**

- Press the **Windows key**, type `git bash`, and press **Enter**.
- A black window with a `$` prompt should open.
- Type `git --version` and press **Enter**.
- You should see something like `git version 2.44.0`. If you do, Git Bash is working.

---

## 5. Install Python

Python is used to run a small local web server that lets the editor load its files correctly.

1. Go to **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python 3.x.x"** button (the latest version is fine).
3. Open the downloaded file (e.g., `python-3.12.x-amd64.exe`).
4. **IMPORTANT — Before clicking anything else**, check the box at the bottom that says **"Add Python to PATH"**. This is easy to miss.

   > ✅ **Add Python 3.x to PATH** ← make sure this is checked

5. Click **Install Now** (the top option).
6. Click **Yes** when Windows asks for permission.
7. When the install finishes, click **Close**.

**Test it worked:**

- Open **Git Bash** (press Windows key, type `git bash`, Enter).
- Type `python --version` and press **Enter**.
- You should see something like `Python 3.12.3`.
- If you see an error, try `python3 --version` instead. Either response showing a version number means Python is installed.

---

## 6. Download (Clone) the Project Files

"Cloning" means downloading a full copy of the project from GitHub to your computer — including all files and the entire history of changes.

**Step 6a — Tell Git who you are (one-time setup)**

Open **Git Bash** and type the two commands below, replacing the example name and email with your own. Press **Enter** after each one.

```
git config --global user.name "Your Full Name"
git config --global user.email "your@email.com"
```

Use the **same email address** you registered on GitHub.

**Step 6b — Choose where to save the project**

Decide on a folder. Most people use their **Documents** folder. In Git Bash, type:

```
cd ~/Documents
```

Press **Enter**. (The `~` means "your home folder" — Git Bash understands this on all systems.)

If you prefer a different location, navigate there with `cd`. For example:
- Desktop: `cd ~/Desktop`
- A custom folder: `cd "/c/Users/YourName/Work"`

**Step 6c — Clone the repository**

Type this exactly as shown and press **Enter**:

```
git clone https://github.com/Rodgers-Consulting-Inc/RodgersWay_VisualPlaybook.git
```

Git Bash will ask for your **GitHub username** and then your **password**.

> **Note on passwords:** GitHub no longer accepts your regular account password for this step. You need a **Personal Access Token** (PAT). Here's how to get one:
>
> 1. On GitHub.com, click your profile picture (top-right) → **Settings**.
> 2. Scroll all the way down on the left sidebar → click **Developer settings**.
> 3. Click **Personal access tokens** → **Tokens (classic)**.
> 4. Click **Generate new token** → **Generate new token (classic)**.
> 5. Give it a name like `Editor access`.
> 6. Set **Expiration** to `No expiration` (or a date that works for you).
> 7. Under **Scopes**, check **repo** (the very first checkbox — this covers all repo permissions).
> 8. Scroll to the bottom and click **Generate token**.
> 9. **Copy the token immediately** — GitHub will never show it again. Paste it in a safe place (like a secure notes app or password manager).
>
> Use this token as your password when Git Bash asks.

After cloning finishes, you will see a new folder called `RodgersWay_VisualPlaybook` in your Documents (or wherever you navigated in Step 6b).

**Step 6d — Enter the project folder**

```
cd RodgersWay_VisualPlaybook
```

You are now "inside" the project. Your Git Bash prompt will show `(main)` to confirm you are on the main branch.

---

## 7. Start the Local Web Server

Every time you want to edit, you need to start a small web server first. This is a one-command step.

**Make sure you are in the project folder** (your Git Bash prompt should show `RodgersWay_VisualPlaybook`). If you closed Git Bash since last time, re-open it and type:

```
cd ~/Documents/RodgersWay_VisualPlaybook
```

Then start the server:

```
python -m http.server 8080
```

You will see output like:

```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

**The server is now running.** This Git Bash window needs to stay open the entire time you're editing — do not close it. If you accidentally close it, just open a new Git Bash window, navigate back to the project folder, and run the command again.

> **To stop the server:** Click inside the Git Bash window and press **Ctrl + C**.

---

## 8. Open the Editor in Your Browser

With the server running, open your browser (Chrome or Edge recommended) and go to:

**http://localhost:8080/editor.html**

The editor will load. You'll see:

- A **sidebar on the left** listing modules and slides.
- A **main editing area** in the center with image slots, a teach tab, and a voice tab.
- A **toolbar at the top** with options like Load, Backup, and Publish.

You can also open the **public viewer** (what learners see) in another tab:

**http://localhost:8080/**

> **Bookmark both URLs** in your browser — you'll use them every session.

---

## 9. Making and Saving Edits

### Adding a new slide

1. In the left sidebar, click the module you want to add a slide to.
2. Click **+ ADD** (or the add slide button in the toolbar) to create a new slide.
3. Fill in the slide title.

### Adding images to a slide

1. Click on the **Image A** or **Image B** slot in the editor.
2. A file picker will open — find and select the image on your computer.
3. Use the **Type** dropdown next to each image to label it (e.g., "Real-world view", "CAD view").

### Adding teaching notes

1. Click the **Teach** tab in the slide editor.
2. Fill in the five teaching note fields. These appear in the viewer after the narration plays.

### Recording narration

1. Click the **Voice** tab.
2. Click **Record**. Your browser will ask for microphone permission — click **Allow**.
3. Speak your narration clearly.
4. Click **Stop** when finished.
5. You can also click **Upload** to use an existing `.mp3`, `.wav`, or `.m4a` file.

### How saving works

The editor **autosaves your draft to your browser** (a storage area called `localStorage`). This means:

- Drafts are saved automatically — you do not need to click Save.
- Drafts are **only in this browser on this computer** — no one else sees them yet.
- If you clear your browser's storage or switch to a different browser, the draft is lost.

**Backup frequently:** Click **Backup** in the toolbar to download a `.json` file of your work. Store these backup files somewhere safe. This is your safety net.

---

## 10. Publishing Your Changes to GitHub

When you're ready to share your edits with everyone (and update the live public viewer), follow these steps.

### Step 10a — Publish from the editor

1. In the editor, click **Publish** in the toolbar.
2. The editor will package everything into a **zip file** and download it to your computer (usually goes to your Downloads folder). It will be named something like `playbook-export.zip`.

### Step 10b — Unzip into the project folder

1. Go to your **Downloads** folder and find the zip file.
2. Right-click it → **Extract All** → Browse to your project folder (`Documents/RodgersWay_VisualPlaybook`).
3. Click **Extract**.
4. When asked if you want to replace existing files, click **Yes to All**.

This will update the `data/` and `media/` folders inside your project with your new content.

### Step 10c — Pull the latest changes first

Before pushing your work, always grab any changes your colleagues may have pushed:

```
git pull origin main
```

If it says `Already up to date.` — great, nothing to merge.

If there is a conflict (rare), reach out to a colleague or your technical contact before proceeding.

### Step 10d — Stage and commit your changes

Tell Git which files changed:

```
git add .
```

(The `.` means "all changed files in this folder.")

Write a short description of what you changed:

```
git commit -m "Add slides for Module 3 drainage section"
```

Replace the message in quotes with a brief description of your actual changes.

### Step 10e — Push to GitHub

```
git push origin main
```

Git Bash will ask for your GitHub username and your **Personal Access Token** (the one you created in Step 6c). Type them and press Enter after each.

You will see output ending with something like:

```
To https://github.com/Rodgers-Consulting-Inc/RodgersWay_VisualPlaybook.git
   abc1234..def5678  main -> main
```

That means your changes are now on GitHub.

### Step 10f — Wait for the live site to update

GitHub Pages takes about 1 minute to rebuild the public viewer. Then visit:

> https://rodgers-consulting-inc.github.io/RodgersWay_VisualPlaybook/

Press **Ctrl + Shift + R** (Windows) or **Cmd + Shift + R** (Mac) to force-refresh the page and see your changes.

---

## 11. Your Daily Editing Routine

Once you're set up, every editing session looks like this:

```
1. Open Git Bash
2. cd ~/Documents/RodgersWay_VisualPlaybook
3. git pull origin main          ← get latest changes from colleagues
4. python -m http.server 8080    ← start the server (keep window open)
5. Open browser → http://localhost:8080/editor.html
6. Edit slides / add images / record narration
7. Click Backup in the editor    ← save a safety copy
8. When ready to publish:
   a. Click Publish in editor → download zip
   b. Extract zip into project folder (replace files)
   c. In Git Bash (open a NEW tab or window, server still running in the first):
      git pull origin main
      git add .
      git commit -m "Describe what you changed"
      git push origin main
9. Wait ~1 min, then refresh the public viewer link to confirm
```

> **Tip — Two Git Bash windows:** Keep your server running in one Git Bash window and open a second window for git commands. To open a second Git Bash window, right-click the Git Bash icon in the taskbar and choose "Git Bash".

---

## 12. Troubleshooting

### "The editor loads but shows no content"

- Make sure you started the server (`python -m http.server 8080`) and are visiting `http://localhost:8080/editor.html`, not a `file://` path.
- Click **Load** in the editor toolbar to re-read the data file from the server.

### "python is not recognized as a command"

- Python was not added to PATH during install. Re-run the Python installer, choose "Modify", and make sure "Add Python to environment variables" is checked.
- Alternatively, try `python3 -m http.server 8080` instead.

### "Port 8080 is already in use"

- Another program is using port 8080. Use a different port number: `python -m http.server 8081`
- Then visit `http://localhost:8081/editor.html` instead.

### "Authentication failed" when doing git push/pull

- Your Personal Access Token may have expired or been entered incorrectly.
- Generate a new token (Step 6c) and try again.
- On Windows, Git may store old credentials. Open **Credential Manager** (search in Start menu) → **Windows Credentials** → find any entry for `github.com` → delete it, then try the git command again and enter your new token.

### "My edits disappeared from the editor"

- The editor saves drafts in browser `localStorage`. This can be cleared if you cleared browser history/data.
- This is why you should **Backup often**. If you have a backup file, click **Load** in the editor and select your backup `.json` file to restore it.

### "The public viewer didn't update after I pushed"

- Wait 1–2 minutes and try again with a hard refresh (Ctrl + Shift + R).
- Check that your push actually succeeded — Git Bash should show output confirming it.
- On GitHub.com, go to your repository → click the **Actions** tab to see if the Pages build completed.

### "I got a merge conflict"

- This means two people edited the same file at the same time.
- Do not proceed — contact your team's technical contact. They can help resolve it without losing anyone's work.

---

*Last updated: May 2026 | For questions or access issues, contact your repository administrator.*
