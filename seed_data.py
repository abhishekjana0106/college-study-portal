import os
import sqlite3
from werkzeug.security import generate_password_hash
from config import Config
from database import init_db

def create_sample_pdf(filepath, title, subject, content_lines):
    """Generate a clean, readable PDF-like or styled document."""
    # We can write a clean text/pdf formatted file
    content = f"""%PDF-1.4
1 0 obj
<<
  /Type /Catalog
  /Pages 2 0 R
>>
endobj
2 0 obj
<<
  /Type /Pages
  /Kids [3 0 R]
  /Count 1
>>
endobj
3 0 obj
<<
  /Type /Page
  /Parent 2 0 R
  /MediaBox [0 0 612 792]
  /Contents 4 0 R
  /Resources <<
    /Font <<
      /F1 5 0 R
    >>
  >>
>>
endobj
4 0 obj
<<
  /Length {len(title) + 500}
>>
stream
BT
/F1 18 Tf
50 720 Td
({title}) Tj
/F1 12 Tf
0 -30 Td
(Subject: {subject}) Tj
0 -20 Td
(Centralized College Academic Repository) Tj
0 -40 Td
"""
    for line in content_lines[:15]:
        safe_line = line.replace('(', '[').replace(')', ']')
        content += f"({safe_line}) Tj\n0 -18 Td\n"

    content += """ET
endstream
endobj
5 0 obj
<<
  /Type /Font
  /Subtype /Type1
  /BaseFont /Helvetica
>>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000117 00000 n 
0000000262 00000 n 
0000000850 00000 n 
trailer
<<
  /Size 6
  /Root 1 0 R
>>
startxref
940
%%EOF
"""
    with open(filepath, 'wb') as f:
        f.write(content.encode('latin1', errors='replace'))

def seed_database():
    init_db()
    conn = sqlite3.connect(Config.DATABASE)
    cur = conn.cursor()

    # 1. Insert Departments
    departments_data = [
        ("Computer Science & Engineering", "CSE", "Core computing, software engineering, algorithms, and systems.", "fas fa-laptop-code"),
        ("Information Technology", "IT", "Applied information systems, networking, cloud, and web development.", "fas fa-network-wired"),
        ("Artificial Intelligence & Data Science", "AI-DS", "Modern AI, machine learning, neural networks, and big data.", "fas fa-brain"),
        ("Electronics & Communication", "ECE", "Circuits, embedded systems, signal processing, and communication.", "fas fa-microchip"),
        ("Electrical & Electronics", "EEE", "Power systems, control systems, electrical drives, and green energy.", "fas fa-bolt"),
        ("Mechanical Engineering", "MECH", "Thermodynamics, mechanics, CAD/CAM, fluid machinery, and robotics.", "fas fa-cogs"),
        ("Civil Engineering", "CIVIL", "Structural engineering, surveying, geo-tech, and construction management.", "fas fa-building"),
        ("Basic Sciences & Humanities", "BSH", "Foundational mathematics, physics, chemistry, and communication skills.", "fas fa-atom")
    ]

    dept_map = {}
    for name, code, desc, icon in departments_data:
        cur.execute("""
            INSERT INTO departments (name, code, description, icon) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET name=excluded.name, description=excluded.description, icon=excluded.icon
        """, (name, code, desc, icon))
        cur.execute("SELECT id FROM departments WHERE code = ?", (code,))
        dept_map[code] = cur.fetchone()[0]

    # 2. Insert Subjects
    subjects_data = [
        # CSE
        ("Data Structures and Algorithms", "CS301", dept_map["CSE"], 3, "Arrays, Stacks, Queues, Linked Lists, Trees, Graphs, Sorting & Searching algorithms."),
        ("Database Management Systems", "CS401", dept_map["CSE"], 4, "Relational algebra, SQL, Normalization, Transactions, Concurrency control, and NoSQL."),
        ("Operating Systems", "CS402", dept_map["CSE"], 4, "Process scheduling, Threads, Deadlocks, Memory management, Virtual memory, and File systems."),
        ("Computer Networks", "CS501", dept_map["CSE"], 5, "OSI model, TCP/IP, Routing algorithms, Congestion control, Application layer protocols."),
        ("Software Engineering", "CS502", dept_map["CSE"], 5, "Agile methodology, SDLC, Requirement engineering, UML diagrams, Testing and Maintenance."),
        ("Machine Learning", "CS601", dept_map["CSE"], 6, "Supervised & Unsupervised learning, Regression, Classification, SVM, Decision trees, Neural nets."),
        ("Cloud Computing", "CS602", dept_map["CSE"], 6, "Virtualization, AWS, Azure, Docker containers, Kubernetes, Serverless architectures."),
        ("Compiler Design", "CS603", dept_map["CSE"], 6, "Lexical analysis, Parsing, Syntax directed translation, Intermediate code generation, Optimization."),
        
        # IT
        ("Web Technologies", "IT501", dept_map["IT"], 5, "HTML5, CSS3, JavaScript, RESTful APIs, Node.js, and Full-stack web frameworks."),
        ("Information Security", "IT601", dept_map["IT"], 6, "Symmetric/Asymmetric cryptography, RSA, Firewalls, Penetration testing, Security policies."),
        ("Mobile App Development", "IT701", dept_map["IT"], 7, "Android & iOS architectures, Flutter/React Native, UI design, App deployment."),
        
        # AI & DS
        ("Artificial Intelligence & Expert Systems", "AI501", dept_map["AI-DS"], 5, "State space search, Heuristics, A* search, Game playing, Knowledge representation."),
        ("Deep Learning & Computer Vision", "AI601", dept_map["AI-DS"], 6, "CNNs, RNNs, Transformers, Object detection, Transfer learning with PyTorch/TensorFlow."),
        ("Big Data Analytics", "AI701", dept_map["AI-DS"], 7, "Hadoop ecosystem, MapReduce, Apache Spark, Data pipelines, Feature engineering."),

        # ECE
        ("Digital Logic & Microprocessors", "EC301", dept_map["ECE"], 3, "Boolean algebra, Flip-flops, Counters, 8085/8086 architecture, Assembly language."),
        ("Signals and Systems", "EC401", dept_map["ECE"], 4, "Continuous and discrete signals, Fourier Transform, Laplace Transform, Z-Transform."),
        ("VLSI Design", "EC601", dept_map["ECE"], 6, "MOSFET theory, CMOS inverters, Layout design rules, Verilog HDL programming."),

        # MECH
        ("Engineering Thermodynamics", "ME301", dept_map["MECH"], 3, "Laws of thermodynamics, Carnot cycle, Entropy, Rankine cycle, Refrigeration cycles."),
        ("Fluid Mechanics and Machinery", "ME401", dept_map["MECH"], 4, "Fluid statics, Bernoulli's equation, Pumps, Turbines, Dimensional analysis."),
        
        # BSH
        ("Engineering Mathematics I", "MA101", dept_map["BSH"], 1, "Differential calculus, Matrices, Eigenvalues, Partial differentiation, Taylor series."),
        ("Engineering Physics", "PH101", dept_map["BSH"], 1, "Quantum mechanics, Lasers, Fiber optics, Superconductivity, Nanomaterials.")
    ]

    subj_map = {}
    for name, code, dept_id, sem, desc in subjects_data:
        cur.execute("""
            INSERT INTO subjects (name, code, department_id, semester, description)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(code, department_id) DO UPDATE SET name=excluded.name, semester=excluded.semester, description=excluded.description
        """, (name, code, dept_id, sem, desc))
        cur.execute("SELECT id FROM subjects WHERE code = ? AND department_id = ?", (code, dept_id))
        subj_map[code] = cur.fetchone()[0]

    # 3. Insert Users
    users_data = [
        ("admin", "admin@college.edu", generate_password_hash("admin123"), "System Administrator", "ADMIN001", dept_map["CSE"], 8, "admin"),
        ("prof_sharma", "sharma@college.edu", generate_password_hash("faculty123"), "Dr. R. K. Sharma (HOD CSE)", "FAC001", dept_map["CSE"], 0, "faculty"),
        ("prof_priya", "priya@college.edu", generate_password_hash("faculty123"), "Prof. Priya Nair", "FAC002", dept_map["AI-DS"], 0, "faculty"),
        ("student1", "aarav@college.edu", generate_password_hash("student123"), "Aarav Patel", "21CS045", dept_map["CSE"], 5, "student"),
        ("student2", "sneha@college.edu", generate_password_hash("student123"), "Sneha Rao", "22IT018", dept_map["IT"], 4, "student")
    ]

    user_map = {}
    for uname, email, pwd_hash, fname, roll, dept_id, sem, role in users_data:
        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name, roll_number, department_id, semester, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET password_hash=excluded.password_hash, role=excluded.role, full_name=excluded.full_name
        """, (uname, email, pwd_hash, fname, roll, dept_id, sem, role))
        cur.execute("SELECT id FROM users WHERE username = ?", (uname,))
        user_map[uname] = cur.fetchone()[0]

    # 4. Generate Sample PDF files in uploads folder
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    sample_resources = [
        {
            "title": "Dec 2024 End-Semester Question Paper - Data Structures & Algorithms",
            "desc": "Official college end-semester exam paper with answer pattern, section-wise marks distribution, and solution outline.",
            "type": "Question Paper",
            "dept": dept_map["CSE"],
            "sem": 3,
            "subj": subj_map["CS301"],
            "year": "2024-2025",
            "exam": "End-Semester",
            "file": "CS301_EndSem_Dec2024.pdf",
            "uploader": user_map["prof_sharma"],
            "status": "approved",
            "downloads": 142,
            "views": 430,
            "featured": 1,
            "tags": "data structures, exam paper, pyq, end sem, algorithms",
            "pdf_title": "End-Semester Exam - Data Structures (CS301)",
            "pdf_subject": "Data Structures & Algorithms - CSE Sem 3",
            "content": [
                "Part A (10 x 2 = 20 Marks): Answer all questions.",
                "1. Define Time Complexity and Big-O notation.",
                "2. What is an AVL Tree and how does it balance?",
                "3. Differentiate between BFS and DFS traversal.",
                "4. Explain Infix to Postfix conversion rules.",
                "Part B (5 x 16 = 80 Marks): Comprehensive questions.",
                "5. (a) Construct a Red-Black Tree for given keys.",
                "5. (b) Explain Dijkstra's shortest path algorithm with example.",
                "6. Write quicksort algorithm and derive its average time complexity."
            ]
        },
        {
            "title": "Operating Systems Complete Unit 1 to 5 Lecture Notes",
            "desc": "Comprehensive lecture notes prepared by Dr. R. K. Sharma covering Process Scheduling, Deadlocks, Virtual Memory, and File Allocation methods.",
            "type": "Lecture Notes",
            "dept": dept_map["CSE"],
            "sem": 4,
            "subj": subj_map["CS402"],
            "year": "2025-2026",
            "exam": "N/A",
            "file": "CS402_OS_Lecture_Notes_Unit1_5.pdf",
            "uploader": user_map["prof_sharma"],
            "status": "approved",
            "downloads": 289,
            "views": 750,
            "featured": 1,
            "tags": "operating systems, lecture notes, study material, processes, memory management",
            "pdf_title": "Operating Systems - Complete Course Notes",
            "pdf_subject": "Operating Systems (CS402)",
            "content": [
                "Unit 1: Introduction to OS, Dual-mode operation, System calls.",
                "Unit 2: Process Management, CPU Scheduling (FCFS, SJF, RR, Priority).",
                "Unit 3: Process Synchronization, Critical Section, Semaphores, Monitors.",
                "Unit 4: Deadlocks: Characterization, Prevention, Avoidance (Banker's Algorithm).",
                "Unit 5: Memory Management: Paging, Segmentation, Virtual Memory, Page Faults."
            ]
        },
        {
            "title": "Database Management Systems Mid-Term Question Paper with Answer Key",
            "desc": "Mid-Term 1 question paper including ER modeling, Relational Algebra, BCNF normalization questions and SQL queries.",
            "type": "Question Paper",
            "dept": dept_map["CSE"],
            "sem": 4,
            "subj": subj_map["CS401"],
            "year": "2024-2025",
            "exam": "Mid-Term 1",
            "file": "CS401_MidTerm1_DBMS_2024.pdf",
            "uploader": user_map["student1"],
            "status": "approved",
            "downloads": 95,
            "views": 210,
            "featured": 0,
            "tags": "dbms, mid-term, sql, normalization, question paper",
            "pdf_title": "DBMS Mid-Term Exam Paper",
            "pdf_subject": "Database Management Systems (CS401)",
            "content": [
                "Q1. Draw an ER diagram for a Hospital Management System.",
                "Q2. Explain 1NF, 2NF, 3NF, and BCNF with concrete counterexamples.",
                "Q3. Write SQL queries for nested subqueries and joins.",
                "Q4. Discuss ACID properties and serializability."
            ]
        },
        {
            "title": "Machine Learning Lab Manual & Practical Experiments",
            "desc": "Step-by-step practical lab experiments using Python, Scikit-Learn, Pandas, and Matplotlib. Includes Linear Regression, KNN, Decision Trees, and Naive Bayes.",
            "type": "Lab Manual",
            "dept": dept_map["AI-DS"],
            "sem": 6,
            "subj": subj_map["CS601"],
            "year": "2025-2026",
            "exam": "N/A",
            "file": "AI_DS_Machine_Learning_Lab_Manual.pdf",
            "uploader": user_map["prof_priya"],
            "status": "approved",
            "downloads": 178,
            "views": 412,
            "featured": 1,
            "tags": "machine learning, lab manual, python, scikit-learn, experiments",
            "pdf_title": "Machine Learning Laboratory Manual",
            "pdf_subject": "Machine Learning (CS601 / AI601)",
            "content": [
                "Experiment 1: Implementation of Linear and Polynomial Regression.",
                "Experiment 2: K-Nearest Neighbor (KNN) Classification.",
                "Experiment 3: ID3 Decision Tree Induction algorithm.",
                "Experiment 4: Support Vector Machine (SVM) for image classification.",
                "Experiment 5: K-Means Clustering on customer segmentation dataset."
            ]
        },
        {
            "title": "Computer Networks Nov 2024 End-Semester Model Paper",
            "desc": "Model question paper prepared according to latest university syllabus covering subnetting, distance vector routing, TCP handshake and flow control.",
            "type": "Question Paper",
            "dept": dept_map["CSE"],
            "sem": 5,
            "subj": subj_map["CS501"],
            "year": "2024-2025",
            "exam": "Model Exam",
            "file": "CS501_Model_Paper_Networks_2024.pdf",
            "uploader": user_map["student1"],
            "status": "approved",
            "downloads": 110,
            "views": 290,
            "featured": 0,
            "tags": "computer networks, model paper, routing, tcp ip, semester 5",
            "pdf_title": "Model Exam - Computer Networks",
            "pdf_subject": "Computer Networks (CS501)",
            "content": [
                "1. Explain OSI 7-Layer Reference Model with functions of each layer.",
                "2. Perform CIDR Subnetting for a class B network with 6 subnets.",
                "3. Differentiate between Distance Vector and Link State Routing.",
                "4. Explain 3-Way Handshake in TCP connection establishment and termination."
            ]
        },
        {
            "title": "Engineering Mathematics I Solved Question Bank & Formula Sheet",
            "desc": "Quick revision formula sheet, solved calculus problems, eigenvalues & eigenvectors step-by-step solutions for First Year students.",
            "type": "Lecture Notes",
            "dept": dept_map["BSH"],
            "sem": 1,
            "subj": subj_map["MA101"],
            "year": "2025-2026",
            "exam": "End-Semester",
            "file": "MA101_Maths1_Formula_Sheet_Solved.pdf",
            "uploader": user_map["prof_sharma"],
            "status": "approved",
            "downloads": 315,
            "views": 890,
            "featured": 1,
            "tags": "mathematics, formula sheet, semester 1, solved problems, calculus",
            "pdf_title": "Engineering Mathematics I - Solved Guide",
            "pdf_subject": "Engineering Mathematics I (MA101)",
            "content": [
                "1. Matrices: Cayley-Hamilton Theorem and Diagonalization.",
                "2. Differential Calculus: Curvature, Evolutes, and Envelopes.",
                "3. Functions of Several Variables: Maxima & Minima, Lagrange Multipliers.",
                "4. Multiple Integrals: Double & Triple integrals in polar/spherical coordinates."
            ]
        },
        {
            "title": "Cloud Computing Assignment 1 - AWS Architectures & Docker",
            "desc": "Assignment problems covering microservices deployment, Docker containerization, AWS S3, and EC2 Auto-scaling setup.",
            "type": "Assignment",
            "dept": dept_map["CSE"],
            "sem": 6,
            "subj": subj_map["CS602"],
            "year": "2025-2026",
            "exam": "N/A",
            "file": "CS602_Cloud_Assignment_1.pdf",
            "uploader": user_map["student2"],
            "status": "pending",
            "downloads": 12,
            "views": 45,
            "featured": 0,
            "tags": "cloud computing, assignment, docker, aws, microservices",
            "pdf_title": "Cloud Computing - Assignment 1",
            "pdf_subject": "Cloud Computing (CS602)",
            "content": [
                "Task 1: Create a multi-container Docker application using docker-compose.",
                "Task 2: Design high-availability architecture on AWS using EC2, ALB, and RDS.",
                "Task 3: Compare cost and latency between Serverless (AWS Lambda) vs Containers."
            ]
        }
    ]

    for item in sample_resources:
        filepath = os.path.join(Config.UPLOAD_FOLDER, item["file"])
        create_sample_pdf(filepath, item["pdf_title"], item["pdf_subject"], item["content"])
        filesize = os.path.getsize(filepath)

        cur.execute("""
            INSERT INTO resources (
                title, description, resource_type, department_id, semester, subject_id,
                academic_year, exam_type, file_name, original_file_name, file_size,
                file_ext, uploader_id, status, download_count, view_count, is_featured, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["title"], item["desc"], item["type"], item["dept"], item["sem"],
            item["subj"], item["year"], item["exam"], item["file"], item["file"],
            filesize, "pdf", item["uploader"], item["status"], item["downloads"],
            item["views"], item["featured"], item["tags"]
        ))

    # 5. Insert Ratings & Bookmarks
    cur.execute("SELECT id FROM resources WHERE status = 'approved'")
    approved_ids = [r[0] for r in cur.fetchall()]

    if approved_ids:
        cur.execute("""
            INSERT OR IGNORE INTO resource_ratings (resource_id, user_id, rating, review)
            VALUES (?, ?, ?, ?)
        """, (approved_ids[0], user_map["student1"], 5, "Extremely useful! Exactly the format asked in the final semester exam."))

        cur.execute("""
            INSERT OR IGNORE INTO resource_ratings (resource_id, user_id, rating, review)
            VALUES (?, ?, ?, ?)
        """, (approved_ids[1], user_map["student2"], 5, "Crystal clear notes on Banker's algorithm and Virtual Memory."))

        cur.execute("""
            INSERT OR IGNORE INTO bookmarks (resource_id, user_id)
            VALUES (?, ?)
        """, (approved_ids[0], user_map["student1"]))

        cur.execute("""
            INSERT OR IGNORE INTO bookmarks (resource_id, user_id)
            VALUES (?, ?)
        """, (approved_ids[1], user_map["student1"]))

    # 6. Insert Activity Log
    cur.execute("""
        INSERT INTO activity_logs (user_id, action, details, ip_address)
        VALUES (?, 'SYSTEM_INIT', 'System initialized with departments, subjects, and sample resources', '127.0.0.1')
    """, (user_map["admin"],))

    conn.commit()
    conn.close()
    print("Database successfully seeded with realistic academic resources!")

if __name__ == "__main__":
    seed_database()
