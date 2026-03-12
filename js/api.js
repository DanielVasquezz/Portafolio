const API_URL = "http://localhost:8000";

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