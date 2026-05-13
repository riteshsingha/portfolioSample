# Ritesh Singha — Portfolio

Personal portfolio of **Ritesh Singha**, AEM Developer & Adobe Certified Expert (AEM Sites Developer), currently at Epsilon, Bengaluru.

Built as a fast, dependency-free static site with **HTML, CSS, and vanilla JavaScript** — no build step, no jQuery, no frameworks.

---

## Sections

- **Hero** — name, rotating role tagline, primary/secondary CTAs, social links
- **Stats** — career highlights at a glance (years, components, sites, releases, certifications)
- **About** — short bio + "currently" line + résumé (download / view)
- **Experience** — vertical timeline of roles
- **Projects** — case-study cards (AEM components, OAuth 2.0, Lucene search, release pipeline, security hardening, side projects)
- **Skills** — grouped chips (Core / Tooling / Frontend / Currently learning)
- **Certifications** — Adobe Certified Expert badge card
- **Contact** — labeled & validated form (Formspree-ready) + socials

---

## Features

- Light / Dark theme toggle that respects `prefers-color-scheme` and persists to `localStorage`
- Sticky, blurred glass navbar with active-section highlighting (IntersectionObserver)
- Typewriter hero subtitle (rotates through roles)
- Scroll-reveal animations (with `prefers-reduced-motion` respected)
- Mobile slide-in menu (auto-closes on link click and on `Esc`)
- Accessible: skip-to-content link, focus-visible rings, ARIA labels, semantic landmarks, labeled form fields
- SEO-ready: meta description, Open Graph + Twitter cards, JSON-LD `Person` schema, canonical, theme-color
- Inline SVG favicon (no extra request)
- Floating action stack (theme + scroll-to-top) — no overlap

---

## Tech stack

- HTML5 (semantic landmarks: `header`, `main`, `section`, `footer`)
- CSS3 (custom properties / theming, Grid, Flexbox, `clamp()` fluid type)
- Vanilla JavaScript (ES2020+, IntersectionObserver, Fetch)
- Font Awesome 6 (free CDN)
- Google Fonts: Poppins + Ubuntu

---

## File structure

```
career-portfolio/
├── index.html          # All page markup
├── style.css           # Theme tokens + components
├── script.js           # Theme, nav, typewriter, reveal, form, year
├── images/
│   ├── main.jpg        # Hero background
│   ├── dev.jpg         # About portrait
│   └── img1.jpeg
├── resume.pdf
└── README.md
```

---

## Run locally

No build step. Just open `index.html`, or serve from any static server:

```bash
# Python
python -m http.server 8080

# Node
npx serve .
```

Then visit `http://localhost:8080`.

---

## Wiring up the contact form

The form ships in **mailto fallback mode** — submissions open the visitor's email client.

To accept submissions directly:

1. Create a free endpoint at [Formspree](https://formspree.io) or [Web3Forms](https://web3forms.com).
2. Open `script.js` and set the `ENDPOINT` constant:

   ```js
   const ENDPOINT = 'https://formspree.io/f/yourID';
   ```

That's it — the existing validation, success / error states, and accessibility are already wired.

---

## Deploy

Drop the folder into any static host:

- **GitHub Pages** — push to `main`, enable Pages in repo settings.
- **Netlify / Vercel** — drag-and-drop or connect the repo. Zero config.
- **Cloudflare Pages** — connect the repo, build command empty, output dir `/`.

---

## Recommended next optimizations

- Compress `images/main.jpg`, `images/dev.jpg` to **WebP / AVIF** (target ~100 KB each).
- Compress `resume.pdf` to under 300 KB.
- Replace social/résumé URLs in `index.html` (LinkedIn, GitHub) with your real handles.
- Add a real Open Graph image (`og-image.png`, 1200×630) and update the `og:image` meta tag.

---

## Author

**Ritesh Singha**
Adobe Certified Expert — AEM Sites Developer
Bengaluru, India · `hriteshsingha@gmail.com`

[LinkedIn](https://www.linkedin.com/in/riteshsingha) · [GitHub](https://github.com/riteshsingha)

---

## License

Released under the [MIT License](https://opensource.org/licenses/MIT).
