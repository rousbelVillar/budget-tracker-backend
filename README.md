# 🧠 Budget Tracker Backend

A **RESTful backend service for a personal finance application**, built with Python.  
This service manages transactions and categories, persists data using a relational database, and exposes clean JSON APIs designed to integrate with a the frontend.

---

## 📌 Project Overview

This backend provides the data and business logic for a budget tracking application.  
It handles:

- Financial transactions
- Spending categories
- Database schema evolution
- Query abstraction
- Automated testing of core workflows

The project is structured to demonstrate ** backend engineering skills**, not just CRUD endpoints.

---

## ✨ Highlights

- **Real-world backend domain**: Finance-focused data modeling
- **Database-first design**: Alembic-managed schema migrations
- **Clean separation of concerns**: App entrypoint, domain logic, persistence
- **Tested business logic**: Pytest coverage for transactions and categories
- **Scalable foundation**: PostgreSQL-ready architecture

---

## 🧠 What This Backend Demonstrates

- REST API design with Python
- Relational data modeling (transactions ↔ categories)
- Schema migrations and version control
- Test-driven development using Pytest
- Backend/frontend decoupling via API contracts
- Maintainable project structure for long-term growth

---

## 🛠 Tech Stack

| Category      | Technology                     |
| ------------- | ------------------------------ |
| Language      | Python 3.10+                   |
| Web Framework | Flask-style application layout |
| ORM           | SQLAlchemy                     |
| Migrations    | Alembic                        |
| Testing       | Pytest                         |
| Database      | SQLite (PostgreSQL-ready)      |

---

## 🔌 API Overview

```http
GET /transactions
POST /transactions
GET /categories
POST /categories
```

---

## 🔄 Migrations

```bash
alembic upgrade head
```

---

---

## 👤 Author

**Rousbel Villar**  
GitHub: https://github.com/rousbelVillar  
LinkedIn: https://www.linkedin.com/in/rousbel-villar-2496628b/
