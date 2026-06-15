---
title: SLIM Invoicing System
slug: slim-invoicing
date: 2026-05-27
tags: [Python, VBA, SQLAlchemy, Pydantic, pytest, Excel, Click]
summary: A laboratory invoicing system built across four versions over several years — each iteration a direct response to a concrete limitation in the one before it.
github: https://github.com/Firehawk41/SLIM-Invoicing-Program
featured: true
---

SLIM Invoicing automates a genuinely complex billing workflow — parsing lab testing requests, matching analyses against quoted prices, and outputting a sales order CSV ready for accounting software. What started as a procedural VBA script is now a fully tested Python application with clean domain separation. Four versions, several years, one problem solved properly.

## What it does

This project takes an Excel testing request form and produces an invoice in CSV format, ready for upload into accounting software. It does this in three stages:

**1. Parse** — the TR (testing request) stack reads the xlsx file and stores the domain values. Four separate stacks (analysis, chemical, customer and element) populate those properties from the database.

**2. Price** — the SO (sales order) stack populates from the TR stack and calculates the price via the Pricing Engine. Pricing is complicated by having to price per analysis per turnaround time, and by whether discounted bundles of analyses exist in the quote database.

**3. Write** — the writer, part of the SO stack, outputs to CSV. The writer is independent of the domain objects — adding a different output format means adding a different writer, nothing else.

## The progression

Four versions are included in the repository. Each one exists because the previous version hit a wall.

**V1 — Procedural**
The starting point: data stored in arrays, logic in loops. Built just after discovering Codecademy and Stack Overflow. It worked, but debugging was painful and adding features meant touching everything.

**V2 — OOP**
Refactored from the ground up after being asked to add monthly summary invoices for a specific customer. I knew I'd outgrown the previous code. Consulting with ChatGPT on the design, I introduced class modules with interfaces so that each invoice type — individual, weekly summary, monthly summary — could share the same codebase without duplication.

**V3 — Separation of concerns**
Triggered by a request to switch output from Word to CSV. I expected a quick fix — just swap the writer. Instead I found the domain objects were coupled tightly to the output format. Changing what went into the CSV meant digging deeper and deeper into the code. After an extensive audit I redesigned the system from scratch around a clean pipeline with independent stacks. From the start of this refactor, V4 was already in mind.

**V4 — Python port**
The logical endpoint. VBA was always a constraint of the lab environment, not a choice. Python is faster, safer, and properly testable with pytest. Because V3 was designed with the port in mind, executing V4 was a matter of converting the architecture notes to a CLAUDE.md spec and feeding the stacks to Claude Code one by one. It converted the VBA logic to Python and validated the full pipeline end-to-end in two days — 355 tests passing.

## Architecture

The composition root — where every dependency is constructed once and wired explicitly:

```python
def create_app(session: Session, default_payment_terms: int = _DEFAULT_PAYMENT_TERMS) -> App:
    """Wire all services and return a ready-to-use App."""
    element_svc  = ElementService(session)
    analysis_svc = AnalysisService(session)
    chemical_svc = ChemicalService(session)
    customer_svc = CustomerService(session)
    so_svc       = SalesOrderService(session)
    quote_repo   = QuoteRepository(session)
    quote_cache  = QuoteCache(quote_repo)
    quote_svc    = QuoteService(quote_repo, quote_cache)
    quote_cache.build()
    resolver       = TRFormInputResolver(customer_svc, chemical_svc)
    tr_svc         = TRSubmissionService(session, chemical_svc, analysis_svc, element_svc, resolver)
    pricing_engine = SalesOrderPricingEngine(quote_svc, default_payment_terms)
    li_builder     = SalesOrderLineItemBuilder(pricing_engine, analysis_svc)
    builder        = SalesOrderBuilder(li_builder, customer_svc, so_svc)
    loader         = SubmissionLoader(tr_svc)
    return App(loader=loader, builder=builder)
```

Nothing in the application self-constructs. This is what made 355 tests possible.

## What I learned

The design phase is more important than the code writing phase. Careful design saves many hours of refactor later.
