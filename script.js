/* ==========================================================================
   Ritesh Singha — Portfolio
   Vanilla JS, no dependencies. Loaded with `defer`.
   ========================================================================== */
(() => {
    'use strict';

    const $  = (sel, root = document) => root.querySelector(sel);
    const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

    /* ────────────────────────────────────────────
       Theme: respects saved preference, then system
       ──────────────────────────────────────────── */
    const themeToggle = $('#themeToggle');
    const themeIcon   = $('#themeIcon');
    const body        = document.body;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    const applyTheme = (theme) => {
        body.classList.remove('light-mode', 'dark-mode');
        body.classList.add(theme);
        if (themeIcon) {
            themeIcon.classList.toggle('fa-moon', theme === 'light-mode');
            themeIcon.classList.toggle('fa-sun',  theme === 'dark-mode');
        }
        if (themeToggle) {
            themeToggle.setAttribute(
                'aria-label',
                theme === 'dark-mode' ? 'Switch to light mode' : 'Switch to dark mode'
            );
        }
    };

    const savedTheme = localStorage.getItem('theme');
    applyTheme(savedTheme || (prefersDark.matches ? 'dark-mode' : 'light-mode'));

    themeToggle?.addEventListener('click', () => {
        const next = body.classList.contains('light-mode') ? 'dark-mode' : 'light-mode';
        applyTheme(next);
        localStorage.setItem('theme', next);
    });

    prefersDark.addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark-mode' : 'light-mode');
        }
    });

    /* ────────────────────────────────────────────
       Sticky navbar + scroll-up button
       ──────────────────────────────────────────── */
    const navbar      = $('.navbar');
    const scrollUpBtn = $('.scroll-up-btn');

    const onScroll = () => {
        const y = window.scrollY;
        navbar?.classList.toggle('sticky', y > 20);
        scrollUpBtn?.classList.toggle('show', y > 500);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    scrollUpBtn?.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    /* ────────────────────────────────────────────
       Mobile menu (toggle, close on link, close on Esc)
       ──────────────────────────────────────────── */
    const menuBtn = $('#menuBtn');
    const navEl   = $('.navbar nav');

    const setMenu = (open) => {
        navEl?.classList.toggle('active', open);
        menuBtn?.setAttribute('aria-expanded', String(open));
        const icon = menuBtn?.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-bars',  !open);
            icon.classList.toggle('fa-xmark', open);
        }
    };

    menuBtn?.addEventListener('click', () => {
        setMenu(!navEl?.classList.contains('active'));
    });

    $$('.navbar .menu a').forEach((a) =>
        a.addEventListener('click', () => setMenu(false))
    );

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navEl?.classList.contains('active')) setMenu(false);
    });

    /* ────────────────────────────────────────────
       Typewriter effect for hero subtitle
       ──────────────────────────────────────────── */
    const typed = $('#typedRole');
    if (typed && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const roles = [
            'AEM Developer',
            'Java Backend Engineer',
            'Adobe Certified Expert',
            'Aspiring AI Engineer'
        ];
        let r = 0, c = 0, deleting = false;

        const tick = () => {
            const word = roles[r];
            typed.textContent = deleting
                ? word.slice(0, --c)
                : word.slice(0, ++c);

            let delay = deleting ? 45 : 90;
            if (!deleting && c === word.length) {
                delay = 1600;
                deleting = true;
            } else if (deleting && c === 0) {
                deleting = false;
                r = (r + 1) % roles.length;
                delay = 250;
            }
            setTimeout(tick, delay);
        };
        setTimeout(tick, 800);
    }

    /* ────────────────────────────────────────────
       Reveal-on-scroll + active nav-link highlighting
       ──────────────────────────────────────────── */
    if ('IntersectionObserver' in window) {
        const revealObs = new IntersectionObserver(
            (entries) => {
                entries.forEach((e) => {
                    if (e.isIntersecting) {
                        e.target.classList.add('visible');
                        revealObs.unobserve(e.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
        );
        $$('.reveal').forEach((el) => revealObs.observe(el));

        const sections = $$('main section[id]');
        const navLinks = $$('.navbar .menu a');
        const linkBy = new Map(
            navLinks.map((a) => [a.getAttribute('href')?.slice(1), a])
        );

        const navObs = new IntersectionObserver(
            (entries) => {
                entries.forEach((e) => {
                    const id = e.target.id;
                    const link = linkBy.get(id);
                    if (!link) return;
                    if (e.isIntersecting) {
                        navLinks.forEach((l) => l.classList.remove('active'));
                        link.classList.add('active');
                    }
                });
            },
            { rootMargin: '-45% 0px -50% 0px', threshold: 0 }
        );
        sections.forEach((s) => navObs.observe(s));
    } else {
        $$('.reveal').forEach((el) => el.classList.add('visible'));
    }

    /* ────────────────────────────────────────────
       Contact form — client-side validation + UX
       POSTs JSON to the FastAPI backend (backend/app/routes/contact.py).
       Override the endpoint at runtime by setting `window.CONTACT_API`.
       ──────────────────────────────────────────── */
    const form   = $('#contactForm');
    const status = $('#formStatus');
    const submitBtn = form?.querySelector('button[type="submit"]');

    const DEFAULT_ENDPOINT = 'http://127.0.0.1:8000/api/contact';
    const ENDPOINT = window.CONTACT_API || DEFAULT_ENDPOINT;

    const setStatus = (text, kind = '') => {
        if (!status) return;
        status.textContent = text;
        status.className = `form-status${kind ? ' ' + kind : ''}`;
    };

    // Required fields only — exclude the honeypot from validation pass.
    const requiredFields = () =>
        $$('input[required], textarea[required]', form);

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!form) return;

        let firstInvalid = null;
        requiredFields().forEach((f) => {
            const ok = f.checkValidity();
            f.classList.toggle('invalid', !ok);
            if (!ok && !firstInvalid) firstInvalid = f;
        });

        if (firstInvalid) {
            setStatus('Please fill in the highlighted fields.', 'error');
            firstInvalid.focus();
            return;
        }

        const payload = {
            name:    $('#cf-name').value.trim(),
            email:   $('#cf-email').value.trim(),
            subject: $('#cf-subject').value.trim(),
            message: $('#cf-message').value.trim(),
            website: $('#cf-website')?.value || ''   // honeypot
        };

        try {
            submitBtn?.setAttribute('disabled', 'true');
            setStatus('Sending…');

            const res = await fetch(ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                const data = await res.json().catch(() => ({}));
                form.reset();
                setStatus(data.message || 'Thanks! Your message has been sent.', 'success');
                return;
            }

            if (res.status === 429) {
                setStatus('Too many requests — please wait a minute and try again.', 'error');
                return;
            }

            if (res.status === 422) {
                setStatus('Please check the form fields and try again.', 'error');
                return;
            }

            const data = await res.json().catch(() => ({}));
            setStatus(data.detail || 'Couldn\u2019t send the message. Please email me directly.', 'error');
        } catch (err) {
            console.error('Contact form error:', err);
            setStatus(
                'Network error \u2014 the backend may be offline. Please email me at hriteshsingha@gmail.com.',
                'error'
            );
        } finally {
            submitBtn?.removeAttribute('disabled');
        }
    });

    /* ────────────────────────────────────────────
       Footer year
       ──────────────────────────────────────────── */
    const yearEl = $('#year');
    if (yearEl) yearEl.textContent = String(new Date().getFullYear());
})();
