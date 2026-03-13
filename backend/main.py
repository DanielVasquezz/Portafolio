from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Daniel Vasquez Portfolio API', version='1.0.0')

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

# Lee las variables de Railway — nunca hardcodees contraseñas
mail_config = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM     = os.getenv('MAIL_USERNAME'),
    MAIL_PORT     = 587,
    MAIL_SERVER   = 'smtp.gmail.com',
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS  = False,
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
    # 1. Guardar en DB
    db_message = models.Message(**contact.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # 2. Enviar email solo si las variables están configuradas
    # El if evita que crashee si las variables no están
    if os.getenv('MAIL_USERNAME') and os.getenv('MAIL_PASSWORD'):
        html = f"""
        <h2>Nuevo mensaje en tu portafolio 🎉</h2>
        <p><b>Nombre:</b> {contact.name}</p>
        <p><b>Email:</b> <a href="mailto:{contact.email}">{contact.email}</a></p>
        <p><b>Mensaje:</b></p>
        <p>{contact.message}</p>
        """

        email = MessageSchema(
            subject    = f"Portfolio: mensaje de {contact.name}",
            recipients = ['danielvasquezorellana03@gmail.com'],
            body       = html,
            subtype    = 'html'
        )

        fm = FastMail(mail_config)
        await fm.send_message(email)

    return db_message