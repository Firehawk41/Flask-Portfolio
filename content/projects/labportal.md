---
title: LabPortal — Lab Testing Request Portal
slug: labportal
date: 2025-06-01
tags: [Python, Flask, PostgreSQL, SQLAlchemy, Docker]
summary: A Flask web application for an ISO 17025 accredited analytical chemistry lab — customers submit multi-section testing requests, lab staff manage submissions through an admin dashboard.
github: https://github.com/Firehawk41/LabPortal
featured: true
---

## The problem

The lab's testing request workflow was entirely email-based. Customers would send in requests with company details, sample descriptions, and analysis selections scattered across free-form emails and attachments. Staff had to parse each one manually, reconcile the information by hand, and follow up when anything was missing. There was no status tracking, no audit trail, and no consistent structure — just institutional memory and inbox search.

## What I built

LabPortal replaces the email workflow with a structured web application. Customers log in and complete a guided multi-section form: company information, payment terms, email distribution lists, and one or more samples with individual analysis selections. On submission, the request is stored and immediately visible to lab staff through an admin dashboard.

The admin side lets staff update submission status (received → in progress → complete), view the full detail of each request, manage customer accounts, and submit requests directly on behalf of a customer when needed. There is no public self-registration — admins create all customer accounts, which matches how an accredited lab controls access to its services. Every admin action that creates or updates a submission writes an `AuditLog` entry recording who acted and on whose behalf.

## Key decisions

- **Application factory + Blueprints** — `create_app()` in `__init__.py` wires up extensions and registers three blueprints (`auth`, `main`, `admin`), keeping each concern isolated and the app testable without a running server
- **Repository pattern** — `SubmissionRepository` is the only place that touches the ORM for submissions; routes call the repository with pure domain objects and never import SQLAlchemy models directly, so the persistence layer can change without touching business logic
- **Pure domain dataclasses** — `domain.py` holds `Sample` and `TestingRequest` as plain Python dataclasses with no Flask or SQLAlchemy imports; `schemas.py` (marshmallow) validates and deserializes incoming JSON into these objects before any database work begins
- **CSP-safe profile injection** — server-side profile data (company name, saved email lists) is injected via a `data-profile` attribute on the form element rather than an inline `<script>` tag, keeping the app compatible with a strict `Content-Security-Policy: no 'unsafe-inline'` header on every response

## What I learned

Enforcing a hard boundary between domain logic and Flask made the architecture more explicit than it needed to be for a project this size — but it surfaced every implicit assumption about where state lives. When a route can only call a repository method and receive a dataclass back, it becomes obvious immediately when business logic has leaked into the wrong layer. The CSP constraint had a similar clarifying effect: it forced every dynamic value to be declared as data rather than code, which turned out to be a useful discipline regardless of the security benefit.
