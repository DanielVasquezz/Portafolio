from fastapi import FastAPI, Depends, BackgroundTasks
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

<<<<<<< HEAD
async def send_email_notification(name: str, email: str, message: str):
    try:
        # ✅ Lee las variables AQUÍ — cada vez que se llama la función
        # No al arrancar la app — así siempre tiene los valores actuales
        mail_config = ConnectionConfig(
            MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
            MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
            MAIL_FROM     = os.getenv('MAIL_USERNAME'),
            MAIL_PORT     = 587,
            MAIL_SERVER   = 'smtp.gmail.com',
            MAIL_STARTTLS = True,
            MAIL_SSL_TLS  = False,
        )

=======
mail_config = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM     = os.getenv('MAIL_USERNAME'),
    MAIL_PORT     = 587,
    MAIL_SERVER   = 'smtp.gmail.com',
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS  = False,
)

# Función separada para enviar el email
# Se ejecuta en background — no bloquea la respuesta
async def send_email_notification(name: str, email: str, message: str):
    try:
>>>>>>> 71952af1f2bbcc685e4e18f647eaa703f675f3d0
        html = f"""
        <h2>Nuevo mensaje en tu portafolio 🎉</h2>
        <p><b>Nombre:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Mensaje:</b> {message}</p>
        """
<<<<<<< HEAD

=======
>>>>>>> 71952af1f2bbcc685e4e18f647eaa703f675f3d0
        msg = MessageSchema(
            subject    = f"Portfolio: mensaje de {name}",
            recipients = ['danielvasquezorellana03@gmail.com'],
            body       = html,
            subtype    = 'html'
        )
<<<<<<< HEAD

        fm = FastMail(mail_config)
        await fm.send_message(msg)
        print("✅ Email enviado")

=======
        fm = FastMail(mail_config)
        await fm.send_message(msg)
        print("✅ Email enviado")
>>>>>>> 71952af1f2bbcc685e4e18f647eaa703f675f3d0
    except Exception as e:
        print(f"❌ Error email: {e}")

@app.get('/')
def root():
    return {'message': 'Portfolio API running ✅'}

@app.get('/health')
def health_check():
    return {'status': 'ok'}

<<<<<<< HEAD
@app.get('/debug-env')
def debug_env():
    return {
        'mail_username_exists': bool(os.getenv('MAIL_USERNAME')),
        'mail_password_exists': bool(os.getenv('MAIL_PASSWORD')),
        'mail_username_value':  os.getenv('MAIL_USERNAME'),
    }

=======
# BackgroundTasks permite ejecutar tareas después de responder
>>>>>>> 71952af1f2bbcc685e4e18f647eaa703f675f3d0
@app.post('/contact', response_model=schemas.ContactResponse)
async def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
<<<<<<< HEAD
    # Guardar en DB
=======
    # 1. Guardar en DB
>>>>>>> 71952af1f2bbcc685e4e18f647eaa703f675f3d0
    db_message = models.Message(**contact.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

<<<<<<< HEAD
    # Enviar email en background
=======
    # 2. Enviar email en background si las variables existen
    # add_task agrega la función a una cola de tareas
    # FastAPI la ejecuta DESPUÉS de devolver la respuesta
    # Por eso el usuario no espera — recibe ✅ inmediatamente
>>>>>>> 71952af1f2bbcc685e4e18f647eaa703f675f3d0
    if os.getenv('MAIL_USERNAME') and os.getenv('MAIL_PASSWORD'):
        background_tasks.add_task(
            send_email_notification,
            contact.name,
            contact.email,
            contact.message
        )

    return db_message