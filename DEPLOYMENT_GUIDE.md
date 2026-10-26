# 🌐 HOW TO MAKE THE PORTAL LIVE USING GITHUB & CLOUD HOSTING

This guide provides step-by-step instructions on how to publish your **Centralized College Study Material and Question Paper Portal** online so that **anyone across the world can access it 24/7 on their phones and laptops**.

---

## ⚠️ Important Note About "GitHub Pages"
- **GitHub Pages** only supports static websites (plain HTML, CSS, JavaScript).
- Because our portal is a **full-stack Python Flask web application** with an interactive **SQLite database, file upload handling, and user authentication**, it cannot run directly on GitHub Pages alone.
- **However, GitHub is the industry-standard foundation used to deploy Python applications!**  
  You push your code to **GitHub**, and then link your GitHub repository to a free Python cloud host like **Render** or **Railway**. The cloud platform connects to your GitHub repository and automatically deploys your live website whenever you update your code!

---

## 🚀 METHOD 1: Deploying via GitHub + Render (Recommended • 100% Free • Permanent Live URL)

Render ([render.com](https://render.com)) is a premier cloud platform for hosting Python Flask applications directly from GitHub with free SSL/HTTPS.

### Step 1: Create a GitHub Repository
1. Log in to [GitHub](https://github.com/) (create a free account if you don't have one).
2. Click the **`+`** icon at the top right and select **"New repository"**.
3. Name your repository (e.g., `college-study-portal` or `academix-portal`).
4. Set it to **Public**.
5. Do **not** check "Initialize with README" (we already have files created).
6. Click **"Create repository"**.

### Step 2: Push Your Project to GitHub

#### Option A: Using Git CLI (if installed)
Open PowerShell or Command Prompt in the project directory:
```powershell
cd C:\Users\Abhishek\.gemini\antigravity\scratch\college_portal

git init
git add .
git commit -m "Initial commit of college study portal"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
git push -u origin main
```

#### Option B: Using GitHub Web Browser (No Git installation needed!)
1. On your newly created GitHub repository page, click the link that says **"uploading an existing file"**.
2. Open File Explorer to:
   `C:\Users\Abhishek\.gemini\antigravity\scratch\college_portal`
3. Select and drag all project files and folders (`app.py`, `config.py`, `database.py`, `Procfile`, `render.yaml`, `requirements.txt`, `routes/`, `templates/`, `static/`, etc.) into the GitHub upload box.
4. Click **"Commit changes"**.

---

### Step 3: Deploy for Free on Render.com
1. Go to [Render.com](https://render.com/) and click **"Get Started"** (Sign up using your GitHub account with 1 click).
2. Once on your Render Dashboard, click the **"New +"** button and select **"Web Service"**.
3. Select **"Build and deploy from a Git repository"** and click **Next**.
4. Choose your `college-study-portal` GitHub repository and click **"Connect"**.
5. Render will automatically fill in the settings (configured by our included `render.yaml`):
   - **Name:** `college-study-portal` (or any custom name)
   - **Region:** Choose the closest region (e.g., Singapore or Frankfurt or Oregon)
   - **Branch:** `main`
   - **Language:** `Python 3`
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt && python seed_data.py
     ```
   - **Start Command:** 
     ```bash
     gunicorn "app:create_app()" --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```
   - **Instance Type:** Select **"Free"**.
6. Click **"Deploy Web Service"**.

---

### Step 4: Your Website is Live! 🎉
Render will build the Python environment, seed the database with departments, subjects, and sample question papers, and launch the web server.

Within 1 to 2 minutes, you will receive your permanent public HTTPS URL at the top left of the Render dashboard:
```
https://college-study-portal-xxxx.onrender.com
```

Anyone in the world—students, teachers, and examiners—can now access your live portal on their smartphones and computers!

---

## ⚡ METHOD 2: Instant 10-Second Live Public URL (For Live Demos & Viva)

If you need a live public URL **right now** for a classroom presentation or viva defense without signing up for cloud hosting:

You can use **Cloudflare Tunnel** or **ngrok** to project your local running portal onto a public HTTPS link.

### Using Cloudflare Tunnel (Zero Sign-up):
1. In PowerShell, start your Flask portal:
   ```powershell
   cd C:\Users\Abhishek\.gemini\antigravity\scratch\college_portal
   python app.py
   ```
2. Open a second PowerShell window and run:
   ```powershell
   winget install Cloudflare.cloudflared
   cloudflared tunnel --url http://localhost:5000
   ```
3. Cloudflare will output an instant, secure public URL such as:
   ```
   https://random-words-here.trycloudflare.com
   ```
4. Share this link with anyone, and they can browse, upload, and download notes on their phones in real-time!

---

## 🐍 METHOD 3: PythonAnywhere (Alternative Free Host)

1. Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Open a **Bash Console** in your PythonAnywhere dashboard and clone your GitHub repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/college-study-portal.git
   cd college-study-portal
   pip install -r requirements.txt
   python seed_data.py
   ```
3. Go to the **Web** tab, click **"Add a new web app"**, choose **Flask**, and set the WSGI configuration file to:
   ```python
   import sys
   path = '/home/YOUR_USERNAME/college-study-portal'
   if path not in sys.path:
       sys.path.append(path)

   from app import create_app
   application = create_app()
   ```
4. Click **Reload**. Your site is now live at:
   ```
   https://YOUR_USERNAME.pythonanywhere.com
   ```

---

## 📋 Pre-Configured Live Demonstration Accounts

Once your site is live, use these pre-seeded accounts to demonstrate the platform to professors and examiners:

| Role | Username | Password | Key Feature to Demo |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Review queue, approve/reject student uploads, user management |
| **Faculty Member** | `prof_sharma` | `faculty123` | Direct publication without review queue, syllabus management |
| **Student** | `student1` | `student123` | Browse, in-browser PDF preview, download tracking, bookmarks, rating |

---

## 🔄 Automatic Continuous Deployment (CI/CD)
Because your cloud web service is connected to GitHub:
- Whenever you make changes to files (templates, styles, Python code), simply push your changes to GitHub:
  ```powershell
  git add .
  git commit -m "Updated features"
  git push
  ```
- **Render will automatically detect the push and redeploy your live website with zero downtime!**
