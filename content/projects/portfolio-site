---
title: This Portfolio Site
slug: portfolio-site
date: 2026-05-28
tags: [Python, Flask, Jinja2, CSS, Render, Claude]
summary: A Flask portfolio and blog site — designed, specified, and deployed using an AI-assisted workflow. The site is both the deliverable and an honest account of how I work.
github: https://github.com/jamiethomson/portfolio
featured: true
---

This site is both a container for my portfolio and an entry in it.

## Stack decisions

**Flask over a static site generator.** The key reason to use Flask is that it's extendable — the same deployment that hosts this site can host live Python tools as separate Render services when I'm ready.

**Markdown flat files over a database.** For a portfolio with low content volume and no user interaction, SQLite adds complexity with no benefit. Each project and post is a `.md` file with YAML front matter. Adding content means creating a file and pushing to GitHub, then Render redeploys automatically.

**Render over AWS.** I've deployed on AWS before and while it worked, it was overly complicated for small projects and has time limits on free tiers. Render deploys directly from GitHub, the free tier is sufficient for portfolio traffic, and the configuration lives in a `render.yaml` in the repo.

## Design process

I used the Museo Ferrari in Maranello, Italy as inspiration for the design: deep charcoal with Racing Red as the accent colour.

Constraint is a design tool. With one accent color and a near-black base, every red element carries weight.

## The AI-assisted workflow

The workflow looked like this:

1. **Conversational design session in Claude.ai** — architecture decisions, page structure, design system, iterating through mockups until the visual language was right
2. **Spec document** — the design session produced a `CLAUDE.md` file: a detailed technical specification covering directory structure, routes, design tokens, content format, and seed content
3. **Scaffold execution in Claude Code** — Claude Code read the spec and generated the full project: Flask app, Jinja2 templates, CSS, Markdown content, deployment config
4. **Review and deploy** — verified all routes, confirmed the design was on spec, pushed to GitHub, deployed to Render

I was responsible for every architectural decision, the design direction, the spec writing, and the judgment calls at each stage. Claude was responsible for executing a well-defined spec, saving me the tedium of boilerplate.

I've learned that prompting design and code is a skill in its own right — the old adage of rubbish in, rubbish out still applies, it's just the input that changed.
