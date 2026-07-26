# TODO: Csakra Állítás Landing Page

Full detail, acceptance criteria, and verification steps live in [plan.md](plan.md).

Stack: hand-written HTML + CSS, no deps, no build (one inline script for the mobile menu). Hungarian only. CTA = direct contact links.

---

## Phase 1: Foundation

- [x] **Task 1** — Write the Hungarian copy deck (`content/copy.hu.md`) · S · deps: none
- [x] **Task 2** — Shared baseline CSS (`reset.css`, `a11y.css`) + audit harness (`Makefile`) · S · deps: none

### ✅ Checkpoint: Foundation
- [x] Copy reads well in Hungarian, no medical/curative claims — `make claims-check` clean
- [x] `make validate` / `make claims-check` run clean; `make a11y` / `make lighthouse` wired
- [ ] **Client approves copy** — deferred, see note below

> **Deviation from plan (deliberate):** copy approval was folded into the design gate
> rather than blocking Phase 2. Rationale — two of the three variants get deleted, so
> copy corrections only ever need applying to the winner. Blocking here would have cost
> an extra review round trip for no saving.

---

## Phase 2: Design Exploration — *run 3, 4, 5 in parallel*

- [x] **Task 3** — Variant A "Éteri Fény" — light, lavender gradients, serif display · M · deps: 1, 2
- [x] **Task 4** — Variant B "Éjszakai Kozmosz" — dark aubergine, gold, CSS star-field · M · deps: 1, 2
- [x] **Task 5** — Variant C "Organikus Editorial" — warm neutrals, amethyst accent, magazine grid · M · deps: 1, 2

### 🚦 Checkpoint: Design Selection — **DECISION GATE** ← *we are here*

Verified already:
- [x] No horizontal overflow at 320 / 390 / 768 px (measured `scrollWidth` vs `clientWidth`)
- [x] HTML valid — 0 errors across all three
- [x] Contrast — 25 text/background pairs measured, 0 AA failures (incl. Variant B gold-on-dark at 11.9:1)
- [x] Focus order — skip link first, 29 stops, no positive `tabindex`, every control has an accessible name
- [x] Structure — exactly one `h1`, no heading-level jumps, landmarks labelled

Review chooser added for sharing:
- [x] Neutral grey `index.html` at root linking all three variants, CSS-drawn previews
- [x] `impresszum.html` / `adatkezelesi-tajekoztato.html` stubs so footer links don't 404
- [x] `.nojekyll` for GitHub Pages; every preview page is `noindex, nofollow`

> ⚠️ **Carry into Task 6:** root `index.html` is the chooser right now — reclaim it for the
> winner and drop `noindex` from the promoted page, or the live site won't be indexed.

Still needs a human:
- [ ] Client views all three **on a phone and on desktop**
- [ ] **Client picks one** + names elements to graft in from the others
- [ ] Practitioner herself confirms the direction
- [ ] Copy read-through (folded in from the Phase 1 checkpoint)

> Hard stop. No Phase 3 work before this closes.

---

## Phase 3: Harden the Chosen Direction — *sequential*

- [ ] **Task 6** — Promote winner to root, fold in feedback, delete `variants/` · S · deps: Checkpoint B
- [ ] **Task 7** — Accessibility hardening → axe 0 violations, WCAG 2.2 AA · M · deps: 6
- [ ] **Task 8** — SEO: metadata, JSON-LD, sitemap, robots, OG image, favicons · M · deps: 6
- [ ] **Task 9** — Performance: self-hosted subset woff2, AVIF/WebP, critical CSS, CLS 0 · M · deps: 7, 8

### ✅ Checkpoint: Quality Gates
- [ ] Lighthouse 100 / 100 / 100 / 100 — mobile **and** desktop
- [ ] axe 0 violations; keyboard + screen-reader passes done
- [ ] Rich Results Test 0 errors
- [ ] W3C HTML validator 0 errors
- [ ] Client review before anything is published

---

## Phase 4: Compliance and Ship

- [ ] **Task 10** — Impresszum + Adatkezelési tájékoztató + footer disclaimer · S · deps: 6
- [ ] **Task 11** — Cross-browser/device pass + deploy to static host + audit live URL · S · deps: 9, 10

### ✅ Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Live URL audited green
- [ ] Handover note listing every `{{PLACEHOLDER}}` still to fill
- [ ] Iteration 2 backlog captured (szellemgyógyászat)

---

## Blocked on client input

- [ ] Domain name — needed for Task 8 (canonical) and Task 11 (deploy)
- [ ] Real name + business details — needed for Task 10; placeholders unblock Tasks 1–9
- [ ] Does she travel to the client, host at a fixed address, or both? A street address makes
      her eligible for Google's local pack; `areaServed` alone covers most of the benefit
- [ ] Show prices or "árajánlat kérésre"?
- [ ] Facebook/Instagram links + Messenger handle for the CTA
- [ ] Tone: copy drafted informal ("Te") — switch to formal ("Ön") if she prefers

**Answered:** service area = Hajdúsámson + Debrecen + környéke · szellemgyógyászat = a
qualification in the Rólam section, not its own page
