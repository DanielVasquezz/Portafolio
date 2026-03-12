import { postContact } from "./api";

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Lógica del Navbar (Corregido el selector 'n#navbar' a '#navbar')
    const navbar = document.querySelector('#navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar?.classList.add('scrolled');
        } else {
            navbar?.classList.remove('scrolled');
        }
    });

    // 2. Menú Hamburguesa
    const toggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (toggle && navLinks) {
        toggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            toggle.classList.toggle('open');
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                toggle.classList.remove('open');
            });
        });
    }

    // 3. Intersection Observer (Animaciones reveal)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // 4. Manejo del Formulario (Aquí es donde va el postContact)
    const form = document.querySelector('#tu-formulario-id'); // Cambia por tu ID real
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Extraer datos de los inputs
            const formData = new FormData(form);
            const name = formData.get('name');
            const email = formData.get('email');
            const message = formData.get('message');

            try {
                await postContact(name, email, message);
                showResponse('✅ Message sent! I\'ll get back to you soon.', 'success');
                form.reset();
            } catch (error) {
                console.error('Error:', error);
                showResponse('❌ Could not connect. Try emailing me directly.', 'error');
            }
        });
    }
});