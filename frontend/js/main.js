document.addEventListener('DOMContentLoaded', () => {
  
    const navbar = document.querySelector('n#navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        //MENU HAMBURGUESA
        const toggle = document.querySelector('.nav-toggle');
        const navLinks = document.querySelector('.nav-links');

        if (toggle) {

            toggle.addEventListener('click', function() {
                navLinks.classList.toggle('open');
                toggle.classList.toggle('open');
            });

            const links = document.querySelectorAll('.nav-links a');
            links.forEach(function(link) {
                link.addEventListener('click', function() {
                    navLinks.classList.remove('open');
                    toggle.classList.remove('open');
                });
            });
            

            const observer = new IntersectionObserver(
                
                function(entries) {
                    entries.forEach(function(entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');

                            observer.unobserve(entry.target);
                        }
                    });
                }, 
                
                {
                    threshold: 0.1,
                    rootMargin: "0px"
                }
                );

                const revealElements = document.querySelectorAll('.reveal');
                revealElements.forEach(function(el) {
                    observer.observe(el);
                });
        }
    })

})