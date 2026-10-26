import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_VIDEO = os.path.join(BASE_DIR, "project_presentation_video.mp4")
DOWNLOADS_COPY = os.path.join(r"C:\Users\Abhishek\Downloads", "College_Study_Material_Portal_Video_Presentation.mp4")

# Resolution & framerate
WIDTH = 1920
HEIGHT = 1080
FPS = 30

# Colors (RGB)
BG_COLOR = (15, 23, 42)          # Slate 900
PANEL_BG = (30, 41, 59)          # Slate 800
PANEL_BORDER = (51, 65, 85)      # Slate 700
BLUE_ACCENT = (37, 99, 235)      # Royal Blue
CYAN_ACCENT = (56, 189, 248)     # Sky Blue
EMERALD_ACCENT = (16, 185, 129)  # Emerald
AMBER_ACCENT = (245, 158, 11)    # Amber
PURPLE_ACCENT = (168, 85, 247)   # Purple
TEXT_WHITE = (255, 255, 255)
TEXT_MUTED = (148, 163, 184)     # Slate 400
TEXT_DARK = (15, 23, 42)

# Load Fonts
FONT_DIR = r"C:\Windows\Fonts"
font_title = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 52)
font_subtitle = ImageFont.truetype(os.path.join(FONT_DIR, "arial.ttf"), 26)
font_h2 = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 36)
font_card_title = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 24)
font_card_body = ImageFont.truetype(os.path.join(FONT_DIR, "arial.ttf"), 20)
font_badge = ImageFont.truetype(os.path.join(FONT_DIR, "arialbd.ttf"), 18)
font_caption = ImageFont.truetype(os.path.join(FONT_DIR, "arial.ttf"), 22)
font_code = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 20)

def draw_header(d, tag_text, title_text, subtitle_text):
    """Draw consistent top header banner."""
    # Top Tag
    d.rounded_rectangle([100, 50, 480, 88], radius=10, fill=(37, 99, 235, 60), outline=BLUE_ACCENT, width=2)
    d.text((120, 58), tag_text, font=font_badge, fill=CYAN_ACCENT)

    # Title
    d.text((100, 105), title_text, font=font_h2, fill=TEXT_WHITE)
    
    # Subtitle
    d.text((100, 155), subtitle_text, font=font_subtitle, fill=TEXT_MUTED)

    # Divider
    d.line([100, 195, 1820, 195], fill=(51, 65, 85), width=2)

def draw_caption_bar(img, caption_text, chapter_title, progress_pct):
    """Draw bottom narration caption and playback progress bar."""
    d = ImageDraw.Draw(img)
    
    # Bottom container
    d.rectangle([0, 940, WIDTH, HEIGHT], fill=(10, 15, 30))
    d.line([0, 940, WIDTH, 940], fill=PANEL_BORDER, width=2)

    # Progress bar line
    bar_width = int(WIDTH * progress_pct)
    d.rectangle([0, 936, bar_width, 940], fill=CYAN_ACCENT)

    # Chapter indicator
    d.text((100, 955), f"SCENE: {chapter_title.upper()}", font=font_badge, fill=AMBER_ACCENT)
    
    # Narration caption
    d.text((100, 990), f"\" {caption_text} \"", font=font_caption, fill=TEXT_WHITE)

def build_scene_1():
    """Scene 1: Title & Academic Overview"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    # Decorative background glows
    d.ellipse([1400, -100, 2000, 500], fill=(20, 40, 80))
    d.ellipse([-200, 600, 400, 1200], fill=(20, 30, 60))

    # Badge
    d.rounded_rectangle([720, 150, 1200, 195], radius=12, fill=(30, 58, 138), outline=BLUE_ACCENT, width=2)
    d.text((750, 160), "ACADEMIC PROJECT DEMONSTRATION • 2026", font=font_badge, fill=CYAN_ACCENT)

    # Main Title
    d.text((220, 240), "THE CENTRALIZED COLLEGE STUDY MATERIAL &", font=font_title, fill=TEXT_WHITE)
    d.text((380, 310), "PREVIOUS QUESTION PAPER PORTAL", font=font_title, fill=CYAN_ACCENT)

    # Subtitle
    d.text((300, 400), "A High-Performance Academic Repository with Online & Offline Campus LAN Access", font=font_subtitle, fill=TEXT_MUTED)

    # 4 Highlights Pills
    pills = [
        ("Study Materials & PYQs", BLUE_ACCENT),
        ("Dept & Semester Hierarchy", EMERALD_ACCENT),
        ("Role-Based Moderation", PURPLE_ACCENT),
        ("100% Offline Campus LAN", AMBER_ACCENT)
    ]
    start_x = 220
    for title, col in pills:
        d.rounded_rectangle([start_x, 500, start_x + 340, 570], radius=16, fill=PANEL_BG, outline=col, width=2)
        d.text((start_x + 25, 522), title, font=font_card_title, fill=TEXT_WHITE)
        start_x += 370

    # Tech Stack Box
    d.rounded_rectangle([360, 640, 1560, 820], radius=20, fill=(24, 32, 47), outline=(45, 55, 72), width=2)
    d.text((760, 670), "TECHNOLOGY STACK ARCHITECTURE", font=font_card_title, fill=AMBER_ACCENT)

    techs = [
        ("Backend Framework", "Python 3.13 & Flask 3.1"),
        ("Database Engine", "SQLite3 with WAL Mode"),
        ("Frontend Engine", "Tailwind CSS & Vanilla JS"),
        ("Offline Engine", "Socket LAN & PWA Worker")
    ]
    tx = 420
    for label, val in techs:
        d.text((tx, 720), label, font=font_card_body, fill=TEXT_MUTED)
        d.text((tx, 755), val, font=font_card_title, fill=TEXT_WHITE)
        tx += 290

    return img, "Welcome to the project demonstration of the Centralized College Academic Repository and Previous Question Paper Portal.", "1. Project Introduction"

def build_scene_2():
    """Scene 2: Problem Statement & Motivation"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    draw_header(d, "PROBLEM STATEMENT & MOTIVATION", "Why Colleges Need a Centralized Academic Repository", "Addressing the friction and fragmentation of academic resource distribution.")

    # Left Column: The Problem (Red accented)
    d.rounded_rectangle([100, 230, 920, 870], radius=24, fill=PANEL_BG, outline=(225, 29, 72), width=2)
    d.rounded_rectangle([140, 260, 480, 305], radius=10, fill=(159, 18, 57))
    d.text((160, 272), "THE CHALLENGE TODAY", font=font_badge, fill=TEXT_WHITE)

    problems = [
        ("Scattered Distribution", "Notes & PYQs are scattered across WhatsApp chats, Telegram groups, and random Google Drive links."),
        ("Broken Links & File Loss", "Drive links expire, storage quotas fill up, and previous semester question papers are permanently lost."),
        ("Lack of Quality Moderation", "No verification process exists to filter out corrupt scans, incorrect answer keys, or copyrighted spam."),
        ("No Internet on Campus", "Students in examination halls, basement classrooms, and labs frequently face zero internet connectivity.")
    ]
    y = 340
    for title, desc in problems:
        d.ellipse([140, y + 5, 156, y + 21], fill=(244, 63, 94))
        d.text((170, y), title, font=font_card_title, fill=(254, 205, 211))
        # Word wrap description
        words = desc.split()
        line1 = " ".join(words[:8])
        line2 = " ".join(words[8:])
        d.text((170, y + 35), line1, font=font_card_body, fill=TEXT_MUTED)
        if line2:
            d.text((170, y + 65), line2, font=font_card_body, fill=TEXT_MUTED)
        y += 125

    # Right Column: The Academix Solution (Green accented)
    d.rounded_rectangle([1000, 230, 1820, 870], radius=24, fill=PANEL_BG, outline=EMERALD_ACCENT, width=2)
    d.rounded_rectangle([1040, 260, 1420, 305], radius=10, fill=(6, 95, 70))
    d.text((1060, 272), "THE ACADEMIX SOLUTION", font=font_badge, fill=TEXT_WHITE)

    solutions = [
        ("Centralized Catalog", "Single institutional hub organized strictly by Department, Semester, and Subject."),
        ("Permanent Campus Storage", "Institutional database with fast streaming downloads and zero broken external links."),
        ("Faculty Moderation Queue", "Every student submission is verified by teachers or administrators before public listing."),
        ("100% Offline LAN Access", "Engineered to run seamlessly across local college Wi-Fi routers and mobile hotspots.")
    ]
    y = 340
    for title, desc in solutions:
        d.ellipse([1040, y + 5, 1056, y + 21], fill=EMERALD_ACCENT)
        d.text((1070, y), title, font=font_card_title, fill=(167, 243, 208))
        words = desc.split()
        line1 = " ".join(words[:8])
        line2 = " ".join(words[8:])
        d.text((1070, y + 35), line1, font=font_card_body, fill=TEXT_MUTED)
        if line2:
            d.text((1070, y + 65), line2, font=font_card_body, fill=TEXT_MUTED)
        y += 125

    return img, "Traditional sharing relies on fragmented chats and expired links. Academix centralizes resources under institutional moderation.", "2. Problem Statement"

def build_scene_3():
    """Scene 3: Academic Hierarchy & Resource Categories"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    draw_header(d, "ACADEMIC HIERARCHY & TAXONOMY", "Structured Multi-Tier Resource Organization", "Connecting students directly to their syllabus in three clicks or fewer.")

    # Hierarchy Breadcrumb Graphic
    steps = [
        ("1. Department", "CSE, IT, AI-DS, ECE, MECH, etc.", BLUE_ACCENT),
        ("2. Semester", "Semesters 1 through 8", CYAN_ACCENT),
        ("3. Subject", "Data Structures, DBMS, OS, AI", PURPLE_ACCENT),
        ("4. Resource Category", "PYQs, Notes, Lab Manuals, Syllabus", EMERALD_ACCENT)
    ]
    sx = 100
    for title, subtitle, col in steps:
        d.rounded_rectangle([sx, 230, sx + 390, 340], radius=18, fill=PANEL_BG, outline=col, width=2)
        d.text((sx + 30, 255), title, font=font_card_title, fill=col)
        d.text((sx + 30, 295), subtitle, font=font_card_body, fill=TEXT_WHITE)
        if sx < 1300:
            d.polygon([(sx + 405, 275), (sx + 420, 285), (sx + 405, 295)], fill=TEXT_MUTED)
        sx += 440

    # 4 Category Cards
    categories = [
        ("Previous Question Papers (PYQs)", "End-Semester university examinations, Mid-Term 1 & 2 tests, and Model papers with mark distributions.", AMBER_ACCENT),
        ("Faculty Lecture Notes & Slides", "Comprehensive unit 1-5 lecture presentations, handwritten revision sheets, and faculty solved question banks.", EMERALD_ACCENT),
        ("Laboratory Manuals & Code", "Practical experiment guides, step-by-step algorithms, sample datasets, and source code implementations.", PURPLE_ACCENT),
        ("Assignments & Curriculum", "Regulation syllabus documents, assignment problem sets, and faculty model solution guidelines.", BLUE_ACCENT)
    ]

    cx = 100
    cy = 380
    for idx, (title, desc, col) in enumerate(categories):
        x = 100 if idx % 2 == 0 else 980
        y = 380 if idx < 2 else 630
        
        d.rounded_rectangle([x, y, x + 840, y + 210], radius=20, fill=PANEL_BG, outline=col, width=2)
        d.rounded_rectangle([x + 30, y + 30, x + 80, y + 80], radius=12, fill=col)
        d.text((x + 48, y + 42), str(idx + 1), font=font_card_title, fill=TEXT_WHITE)
        d.text((x + 100, y + 45), title, font=font_card_title, fill=TEXT_WHITE)
        
        words = desc.split()
        line1 = " ".join(words[:11])
        line2 = " ".join(words[11:])
        d.text((x + 100, y + 100), line1, font=font_card_body, fill=TEXT_MUTED)
        if line2:
            d.text((x + 100, y + 135), line2, font=font_card_body, fill=TEXT_MUTED)

    return img, "Resources are organized hierarchically by Department, Semester, and Subject across six distinct academic categories.", "3. Academic Hierarchy"

def build_scene_4():
    """Scene 4: System Architecture & Database Design"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    draw_header(d, "SYSTEM ARCHITECTURE & DATABASE", "Modular MVC Architecture & Relational Schema", "Engineered for speed, data integrity, and high-concurrency offline access.")

    # 3 Tier Architecture Diagram
    tiers = [
        ("PRESENTATION TIER", [
            "Tailwind CSS Responsive UI",
            "In-Browser PDF Document Previewer",
            "PWA Service Worker (Offline Cache)",
            "Live Autocomplete Search (AJAX)"
        ], CYAN_ACCENT),
        ("APPLICATION TIER", [
            "Flask 3.1 Web Application",
            "Modular Blueprints (Auth, Main, Admin)",
            "Role Authorization (Student/Faculty/Admin)",
            "Socket-based Local LAN Discovery"
        ], BLUE_ACCENT),
        ("DATABASE TIER", [
            "SQLite3 Relational Database",
            "Write-Ahead Logging (WAL Mode)",
            "Foreign Key Integrity Constraints",
            "Optimized B-Tree Indexes"
        ], EMERALD_ACCENT)
    ]

    tx = 100
    for name, bullets, col in tiers:
        d.rounded_rectangle([tx, 230, tx + 520, 560], radius=20, fill=PANEL_BG, outline=col, width=2)
        d.rounded_rectangle([tx + 30, 255, tx + 490, 305], radius=10, fill=col)
        d.text((tx + 50, 270), name, font=font_badge, fill=TEXT_WHITE)
        
        by = 340
        for b in bullets:
            d.ellipse([tx + 40, by + 4, tx + 52, by + 16], fill=col)
            d.text((tx + 65, by), b, font=font_card_body, fill=TEXT_WHITE)
            by += 45
        tx += 580

    # Database Schema Breakdown Table
    d.rounded_rectangle([100, 600, 1820, 880], radius=20, fill=(20, 30, 48), outline=PANEL_BORDER, width=2)
    d.text((140, 630), "RELATIONAL DATABASE SCHEMA (7 CORE TABLES)", font=font_card_title, fill=AMBER_ACCENT)

    tables = [
        ("departments", "Stores 8 college branches (CSE, IT, ECE, MECH, etc.) with codes and icons."),
        ("subjects", "Courses mapped to departments and semesters 1 to 8 (e.g. CS301 Data Structures)."),
        ("users", "User credentials, PBKDF2 password hashes, rolls, and roles (Student, Faculty, Admin)."),
        ("resources", "Central repository metadata, file paths, upload dates, views, and download counts."),
        ("resource_ratings", "Peer reviews and 1 to 5 star ratings submitted by students."),
        ("bookmarks", "Saved study materials pinned to user profile for quick pre-exam access.")
    ]

    ty = 680
    for idx, (tname, tdesc) in enumerate(tables):
        x = 140 if idx % 2 == 0 else 980
        y = ty if idx % 2 == 0 else ty
        d.text((x, y), tname, font=font_code, fill=CYAN_ACCENT)
        d.text((x + 220, y), tdesc, font=font_card_body, fill=TEXT_MUTED)
        if idx % 2 == 1:
            ty += 60

    return img, "Built on Flask 3.1 with a high-performance SQLite WAL database and modular blueprints for seamless concurrent campus use.", "4. System Architecture"

def build_scene_5():
    """Scene 5: Student Experience & Core Features"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    draw_header(d, "STUDENT EXPERIENCE & INTERACTIVE UI", "Feature-Rich Repository for Seamless Revision", "Empowering students with instant search, previewing, and peer reviews.")

    features = [
        ("Live Autocomplete Search", "Search by subject code, topic, or keyword with real-time dropdown suggestions as you type.", CYAN_ACCENT),
        ("In-Browser Document Preview", "Embedded PDF and document viewer allowing students to inspect question papers before downloading.", BLUE_ACCENT),
        ("1-Click Fast Downloads", "Direct file downloads with live download counter updates and Range header streaming.", EMERALD_ACCENT),
        ("5-Star Ratings & Reviews", "Verified peer reviews and feedback ratings to help students find the most effective notes.", AMBER_ACCENT),
        ("Personal Pre-Exam Bookmarks", "Save critical question papers and formula sheets to your personal profile for rapid pre-exam review.", PURPLE_ACCENT),
        ("Multi-Tier Dynamic Filters", "Filter simultaneously by Department, Semester, Subject, Resource Type, Year, and Exam Type.", (236, 72, 153))
    ]

    for idx, (title, desc, col) in enumerate(features):
        col_idx = idx % 3
        row_idx = idx // 3
        x = 100 + col_idx * 580
        y = 240 + row_idx * 320
        
        d.rounded_rectangle([x, y, x + 540, y + 280], radius=20, fill=PANEL_BG, outline=col, width=2)
        d.rounded_rectangle([x + 30, y + 30, x + 75, y + 75], radius=12, fill=col)
        d.text((x + 45, y + 40), str(idx + 1), font=font_card_title, fill=TEXT_WHITE)
        d.text((x + 95, y + 42), title, font=font_card_title, fill=TEXT_WHITE)
        
        words = desc.split()
        line1 = " ".join(words[:9])
        line2 = " ".join(words[9:])
        d.text((x + 30, y + 110), line1, font=font_card_body, fill=TEXT_MUTED)
        if line2:
            d.text((x + 30, y + 145), line2, font=font_card_body, fill=TEXT_MUTED)

    return img, "Students can search subjects, preview papers directly inside the browser, and download verified notes in a single click.", "5. Student Experience"

def build_scene_6():
    """Scene 6: File Upload Pipeline & Moderation Queue"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    draw_header(d, "CONTENT INGESTION & MODERATION WORKFLOW", "Ensuring High Quality & Preventing Spam", "Multi-stage validation pipeline with role-based moderation authority.")

    # 4-Stage Ingestion Pipeline
    pipeline_steps = [
        ("1. Drag & Drop Upload", "Students select file and academic metadata (Dept, Sem, Subject).", BLUE_ACCENT),
        ("2. File Security Filter", "MIME type check, UUID renaming, 64 MB size verification.", CYAN_ACCENT),
        ("3. Pending Moderation Queue", "Student uploads enter review queue; Faculty uploads auto-publish.", AMBER_ACCENT),
        ("4. Live Publication", "Admin/Faculty approves with 1-click; Resource goes live for all.", EMERALD_ACCENT)
    ]

    sx = 100
    for title, subtitle, col in pipeline_steps:
        d.rounded_rectangle([sx, 230, sx + 390, 360], radius=20, fill=PANEL_BG, outline=col, width=2)
        d.text((sx + 25, 260), title, font=font_card_title, fill=col)
        words = subtitle.split()
        line1 = " ".join(words[:6])
        line2 = " ".join(words[6:])
        d.text((sx + 25, 305), line1, font=font_card_body, fill=TEXT_WHITE)
        if line2:
            d.text((sx + 25, 335), line2, font=font_card_body, fill=TEXT_WHITE)
        if sx < 1300:
            d.polygon([(sx + 405, 290), (sx + 420, 300), (sx + 405, 310)], fill=TEXT_MUTED)
        sx += 440

    # Moderation Policy Comparison Box
    d.rounded_rectangle([100, 430, 920, 880], radius=24, fill=PANEL_BG, outline=AMBER_ACCENT, width=2)
    d.text((140, 465), "STUDENT CONTRIBUTION WORKFLOW", font=font_card_title, fill=AMBER_ACCENT)
    
    student_points = [
        "Uploads enter 'Pending' status upon submission.",
        "Students track status in their personal 'My Uploads' dashboard.",
        "Status badges: [Approved (Green)] [In Review (Yellow)] [Rejected (Red)].",
        "If rejected, moderator feedback explains exactly what to correct."
    ]
    sy = 520
    for p in student_points:
        d.ellipse([140, sy + 5, 152, sy + 17], fill=AMBER_ACCENT)
        d.text((170, sy), p, font=font_card_body, fill=TEXT_WHITE)
        sy += 75

    # Admin Control Panel Box
    d.rounded_rectangle([1000, 430, 1820, 880], radius=24, fill=PANEL_BG, outline=EMERALD_ACCENT, width=2)
    d.text((1040, 465), "ADMINISTRATOR MODERATION PANEL", font=font_card_title, fill=EMERALD_ACCENT)

    admin_points = [
        "Dedicated Review Queue with instant preview modal.",
        "One-click 'Approve' publishes document immediately to the portal.",
        "'Reject' option with customizable feedback reason for the student.",
        "Audit trail logs moderator ID, timestamp, and action for compliance."
    ]
    ay = 520
    for p in admin_points:
        d.ellipse([1040, ay + 5, 1052, ay + 17], fill=EMERALD_ACCENT)
        d.text((1070, ay), p, font=font_card_body, fill=TEXT_WHITE)
        ay += 75

    return img, "Every student upload undergoes automated file validation and faculty moderation to guarantee quality before public release.", "6. Moderation Workflow"

def build_scene_7():
    """Scene 7: Offline & Campus LAN Access"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    draw_header(d, "KEY INNOVATION • OFFLINE & CAMPUS LAN", "Zero Internet Required on Campus", "Enabling high-speed access over local Wi-Fi routers and mobile hotspots.")

    # Big Banner Highlight
    d.rounded_rectangle([100, 230, 1820, 390], radius=24, fill=(16, 40, 30), outline=EMERALD_ACCENT, width=2)
    d.text((150, 260), "CAMPUS INTRANET & OFFLINE CAPABILITY", font=font_card_title, fill=EMERALD_ACCENT)
    d.text((150, 305), "The portal binds to 0.0.0.0:5000 and automatically discovers the machine's local IPv4 address.", font=font_subtitle, fill=TEXT_WHITE)
    d.text((150, 345), "Students connect their smartphones or laptops to the local Wi-Fi or hotspot and access the full repository instantly.", font=font_card_body, fill=TEXT_MUTED)

    # 3 Steps to Connect Card
    lan_steps = [
        ("Step 1: Local Network", "Connect host PC and mobile phones to same Wi-Fi router or turn on Laptop Hotspot.", CYAN_ACCENT),
        ("Step 2: Instant IP Detection", "The terminal outputs: http://192.168.x.x:5000 for effortless sharing.", BLUE_ACCENT),
        ("Step 3: PWA Offline Caching", "Service Worker caches pages and static assets for persistent offline study.", PURPLE_ACCENT)
    ]

    lx = 100
    for title, subtitle, col in lan_steps:
        d.rounded_rectangle([lx, 430, lx + 520, 680], radius=20, fill=PANEL_BG, outline=col, width=2)
        d.rounded_rectangle([lx + 30, 460, lx + 80, 510], radius=12, fill=col)
        d.text((lx + 48, 472), "#", font=font_card_title, fill=TEXT_WHITE)
        d.text((lx + 100, 475), title, font=font_card_title, fill=TEXT_WHITE)
        
        words = subtitle.split()
        line1 = " ".join(words[:7])
        line2 = " ".join(words[7:])
        d.text((lx + 30, 550), line1, font=font_card_body, fill=TEXT_MUTED)
        if line2:
            d.text((lx + 30, 585), line2, font=font_card_body, fill=TEXT_MUTED)
        lx += 580

    # Live Endpoint Simulation Card
    d.rounded_rectangle([100, 720, 1820, 880], radius=20, fill=(24, 32, 47), outline=AMBER_ACCENT, width=2)
    d.text((140, 750), "CAMPUS ACCESS ENDPOINT:", font=font_badge, fill=AMBER_ACCENT)
    d.text((140, 785), "http://192.168.1.15:5000", font=font_title, fill=TEXT_WHITE)
    d.text((950, 800), "[ACTIVE LOCAL CAMPUS NETWORK - ZERO MOBILE DATA REQUIRED]", font=font_badge, fill=EMERALD_ACCENT)

    return img, "A key innovation: the entire portal operates completely offline over college Wi-Fi or local hotspots without internet data.", "7. Offline & Campus LAN"

def build_scene_8():
    """Scene 8: Security, Auditing & Test Verification"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    draw_header(d, "SECURITY & VERIFICATION", "Security Architecture, Audit Logs & Testing", "Rigorous verification ensuring reliability, data safety, and zero vulnerabilities.")

    # 3 Pillars
    pillars = [
        ("SECURITY ENFORCEMENT", [
            "PBKDF2 Password Hashing (SHA-256)",
            "Strict MIME type and extension whitelist",
            "Random 12-char UUID filename sanitization",
            "64 MB max upload size restriction",
            "Role authorization decorators on all routes"
        ], CYAN_ACCENT),
        ("AUDIT TRAIL LOGGING", [
            "Real-time logging to activity_logs table",
            "Tracks user ID, action, details, and IP",
            "Audit trail for uploads, approvals, and logins",
            "Administrative log viewer for oversight",
            "Zero repudiation of moderation actions"
        ], PURPLE_ACCENT),
        ("TEST VERIFICATION SUITE", [
            "17 Unit & Integration Tests (100% PASS)",
            "Full lifecycle tested: Upload -> Queue -> Approve",
            "Cascading API endpoints verified",
            "Document streaming & preview verified",
            "Offline PWA endpoint verified"
        ], EMERALD_ACCENT)
    ]

    px = 100
    for title, points, col in pillars:
        d.rounded_rectangle([px, 230, px + 520, 680], radius=20, fill=PANEL_BG, outline=col, width=2)
        d.rounded_rectangle([px + 30, 260, px + 490, 310], radius=10, fill=col)
        d.text((px + 50, 275), title, font=font_badge, fill=TEXT_WHITE)

        py = 345
        for p in points:
            d.ellipse([px + 35, py + 4, px + 47, py + 16], fill=col)
            d.text((px + 60, py), p, font=font_card_body, fill=TEXT_WHITE)
            py += 60
        px += 580

    # 100% Pass Badge Box
    d.rounded_rectangle([100, 720, 1820, 880], radius=20, fill=(16, 40, 30), outline=EMERALD_ACCENT, width=2)
    d.text((150, 755), "TEST SUITE STATUS: ALL 17 UNIT & INTEGRATION TESTS PASSED (100% PASS RATE)", font=font_card_title, fill=EMERALD_ACCENT)
    d.text((150, 805), "Automated test suite (test_app.py) validates complete student and administrator workflow.", font=font_card_body, fill=TEXT_WHITE)

    return img, "The system includes robust security, user activity logs, and a verified automated test suite with a 100% pass rate.", "8. Security & Testing"

def build_scene_9():
    """Scene 9: Summary & Project Deliverables"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)

    # Decorative
    d.ellipse([1300, 100, 1900, 700], fill=(20, 40, 80))
    d.ellipse([100, 500, 700, 1100], fill=(20, 30, 60))

    d.rounded_rectangle([700, 100, 1220, 145], radius=12, fill=(30, 58, 138), outline=BLUE_ACCENT, width=2)
    d.text((740, 112), "PROJECT SUMMARY & DELIVERABLES", font=font_badge, fill=CYAN_ACCENT)

    d.text((360, 180), "CENTRALIZED COLLEGE STUDY MATERIAL &", font=font_title, fill=TEXT_WHITE)
    d.text((450, 250), "PREVIOUS QUESTION PAPER PORTAL", font=font_title, fill=CYAN_ACCENT)

    # 4 Deliverables Cards
    deliverables = [
        ("1. Full-Stack Web Application", "Complete Python Flask, SQLite, and Tailwind CSS codebase with pre-seeded data.", BLUE_ACCENT),
        ("2. 89-Page Complete Codebook PDF", "All-in-one PDF with code line numbers, schemas, and architecture documentation.", EMERALD_ACCENT),
        ("3. HD Video Presentation (MP4)", "Full project walkthrough video ready for college presentations and viva defense.", PURPLE_ACCENT),
        ("4. Academic Project Report", "Comprehensive SRS documentation, ER diagrams, test cases, and future scope.", AMBER_ACCENT)
    ]

    dx = 100
    for title, desc, col in deliverables:
        d.rounded_rectangle([dx, 360, dx + 390, 620], radius=20, fill=PANEL_BG, outline=col, width=2)
        d.rounded_rectangle([dx + 30, 390, dx + 80, 440], radius=12, fill=col)
        d.text((dx + 48, 402), "#", font=font_card_title, fill=TEXT_WHITE)
        d.text((dx + 30, 470), title, font=font_card_title, fill=TEXT_WHITE)
        
        words = desc.split()
        line1 = " ".join(words[:6])
        line2 = " ".join(words[6:])
        d.text((dx + 30, 520), line1, font=font_card_body, fill=TEXT_MUTED)
        if line2:
            d.text((dx + 30, 555), line2, font=font_card_body, fill=TEXT_MUTED)
        dx += 440

    # Final Thank You Box
    d.rounded_rectangle([360, 670, 1560, 850], radius=24, fill=(24, 32, 47), outline=EMERALD_ACCENT, width=2)
    d.text((620, 710), "THANK YOU FOR WATCHING THE PRESENTATION", font=font_h2, fill=TEXT_WHITE)
    d.text((540, 775), "Empowering Academic Excellence Through Centralized Knowledge Sharing", font=font_subtitle, fill=CYAN_ACCENT)

    return img, "Thank you for watching the presentation of the Centralized College Study Material and Previous Question Paper Portal.", "9. Conclusion"

def render_video():
    print(f"Creating High-Definition Video Representation: {OUTPUT_VIDEO}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, float(FPS), (WIDTH, HEIGHT))

    scene_builders = [
        (build_scene_1, 7.5),   # 7.5 seconds
        (build_scene_2, 8.5),   # 8.5 seconds
        (build_scene_3, 9.0),   # 9.0 seconds
        (build_scene_4, 9.0),   # 9.0 seconds
        (build_scene_5, 9.0),   # 9.0 seconds
        (build_scene_6, 9.0),   # 9.0 seconds
        (build_scene_7, 10.0),  # 10.0 seconds
        (build_scene_8, 8.5),   # 8.5 seconds
        (build_scene_9, 8.0)    # 8.0 seconds
    ]

    total_duration = sum(dur for _, dur in scene_builders)
    total_frames = int(total_duration * FPS)
    current_frame = 0

    print(f"Total Video Duration: {total_duration:.1f}s | Total Frames: {total_frames}")

    # Build base images for all scenes
    rendered_scenes = []
    for idx, (builder, dur) in enumerate(scene_builders):
        print(f"Rendering Base Scene {idx + 1}/{len(scene_builders)}...")
        base_img, caption, chapter = builder()
        rendered_scenes.append((base_img, caption, chapter, int(dur * FPS)))

    # Frame generation loop with smooth crossfade transitions
    TRANSITION_FRAMES = 12  # 0.4s crossfade

    for s_idx, (base_img, caption, chapter, num_frames) in enumerate(rendered_scenes):
        print(f"Encoding Scene {s_idx + 1} ({num_frames} frames)...")
        
        # Pre-render frame with caption
        scene_img = base_img.copy()
        
        for f in range(num_frames):
            frame_img = scene_img.copy()
            progress_pct = current_frame / float(total_frames)
            
            draw_caption_bar(frame_img, caption, chapter, progress_pct)
            
            # Convert PIL RGB to OpenCV BGR
            cv_frame = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGB2BGR)

            # Fade in transition at start of scene (except first scene)
            if s_idx > 0 and f < TRANSITION_FRAMES:
                alpha = f / float(TRANSITION_FRAMES)
                cv_frame = cv2.addWeighted(cv_frame, alpha, prev_last_frame, 1.0 - alpha, 0)

            out.write(cv_frame)
            current_frame += 1

            if f == num_frames - 1:
                prev_last_frame = cv_frame.copy()

    out.release()
    print(f"SUCCESS: Video exported to {OUTPUT_VIDEO}")
    
    # Copy to user Downloads folder
    try:
        shutil.copy2(OUTPUT_VIDEO, DOWNLOADS_COPY)
        print(f"SUCCESS: Copied video to {DOWNLOADS_COPY}")
    except Exception as e:
        print(f"Could not copy to Downloads: {e}")

if __name__ == "__main__":
    render_video()
