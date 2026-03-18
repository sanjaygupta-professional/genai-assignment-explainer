# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive study guides for a DBA Gen AI course (GGU/upGrad Course 8919). The site is a collection of **self-contained HTML files** — no build system, no framework, no bundler. Each page is a standalone document with inline `<style>` and `<script>` tags (except workbooks, which share `workbook-shared.css`).

Deployed to **Vercel** as static files. Also hosted on GitHub Pages.

## Architecture

| File | Type | Description |
|---|---|---|
| `index.html` | Landing page | Card grid linking to all explainers/workbooks/playgrounds |
| `assignment1.html` | Explainer | Assignment 1 guide — collapsible sections, interactive job selector |
| `group-assignment.html` | Explainer | Group assignment guide — same explainer pattern as assignment1 |
| `assignment1-workbook.html` | Workbook | Step-by-step working notebook (Job #5: DBA Gen AI Professor) |
| `legal-assistant-workbook.html` | Workbook | Step-by-step working notebook (Job #1: Legal Assistant) |
| `rag-infra-playground.html` | Playground | Interactive RAG architecture configurator |
| `workbook-shared.css` | Shared CSS | Common styles for all workbook pages |
| `group-assignment-report.md` | Content | SamarthSchool group assignment written report |
| `create_pitch_deck.py` | Script | Python (3.12) script using `python-pptx` to generate SamarthSchool pitch deck |

### Page Types

**Explainers** (`assignment1.html`, `group-assignment.html`): Single-scroll pages with a fixed header, section nav, collapsible accordion sections, rubric breakdowns, and embedded interactive elements (e.g., job selector in assignment1). CSS is fully inline in `<style>`.

**Workbooks** (`*-workbook.html`): Sidebar + main content layout. Link `workbook-shared.css` for layout/typography. Feature progress bars, section checklists, page budget counters, and `IntersectionObserver`-based active sidebar tracking. The JS is inline at the bottom of each file.

**Playgrounds** (`rag-infra-playground.html`): Tool-style interactive pages with configuration controls and live preview panels. Fully self-contained.

## Design System (DesignArena)

All pages use the same visual language. The CSS custom properties are defined identically across files:

- **Fonts**: Playfair Display (headings), Inter (body) — loaded from Google Fonts
- **Palette**: warm/earthy — cream `#F7F6F5`, teal `#487265`, sage `#A0C3C4`, gold `#D4C68B`, copper `#BC976A`
- **Layout**: `--max-w: 780px` (explainers), `--sidebar-w: 220px` (workbooks), `--header-h: 55px`
- **Style rules**: no box-shadows, `border-radius: 12px` on cards, 1px solid borders, rounded pills for tags

When creating new pages, copy the `:root` CSS variables block from an existing page rather than inventing new colors.

## Adding a New Workbook

1. Copy an existing workbook HTML file as template
2. Keep the `<link rel="stylesheet" href="workbook-shared.css">` — do not inline the shared styles
3. Customize the sidebar nav, hero strip, and section content
4. Update `index.html` to add a card linking to the new workbook
5. The JS at the bottom handles sidebar highlighting, progress bar, and page budget — adjust `PAGE_WEIGHTS` array for the new workbook's sections

## Adding a New Explainer

1. Copy `assignment1.html` or `group-assignment.html` as template — styles are fully inline
2. Keep the DesignArena CSS variables block identical
3. Update `index.html` card grid

## Deployment

Static file hosting — no build step required. Just push to `main`.

- **Vercel**: auto-deploys from GitHub (project ID in `.vercel/project.json`)
- Files are served as-is; any `.html` file at the root is a routable page
