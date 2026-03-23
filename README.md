# STONSET - Institutional Resource Management System

A comprehensive platform for managing classroom, laboratory, and facility reservations in educational institutions. STONSET eliminates scheduling conflicts, maximizes resource utilization, and provides real-time visibility across your entire facility ecosystem.

## Overview

STONSET is a full-stack web application built with modern technologies designed for universities and educational institutions. It provides an intuitive interface for booking facilities, managing reservations, and gaining actionable insights into resource utilization patterns.

## Tech Stack

**Frontend:**
- React 18 with TypeScript
- Vite 5 (build tool)
- TailwindCSS (styling)
- React Router v6 (routing)
- Zustand (state management)
- Axios (HTTP client)

**Backend:**
- Python FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (database)
- Alembic (migrations)
- JWT (authentication)

**Deployment:**
- Docker-ready architecture
- Environment-based configuration

## Project Structure

```
bdProject/
├── frontend/                  # React TypeScript application
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   ├── pages/             # Page components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API service integrations
│   │   ├── store/             # Zustand state management
│   │   ├── types/             # TypeScript interfaces
│   │   ├── utils/             # Utility functions
│   │   └── style.css          # Global styles
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── backend/                   # FastAPI Python application
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── repositories/       # Data access layer
│   │   ├── services/          # Business logic
│   │   ├── api/               # API endpoints
│   │   ├── db/                # Database config
│   │   ├── core/              # Configuration & security
│   │   └── main.py            # Application entry
│   ├── alembic/               # Database migrations
│   ├── requirements.txt
│   └── start_backend.sh       # Backend startup script
│
└── setup.sql                  # Database initialization

```

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 12+

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`

### Database
```bash
psql -U postgres -d bd_project -f setup.sql
```

## Key Features

- **Smart Reservations**: Intuitive booking system with conflict prevention
- **Real-Time Status**: Live tracking of reservation approvals and updates
- **Role-Based Access**: Distinct interfaces for teachers, administrators, and managers
- **Comprehensive Reports**: Facility utilization analytics and insights
- **Multi-Department Support**: Organize facilities by departments and categories
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Secure Authentication**: JWT-based with automatic token refresh

## API Documentation

Interactive API docs available at `http://localhost:8000/docs` (Swagger UI)

## Contact

- Email: mousaabelharmali31@gmail.com
- Phone: +212 657 288 139

## License

© 2026 STONSET. All rights reserved.
