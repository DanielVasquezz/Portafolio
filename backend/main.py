from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig



mail_config = ConnectionConfig(
    MAIL_USERNAME   = os.getenv('MAIL_USERNAME'),  # tu Gmail
    MAIL_PASSWORD   = os.getenv('MAIL_PASSWORD'),  # contraseña de app
    MAIL_FROM       = os.getenv('MAIL_USERNAME'),
    MAIL_PORT       = 587,
    MAIL_SERVER     = 'smtp.gmail.com',
    MAIL_STARTTLS   = True,
    MAIL_SSL_TLS    = False,
)






ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


if ENVIRONMENT == 'production':
    origins = [
        'https://danielvasquezz.github.io',
    ]
else:
    origins = [
        'http://localhost:5500',
        'http://127.0.0.1:5500',
    ]

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    tittle='Daniel Vasquez Portafolio API',
    version='1.0.0'
)

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
    return {'message':'Portafolio API running'}

@app.get('/health')
def health_check():
    return {'status': 'ok'}

@app.post('/contact', response_model=schemas.ContactResponse)
async def create_contact(  # ← agrega async
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    # Guardar en DB como antes
    db_message = models.Message(**contact.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # Enviar email de notificación
    html = f"""
    <h3>Nuevo mensaje en tu portafolio 🎉</h3>
    <p><b>Nombre:</b> {contact.name}</p>
    <p><b>Email:</b> {contact.email}</p>
    <p><b>Mensaje:</b> {contact.message}</p>
    """

    message = MessageSchema(
        subject  = f"Portfolio: mensaje de {contact.name}",
        recipients = ['danielvasquezorellana03@gmail.com'],
        body     = html,
        subtype  = 'html'
    )

    fm = FastMail(mail_config)
    await fm.send_message(message)

    return db_message