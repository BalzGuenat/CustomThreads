# Web Generator

This folder contains the GitHub Pages web app for generating Fusion 360 thread XML directly in the browser.

Live site: [https://eckphi.github.io/CustomThreads/](https://eckphi.github.io/CustomThreads/)

## Files

- `index.html`: UI layout and form inputs
- `style.css`: App styling and responsive layout
- `js/calculator.js`: Ported thread calculation logic from Python
- `js/xml.js`: XML assembly and file download helpers
- `js/app.js`: Form wiring, validation, preview, and download actions

Phase 2 UX includes shareable URLs for prefilled configurations.

## Local Run

Because the app uses ES modules, serve it through a local web server instead of opening `index.html` directly.

Example with Python:

```bash
cd web
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Deploy

Deployment is handled by `.github/workflows/deploy-pages.yml`.

- Trigger: push to `master` when files in `web/` change
- Output: published GitHub Pages site from this folder

## Behavior Parity

The browser generator mirrors Python logic from:

- `src/customthreads/generator.py`
- `src/customthreads/models.py`

It preserves:

- Pitch range generation with floating-point guard
- Designation format: `M{size}x{pitch}`
- Tolerance class labels: `O.x`
- Metric geometry formulas for major/pitch/minor diameters
- XML node structure compatible with Fusion 360 thread files
