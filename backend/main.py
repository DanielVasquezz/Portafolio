from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
import os
import resend

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

async def send_email_notification(name: str, email: str, message: str):
    try:
        resend.api_key = os.getenv('RESEND_API_KEY')

        resend.Emails.send({
            'from': 'Portfolio <onboarding@resend.dev>',
            'to': 'danielvasquezorellana03@gmail.com',
            'subject': f'Portfolio: mensaje de {name}',
            'html': f"""
                <h2>Nuevo mensaje en tu portafolio!</h2>
                <p><b>Nombre:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Mensaje:</b> {message}</p>
            """
        })
        print('✅ Email enviado con Resend')
    except Exception as e:
        print(f'❌ Error Resend: {e}')

@app.get('/')
def root():
    return {'message': 'Portfolio API running'}

@app.get('/health')
def health_check():
    return {'status': 'ok'}

@app.get('/debug-env')
def debug_env():
    return {
        'resend_key_exists': bool(os.getenv('RESEND_API_KEY')),
    }

@app.post('/contact', response_model=schemas.ContactResponse)
async def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    db_message = models.Message(**contact.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    if os.getenv('RESEND_API_KEY'):
        background_tasks.add_task(
            send_email_notification,
            contact.name,
            contact.email,
            contact.message
        )

    return db_message
