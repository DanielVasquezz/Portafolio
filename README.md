# Daniel Vásquez — Portfolio

Personal portfolio website built with a real backend API.

## 🚀 Tech Stack

**Frontend**
- HTML5, CSS3, JavaScript (ES Modules)
- Responsive design, CSS Grid & Flexbox

**Backend**
- Python + FastAPI
- SQLite + SQLAlchemy ORM
- Pydantic data validation
- REST API with automatic docs

## 📁 Project Structure

portfolio/
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── main.js
│       └── api.js
├── backend/
│   ├── main.py       ← FastAPI app & endpoints
│   ├── database.py   ← DB connection
│   ├── models.py     ← SQLAlchemy models
│   ├── schemas.py    ← Pydantic schemas
│   └── requirements.txt
└── README.md

## ⚙️ Run locally

**Backend**
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

API running at: http://localhost:8000
API docs at:    http://localhost:8000/docs

**Frontend**
Open frontend/index.html with Live Server in VS Code

## 📬 Contact

- Email: danielvasquezorellana03@gmail.com
- GitHub: github.com/DanielVasquezz
- LinkedIn: linkedin.com/in/daniel-vasquez-047a36340