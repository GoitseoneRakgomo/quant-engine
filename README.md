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

## System Architecture

The following diagram shows the high‑level architecture of QuantifyPro:

```mermaid
graph TD
    A[Browser] -->|HTTP Requests| B(Flask App)
    B --> C[Authentication<br/>Flask‑Login]
    B --> D[View Functions]
    B --> E[API Endpoints]
    D --> F[Render Templates]
    F --> G[Tailwind CSS / JS]
    E --> H[(SQLite Database)]
    C --> H
    H --> I[User Table]
    H --> J[Future Tables<br/>(Projects, Measurements, etc.)]