const API_URL = location.hostname === 'localhost' || 
location.hostname === '127.0.0.1' ? 'http://localhost:8000' : 'https://portafolio-production-93f7.up.railway.app';

export async function postContact(name, email, message){

    const res = await fetch(`${API_URL}/contact`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name,
            email,
            message
        })
    });
    if(!res.ok){
        throw new Error("Error al enviar el mensaje");
    }

    return await res.json();
}       