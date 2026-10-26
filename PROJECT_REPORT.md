# 📚 ACADEMIC PROJECT REPORT

## CENTRALIZED COLLEGE STUDY MATERIAL AND PREVIOUS QUESTION PAPER PORTAL

**Project Type:** Full-Stack Academic Web Application  
**Domain:** Educational Technology, Database Management Systems, Network Systems  
**Keywords:** Study Materials, Previous Question Papers, File Sharing, Upload and Download, Database Management, Online and Offline Access, Progressive Web App (PWA).

---

### ABSTRACT
The **Centralized College Study Material and Previous Question Paper Portal** is a web-based application that allows students, faculty members, and administrators to access, upload, share, and download academic resources. Users can easily find and contribute study materials, lecture notes, assignments, lab manuals, and previous years’ question papers. 

The system provides a centralized platform where resources are systematically organized by **Department**, **Semester**, and **Subject**. It includes secure file upload functionality with multi-format validation, relational database management, peer ratings and reviews, user bookmarking, and an administrative control panel to manage users and moderate uploaded content. 

A key innovation of this system is that the responsive web application supports both **online internet access** and **offline access through a local campus network (LAN) or wireless hotspot**. The primary objective of this project is to encourage collaborative knowledge sharing, simplify access to educational resources, save student revision time, eliminate fragmented file distribution, and make high-quality learning materials universally available to everyone.

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background & Motivation
In contemporary higher education institutions, academic study materials and past university examination question papers are essential for student success and exam preparation. Analyzing previous year question papers (PYQs) helps students understand examination patterns, marks allocation, and recurring questions. 

However, in most colleges, educational resources remain highly decentralized. Students typically depend on informal WhatsApp groups, temporary Google Drive links, physical photocopies, or fragmented social media posts. Such channels suffer from:
- Broken or expired links.
- Lack of academic structure (mixed subjects and semesters).
- High risk of malware or corrupted files.
- Complete unavailability when students lack active internet data on campus.

### 1.2 Problem Statement
There is an urgent need for a unified, institutional repository that organizes academic documents systematically by department, semester, and subject, while remaining accessible over local college networks without requiring internet connectivity.

### 1.3 Objectives of the Project
1. **Centralized Academic Hub:** Provide a single platform where students can find all study materials and previous question papers for any subject within 3 clicks.
2. **Quality Moderation:** Implement a moderation review workflow where student contributions are vetted by faculty or administrators before public publication.
3. **In-Browser Document Preview:** Allow students to view and inspect PDFs and images directly inside the browser before downloading.
4. **Offline & LAN Capability:** Enable full system operation over local Wi-Fi, lab LAN, or offline hotspots with automatic IP discovery.
5. **Peer Feedback & Bookmarks:** Incorporate a 5-star rating system, peer reviews, and personal bookmarking for personalized exam revision.

---

## CHAPTER 2: LITERATURE SURVEY & COMPARATIVE ANALYSIS

| Parameter | Traditional Methods (WhatsApp / Drive) | Existing College Portals | Proposed Centralized Portal |
|---|---|---|---|
| **Organization** | Unorganized chat streams | Often outdated, static PDFs | Hierarchical (Dept $\rightarrow$ Sem $\rightarrow$ Subject $\rightarrow$ Category) |
| **Searchability** | Poor or none | Basic keyword text search | Real-time autocomplete, dynamic multi-tier filters |
| **Document Preview** | Must download file first | Must download file first | Instant In-Browser PDF/Image previewer |
| **Offline Campus LAN** | Requires Internet data | Requires Internet data | Works 100% offline via local Wi-Fi / Hotspot |
| **Moderation Queue** | Zero verification / spam prone | Manual email request to webmaster | Interactive Admin Review Queue with feedback |
| **Student Bookmarks** | None | None | Saved bookmarks list per user account |
| **Mobile Responsiveness** | Inconsistent | Poor desktop-only layout | 100% responsive Tailwind CSS + PWA |

---

## CHAPTER 3: SYSTEM REQUIREMENTS SPECIFICATIONS (SRS)

### 3.1 Software Requirements
- **Operating System:** Windows 10/11, macOS, or Linux
- **Runtime Environment:** Python 3.9+ (Python 3.13 verified)
- **Web Framework:** Flask 3.1
- **Database Engine:** SQLite 3 with Write-Ahead Logging (WAL) and Foreign Key constraints
- **Frontend UI:** HTML5, Tailwind CSS, FontAwesome 6, Vanilla JavaScript (ES6+)
- **Browser:** Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari

### 3.2 Hardware Requirements
- **Processor:** Dual-Core 1.8 GHz or higher
- **RAM:** 2 GB minimum (4 GB recommended)
- **Disk Storage:** 500 MB for source code and initial database (scalable based on uploaded materials)
- **Network Interface:** Standard 802.11 b/g/n Wi-Fi card or Ethernet LAN port

---

## CHAPTER 4: SYSTEM ARCHITECTURE & DATABASE DESIGN

### 4.1 System Architecture
```
  [ Student / Faculty Client ]        [ Mobile Device (Campus LAN) ]
              │                                      │
              └───────────────┬──────────────────────┘
                              ▼
                   [ Flask 3 Web Server ]
              (Host: 0.0.0.0, Port: 5000)
                              │
          ┌───────────────────┼────────────────────┐
          ▼                   ▼                    ▼
   [ Authentication ]  [ Resource Engine ]   [ Admin Moderation ]
   - Session Auth      - Upload Pipeline     - Review Queue
   - Password Hashing  - File Storage        - User Roles
   - Role Permissions  - PDF Preview         - Academic CRUD
          │                   │                    │
          └───────────────────┼────────────────────┘
                              ▼
                     [ SQLite3 Database ]
           (WAL Mode + Foreign Key Enforcement)
```

### 4.2 Entity-Relationship (ER) Schema

#### 1. `departments`
- `id` (INTEGER, Primary Key, Autoincrement)
- `name` (TEXT, Unique, NOT NULL)
- `code` (TEXT, Unique, NOT NULL) — *e.g., CSE, IT, MECH*
- `description` (TEXT)
- `icon` (TEXT)
- `is_active` (INTEGER, Default 1)
- `created_at` (TIMESTAMP)

#### 2. `subjects`
- `id` (INTEGER, Primary Key, Autoincrement)
- `name` (TEXT, NOT NULL) — *e.g., Data Structures and Algorithms*
- `code` (TEXT, NOT NULL) — *e.g., CS301*
- `department_id` (INTEGER, Foreign Key $\rightarrow$ `departments.id`)
- `semester` (INTEGER, NOT NULL, 1 to 8)
- `description` (TEXT)
- `is_active` (INTEGER, Default 1)

#### 3. `users`
- `id` (INTEGER, Primary Key, Autoincrement)
- `username` (TEXT, Unique, NOT NULL)
- `email` (TEXT, Unique, NOT NULL)
- `password_hash` (TEXT, NOT NULL)
- `full_name` (TEXT, NOT NULL)
- `roll_number` (TEXT)
- `department_id` (INTEGER, Foreign Key $\rightarrow$ `departments.id`)
- `semester` (INTEGER)
- `role` (TEXT, Default 'student') — *'student', 'faculty', 'admin'*
- `is_active` (INTEGER, Default 1)

#### 4. `resources`
- `id` (INTEGER, Primary Key, Autoincrement)
- `title` (TEXT, NOT NULL)
- `description` (TEXT)
- `resource_type` (TEXT, NOT NULL) — *'Question Paper', 'Lecture Notes', 'Lab Manual', 'Assignment', 'Syllabus', 'Reference Book'*
- `department_id` (INTEGER, Foreign Key $\rightarrow$ `departments.id`)
- `semester` (INTEGER, NOT NULL)
- `subject_id` (INTEGER, Foreign Key $\rightarrow$ `subjects.id`)
- `academic_year` (TEXT) — *e.g., '2024-2025'*
- `exam_type` (TEXT) — *'End-Semester', 'Mid-Term 1', 'Mid-Term 2', 'Model Exam', 'Supplementary', 'N/A'*
- `file_name` (TEXT, NOT NULL) — *Unique stored file path*
- `original_file_name` (TEXT, NOT NULL)
- `file_size` (INTEGER)
- `file_ext` (TEXT)
- `uploader_id` (INTEGER, Foreign Key $\rightarrow$ `users.id`)
- `status` (TEXT, Default 'pending') — *'pending', 'approved', 'rejected'*
- `rejection_reason` (TEXT)
- `download_count` (INTEGER, Default 0)
- `view_count` (INTEGER, Default 0)
- `is_featured` (INTEGER, Default 0)
- `tags` (TEXT)

#### 5. `resource_ratings`
- `id` (INTEGER, Primary Key, Autoincrement)
- `resource_id` (INTEGER, Foreign Key $\rightarrow$ `resources.id`)
- `user_id` (INTEGER, Foreign Key $\rightarrow$ `users.id`)
- `rating` (INTEGER, Check 1 to 5)
- `review` (TEXT)
- *Constraint: Unique(resource_id, user_id)*

#### 6. `bookmarks`
- `id` (INTEGER, Primary Key, Autoincrement)
- `resource_id` (INTEGER, Foreign Key $\rightarrow$ `resources.id`)
- `user_id` (INTEGER, Foreign Key $\rightarrow$ `users.id`)
- *Constraint: Unique(resource_id, user_id)*

#### 7. `activity_logs`
- `id` (INTEGER, Primary Key, Autoincrement)
- `user_id` (INTEGER, Foreign Key $\rightarrow$ `users.id`)
- `action` (TEXT)
- `details` (TEXT)
- `ip_address` (TEXT)
- `created_at` (TIMESTAMP)

---

## CHAPTER 5: IMPLEMENTATION & KEY MODULES

### 5.1 Dynamic Cascading Dropdown Architecture
When uploading or browsing materials, selecting a department and semester triggers an asynchronous AJAX request to `/api/subjects?dept_id=X&semester=Y`. The endpoint returns only the curriculum subjects associated with that department and semester, preventing incorrect subject tagging.

### 5.2 Secure File Ingestion Pipeline
1. Sanitizes user input filenames using `werkzeug.utils.secure_filename`.
2. Verifies file extension against strict whitelist (`pdf`, `doc`, `docx`, `ppt`, `txt`, `zip`, `rar`, `png`, `jpg`).
3. Prepends a random 12-character hex UUID to prevent filename collisions.
4. Checks byte limit (enforced at 64 MB maximum).
5. Writes the file to `static/uploads/` and logs file size in bytes.

### 5.3 Local Area Network (LAN) & Offline Engine
To fulfill the offline requirement:
```python
def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
```
The server binds to `0.0.0.0:5000`. Any student on the same Wi-Fi router or laptop mobile hotspot connects directly to `http://<IP>:5000`. A Service Worker (`sw.js`) and Web Manifest (`manifest.json`) cache assets for instant offline PWA access.

---

## CHAPTER 6: SYSTEM TESTING & TEST CASES

| Test ID | Test Scenario | Input Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **TC-01** | User Registration | Valid details with unique email | Account created, session established, redirect to Home | Account created successfully | **PASS** |
| **TC-02** | File Upload (Student) | PDF file (2.4 MB) with valid metadata | File saved, status set to 'pending', added to review queue | Uploaded and set to 'pending' | **PASS** |
| **TC-03** | File Upload (Faculty) | PDF file with valid metadata | File saved, status set to 'approved', published immediately | Directly published | **PASS** |
| **TC-04** | File Type Validation | Executable file (`.exe`) | Rejected with alert message "File format not supported" | Upload blocked | **PASS** |
| **TC-05** | Document Preview | Valid PDF resource ID | PDF rendered in in-browser iframe | PDF renders cleanly | **PASS** |
| **TC-06** | Download Tracking | Click "Download" button | File streamed, `download_count` incremented by 1 | Counter increments | **PASS** |
| **TC-07** | Admin Approval | Admin clicks "Approve" | Status updated to 'approved', published to browse page | Status changes to approved | **PASS** |
| **TC-08** | Offline LAN Access | Connect phone to host hotspot | Browse `http://<host_ip>:5000` | Portal opens and downloads work offline | **PASS** |

---

## CHAPTER 7: CONCLUSION & FUTURE SCOPE

### 7.1 Conclusion
The **Centralized College Study Material and Previous Question Paper Portal** successfully solves the problem of academic resource fragmentation in higher education institutions. By structuring resources into a Department $\rightarrow$ Semester $\rightarrow$ Subject hierarchy, enforcing content quality moderation, and supporting both online and campus LAN offline environments, the portal provides a modern, fast, and equitable learning platform for all students.

### 7.2 Future Scope
1. **Automated OCR & Search inside PDFs:** Extracting text from handwritten notes and question paper images using Tesseract OCR.
2. **AI Question Paper Pattern Analyzer:** Automatic frequency analysis highlighting topics asked most frequently across the past 5 years.
3. **Push Notifications:** Instant alerts via Web Push when new lecture notes or model papers are published for a student's enrolled subjects.
