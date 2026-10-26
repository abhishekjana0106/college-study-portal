# 🎓 Centralized College Study Material & Previous Question Paper Portal (Academix)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite3%20WAL-lightgrey.svg)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Frontend-Tailwind%20CSS-38bdf8.svg)](https://tailwindcss.com/)
[![LAN / Offline](https://img.shields.io/badge/Access-Online%20%26%20Campus%20LAN-emerald.svg)](#-offline--local-campus-network-access)

A full-stack, responsive web application engineered to centralize academic resources across college departments. The platform allows students and faculty to access, upload, share, moderate, and download past examination question papers, lecture notes, lab manuals, and assignments with seamless online and offline local network (LAN) accessibility.

---

## 📌 Project Abstract
The **Centralized College Study Material and Previous Question Paper Portal** is a web-based application that allows anyone to access, upload, share, and download academic resources. Users can easily find and contribute study materials, lecture notes, assignments, and previous years’ question papers. 

The system provides a centralized platform where resources are organized by **Department**, **Semester**, and **Subject**. It includes file upload functionality with format validation, database management, peer ratings and reviews, bookmarking, and an administrative control panel to manage users and moderate uploaded content. The responsive website supports both **online internet access** and **offline access through a local college network or hotspot**.

**Keywords:** *Study Materials, Previous Question Papers, File Sharing, Upload and Download, Database Management, Online and Offline Access, PWA.*

---

## 🌟 Key Features

### 1. 🗂️ Academic Resource Organization
- **Hierarchical Classification:** Resources cataloged strictly by Department (CSE, IT, AI-DS, ECE, EEE, MECH, CIVIL, BSH), Semester (Semesters 1 to 8), and Subject.
- **Categorized Material Types:**
  - Previous Year Examination Question Papers (PYQs)
  - Faculty Lecture Notes & Slides
  - Laboratory Manuals & Code
  - Assignments & Model Solutions
  - Regulation Syllabus & Curriculum
  - Reference Books & Guides
- **Exam Types:** Filter by End-Semester, Mid-Term 1, Mid-Term 2, Model Exam, and Supplementary.

### 2. 🔍 Search & Exploration
- **Real-Time Autocomplete Search:** Instant suggestion bar for subject codes (e.g. `CS301`, `DBMS`) and topics.
- **Multi-parameter Filtering:** Instant filtering by Department, Semester, Subject, Resource Type, and Academic Year.
- **Sorting Modes:** Sort by Newest, Most Downloaded, Highest Rated, or Alphabetical.

### 3. 📄 Document Preview & Download
- **In-Browser PDF & Image Preview:** Embedded viewer allowing students to inspect question papers before downloading.
- **One-Click Downloads:** Download files directly with real-time download counter tracking.
- **Ratings & Reviews:** 5-star peer rating system with feedback comments.
- **Personal Bookmarks:** Pin critical question papers and notes for quick revision before examinations.
- **Share Options:** 1-click URL copying and WhatsApp sharing for student study groups.

### 4. 📤 File Upload & Moderation Workflow
- **Drag-and-Drop Dropzone:** Clean drag-and-drop file upload with format and size validation (up to 64 MB).
- **Dynamic Cascading Dropdowns:** Selecting a department and semester automatically filters only the relevant subjects.
- **Role-Based Moderation:**
  - *Student uploads* enter a **Pending Review Queue** to prevent copyright infringement or spam.
  - *Faculty/Admin uploads* are automatically verified and published instantly.
- **Contributor Tracking:** Students can track their submission status (*Approved*, *Pending*, *Rejected with feedback*) in their "My Uploads" dashboard.

### 5. 🛡️ Role-Based Authentication & Admin Panel
- **3 Access Roles:** `Guest` (view/download), `Student` (upload/bookmark/rate), `Faculty` (instant upload/manage), `Admin` (full system control).
- **Executive Admin Dashboard:**
  - Live KPI cards: Total Resources, Pending Queue, Total Downloads, Total Users.
  - Review Queue: 1-click Approve or Reject with custom feedback for students.
  - Resource Manager: Edit metadata, toggle "Featured" materials on the homepage, delete inappropriate files.
  - User Management: Change user roles, activate/deactivate accounts.
  - Academic Structure CRUD: Add/edit Departments and Subjects.
  - Audit Logs: Detailed activity trail with timestamps, user IDs, actions, and IP addresses.

### 6. 📶 Offline & Local Campus Network (LAN) Support
- **Zero-Internet Campus Operation:** Configured to bind on `0.0.0.0:5000` so any smartphone, tablet, or PC connected to the college Wi-Fi, lab LAN, or laptop hotspot can access the repository at `http://<HOST_IP>:5000`.
- **Progressive Web App (PWA):** Service worker (`sw.js`) and Web Manifest (`manifest.json`) cache core pages and static assets for offline browsing.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Backend Framework** | Python 3, Flask 3.1, Werkzeug (Security & File Uploads) |
| **Database** | SQLite3 with WAL (Write-Ahead Logging) & Foreign Keys |
| **Frontend UI** | HTML5, Tailwind CSS (CDN), FontAwesome 6 Icons |
| **Offline & PWA** | Vanilla JavaScript (ES6+), Service Worker API, Cache API, Manifest |
| **Network Engine** | Python Socket (automatic LAN IP discovery) |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9 or higher (Python 3.13 tested and verified)
- Web browser (Chrome, Edge, Firefox, Safari)

### Option A: 1-Click Launch (Windows)
Double-click the **`start.bat`** file in the project directory. It automatically seeds the database on first run and starts the web server.

### Option B: Terminal / Command Prompt
```powershell
# 1. Navigate to the project directory
cd C:\Users\Abhishek\.gemini\antigravity\scratch\college_portal

# 2. (First time only) Seed database with departments, subjects, and sample resources
python seed_data.py

# 3. Start the application
python app.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🔑 Default Credentials

The database comes pre-seeded with realistic test accounts for instant evaluation:

| Role | Username | Password | Email |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | `admin@college.edu` |
| **Faculty (HOD)** | `prof_sharma` | `faculty123` | `sharma@college.edu` |
| **Faculty (AI-DS)** | `prof_priya` | `faculty123` | `priya@college.edu` |
| **Student 1** | `student1` | `student123` | `aarav@college.edu` |
| **Student 2** | `student2` | `student123` | `sneha@college.edu` |

*(You can also register new student and faculty accounts anytime from the registration page!)*

---

## 📶 Offline & Local Campus Network Access

To share the portal with other devices in your college lab, classroom, or hostel without internet:

1. Connect the host computer and mobile devices to the **same Wi-Fi router** or **turn on a Mobile Hotspot** from the host laptop.
2. When `app.py` runs, it outputs your local IP address in the terminal banner:
   ```
   * Local Access:     http://localhost:5000
   * LAN/Offline WiFi: http://192.168.1.15:5000
   ```
3. On any mobile phone, tablet, or other laptop, open a browser and type:
   ```
   http://<YOUR_IP>:5000
   ```
4. All students on the local network can now search, view, upload, and download study materials completely offline!

---

## 📂 Project Architecture

```
college_portal/
├── app.py                 # Application factory, context processors, local IP discovery
├── config.py              # Central configuration (database, upload paths, limits)
├── database.py            # SQLite schema definition, indexes, connection management
├── helpers.py             # Auth decorators, audit logger, file format validators
├── seed_data.py           # Pre-populates 8 departments, 21 subjects, users & sample PDFs
├── requirements.txt       # Dependencies list
├── start.bat              # One-click Windows runner
├── README.md              # Project documentation
├── PROJECT_REPORT.md      # Comprehensive academic project report for college submission
├── routes/
│   ├── auth.py            # Login, registration, profile, password management
│   ├── main.py            # Home, browse catalog, preview, download, ratings, bookmarks
│   ├── upload.py          # Upload form with validation & "My Uploads" status tracker
│   ├── admin.py           # Dashboard, review queue, user & academic CRUD, audit logs
│   └── api.py             # AJAX endpoints for dynamic subject loading & live search
├── static/
│   ├── css/custom.css     # UI scrollbars, print formatting, glassmorphism
│   ├── js/main.js         # Quick search autocomplete, dynamic DOM handlers
│   ├── js/sw.js           # Progressive Web App service worker for offline caching
│   ├── manifest.json      # PWA web manifest
│   └── uploads/           # Directory where academic PDFs, papers & docs are stored
└── templates/
    ├── base.html          # Global responsive layout with LAN IP banner & navigation
    ├── index.html         # Homepage: Hero banner, quick search, department grid, featured
    ├── browse.html        # Comprehensive repository with filters, sorting & pagination
    ├── resource_detail.html # Document previewer, download action, reviews & bookmarks
    ├── upload.html        # Upload form with cascading department/semester/subject selector
    ├── my_uploads.html    # User's uploaded materials with status badges & feedback
    ├── bookmarks.html     # User's saved/pinned study resources
    ├── offline.html       # Campus LAN & offline network guide
    ├── error.html         # Error template (404, 500, 413)
    ├── auth/              # Login, register, profile templates
    └── admin/             # Dashboard, pending queue, resources, users, depts, subjects, logs
```
