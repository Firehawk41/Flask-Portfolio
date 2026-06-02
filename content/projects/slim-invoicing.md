---
title: SLIM Invoicing
slug: slim-invoicing
date: 2025-01-15
tags: [Python, VBA, Excel, Access]
summary: Lab billing automation system — originally built in VBA, ported to Python. Reads Excel test request forms, queries an Access database for quoted prices, and outputs a CSV for import into NetSuite.
github: https://github.com/jamiethomson/labplus
featured: true
---

## The problem

PreciLab's billing workflow was entirely manual. Test request forms came in as Excel files, pricing lived in an Access database, and someone had to reconcile them by hand before generating an invoice in NetSuite. It was slow, error-prone, and entirely dependent on institutional knowledge.

## What I built

SLIM Invoicing automates the full pipeline. It reads the Excel test request form, resolves customer and sample data, queries the Access database for the correct quoted prices, and outputs a clean CSV ready for NetSuite import.

The original was built in VBA — constrained by the lab environment. The Python port refactored the architecture into four domain layers (Entity → Repository → Cache → Service) across Analysis, Chemical, Customer, and Element domains.

## Key decisions

- **Four-layer domain architecture** keeps business logic separate from I/O
- **Composition root pattern** in `modInvoiceSystem` wires dependencies explicitly
- **Markdown-driven config** for test type mappings — non-developers can update without touching code

## What I learned

Porting 48 VBA modules to Python is less a translation job and more a design job. VBA encourages global state and procedural flow; Python rewards explicit dependency management. The rewrite forced every implicit assumption into the open.
