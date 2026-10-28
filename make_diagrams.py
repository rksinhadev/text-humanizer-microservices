import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('submission_package/Documentation/diagrams', exist_ok=True)

# Helper function to save figure cleanly
def save_fig(fig, name):
    path = os.path.join('submission_package/Documentation/diagrams', name)
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {path}")

# 1. Use Case Diagram
def generate_use_case():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Boundary box
    rect = patches.FancyBboxPatch((3.0, 0.5), 6.5, 7.0, boxstyle="round,pad=0.2",
                                  ec="#1f77b4", fc="#f0f8ff", lw=2)
    ax.add_patch(rect)
    ax.text(6.25, 7.1, "Text Humanizer Microservices System", ha='center', va='center',
            fontsize=13, fontweight='bold', color="#0f4c81")

    # Actor (Stick Figure or Circle)
    ax.plot(1.2, 4.8, 'o', ms=20, mfc='#ffffff', mec='#333333', mew=2)
    ax.plot([1.2, 1.2], [4.4, 3.2], color='#333333', lw=2.5) # Body
    ax.plot([0.7, 1.7], [3.9, 3.9], color='#333333', lw=2.5) # Arms
    ax.plot([1.2, 0.8], [3.2, 2.2], color='#333333', lw=2.5) # Left Leg
    ax.plot([1.2, 1.6], [3.2, 2.2], color='#333333', lw=2.5) # Right Leg
    ax.text(1.2, 1.8, "End User\n(Student/Writer)", ha='center', va='center', fontsize=11, fontweight='bold')

    # Use cases
    use_cases = [
        (6.25, 6.2, "UC1: Register & Authenticate (JWT)"),
        (6.25, 5.0, "UC2: Submit AI Text for Humanization"),
        (6.25, 3.8, "UC3: Inspect Naturalness Score & Copy Result"),
        (6.25, 2.6, "UC4: View Persistent Audit / History Logs"),
        (6.25, 1.4, "UC5: Delete History Record & Check Health")
    ]

    for (x, y, text) in use_cases:
        ellipse = patches.Ellipse((x, y), 5.6, 0.85, ec='#2ca02c', fc='#e8f5e9', lw=1.8)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='semibold')
        # Line from actor
        ax.annotate("", xy=(x - 2.8, y), xytext=(1.7, 3.9),
                    arrowprops=dict(arrowstyle="->", color="#555555", lw=1.5))

    save_fig(fig, 'use_case_diagram.png')

# 2. DFD Level 0 & 1 Combined Architecture
def generate_dfd():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(5.5, 7.6, "Data Flow Diagram (Level 1) - Text Humanizer Services", 
            ha='center', va='center', fontsize=13, fontweight='bold', color="#222222")

    # External Entity: User
    rect_user = patches.Rectangle((0.5, 3.2), 2.0, 1.5, ec="#333333", fc="#e0e0e0", lw=2)
    ax.add_patch(rect_user)
    ax.text(1.5, 3.95, "Client Browser\n(Web Frontend)", ha='center', va='center', fontsize=10, fontweight='bold')

    # Process: API Gateway
    rect_gw = patches.FancyBboxPatch((3.5, 3.2), 2.2, 1.5, boxstyle="round,pad=0.1", ec="#1f77b4", fc="#bbdefb", lw=2)
    ax.add_patch(rect_gw)
    ax.text(4.6, 3.95, "0.0 API Gateway\n(Reverse Proxy\nPort 5000)", ha='center', va='center', fontsize=9.5, fontweight='bold')

    # Downstream Services
    services = [
        (7.5, 5.7, "1.0 Auth Service\n(Port 5001 / JWT)", "#ffe0b2", "#f57c00"),
        (7.5, 3.2, "2.0 AI Engine\n(Port 5003 / NLP)", "#c8e6c9", "#388e3c"),
        (7.5, 0.7, "3.0 History Service\n(Port 5004 / CRUD)", "#e1bee7", "#7b1fa2"),
    ]

    for (x, y, title, fc, ec) in services:
        proc = patches.FancyBboxPatch((x, y), 2.5, 1.4, boxstyle="round,pad=0.1", ec=ec, fc=fc, lw=2)
        ax.add_patch(proc)
        ax.text(x+1.25, y+0.7, title, ha='center', va='center', fontsize=9, fontweight='bold')

    # Data Store: MySQL DB
    ax.plot([10.2, 10.8], [3.2, 3.2], color="#333333", lw=2)
    ax.plot([10.2, 10.8], [4.6, 4.6], color="#333333", lw=2)
    ax.text(10.5, 3.9, "D1 | MySQL Database\n(users & history)", ha='center', va='center', fontsize=8.5, fontweight='bold', rotation=90)

    # Connections
    # User <-> Gateway
    ax.annotate("HTTP Request", xy=(3.5, 4.2), xytext=(2.5, 4.2),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.5), fontsize=8)
    ax.annotate("JSON / HTML", xy=(2.5, 3.6), xytext=(3.5, 3.6),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.5), fontsize=8)

    # Gateway <-> Auth
    ax.annotate("/api/auth", xy=(7.5, 6.2), xytext=(5.7, 4.5),
                arrowprops=dict(arrowstyle="<->", color="#f57c00", lw=1.5), fontsize=8)

    # Gateway <-> AI
    ax.annotate("/api/humanize", xy=(7.5, 3.9), xytext=(5.7, 3.9),
                arrowprops=dict(arrowstyle="<->", color="#388e3c", lw=1.5), fontsize=8)

    # Gateway <-> History
    ax.annotate("/api/history", xy=(7.5, 1.6), xytext=(5.7, 3.4),
                arrowprops=dict(arrowstyle="<->", color="#7b1fa2", lw=1.5), fontsize=8)

    # Auth <-> DB
    ax.annotate("SQL", xy=(10.2, 4.2), xytext=(9.7, 6.2),
                arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.3), fontsize=7.5)

    # History <-> DB
    ax.annotate("SQL", xy=(10.2, 3.6), xytext=(9.7, 1.6),
                arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.3), fontsize=7.5)

    save_fig(fig, 'dfd_level1.png')

# 3. Modular Architecture Diagram
def generate_modular_arch():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5.5, 7.5, "Modular System Architecture (Lab 8)", 
            ha='center', va='center', fontsize=14, fontweight='bold', color="#111111")

    # Presentation Tier
    p_box = patches.Rectangle((0.6, 5.0), 9.8, 1.8, ec="#3949ab", fc="#e8eaf6", lw=2)
    ax.add_patch(p_box)
    ax.text(1.0, 6.4, "PRESENTATION TIER (UI & ROUTING)", fontsize=11, fontweight='bold', color="#1a237e")
    ax.text(2.6, 5.7, "[templates/index.html]\nHTML5 Responsive View", ha='center', fontsize=9, bbox=dict(boxstyle="round", fc="#ffffff", ec="#3949ab"))
    ax.text(5.5, 5.7, "[static/script.js & style.css]\nState & Async Fetch Client", ha='center', fontsize=9, bbox=dict(boxstyle="round", fc="#ffffff", ec="#3949ab"))
    ax.text(8.5, 5.7, "[gateway.py]\nReverse Proxy & Gateway :5000", ha='center', fontsize=9, bbox=dict(boxstyle="round", fc="#ffffff", ec="#3949ab"))

    # Service Tier
    s_box = patches.Rectangle((0.6, 2.6), 9.8, 2.0, ec="#00897b", fc="#e0f2f1", lw=2)
    ax.add_patch(s_box)
    ax.text(1.0, 4.2, "MICROSERVICES APPLICATION TIER", fontsize=11, fontweight='bold', color="#004d40")
    ax.text(2.3, 3.4, "auth_service.py (:5001)\n* bcrypt Hashing\n* JWT Generation/Verify", ha='center', fontsize=8.5, bbox=dict(boxstyle="round", fc="#ffffff", ec="#00897b"))
    ax.text(5.5, 3.4, "ai_service.py (:5003)\n* Sentence Tokenization\n* Transformers Paraphrase", ha='center', fontsize=8.5, bbox=dict(boxstyle="round", fc="#ffffff", ec="#00897b"))
    ax.text(8.7, 3.4, "history_service.py (:5004)\n* Transformation Logs\n* User-linked CRUD API", ha='center', fontsize=8.5, bbox=dict(boxstyle="round", fc="#ffffff", ec="#00897b"))

    # Data Tier
    d_box = patches.Rectangle((0.6, 0.4), 9.8, 1.8, ec="#fb8c00", fc="#fff3e0", lw=2)
    ax.add_patch(d_box)
    ax.text(1.0, 1.8, "PERSISTENCE & INFRASTRUCTURE TIER", fontsize=11, fontweight='bold', color="#e65100")
    ax.text(3.0, 1.1, "db.py / mysql-connector\nConnection Pool & Transactions", ha='center', fontsize=9, bbox=dict(boxstyle="round", fc="#ffffff", ec="#fb8c00"))
    ax.text(7.5, 1.1, "MySQL Database (:3306)\nTables: `users` | `history`", ha='center', fontsize=9, bbox=dict(boxstyle="round", fc="#ffffff", ec="#fb8c00"))

    # Inter-tier arrows
    ax.annotate("", xy=(5.5, 4.6), xytext=(5.5, 5.0), arrowprops=dict(arrowstyle="<->", color="#333333", lw=2))
    ax.annotate("", xy=(5.5, 2.2), xytext=(5.5, 2.6), arrowprops=dict(arrowstyle="<->", color="#333333", lw=2))

    save_fig(fig, 'modular_architecture.png')

# 4. Sequence Diagram
def generate_sequence():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(5.0, 9.6, "UML Sequence Diagram: Authentication & Humanization Flow", 
            ha='center', va='center', fontsize=12, fontweight='bold', color="#111111")

    actors = [
        (1.0, "Client UI"),
        (3.5, "API Gateway"),
        (6.0, "Auth Service"),
        (8.5, "AI Service")
    ]

    # Lifelines
    for (x, name) in actors:
        box = patches.FancyBboxPatch((x-0.8, 8.8), 1.6, 0.5, boxstyle="round,pad=0.05", ec="#333333", fc="#eceff1")
        ax.add_patch(box)
        ax.text(x, 9.05, name, ha='center', va='center', fontsize=9.5, fontweight='bold')
        ax.plot([x, x], [8.8, 0.5], 'k--', lw=1, alpha=0.6)

    # Messages
    steps = [
        (1.0, 3.5, 8.2, "1. POST /api/auth/login", "#1976d2"),
        (3.5, 6.0, 7.6, "2. Forward credentials", "#1976d2"),
        (6.0, 3.5, 7.0, "3. Verify & return JWT", "#388e3c"),
        (3.5, 1.0, 6.4, "4. Return Auth Token", "#388e3c"),
        (1.0, 3.5, 5.6, "5. POST /api/humanize (Bearer Token + Text)", "#1976d2"),
        (3.5, 8.5, 4.8, "6. Forward text payload", "#1976d2"),
        (8.5, 8.5, 4.0, "7. Neural Paraphrase Transformation", "#e65100"),
        (8.5, 3.5, 3.2, "8. Humanized text response", "#388e3c"),
        (3.5, 1.0, 2.4, "9. Deliver finished result", "#388e3c")
    ]

    for (x1, x2, y, label, col) in steps:
        if x1 == x2:
            # Self call
            ax.annotate("", xy=(x1+0.4, y-0.3), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.5, connectionstyle="arc3,rad=-0.5"))
            ax.text(x1+0.5, y-0.15, label, fontsize=8.5, fontweight='bold', color=col)
        else:
            ax.annotate("", xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.6))
            ax.text((x1+x2)/2, y+0.18, label, ha='center', fontsize=8.5, fontweight='bold', color=col)

    save_fig(fig, 'sequence_diagram.png')

generate_use_case()
generate_dfd()
generate_modular_arch()
generate_sequence()
print("All experiment diagrams generated successfully!")
