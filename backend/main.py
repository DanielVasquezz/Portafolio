from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
import os

# Crea las tablas en la DB al arrancar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Daniel Vasquez Portfolio API',  # ← corregido typo
    version='1.0.0'
)

# CORS — un solo bloque, limpio
origins = [
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    'http://localhost:3000',
    'https://danielvasquezz.github.io',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def root():
    return {'message': 'Portfolio API running ✅'}

@app.get('/health')
def health_check():
    return {'status': 'ok'}

@app.post('/contact', response_model=schemas.ContactResponse)
async def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    db_message = models.Message(**contact.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message