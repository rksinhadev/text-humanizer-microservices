# Project Title: AI-Powered Text Humanizer (Microservices Architecture)
**Course:** CS545 – Software Engineering Lab  
**Institution:** Indian Institute of Information Technology Vadodara (IIIT Vadodara)  
**Academic Year:** Autumn 2026-27 | MCA 2nd Year  
**Group Number:** 29  

---

## Group Members & Enrollment Details
1. **Ritik Kumar Sinha** (Enrollment No: 20252651043)
2. **Kruti Kansagara** (Enrollment No: 20252651027)
3. **Sahil Siddiqui** (Enrollment No: 20252651055)
4. **Jeeshan Adil** (Enrollment No: 20252651026)

**Faculty In-Charge:** Prof. Rishabh Gupta

---

## 1. Project Overview & Motivation
Text Humanizer is a distributed, microservices-based application engineered to process AI-generated or machine-synthesized text and restructure it into natural, nuanced, and human-like writing. It removes detectable stylistic footprints, alters syntactic monotony, and enriches vocabulary while preserving the underlying semantic intent.

### Core Capabilities
* **API Gateway Routing:** Single entry point for clients, managing reverse proxy routing, header forwarding, and unified error handling.
* **Authentication Microservice:** JWT-secured registration, login, and token verification backed by salted bcrypt password hashing.
* **AI Transformation Microservice:** Paraphrasing and humanization engine utilizing neural sentence transformation pipelines.
* **History Microservice:** Manages persistent audit logs of past humanization jobs, inputs, outputs, timestamps, and user associations.
* **Interactive Responsive UI:** Modern dashboard with instant humanization preview, word/character counters, clipboard tools, and historical review.

---

## 2. Software Requirements & Prerequisites
### System Requirements
* **Operating System:** Windows 10/11, Linux (Ubuntu 20.04+), or macOS
* **Python Runtime:** Python 3.10+ (Recommended Python 3.11 or 3.12)
* **Database:** MySQL Server 8.0+ / MariaDB 10.5+
* **Containerization (Optional):** Docker & Docker Compose v2+

### Core Dependencies (`requirements.txt`)
* `Flask` (Web framework for services and gateway)
* `mysql-connector-python` (Database connectivity)
* `bcrypt` (Secure credential hashing)
* `PyJWT` (Stateless token authorization)
* `python-dotenv` (Environment configuration)
* `requests` (Inter-service HTTP communication)
* `transformers`, `torch`, `sentencepiece` (AI model inference pipeline)

---

## 3. Architecture & Service Ports
| Service Name | Default Port | Responsibility |
| :--- | :--- | :--- |
| **API Gateway** | `5000` | Static asset serving, frontend routing, reverse proxy to downstream microservices |
| **Auth Service** | `5001` | User registration, login validation, JWT issuing & verification |
| **AI Service** | `5003` | Text preprocessing, contextual humanization model execution, AI rewriting |
| **History Service** | `5004` | Retrieval, creation, and deletion of user transformation records |
| **MySQL Database** | `3306` | Relational persistence for user accounts and history logs |

---

## 4. Setup & Execution Instructions

### Option A: Local Execution (Native Python)
1. **Clone/Navigate to directory:**
   ```bash
   cd text-humanizer-microservices
   ```
2. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and configure your MySQL credentials:
   ```env
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=text_humanizer
   JWT_SECRET=supersecretkey123
   ```
3. **Initialize Database:**
   Import or run the schema in `database/init.sql`:
   ```bash
   mysql -u root -p < database/init.sql
   ```
4. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run All Microservices Simultaneously:**
   ```bash
   python run_all.py
   ```
6. **Access Application:**
   Open your browser at `http://127.0.0.1:5000`.

---

### Option B: Docker Compose Execution
```bash
docker compose up --build
```
The gateway will be accessible at `http://localhost:5000`.

---

## 5. Individual Group Member Contributions
| Member Name | Enrollment No. | Key Responsibilities & Module Ownership |
| :--- | :--- | :--- |
| **Ritik Kumar Sinha** | 20252651043 | **AI Transformation Service & Model Pipeline:** Developed `ai_service.py`, integrated the NLP rewriting pipeline, implemented tokenization and output smoothing algorithms, formulated SRS functional requirements and test suite for AI accuracy. |
| **Kruti Kansagara** | 20252651027 | **Frontend Dashboard & UX:** Engineered `templates/index.html`, `static/style.css`, and `static/script.js`. Implemented asynchronous fetch requests to gateway, token storage in browser `localStorage`, live copy buttons, and status alerts. Designed Use Case & DFD diagrams. |
| **Sahil Siddiqui** | 20252651055 | **Auth Service & Gateway Reverse Proxy:** Built `auth_service.py` with bcrypt hashing and JWT token issuance, designed `gateway.py` with transparent reverse proxying, header forwarding, error propagation, and architectural sequence diagrams. |
| **Jeeshan Adil** | 20252651026 | **History Service, Database Schema & Testing:** Designed relational database schema (`init.sql`, `db.py`), built `history_service.py` for persistent user history CRUD operations, authored functional test scenarios (Lab 9), modular decomposition diagrams, and containerization setup. |
