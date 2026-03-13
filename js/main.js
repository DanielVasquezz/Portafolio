import { postContact } from "./api.js";

document.addEventListener('DOMContentLoaded', () => {

  // ── 1. NAVBAR SCROLL ──────────────────────────────
  const navbar = document.querySelector('#navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  });

  // ── 2. MENÚ HAMBURGUESA ───────────────────────────
  const toggle   = document.querySelector('.nav-toggle');
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

  // ── 3. SCROLL REVEAL ──────────────────────────────
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // ── 4. FORMULARIO ─────────────────────────────────
  const form       = document.querySelector('#contact-form'); // ← corregido
  const responseEl = document.querySelector('#form-response');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const name    = document.querySelector('#name').value.trim();
      const email   = document.querySelector('#email').value.trim();
      const message = document.querySelector('#message').value.trim();

      if (!name || !email || !message) {
        showResponse('Please fill in all fields.', 'error');
        return;
      }

      const button       = form.querySelector('button');
      button.disabled    = true;
      button.textContent = 'Sending...';

      try {
        await postContact(name, email, message);
        showResponse('✅ Message sent! I\'ll get back to you soon.', 'success');
        form.reset();
      } catch (error) {
        console.error('Error:', error);
        showResponse('❌ Could not connect. Try emailing me directly.', 'error');
      } finally {
        button.disabled    = false;
        button.textContent = 'Send message';
      }
    });
  }

  // ── HELPER — muestra mensaje de respuesta ─────────
  // Esta función la usan el formulario y cualquier otro
  // componente que necesite mostrar feedback al usuario
  function showResponse(message, type) {
    responseEl.textContent   = message;
    responseEl.className     = type;
    responseEl.style.display = 'block';

    // Se oculta solo después de 5 segundos
    setTimeout(() => {
      responseEl.style.display = 'none';
    }, 5000);
  }

});