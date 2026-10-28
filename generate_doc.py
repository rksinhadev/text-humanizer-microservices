import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_report():
    doc = Document()

    # Page Margins: 1 inch everywhere
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # ---------------- PAGE 1: TITLE PAGE ----------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_inst.add_run("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY\nVADODARA\n\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_course.add_run("CS545\nSOFTWARE ENGINEERING\nPROJECT REPORT\n\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    p_prog = doc.add_paragraph()
    p_prog.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_prog.add_run("Master of Computer Applications (MCA)\nSecond Year\n\n\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_title.add_run("Project Title:\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    r2 = p_title.add_run("AI-POWERED TEXT HUMANIZER\n(MICROSERVICES ARCHITECTURE)\n\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(15)
    r2.bold = True
    r2.font.color.rgb = RGBColor(15, 76, 129)

    p_grp = doc.add_paragraph()
    p_grp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_grp.add_run("Group No. 29\n\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sub.add_run("Submitted By:\n")
    r.bold = True
    r.font.size = Pt(12)
    p_members = doc.add_paragraph()
    p_members.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_members.add_run("Ritik Kumar Sinha (20252651043)\nKruti Kansagara (20252651027)\nSahil Siddiqui (20252651055)\nJeeshan Adil (20252651026)\n\n\n")
    r.font.size = Pt(11)

    p_to = doc.add_paragraph()
    p_to.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_to.add_run("Submitted To:\n")
    r.bold = True
    r.font.size = Pt(12)
    r2 = p_to.add_run("Faculty Name: Prof. Rishabh Gupta\nDepartment: Department of Computer Science & Engineering\nIndian Institute of Information Technology Vadodara\nAutumn 2026-27")
    r2.font.size = Pt(11)

    doc.add_page_break()

    # ---------------- PAGE 2: CERTIFICATE ----------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("CERTIFICATE\n\n")
    r.font.size = Pt(16)
    r.bold = True

    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.line_spacing = 1.5
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p_cert.add_run("This is to certify that ")
    r.font.size = Pt(12)
    r_names = p_cert.add_run("Ritik Kumar Sinha (20252651043), Kruti Kansagara (20252651027), Sahil Siddiqui (20252651055), and Jeeshan Adil (20252651026)")
    r_names.bold = True
    r_names.font.size = Pt(12)
    r2 = p_cert.add_run(", students of the Master of Computer Applications (MCA) programme at the Indian Institute of Information Technology Vadodara, have completed the laboratory work for CS545 – Software Engineering, covering Experiments 1 to 9, during the academic year 2026-27.\n\nThe work has been submitted as part of the course requirements.\n\n\n")
    r2.font.size = Pt(12)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.line_spacing = 1.5
    r = p_sig.add_run("Date: 28th October 2026\n\n\nFaculty Signature: ______________________\nFaculty Name: Prof. Rishabh Gupta")
    r.font.size = Pt(12)

    doc.add_page_break()

    # ---------------- PAGE 3: DECLARATION ----------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DECLARATION\n\n")
    r.font.size = Pt(16)
    r.bold = True

    p_dec = doc.add_paragraph()
    p_dec.paragraph_format.line_spacing = 1.5
    p_dec.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p_dec.add_run("We hereby declare that the work presented in this Software Engineering Lab Report is our original work, completed as part of the CS545 Software Engineering course.\n\nThe diagrams, tables, system analysis, implementation modules, and testing test cases have been prepared by us. Any external technical references, algorithms, or resources used have been appropriately acknowledged and cited.\n\n\n")
    r.font.size = Pt(12)

    # Student Signature Table
    table_dec = doc.add_table(rows=5, cols=3)
    table_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Student Name", "Enrollment Number", "Signature"]
    for i, h in enumerate(headers):
        cell = table_dec.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "E0E0E0")

    students = [
        ("Ritik Kumar Sinha", "20252651043"),
        ("Kruti Kansagara", "20252651027"),
        ("Sahil Siddiqui", "20252651055"),
        ("Jeeshan Adil", "20252651026")
    ]
    for row_idx, (name, enr) in enumerate(students, start=1):
        table_dec.cell(row_idx, 0).text = name
        table_dec.cell(row_idx, 1).text = enr
        table_dec.cell(row_idx, 2).text = "__________________"

    p_date = doc.add_paragraph("\nDate: 28th October 2026")

    doc.add_page_break()

    # ---------------- PAGE 4: ACKNOWLEDGEMENT ----------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("ACKNOWLEDGEMENT\n\n")
    r.font.size = Pt(16)
    r.bold = True

    p_ack = doc.add_paragraph()
    p_ack.paragraph_format.line_spacing = 1.5
    p_ack.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p_ack.add_run("We would like to express our deepest gratitude to our course instructor, ")
    r_fac = p_ack.add_run("Prof. Rishabh Gupta")
    r_fac.bold = True
    r2 = p_ack.add_run(", for his continuous mentorship, constructive evaluations, and invaluable guidance throughout the CS545 Software Engineering Laboratory sessions.\n\nHis insightful feedback during every stage of the software engineering life cycle—from initial software requirements specification to agile modeling, architectural diagrams, microservice decoupling, and validation test suites—has significantly enriched our understanding of enterprise software design.\n\nWe also extend our sincere appreciation to the Department of Computer Science & Engineering and Indian Institute of Information Technology Vadodara for providing the laboratory infrastructure and computational environment necessary to bring this microservices project to fruition.\n\nFinally, we thank our peers and group members for their collaborative spirit, mutual technical support, and dedication throughout this semester.")
    
    doc.add_page_break()

    # ---------------- PAGE 5: TABLE OF CONTENTS ----------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("TABLE OF CONTENTS\n\n")
    r.font.size = Pt(16)
    r.bold = True

    toc_table = doc.add_table(rows=11, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_headers = ["Exp. No.", "Experiment Title / Topic", "Page No."]
    for i, h in enumerate(toc_headers):
        cell = toc_table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "D9E1F2")

    toc_data = [
        ("Lab-1", "Software Requirements Specification (SRS)", "6"),
        ("Lab-2", "Software Process Model (Agile Scrum)", "7"),
        ("Lab-3", "Use Case Modeling & Diagram", "8"),
        ("Lab-4", "Data Flow Diagrams (DFD Level 0 & Level 1)", "9"),
        ("Lab-5", "UML Class Diagram & Domain Entities", "10"),
        ("Lab-6", "UML Sequence Diagram & Interaction Workflows", "11"),
        ("Lab-8", "Modular System Architecture & Decomposition", "12"),
        ("Lab-9", "Functional Test Cases & Verification Suite", "13"),
        ("-", "Overall Project Conclusion", "14"),
        ("-", "References & Technical Citations", "15")
    ]

    for row_idx, (num, title, pg) in enumerate(toc_data, start=1):
        toc_table.cell(row_idx, 0).text = num
        toc_table.cell(row_idx, 1).text = title
        toc_table.cell(row_idx, 2).text = pg
        toc_table.cell(row_idx, 0).paragraphs[0].runs[0].bold = True

    doc.add_page_break()

    # ---------------- EXPERIMENT 1 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 1\nSOFTWARE REQUIREMENTS SPECIFICATION (SRS)")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("1.1 Aim & Scope", level=2)
    doc.add_paragraph("To formulate a complete Software Requirements Specification (SRS) for the AI-Powered Text Humanizer microservices platform, defining system scope, stakeholder personas, functional requirements, and performance parameters.")

    doc.add_heading("1.2 Functional Requirements", level=2)
    frs = [
        ("FR-1: User Authentication", "The system shall permit secure account registration and authentication using salted bcrypt hashing. Successful logins generate a signed, stateless JSON Web Token (JWT)."),
        ("FR-2: Text Paraphrase Inference", "The system shall accept input text payloads via `/api/humanize`, apply sentence boundary detection, tokenize phrases, and run neural transformations to smooth syntactic cadence."),
        ("FR-3: Transformation Audit & History", "The system shall automatically associate each humanized execution with the authenticated user ID and persist input, output, and execution timestamps."),
        ("FR-4: Reverse Proxy API Gateway", "A central gateway shall accept all incoming browser requests on port 5000 and forward traffic to the appropriate downstream microservice without leaking internal ports.")
    ]
    for title, desc in frs:
        p = doc.add_paragraph()
        r = p.add_run(f"• {title}: ")
        r.bold = True
        p.add_run(desc)

    doc.add_heading("1.3 Non-Functional Requirements", level=2)
    nfrs = [
        ("Response Latency", "Text rewriting under 300 words must complete within 2.5 seconds on CPU/GPU."),
        ("Security & Privacy", "Passwords never stored in plain text. JWT tokens signed with HMAC-SHA256."),
        ("Modularity & Decoupling", "Microservices remain fully autonomous; failures in the AI service do not halt user logins."),
        ("Portability", "Entire stack packaged via standard Dockerfile and Docker Compose manifests.")
    ]
    for title, desc in nfrs:
        p = doc.add_paragraph()
        r = p.add_run(f"• {title}: ")
        r.bold = True
        p.add_run(desc)

    doc.add_page_break()

    # ---------------- EXPERIMENT 2 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 2\nSOFTWARE PROCESS MODEL")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("2.1 Model Selection: Agile Scrum Framework", level=2)
    doc.add_paragraph("For developing the Text Humanizer platform, an Agile Scrum process model was chosen over traditional Waterfall. Because microservices involve independently deployable components (Auth, AI, History, Gateway) and machine learning models require iterative evaluation, Agile's short sprint cycles facilitated rapid prototyping and continuous feedback.")

    doc.add_heading("2.2 Sprint Execution Plan", level=2)
    sprint_table = doc.add_table(rows=5, cols=3)
    sprint_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sp_headers = ["Sprint", "Focus Area", "Key Deliverables"]
    for i, h in enumerate(sp_headers):
        cell = sprint_table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "E0E0E0")

    sprints = [
        ("Sprint 1", "Requirements & DB Architecture", "MySQL schema (`init.sql`), service port allocations, API contracts."),
        ("Sprint 2", "Authentication & Neural Model", "bcrypt/JWT `auth_service.py`, transformer pipeline `ai_service.py`."),
        ("Sprint 3", "API Gateway & History Store", "Reverse proxy `gateway.py`, CRUD endpoints in `history_service.py`."),
        ("Sprint 4", "Frontend & End-to-End Tests", "Single-page responsive UI, functional test suites, Docker integration.")
    ]
    for row_idx, (sp, fa, kd) in enumerate(sprints, start=1):
        sprint_table.cell(row_idx, 0).text = sp
        sprint_table.cell(row_idx, 1).text = fa
        sprint_table.cell(row_idx, 2).text = kd

    doc.add_page_break()

    # ---------------- EXPERIMENT 3 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 3\nUSE CASE DIAGRAM")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("3.1 Use Case Specifications", level=2)
    doc.add_paragraph("The primary actor is the End User (Students, Technical Writers, Researchers). Use cases include registering an account, obtaining credentials, submitting text for humanization, copying transformed output, and managing transformation history logs.")

    if os.path.exists("submission_package/Documentation/diagrams/use_case_diagram.png"):
        doc.add_paragraph()
        doc.add_picture("submission_package/Documentation/diagrams/use_case_diagram.png", width=Inches(6.0))
        p_cap = doc.add_paragraph("Figure 3.1: UML Use Case Diagram for Text Humanizer Microservices")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].italic = True

    doc.add_page_break()

    # ---------------- EXPERIMENT 4 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 4\nDATA FLOW DIAGRAM (DFD)")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("4.1 Level 0 & Level 1 Decomposition", level=2)
    doc.add_paragraph("The DFD models the flow of information across boundaries. At Level 0, the Client Browser interacts with the Text Humanizer boundary and the MySQL data store. At Level 1, the API Gateway demultiplexes client traffic across the Auth Service (Port 5001), AI Engine (Port 5003), and History Service (Port 5004).")

    if os.path.exists("submission_package/Documentation/diagrams/dfd_level1.png"):
        doc.add_paragraph()
        doc.add_picture("submission_package/Documentation/diagrams/dfd_level1.png", width=Inches(6.0))
        p_cap = doc.add_paragraph("Figure 4.1: Level 1 Data Flow Diagram (Microservice Interactions)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].italic = True

    doc.add_page_break()

    # ---------------- EXPERIMENT 5 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 5\nUML CLASS DIAGRAM")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("5.1 Class Diagram & Entity Relationships", level=2)
    doc.add_paragraph("The system architecture follows object-oriented patterns where services wrap data models and encapsulate specific persistence logic. The primary entities are `User` and `HistoryRecord`, interfaced by `AuthService`, `AIService`, and `APIGateway`.")

    cls_table = doc.add_table(rows=5, cols=3)
    cls_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cls_headers = ["Class Name", "Key Attributes", "Key Methods"]
    for i, h in enumerate(cls_headers):
        cell = cls_table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "E0E0E0")

    cls_data = [
        ("User", "id, username, email, password_hash, created_at", "register(), verify_password()"),
        ("HistoryRecord", "id, user_id, original_text, humanized_text, created_at", "create_record(), get_by_user(), delete()"),
        ("APIGateway", "host, port, services_map", "forward(service_base, path), route_auth(), route_humanize()"),
        ("AuthService", "jwt_secret, token_expiry", "hash_pw(), check_pw(), generate_jwt(), verify_token()")
    ]
    for row_idx, (cn, attr, meth) in enumerate(cls_data, start=1):
        cls_table.cell(row_idx, 0).text = cn
        cls_table.cell(row_idx, 1).text = attr
        cls_table.cell(row_idx, 2).text = meth

    doc.add_page_break()

    # ---------------- EXPERIMENT 6 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 6\nUML SEQUENCE DIAGRAM")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("6.1 Dynamic Interaction & Execution Workflow", level=2)
    doc.add_paragraph("The sequence diagram captures the exact runtime message passing among the Client UI, API Gateway, Auth Microservice, AI Inference Engine, and MySQL Database during a text humanization operation.")

    if os.path.exists("submission_package/Documentation/diagrams/sequence_diagram.png"):
        doc.add_paragraph()
        doc.add_picture("submission_package/Documentation/diagrams/sequence_diagram.png", width=Inches(6.0))
        p_cap = doc.add_paragraph("Figure 6.1: UML Sequence Diagram - User Authentication & AI Transformation")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].italic = True

    doc.add_page_break()

    # ---------------- EXPERIMENT 8 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 8\nMODULAR DESIGN & SYSTEM ARCHITECTURE")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("8.1 Modular Decomposition Principles", level=2)
    doc.add_paragraph("High cohesion and low coupling govern the system's modularization. Each microservice resides in its own isolated module with dedicated configuration, dependency tree, and REST API interface.")

    if os.path.exists("submission_package/Documentation/diagrams/modular_architecture.png"):
        doc.add_paragraph()
        doc.add_picture("submission_package/Documentation/diagrams/modular_architecture.png", width=Inches(6.0))
        p_cap = doc.add_paragraph("Figure 8.1: Tiered Modular Architecture Diagram")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].italic = True

    doc.add_page_break()

    # ---------------- EXPERIMENT 9 ----------------
    p = doc.add_paragraph()
    r = p.add_run("LAB EXPERIMENT 9\nFUNCTIONAL TEST CASES")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("9.1 Test Suite & Verification Results", level=2)
    doc.add_paragraph("Comprehensive black-box and white-box test cases were executed against each microservice endpoint to ensure data consistency, error handling, and security.")

    tc_table = doc.add_table(rows=7, cols=5)
    tc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tc_headers = ["Test ID", "Test Scenario", "Input Data", "Expected Output", "Status"]
    for i, h in enumerate(tc_headers):
        cell = tc_table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "E0E0E0")

    tc_data = [
        ("TC-01", "Registration with valid data", "New user credentials", "HTTP 201 Created & DB entry", "PASS"),
        ("TC-02", "Login with valid credentials", "Username & Password", "HTTP 200 OK + Signed JWT", "PASS"),
        ("TC-03", "Login with incorrect password", "Wrong password", "HTTP 401 Unauthorized", "PASS"),
        ("TC-04", "Humanize valid AI text", "50-word AI paragraph", "HTTP 200 OK + Paraphrased text", "PASS"),
        ("TC-05", "Save history record", "Valid JWT + Text", "HTTP 201 Created & Linked ID", "PASS"),
        ("TC-06", "Gateway fallback on service crash", "Killed AI service", "HTTP 503 Service Unavailable", "PASS")
    ]
    for row_idx, (tid, sc, inp, exp, st) in enumerate(tc_data, start=1):
        tc_table.cell(row_idx, 0).text = tid
        tc_table.cell(row_idx, 1).text = sc
        tc_table.cell(row_idx, 2).text = inp
        tc_table.cell(row_idx, 3).text = exp
        tc_table.cell(row_idx, 4).text = st
        tc_table.cell(row_idx, 4).paragraphs[0].runs[0].bold = True

    doc.add_page_break()

    # ---------------- CONCLUSION & REFERENCES ----------------
    p = doc.add_paragraph()
    r = p.add_run("OVERALL CONCLUSION & REFERENCES")
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)

    doc.add_heading("Overall Conclusion", level=2)
    p_concl = doc.add_paragraph()
    p_concl.paragraph_format.line_spacing = 1.5
    p_concl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_concl.add_run("The CS545 Software Engineering laboratory coursework provided hands-on expertise across all software development lifecycle stages. Developing the AI-Powered Text Humanizer under a microservices paradigm demonstrated how requirement specifications, agile planning, UML diagrams, modular separation, and structured functional testing combine to produce resilient, high-quality distributed software. The resulting architecture effectively isolates failures, secures authentication via JWT, and delivers humanized text with high responsiveness.")

    doc.add_heading("References", level=2)
    refs = [
        "Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill.",
        "Newman, S. (2021). Building Microservices: Designing Fine-Grained Systems (2nd ed.). O'Reilly Media.",
        "Fowler, M. (2018). Patterns of Enterprise Application Architecture. Addison-Wesley Professional.",
        "Hugging Face Transformers Documentation, Paraphrasing & Sequence-to-Sequence Models, https://huggingface.co/docs/transformers",
        "Flask Documentation: Modular Applications with Blueprints and Reverse Proxying, https://flask.palletsprojects.com/"
    ]
    for i, ref in enumerate(refs, start=1):
        doc.add_paragraph(f"[{i}] {ref}")

    # Save Document
    doc_path = "submission_package/Report/CS545_Final_Project_Report_Group29.docx"
    doc.save(doc_path)
    print(f"Generated Word Document: {doc_path}")

create_report()
