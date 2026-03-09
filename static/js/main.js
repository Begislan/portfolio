// Custom Preloader Logic
document.addEventListener('DOMContentLoaded', () => {
    const preloader = document.getElementById('premium-preloader');
    if (preloader) {
        setTimeout(() => {
            preloader.classList.add('hidden');
        }, 1500);
    }

    // Navbar Scroll Effect
    const navbar = document.querySelector('.navbar-floating');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar?.classList.add('scrolled');
        } else {
            navbar?.classList.remove('scrolled');
        }
    });

    // Magnetic Button Effect
    const magneticBtns = document.querySelectorAll('.btn-primary-custom, .btn-outline-custom, .navbar-brand');
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', function (e) {
            const position = btn.getBoundingClientRect();
            const x = e.pageX - position.left - position.width / 2;
            const y = e.pageY - position.top - position.height / 2;

            btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });

        btn.addEventListener('mouseout', function () {
            btn.style.transform = 'translate(0px, 0px)';
        });
    });

    // Mouse-Reactive Parallax for Neon Background
    document.addEventListener('mousemove', (e) => {
        const background = document.querySelector('.neon-background');
        if (background) {
            const x = (window.innerWidth / 2 - e.pageX) / 50;
            const y = (window.innerHeight / 2 - e.pageY) / 50;
            background.style.transform = `translate(${x}px, ${y}px)`;
        }
    });
});
