# Portfolio Site — Claude Code Scaffold Spec

## Project overview

Build a personal portfolio and blog site for **Jamie Thomson** using Flask and Jinja2.
The site is portfolio-first: projects are the hero, blog is secondary.
Content is stored as Markdown flat files with YAML front matter — no database.
Target deployment: Render (deploy from GitHub, push-to-deploy).

---

## Design system

Dark mode only. Maranello/car museum aesthetic — deep near-black background, red as the sole accent color. White is used sparingly as primary text only.

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#0E0E0C` | Page background |
| `--bg-nav` | `#111110` | Nav and footer |
| `--bg-card` | `#181816` | Card surfaces |
| `--border` | `#222220` | All borders and dividers |
| `--text-primary` | `#E8E7E3` | Headings, titles, body |
| `--text-secondary` | `#4A4A47` | Descriptions, dates, muted text |
| `--red` | `#CC0000` | Accent: logo, section labels, card left border, CTA button, red rule, active nav |
| `--radius` | `10px` | Card border radius |

Font: system font stack — `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

Red is used as accent only — never as a background fill except the primary CTA button.
Red touches: nav logo mark, section labels, left card border stripe (3px), horizontal rule under hero name, active nav link underline, primary button background.

---

## Directory structure

```
portfolio/
├── app.py
├── requirements.txt
├── render.yaml
├── .gitignore
├── CLAUDE.md
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── projects.html
│   ├── project.html
│   ├── blog.html
│   ├── post.html
│   └── about.html
└── content/
    ├── projects/
    │   ├── labplus.md
    │   └── flask-demo.md
    └── posts/
        └── .gitkeep
```

---

## Content format

### Project front matter
```yaml
---
title: LabPlus Invoice System
slug: labplus
date: 2025-01-15
tags: [Python, VBA, Excel, Access]
summary: Lab billing automation ported from VBA to Python.
github: https://github.com/jamiethomson/labplus
featured: true
---
```

### Post front matter
```yaml
---
title: Porting 48 VBA modules to Python — what I learned
slug: vba-to-python
date: 2025-05-01
summary: What the rewrite taught me about architecture, testing, and knowing when to stop.
---
```

Body content below the `---` is standard Markdown. Code blocks use triple backticks with a language identifier.

---

## Routes

| Route | Template | Description |
|---|---|---|
| `/` | `index.html` | Hero + featured projects (featured: true) + 3 most recent posts |
| `/projects` | `projects.html` | All projects, sorted by date descending |
| `/projects/<slug>` | `project.html` | Single project detail |
| `/blog` | `blog.html` | All posts, sorted by date descending |
| `/blog/<slug>` | `post.html` | Single post |
| `/about` | `about.html` | Static about page |

---

## app.py requirements

- Use `python-frontmatter` to parse Markdown files with YAML front matter
- Use `markdown` library with `fenced_code` and `codehilite` extensions for rendering body content
- Write a `load_projects()` helper that reads all `.md` files from `content/projects/`, parses front matter, renders body to HTML, returns a list of dicts sorted by date descending
- Write a `load_posts()` helper — same pattern for `content/posts/`
- Write a `get_project(slug)` helper that returns a single project dict by slug
- Write a `get_post(slug)` helper — same for posts
- Return 404 if slug not found
- Pass `author = "Jamie Thomson"` into every template via a context processor

---

## base.html requirements

- `<meta>` tags: charset, viewport, description (use page title + author)
- Page title pattern: `{{ title }} — Jamie Thomson`
- Link to `/static/css/style.css`
- Nav: logo mark `JT` (red, links to `/`), links to Projects, Blog, About
- Active nav link highlighted in red — use `request.path` to determine active state
- Footer: `Jamie Thomson · Carrollton, TX` on the left, GitHub / LinkedIn / Email links on the right
- GitHub, LinkedIn, Email links: use placeholder `#` for now — Jamie will update

---

## style.css requirements

Implement the full design system from the Design System section above. Key rules:

- Page background `#0E0E0C`, nav/footer `#111110`
- Cards: `#181816` background, `0.5px solid #222220` border, `3px solid #CC0000` left border, `10px` border radius
- Section labels: `11px`, `#CC0000`, `letter-spacing: 0.1em`, `text-transform: uppercase`
- `.btn-primary`: `#CC0000` background, white text, `6px` border radius
- `.btn-ghost`: transparent background, `#4A4A47` text, `0.5px solid #222220` border
- `.red-rule`: `36px` wide, `2px` tall, `#CC0000` background (used under hero name)
- Tag pills: `11px`, `#4A4A47` text, `#161614` background, `0.5px solid #222220` border, `4px` border radius
- Code blocks: use Pygments `monokai` or `native` theme (dark-compatible)
- Dividers: `0.5px solid #222220`
- Max content width: `960px`, centered, with `2.5rem` side padding

---

## Seed content

### content/projects/labplus.md
```markdown
---
title: LabPlus Invoice System
slug: labplus
date: 2025-01-15
tags: [Python, VBA, Excel, Access]
summary: Lab billing automation system — originally built in VBA, ported to Python. Reads Excel test request forms, queries an Access database for quoted prices, and outputs a CSV for import into NetSuite.
github: https://github.com/jamiethomson/labplus
featured: true
---

## The problem

PreciLab's billing workflow was entirely manual. Test request forms came in as Excel files, pricing lived in an Access database, and someone had to reconcile them by hand before generating an invoice in NetSuite. It was slow, error-prone, and entirely dependent on institutional knowledge.

## What I built

LabPlus automates the full pipeline. It reads the Excel test request form, resolves customer and sample data, queries the Access database for the correct quoted prices, and outputs a clean CSV ready for NetSuite import.

The original was built in VBA — constrained by the lab environment. The Python port refactored the architecture into four domain layers (Entity → Repository → Cache → Service) across Analysis, Chemical, Customer, and Element domains.

## Key decisions

- **Four-layer domain architecture** keeps business logic separate from I/O
- **Composition root pattern** in `modInvoiceSystem` wires dependencies explicitly
- **Markdown-driven config** for test type mappings — non-developers can update without touching code

## What I learned

Porting 48 VBA modules to Python is less a translation job and more a design job. VBA encourages global state and procedural flow; Python rewards explicit dependency management. The rewrite forced every implicit assumption into the open.
```

### content/projects/flask-demo.md
```markdown
---
title: Flask Demo App
slug: flask-demo
date: 2025-03-01
tags: [Python, Flask, HTML, CSS]
summary: A Flask web application built as a practical introduction to web development — demonstrates routing, Jinja2 templating, and deployment on Render.
github: https://github.com/jamiethomson/flask-demo
featured: true
---

## Overview

Placeholder — Jamie to fill in with the actual Flask app description.

## What it does

Placeholder.

## Stack

- Flask
- Jinja2
- Deployed on Render
```

---

## requirements.txt

```
flask
python-frontmatter
markdown
pygments
gunicorn
```

---

## render.yaml

```yaml
services:
  - type: web
    name: jamie-thomson-portfolio
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

---

## .gitignore

```
__pycache__/
*.pyc
.env
*.db
.DS_Store
venv/
.venv/
```

---

## Instructions for Claude Code

1. Create the full directory structure as specified above
2. Implement `app.py` with all helpers and routes
3. Implement `base.html` with nav, footer, and CSS link
4. Implement all page templates — index, projects, project detail, blog, post, about
5. Implement `style.css` with the full design system
6. Write both seed project Markdown files exactly as specified
7. Write `requirements.txt`, `render.yaml`, and `.gitignore`
8. After scaffolding, run `pip install -r requirements.txt` and `flask run` to verify the app starts without errors
9. Confirm all six routes resolve without 500 errors
10. Do not add features not specified here — keep it minimal and working

---

*Generated in Claude.ai design session — May 2026*
