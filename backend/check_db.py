# check_db.py — solo para verificar, después lo borras
from database import SessionLocal
from models import Message

db = SessionLocal()
messages = db.query(Message).all()

for msg in messages:
    print(f"ID: {msg.id} | {msg.name} | {msg.email}")
    print(f"Mensaje: {msg.message}")
    print(f"Fecha: {msg.created_at}")
    print("---")

db.close()