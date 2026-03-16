# QuantifyPro – Digital Measurement & Cost Estimation System

QuantifyPro is a web-based application designed for quantity surveyors to perform digital measurements from drawings and generate cost estimates. The system supports role‑based access (Admin and Client), project templates, measurement rules, and cost libraries.

---

## Features

- **User Authentication** – Secure registration and login with Flask‑Login.
- **Role‑Based Dashboards**
  - **Admin** – Manage users, project templates, measurement rules, and cost libraries.
  - **Client** – Create projects, upload drawings, perform digital takeoffs, and view estimates.
- **Digital Measurement Tools** (planned) – Upload PDF/DXF/images, trace areas/lengths, get real‑time measurements.
- **Cost Estimation** (planned) – Apply cost libraries to measurements and generate detailed reports.
- **API Endpoints** – RESTful endpoints for measurement and estimation (extendable).

---

## Technology Stack

| Component       | Technology                      |
|-----------------|---------------------------------|
| Backend         | Python 3.12 + Flask 2.3.3      |
| Database        | SQLite (development) / PostgreSQL (production) |
| ORM             | Flask‑SQLAlchemy 3.0.5         |
| Authentication  | Flask‑Login 0.6.3               |
| Forms           | Flask‑WTF / WTForms             |
| Frontend        | HTML5, Tailwind CSS, JavaScript |
| Deployment      | (To be decided)                 |

---

sequenceDiagram
    actor Client
    participant Browser
    participant Flask
    participant Database

    Client->>Browser: Uploads drawing
    Browser->>Flask: POST /api/upload (file)
    Flask->>Database: Save file reference
    Flask-->>Browser: Return drawing ID
    Client->>Browser: Performs measurements (e.g., trace area)
    Browser->>Flask: POST /api/measure (drawing ID, coordinates)
    Flask->>Database: Store measurement results
    Flask-->>Browser: Return calculated area/volume
    Client->>Browser: Requests cost estimate
    Browser->>Flask: POST /api/estimate (measurement IDs, cost library)
    Flask->>Database: Retrieve measurements & cost rules
    Flask-->>Browser: Return cost breakdown
