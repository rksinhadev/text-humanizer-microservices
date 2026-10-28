import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_pdf():
    pdf_path = "submission_package/Report/CS545_Final_Project_Report_Group29.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1, # Center
        textColor=colors.HexColor('#002060')
    )

    sub_title_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#0f4c81')
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#002060'),
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#222222'),
        spaceBefore=8,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=4 # Justify
    )

    center_body = ParagraphStyle(
        'CenterBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1
    )

    story = []

    # ---------------- PAGE 1: TITLE PAGE ----------------
    story.append(Paragraph("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY VADODARA", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("CS545<br/>SOFTWARE ENGINEERING<br/>PROJECT REPORT", h1_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Master of Computer Applications (MCA)<br/>Second Year", center_body))
    story.append(Spacer(1, 35))
    story.append(Paragraph("Project Title:", center_body))
    story.append(Spacer(1, 5))
    story.append(Paragraph("AI-POWERED TEXT HUMANIZER<br/>(MICROSERVICES ARCHITECTURE)", sub_title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Group No. 29</b>", center_body))
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>Submitted By:</b>", center_body))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Ritik Kumar Sinha (20252651043)<br/>Kruti Kansagara (20252651027)<br/>Sahil Siddiqui (20252651055)<br/>Jeeshan Adil (20252651026)", center_body))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Submitted To:</b><br/>Faculty Name: Prof. Rishabh Gupta<br/>Department: Department of Computer Science & Engineering<br/>Indian Institute of Information Technology Vadodara<br/>Autumn 2026-27", center_body))
    story.append(PageBreak())

    # ---------------- PAGE 2: CERTIFICATE ----------------
    story.append(Paragraph("CERTIFICATE", title_style))
    story.append(Spacer(1, 30))
    cert_text = (
        "This is to certify that <b>Ritik Kumar Sinha (20252651043)</b>, <b>Kruti Kansagara (20252651027)</b>, "
        "<b>Sahil Siddiqui (20252651055)</b>, and <b>Jeeshan Adil (20252651026)</b>, students of the Master of "
        "Computer Applications (MCA) programme at the Indian Institute of Information Technology Vadodara, "
        "have completed the laboratory work for <b>CS545 – Software Engineering</b>, covering Experiments 1 to 9, "
        "during the academic year 2026-27.<br/><br/>The work has been submitted as part of the course requirements."
    )
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 60))
    story.append(Paragraph("Date: 28th October 2026<br/><br/><br/>Faculty Signature: ______________________<br/>Faculty Name: Prof. Rishabh Gupta", body_style))
    story.append(PageBreak())

    # ---------------- PAGE 3: DECLARATION ----------------
    story.append(Paragraph("DECLARATION", title_style))
    story.append(Spacer(1, 25))
    dec_text = (
        "We hereby declare that the work presented in this Software Engineering Lab Report is our original work, "
        "completed as part of the CS545 Software Engineering course.<br/><br/>"
        "The diagrams, tables, system analysis, implementation modules, and testing test cases have been prepared by us. "
        "Any external technical references, algorithms, or resources used have been appropriately acknowledged."
    )
    story.append(Paragraph(dec_text, body_style))
    story.append(Spacer(1, 30))

    dec_data = [
        ["Student Name", "Enrollment Number", "Signature"],
        ["Ritik Kumar Sinha", "20252651043", "__________________"],
        ["Kruti Kansagara", "20252651027", "__________________"],
        ["Sahil Siddiqui", "20252651055", "__________________"],
        ["Jeeshan Adil", "20252651026", "__________________"]
    ]
    t_dec = Table(dec_data, colWidths=[2.2*inch, 2.0*inch, 2.0*inch])
    t_dec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EEEEEE')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_dec)
    story.append(Spacer(1, 25))
    story.append(Paragraph("Date: 28th October 2026", body_style))
    story.append(PageBreak())

    # ---------------- PAGE 4: ACKNOWLEDGEMENT ----------------
    story.append(Paragraph("ACKNOWLEDGEMENT", title_style))
    story.append(Spacer(1, 25))
    ack_text = (
        "We would like to express our deepest gratitude to our course instructor, <b>Prof. Rishabh Gupta</b>, "
        "for his continuous mentorship, constructive evaluations, and invaluable guidance throughout the CS545 "
        "Software Engineering Laboratory sessions.<br/><br/>"
        "His insightful feedback during every stage of the software engineering life cycle—from initial software "
        "requirements specification to agile modeling, architectural diagrams, microservice decoupling, and validation "
        "test suites—has significantly enriched our understanding of enterprise software design.<br/><br/>"
        "We also extend our sincere appreciation to the Department of Computer Science & Engineering and "
        "Indian Institute of Information Technology Vadodara for providing the laboratory infrastructure and "
        "computational environment necessary to bring this microservices project to fruition.<br/><br/>"
        "Finally, we thank our peers and group members for their collaborative spirit, mutual technical support, "
        "and dedication throughout this semester."
    )
    story.append(Paragraph(ack_text, body_style))
    story.append(PageBreak())

    # ---------------- PAGE 5: TABLE OF CONTENTS ----------------
    story.append(Paragraph("TABLE OF CONTENTS", title_style))
    story.append(Spacer(1, 25))
    toc_data = [
        ["Exp. No.", "Experiment Title / Topic", "Page No."],
        ["Lab-1", "Software Requirements Specification (SRS)", "6"],
        ["Lab-2", "Software Process Model (Agile Scrum)", "7"],
        ["Lab-3", "Use Case Modeling & Diagram", "8"],
        ["Lab-4", "Data Flow Diagrams (DFD Level 0 & Level 1)", "9"],
        ["Lab-5", "UML Class Diagram & Domain Entities", "10"],
        ["Lab-6", "UML Sequence Diagram & Interaction Workflows", "11"],
        ["Lab-8", "Modular System Architecture & Decomposition", "12"],
        ["Lab-9", "Functional Test Cases & Verification Suite", "13"],
        ["-", "Overall Project Conclusion", "14"],
        ["-", "References & Technical Citations", "15"]
    ]
    t_toc = Table(toc_data, colWidths=[1.2*inch, 4.2*inch, 1.2*inch])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#D9E1F2')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ---------------- LAB 1 ----------------
    story.append(Paragraph("LAB EXPERIMENT 1: SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", h1_style))
    story.append(Paragraph("<b>1.1 System Scope & Purpose:</b> The Text Humanizer is an enterprise-ready microservices solution designed to transform rigid, syntactically uniform AI-generated content into expressive, fluent prose while strictly preserving the semantic core.", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>1.2 Functional Requirements (FRs):</b>", h2_style))
    frs = [
        "<b>FR-1 [User Authentication]:</b> The platform shall provide secure sign-up and sign-in capabilities using salted bcrypt hash encryption and signed JSON Web Tokens (JWT).",
        "<b>FR-2 [Text Humanization Engine]:</b> The AI inference pipeline shall process raw text payloads, execute sentence segmentation, and produce natural paraphrase alternatives.",
        "<b>FR-3 [History Management]:</b> The system shall maintain persistent transformation audit logs linking authenticated user IDs to original and output text.",
        "<b>FR-4 [API Gateway Routing]:</b> A centralized reverse-proxy gateway shall handle routing, client authorization headers, and unified error handling."
    ]
    for fr in frs:
        story.append(Paragraph(f"• {fr}", body_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("<b>1.3 Non-Functional Requirements (NFRs):</b>", h2_style))
    nfrs = [
        "<b>Performance:</b> End-to-end response time under 3 seconds for standard paragraph submissions.",
        "<b>Modularity:</b> Microservices are decoupled and stateless to enable zero-downtime scaling.",
        "<b>Security:</b> Bearer token validation across protected API endpoints with HMAC-SHA256 signatures."
    ]
    for nfr in nfrs:
        story.append(Paragraph(f"• {nfr}", body_style))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ---------------- LAB 2 ----------------
    story.append(Paragraph("LAB EXPERIMENT 2: SOFTWARE PROCESS MODEL", h1_style))
    story.append(Paragraph("<b>2.1 Process Framework: Agile Scrum:</b> An Agile Scrum lifecycle was adopted to support iterative ML model tuning and parallel microservice component development across four 2-week sprints.", body_style))
    story.append(Spacer(1, 12))
    
    sp_data = [
        ["Sprint", "Focus Area", "Milestone Deliverables"],
        ["Sprint 1", "Architecture & DB Design", "MySQL schema (`init.sql`), port assignment, Docker setup"],
        ["Sprint 2", "Auth & Neural Service", "bcrypt/JWT `auth_service.py`, pipeline `ai_service.py`"],
        ["Sprint 3", "API Gateway & History", "Reverse proxy `gateway.py`, CRUD endpoints `history_service.py`"],
        ["Sprint 4", "Frontend & Test Suites", "Interactive single-page UI, functional verification suite"]
    ]
    t_sp = Table(sp_data, colWidths=[1.1*inch, 2.2*inch, 3.3*inch])
    t_sp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EEEEEE')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sp)
    story.append(PageBreak())

    # ---------------- LAB 3 ----------------
    story.append(Paragraph("LAB EXPERIMENT 3: USE CASE MODELING", h1_style))
    story.append(Paragraph("The Use Case Diagram defines functional interactions between the End User actor and the Text Humanizer Microservices boundary.", body_style))
    story.append(Spacer(1, 10))
    if os.path.exists("submission_package/Documentation/diagrams/use_case_diagram.png"):
        story.append(Image("submission_package/Documentation/diagrams/use_case_diagram.png", width=6.2*inch, height=3.7*inch))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<i>Figure 3.1: UML Use Case Diagram</i>", center_body))
    story.append(PageBreak())

    # ---------------- LAB 4 ----------------
    story.append(Paragraph("LAB EXPERIMENT 4: DATA FLOW DIAGRAMS (DFD)", h1_style))
    story.append(Paragraph("Level 1 DFD illustrates data transformation across the API Gateway, Auth Microservice, AI Engine, and History persistence layer.", body_style))
    story.append(Spacer(1, 10))
    if os.path.exists("submission_package/Documentation/diagrams/dfd_level1.png"):
        story.append(Image("submission_package/Documentation/diagrams/dfd_level1.png", width=6.2*inch, height=3.8*inch))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<i>Figure 4.1: Level 1 Data Flow Diagram (DFD)</i>", center_body))
    story.append(PageBreak())

    # ---------------- LAB 5 ----------------
    story.append(Paragraph("LAB EXPERIMENT 5: UML CLASS DIAGRAM", h1_style))
    story.append(Paragraph("Entity classes encapsulate domain business rules and data models across services:", body_style))
    story.append(Spacer(1, 10))
    cls_data = [
        ["Class", "Attributes", "Operations"],
        ["User", "id, username, email, password_hash", "register(), verify_password()"],
        ["HistoryRecord", "id, user_id, original, humanized", "create_record(), get_by_user(), delete()"],
        ["APIGateway", "host, port, services_map", "forward(), route_auth(), route_humanize()"],
        ["AuthService", "jwt_secret, token_expiry", "hash_pw(), check_pw(), generate_jwt()"]
    ]
    t_cls = Table(cls_data, colWidths=[1.3*inch, 2.7*inch, 2.6*inch])
    t_cls.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EEEEEE')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cls)
    story.append(PageBreak())

    # ---------------- LAB 6 ----------------
    story.append(Paragraph("LAB EXPERIMENT 6: UML SEQUENCE DIAGRAM", h1_style))
    story.append(Paragraph("The dynamic interactions during user authentication and text humanization are mapped below:", body_style))
    story.append(Spacer(1, 10))
    if os.path.exists("submission_package/Documentation/diagrams/sequence_diagram.png"):
        story.append(Image("submission_package/Documentation/diagrams/sequence_diagram.png", width=6.2*inch, height=4.2*inch))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<i>Figure 6.1: UML Sequence Diagram (Authentication & Text Transformation)</i>", center_body))
    story.append(PageBreak())

    # ---------------- LAB 8 ----------------
    story.append(Paragraph("LAB EXPERIMENT 8: MODULAR SYSTEM ARCHITECTURE", h1_style))
    story.append(Paragraph("Modular architecture isolates responsibilities across Presentation, Microservices Application, and Persistence tiers.", body_style))
    story.append(Spacer(1, 10))
    if os.path.exists("submission_package/Documentation/diagrams/modular_architecture.png"):
        story.append(Image("submission_package/Documentation/diagrams/modular_architecture.png", width=6.2*inch, height=3.8*inch))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<i>Figure 8.1: Modular System Architecture Diagram</i>", center_body))
    story.append(PageBreak())

    # ---------------- LAB 9 ----------------
    story.append(Paragraph("LAB EXPERIMENT 9: FUNCTIONAL TEST CASES", h1_style))
    story.append(Paragraph("Structured test verification scenarios executed across service endpoints:", body_style))
    story.append(Spacer(1, 10))

    tc_data = [
        ["Test ID", "Scenario", "Input", "Expected Output", "Status"],
        ["TC-01", "User Registration", "Valid credentials", "HTTP 201 Created & DB entry", "PASS"],
        ["TC-02", "User Login", "Username & Password", "HTTP 200 OK + Signed JWT", "PASS"],
        ["TC-03", "Invalid Password", "Incorrect password", "HTTP 401 Unauthorized", "PASS"],
        ["TC-04", "Humanize AI text", "50-word paragraph", "HTTP 200 OK + Paraphrased", "PASS"],
        ["TC-05", "Save history", "Valid JWT + Text", "HTTP 201 Created", "PASS"],
        ["TC-06", "Service fallback", "Killed AI service", "HTTP 503 Service Unavailable", "PASS"]
    ]
    t_tc = Table(tc_data, colWidths=[0.8*inch, 1.6*inch, 1.4*inch, 2.0*inch, 0.8*inch])
    t_tc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EEEEEE')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (-1,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tc)
    story.append(PageBreak())

    # ---------------- CONCLUSION & REFERENCES ----------------
    story.append(Paragraph("OVERALL CONCLUSION & REFERENCES", h1_style))
    story.append(Spacer(1, 10))
    concl_p = (
        "The CS545 Software Engineering coursework established a comprehensive practical foundation in distributed "
        "software engineering. By designing and realizing the AI-Powered Text Humanizer under a microservices paradigm, "
        "the team successfully bridged formal requirements (SRS), agile process modeling, UML structural and behavioral "
        "representations (Use Case, DFD, Class, Sequence), modular design, and robust functional test suites. "
        "The resulting system is fault-isolated, scalable, secure, and ready for deployment."
    )
    story.append(Paragraph(concl_p, body_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>References:</b>", h2_style))
    refs = [
        "[1] Pressman, R. S., & Maxim, B. R. (2020). <i>Software Engineering: A Practitioner's Approach</i> (9th ed.). McGraw-Hill.",
        "[2] Newman, S. (2021). <i>Building Microservices: Designing Fine-Grained Systems</i> (2nd ed.). O'Reilly Media.",
        "[3] Fowler, M. (2018). <i>Patterns of Enterprise Application Architecture</i>. Addison-Wesley Professional.",
        "[4] Hugging Face Transformers: State-of-the-Art Natural Language Processing, https://huggingface.co/docs/transformers",
        "[5] Flask Documentation: Modular Web Services and Reverse Proxying, https://flask.palletsprojects.com/"
    ]
    for r in refs:
        story.append(Paragraph(r, body_style))
        story.append(Spacer(1, 3))

    doc.build(story)
    print(f"Generated PDF Document: {pdf_path}")

generate_pdf()
