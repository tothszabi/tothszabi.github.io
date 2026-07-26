# Implementation Plan: Csakra Állítás Landing Page

## Overview

A single-page Hungarian marketing site for a spiritual practitioner, focused in this first
iteration on **csakra állítás**. Hand-written static HTML + CSS, zero runtime dependencies,
zero build step. The primary conversion is direct contact (tap-to-call, email, Messenger).

Because the client does not yet have a visual direction in mind, the plan front-loads a
**design exploration phase**: three complete, browsable variants built from identical copy,
so the choice is made on real pages rather than descriptions. Only the chosen variant is then
hardened for accessibility, SEO, and performance — the other two are deleted.

## Decisions (locked with client)

| Decision | Choice | Rationale |
|---|---|---|
| Language | Hungarian only | Audience searches in Hungarian; avoids hreflang/2× content cost |
| Stack | Pure HTML + CSS | No deps, no build, cleanest path to 100/100 Lighthouse |
| Primary CTA | Direct contact links | No backend, no form spam, no GDPR data processing |
| Content | Placeholder copy, written by us | Client has nothing yet; real copy swaps in later |
| Service area | Hajdúsámson, Debrecen + környéke | Local SEO targets East Hungary, not national |
| Szellemgyógyászat | A qualification, not a page | Iteration 1 is csakra állítás only; nav needs no rebuild later |

## Architecture Decisions

- **Identical copy across all three variants.** Content is authored once in
  `content/copy.hu.md` and is the single source of truth. Variants differ *only* visually,
  so the client compares design, not wording.
- **Each variant owns its own HTML and CSS in full.** No shared layout shell between them.
  Sharing a skeleton would make all three structurally similar and collapse the range of
  choice. Two variants get thrown away — duplicated markup is the acceptable cost.
- **Two files *are* shared**, because they encode non-negotiables rather than taste:
  `styles/reset.css` and `styles/a11y.css` (skip link, `:focus-visible`, reduced-motion).
- **Zero third-party network requests in the shipped page.** Self-hosted `woff2` fonts, no
  Google Fonts, no analytics, no embeds. This buys three things at once: top performance,
  no cookie banner (nothing to consent to), and no GDPR data transfer to third parties.
- **CSS architecture: custom properties + cascade layers.** A `tokens.css` per variant holds
  colour/type/space scales; `@layer` keeps specificity flat without a methodology or a
  framework. No preprocessor.
- **Audit tools are dev-only, via `npx`.** Nothing is installed into the project and nothing
  ships, so this does not violate the low-dependency constraint.
- **Placeholders are conspicuous, never plausible.** Client name renders as `{{NÉV}}`,
  photos as labelled grey blocks, testimonials as visibly marked dummies. A placeholder that
  looks real is a placeholder that ships by accident.

## Project Structure

```
magic/
  content/copy.hu.md            # Task 1 — single source of truth for all wording
  styles/reset.css              # Task 2 — shared
  styles/a11y.css               # Task 2 — shared
  variants/
    a-eteri-feny/               # Task 3
    b-ejszakai-kozmosz/         # Task 4
    c-organikus-editorial/      # Task 5
  index.html                    # review chooser now → promoted winner at Task 6
  styles/chooser.css            # review chooser (deleted at Task 6)
  styles/stub.css               # provisional legal pages (deleted at Task 10)
  .nojekyll                     # GitHub Pages: skip Jekyll processing
  styles/  assets/              # Task 6+
  impresszum.html               # stub now → real content at Task 10
  adatkezelesi-tajekoztato.html # stub now → real content at Task 10
  tasks/plan.md  tasks/todo.md
```

### Review chooser (added for the GitHub Pages share)

Root `index.html` is currently a **neutral, grey-only chooser page** listing the three
variants, so the practitioner can review them from one shared URL on her own phone. It is
deliberately untinted — a purple chooser would bias the choice toward A and B. Previews are
CSS-drawn from each variant's real palette rather than screenshots, so they cannot silently
drift out of date.

Two consequences to carry into later tasks:

- **Task 6 must reclaim root `index.html`.** When the winner is promoted, either delete the
  chooser or move it to `valasztas.html`. Do not leave two things competing for `/`.
- **`impresszum.html` / `adatkezelesi-tajekoztato.html` now exist as stubs.** Every variant
  footer links to them, so on a public URL they would otherwise have 404'd. They are clearly
  marked provisional; Task 10 replaces the content and restyles them to the chosen variant.

Every preview page carries `<meta name="robots" content="noindex, nofollow">`. This matters
more than usual: the pages contain placeholder tokens and **fabricated testimonials**, and
must not be indexed under her name.

## Page Sections (same in every variant)

1. **Hero** — name, one-line promise, primary CTA
2. **Mi az a csakra állítás?** — plain-language explanation
3. **Hogyan zajlik?** — 3–4 step process
4. **Kinek ajánlott?** — who it suits
5. **Rólam és képzettségeim** — bio + portrait + qualifications list (this is where
   **szellemgyógyászat** appears, as credential and adjacent offering rather than a
   promoted service — keeps iteration 1 focused while signalling depth)
6. **Vélemények** — testimonials (dummy until real ones exist)
7. **Árak és foglalás** — pricing + contact CTA
8. **GYIK** — FAQ, `<details>`-based; also feeds `FAQPage` structured data
9. **Footer** — contact, legal links, disclaimer

## Dependency Graph

```
Task 1 (copy deck) ──┬─────────────┐
                     │             │
Task 2 (baseline) ───┼──> Task 3 (Variant A) ──┐
                     ├──> Task 4 (Variant B) ──┼──> CHECKPOINT B ──> Task 6 (promote)
                     └──> Task 5 (Variant C) ──┘   (client picks)         │
                                                                          ├──> Task 7 (a11y)
                                                                          ├──> Task 8 (SEO)
                                                                          └──> Task 9 (perf)
                                                                                   │
                                                            Task 10 (legal) ───────┤
                                                                                   └──> Task 11 (ship)
```

Tasks 3–5 are fully parallelizable. Tasks 7–9 touch the same two files and should run
sequentially. Task 10 is independent of 7–9 and can run any time after Task 6.

---

# Phase 1: Foundation

## Task 1: Write the Hungarian copy deck

**Description:** Author every word the site will display, in Hungarian, into
`content/copy.hu.md` — one section per page section, plus meta title/description, image alt
texts, and CTA labels. Copy is warm and calming but makes **no medical or curative claims**:
no "gyógyít", "kezel", "megszünteti a betegséget". Frame as wellbeing, balance, and
relaxation ("harmónia", "belső egyensúly", "ellazulás"). The primary keyword
*"csakra állítás"* appears in the meta title, the H1, and naturally in body copy.

**Acceptance criteria:**
- [ ] All 9 sections have final-length Hungarian copy (not lorem ipsum), plus meta title (≤60 chars) and description (≤155 chars)
- [ ] Zero medical/curative claims; a plain-language disclaimer sentence is drafted for the footer
- [ ] Client name is `{{NÉV}}`, contact details are `{{TELEFON}}` / `{{EMAIL}}` / `{{MESSENGER}}`; testimonials are labelled `[PÉLDA VÉLEMÉNY — cserélni valódira]`

**Verification:**
- [ ] Manual: read aloud in Hungarian — no awkward machine-translation phrasing
- [ ] `make claims-check` returns no hits outside the disclaimer block (the disclaimer itself legitimately says "nem helyettesíti az orvosi kezelést")
- [ ] Every `{{PLACEHOLDER}}` token is listed in a table at the top of the file

**Dependencies:** None
**Files likely touched:** `content/copy.hu.md`
**Estimated scope:** S

---

## Task 2: Shared baseline CSS and audit harness

**Description:** Create the two shared stylesheets and make every later verification step a
one-liner. `reset.css` is a minimal modern reset (box-sizing, margin zeroing, `img`
`max-width`, `text-wrap: balance` on headings). `a11y.css` holds the non-negotiables:
`.skip-link`, a visible `:focus-visible` ring, `@media (prefers-reduced-motion: reduce)`,
and a `.visually-hidden` utility. Add a `Makefile` wrapping the audit commands and an
`.htmlvalidate.json` config.

**Acceptance criteria:**
- [ ] `styles/reset.css` and `styles/a11y.css` exist and contain no colour or font decisions (variants own those)
- [ ] `make serve`, `make validate`, `make a11y`, `make lighthouse` all run successfully
- [ ] `make lighthouse` runs mobile *and* desktop and writes reports to `reports/`

**Verification:**
- [ ] `make validate` exits 0 against a throwaway minimal HTML file
- [ ] `make serve` serves the directory on a local port
- [ ] `reports/` is git-ignored

**Dependencies:** None
**Files likely touched:** `styles/reset.css`, `styles/a11y.css`, `Makefile`, `.htmlvalidate.json`, `.gitignore`
**Estimated scope:** S

---

## ✅ Checkpoint: Foundation

- [ ] Copy deck reads well in Hungarian and is claim-safe
- [ ] Audit harness runs end to end
- [ ] **Client reviews the copy before three variants are built on top of it** — fixing wording once here beats fixing it three times later

---

# Phase 2: Design Exploration (parallelizable)

Three complete, self-contained pages. Same copy, same section order, genuinely different
design languages. Each is independently viewable in a browser. Each must already be
*roughly* accessible and responsive — polish comes in Phase 3, but a variant that only
works at desktop width is not a fair comparison.

**Shared requirements for Tasks 3, 4 and 5:**
- Renders correctly from 320 px to 1920 px, no horizontal scroll
- All copy pulled verbatim from `content/copy.hu.md`
- `<html lang="hu">`, semantic landmarks, one `<h1>`, sequential heading order
- Text contrast ≥ 4.5:1; all motion wrapped in `prefers-reduced-motion`
- System font stack for now (web fonts are chosen in Task 9, for the winner only)
- Image slots are labelled CSS-drawn placeholder blocks with correct aspect ratios — no stock photos

## Task 3: Variant A — "Éteri Fény" (light, luminous, soft)

**Description:** Light and airy. Off-white base, soft lavender and lilac gradients, wide
radial glows behind the hero, generous whitespace. Elegant serif display headings paired
with a clean humanist sans for body. Rounded, gentle shapes; very low-contrast section
transitions. Reads as premium, calming, feminine wellness — closest to her stated liking
for purple.

**Acceptance criteria:**
- [ ] All 9 sections implemented and styled in `variants/a-eteri-feny/`
- [ ] Purple is a *tint and gradient* system, not flat fills — no single-hue wash
- [ ] Passes the shared requirements above

**Verification:**
- [ ] Manual: view at 320 / 768 / 1440 px — layout holds at each
- [ ] `make validate FILE=variants/a-eteri-feny/index.html` exits 0
- [ ] Keyboard-only tab pass reaches every link and CTA

**Dependencies:** Tasks 1, 2
**Files likely touched:** `variants/a-eteri-feny/index.html`, `variants/a-eteri-feny/styles/{tokens,main}.css`
**Estimated scope:** M

---

## Task 4: Variant B — "Éjszakai Kozmosz" (dark, mystical, dramatic)

**Description:** Dark mode by default. Deep aubergine and indigo background, muted gold
accents, faint constellation/star-field texture rendered in pure CSS (no images), frosted
glass panels for cards. High-contrast display type. Reads as mystical and ceremonial —
the strongest differentiation from generic wellness sites.

**Acceptance criteria:**
- [ ] All 9 sections implemented and styled in `variants/b-ejszakai-kozmosz/`
- [ ] Star-field and glow effects are pure CSS — no image assets, no JS
- [ ] Gold-on-dark text hits ≥ 4.5:1 (this is the likely failure point — verify, don't assume)

**Verification:**
- [ ] Manual: view at 320 / 768 / 1440 px
- [ ] Contrast checked on every text/background pair, including gold accents and muted footer text
- [ ] `make validate FILE=variants/b-ejszakai-kozmosz/index.html` exits 0

**Dependencies:** Tasks 1, 2
**Files likely touched:** `variants/b-ejszakai-kozmosz/index.html`, `variants/b-ejszakai-kozmosz/styles/{tokens,main}.css`
**Estimated scope:** M

---

## Task 5: Variant C — "Organikus Editorial" (warm, grounded, modern)

**Description:** Deliberately avoids the spiritual visual cliché. Warm neutral palette —
sand, clay, sage — with amethyst as a single restrained accent. Editorial magazine layout:
oversized type, asymmetric grid, generous rules and hairlines, numbered process steps.
Reads as grounded, credible, and current; the option to show her that purple-first is not
the only route.

**Acceptance criteria:**
- [ ] All 9 sections implemented and styled in `variants/c-organikus-editorial/`
- [ ] Asymmetric grid degrades to a clean single column below 768 px
- [ ] Purple appears as accent only (≤ 10% of visual weight)

**Verification:**
- [ ] Manual: view at 320 / 768 / 1440 px
- [ ] `make validate FILE=variants/c-organikus-editorial/index.html` exits 0
- [ ] Keyboard-only tab pass reaches every link and CTA

**Dependencies:** Tasks 1, 2
**Files likely touched:** `variants/c-organikus-editorial/index.html`, `variants/c-organikus-editorial/styles/{tokens,main}.css`
**Estimated scope:** M

---

## 🚦 Checkpoint: Design Selection — **DECISION GATE**

- [ ] All three variants open in a browser and are responsive
- [ ] Client views all three on **a phone and a desktop** — most of her visitors will be on mobile
- [ ] **Client picks one direction**, and names any elements to graft in from the other two
- [ ] Confirm the picked direction with the practitioner herself before hardening

Nothing in Phase 3 starts before this gate closes. Hardening three variants would triple
the remaining work and two-thirds of it would be discarded.

---

# Phase 3: Harden the Chosen Direction

## Task 6: Promote the winner and fold in feedback

**Description:** Move the chosen variant to the project root as `index.html` +
`styles/`, apply the graft-in requests from the selection checkpoint, and delete
`variants/`. From here there is exactly one page to maintain.

**Acceptance criteria:**
- [ ] `index.html` at root renders identically to the chosen variant, plus requested tweaks
- [ ] `variants/` deleted; no dead CSS from the discarded directions remains
- [ ] All CSS paths still resolve from the new location
- [ ] Review chooser removed or moved to `valasztas.html`; `styles/chooser.css` deleted with it
- [ ] `<meta name="robots" content="noindex">` **removed** from the promoted page — it was
      there to keep the preview out of search results, and shipping it would make the live
      site invisible to Google. Easy to miss; check it explicitly.

**Verification:**
- [ ] `make serve` → root page renders with full styling, no 404s in the network panel
- [ ] `make validate` exits 0

**Dependencies:** Checkpoint B closed
**Files likely touched:** `index.html`, `styles/*`, (deletes `variants/`)
**Estimated scope:** S

---

## Task 7: Accessibility hardening

**Description:** Take the page from "roughly accessible" to demonstrably WCAG 2.2 AA.
Landmark regions, skip link wired up, `aria-current` on active nav, accessible names on
every icon-only control, `<details>` FAQ keyboard behaviour, 44×44 px minimum touch
targets, forced-colors mode sanity, and a real screen-reader pass over the reading order.

**Acceptance criteria:**
- [ ] `make a11y` reports **0 violations**
- [ ] Full keyboard-only pass: visible focus at every stop, logical order, no traps
- [ ] Every text/background pair ≥ 4.5:1 (≥ 3:1 for large text and UI boundaries)

**Verification:**
- [ ] `make a11y` exits 0
- [ ] VoiceOver pass: headings-list navigation describes the page coherently
- [ ] Lighthouse Accessibility = 100

**Dependencies:** Task 6
**Files likely touched:** `index.html`, `styles/a11y.css`, `styles/main.css`
**Estimated scope:** M

---

## Task 8: SEO and structured data

**Description:** Full on-page SEO for Hungarian search. Meta title/description from the copy
deck, canonical URL, Open Graph and Twitter card tags with a purpose-built 1200×630 share
image, and JSON-LD: `HealthAndBeautyBusiness` with `areaServed` covering **Hajdúsámson,
Debrecen and Hajdú-Bihar county**, plus `Person`, `Service` for csakra állítás, and
`FAQPage` mirroring the GYIK section. Add `sitemap.xml`, `robots.txt`, and a favicon set.

**Acceptance criteria:**
- [ ] All JSON-LD blocks pass Google's Rich Results Test with zero errors
- [ ] Meta title ≤ 60 and description ≤ 155 chars, both containing "csakra állítás"
- [ ] "Hajdúsámson" and "Debrecen" appear in the title, description, H1 area, and `areaServed`
- [ ] `sitemap.xml`, `robots.txt`, OG image, and favicons all present and reachable

**Verification:**
- [ ] Rich Results Test: 0 errors, `FAQPage` eligible
- [ ] OG tags preview correctly in a social debugger
- [ ] Lighthouse SEO = 100

**Dependencies:** Task 6
**Files likely touched:** `index.html`, `sitemap.xml`, `robots.txt`, `assets/og-image.jpg`, `assets/favicon/*`
**Estimated scope:** M

---

## Task 9: Performance and font/image pipeline

**Description:** Replace the system font stack with two self-hosted, subset `woff2` faces
(Latin Extended — Hungarian needs `ő` and `ű`), preloaded, `font-display: swap`, with metric
matched fallbacks to kill CLS. Convert images to AVIF + WebP with `<picture>`, explicit
`width`/`height`, `fetchpriority="high"` on the hero and `loading="lazy"` below the fold.
Inline critical CSS in `<head>`, defer the rest. Add long-cache headers config for the host.

**Acceptance criteria:**
- [ ] Lighthouse Performance = 100 on **both** mobile and desktop throttling
- [ ] CLS = 0; LCP element is the hero and is preloaded
- [ ] Zero third-party network requests; total transfer under 300 KB

**Verification:**
- [ ] `make lighthouse` → all four categories 100/100, mobile and desktop
- [ ] Network panel: no external hosts, fonts served as `woff2`
- [ ] WebPageTest filmstrip shows no layout shift or font flash

**Dependencies:** Tasks 7, 8
**Files likely touched:** `index.html`, `styles/main.css`, `assets/fonts/*`, `assets/img/*`, `_headers`
**Estimated scope:** M

---

## ✅ Checkpoint: Quality Gates

- [ ] Lighthouse 100 / 100 / 100 / 100 — mobile **and** desktop
- [ ] axe: 0 violations; keyboard and screen-reader passes done
- [ ] Rich Results Test: 0 errors
- [ ] W3C HTML validator: 0 errors
- [ ] Review with client before publishing anything

---

# Phase 4: Compliance and Ship

## Task 10: Legal pages and disclaimer

**Description:** Hungarian law expects a service provider's site to carry an **Impresszum**,
and even with no forms and no analytics an **Adatkezelési tájékoztató** is expected once she
publishes contact channels. Add both as minimal static pages, plus the footer disclaimer
drafted in Task 1 stating the service is not medical treatment and does not replace a
doctor's care. Both pages inherit the site styling and are linked from the footer.

**Acceptance criteria:**
- [ ] `impresszum.html` and `adatkezelesi-tajekoztato.html` replaced with real content (they
      currently exist as clearly-marked provisional stubs), restyled to the chosen variant,
      and `styles/stub.css` deleted
- [ ] Footer disclaimer present on all pages, readable (not fine-print-hidden)
- [ ] Business-identity fields left as `{{...}}` placeholders for her real data

**Verification:**
- [ ] `make validate` exits 0 on both pages
- [ ] `make a11y` clean on both pages
- [ ] **Client confirms her real business details and reviews the disclaimer wording** — we draft, she owns it

**Dependencies:** Task 6
**Files likely touched:** `impresszum.html`, `adatkezelesi-tajekoztato.html`, `index.html`
**Estimated scope:** S

---

## Task 11: Cross-browser pass and deploy

**Description:** Verify on real engines, then publish. Deploy target is any static host —
Cloudflare Pages or Netlify, both free, both give HTTPS and a CDN with no build step.
Point the domain, confirm HTTPS, and re-run the full audit against the live URL.

**Acceptance criteria:**
- [ ] Renders correctly in Safari (macOS + iOS), Chrome, and Firefox
- [ ] Live over HTTPS on the real domain, `www` and apex both resolving
- [ ] Lighthouse re-run **against the production URL** still 100 across the board

**Verification:**
- [ ] Manual pass on a real iPhone and a real Android device
- [ ] `make lighthouse URL=https://<domain>` → 100/100/100/100
- [ ] `curl -I https://<domain>` shows HTTPS and long-cache headers on assets

**Dependencies:** Tasks 9, 10
**Files likely touched:** deploy config, DNS (no source changes expected)
**Estimated scope:** S

---

## ✅ Checkpoint: Complete

- [ ] Every acceptance criterion above met
- [ ] Live site audited green on the production URL
- [ ] Handover note listing every `{{PLACEHOLDER}}` she still needs to fill
- [ ] Iteration 2 backlog captured (szellemgyógyászat and other services)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Client dislikes all three variants | High | Variants are deliberately far apart (light / dark / warm-neutral). If none land, her feedback narrows direction 4 cheaply — copy and baseline are already done and reusable |
| Fabricated testimonials ship as real | High | Placeholders are conspicuously labelled `[PÉLDA VÉLEMÉNY]`; Task 11 handover explicitly gates on replacing them |
| Health claims create legal exposure | High | Task 1 bans curative language and greps for it; Task 10 adds the disclaimer; she reviews and owns the final wording |
| Real photos arrive heavy and unoptimized | Medium | Task 9 owns the AVIF/WebP pipeline; placeholder slots already carry the correct aspect ratios so swapping in causes no reflow |
| Perfect 100s slip once real content lands | Medium | Re-run `make lighthouse` after content swap; the pipeline, not the current assets, is what holds the score |
| Gold-on-dark in Variant B fails contrast | Low | Called out in Task 4's criteria as the expected failure point — verified rather than assumed |
| "100% on all tools" reads as a guarantee | Low | Lighthouse 100/100/100/100 is achievable and planned. PageSpeed Insights *field* data (Core Web Vitals) depends on real visitor traffic and cannot be forced pre-launch — set expectations at Checkpoint C |

## Parallelization

- **Safe to parallelize:** Tasks 3, 4, 5 (independent directories, no shared files). Task 10 alongside Tasks 7–9.
- **Must be sequential:** Tasks 7 → 8 → 9 (all edit `index.html` and `styles/main.css`).
- **Gate:** Checkpoint B is a hard stop; no Phase 3 work begins before a direction is chosen.

## Open Questions

1. **Domain** — is one registered? Task 8's canonical URL and Task 11's deploy both need it.
2. **Her real name and business details** — needed for Impresszum, JSON-LD, and page titles. Placeholders unblock everything up to Task 10.
3. ~~Service area~~ — **answered:** Hajdúsámson, Debrecen and the surrounding area (East
   Hungary). Still open: does she **travel to the client, host at a fixed address, or both?**
   `HealthAndBeautyBusiness` needs a street address to be eligible for a local pack;
   `areaServed` alone gets us most of the way if she prefers not to publish one.
4. **Pricing** — show prices, or "árajánlat kérésre"? Affects the Árak section layout.
5. **Existing social presence** — a Facebook/Instagram page to link and to source the Messenger CTA from?
6. ~~Iteration 2 scope~~ — **answered:** szellemgyógyászat stays a qualification inside the
   Rólam section for now. Nav is built flat so a second service page can be added later
   without restructuring.
7. **Tone** — copy is drafted in informal "Te" (warmer, standard in Hungarian wellness).
   Flip to "Ön" if she prefers formal; it is a mechanical find-and-replace on the winner.
