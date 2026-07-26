# Audit harness — csakra állítás landing page
#
# Every tool runs via `npx`, so nothing is installed into the project and
# nothing ships to production. The site itself has zero dependencies.
#
# Usage:
#   make serve                                        # local server on :8080
#   make validate                                     # W3C-style HTML lint (all pages)
#   make validate FILE=variants/a-eteri-feny/index.html
#   make a11y PATH_=/variants/a-eteri-feny/index.html # axe-core (needs `make serve`)
#   make lighthouse                                   # mobile + desktop reports
#   make lighthouse URL=https://example.hu            # audit production
#   make claims-check                                 # scan copy for medical claims
#   make variants                                     # open all three side by side

PORT  ?= 8080
HOST  ?= http://localhost:$(PORT)
PATH_ ?= /index.html
URL   ?= $(HOST)$(PATH_)
FILE  ?= $(shell find . -name '*.html' -not -path './node_modules/*' -not -path './reports/*')

VARIANTS := a-eteri-feny b-ejszakai-kozmosz c-organikus-editorial

.PHONY: help serve validate a11y lighthouse claims-check variants audit clean

help:
	@grep -E '^#   ' $(MAKEFILE_LIST) | sed 's/^#   //'

serve:
	@echo "→ $(HOST)"
	@python3 -m http.server $(PORT)

validate:
	@npx --yes html-validate@8 $(FILE)

a11y:
	@npx --yes @axe-core/cli@4 $(URL) --exit

# Both form factors: a page can score 100 on desktop and fail on mobile.
lighthouse:
	@mkdir -p reports
	@npx --yes lighthouse@12 $(URL) \
		--preset=desktop \
		--output=html --output=json \
		--output-path=./reports/desktop.html \
		--chrome-flags="--headless" \
		--quiet
	@npx --yes lighthouse@12 $(URL) \
		--form-factor=mobile --screenEmulation.mobile \
		--output=html --output=json \
		--output-path=./reports/mobile.html \
		--chrome-flags="--headless" \
		--quiet
	@echo "→ reports/desktop.html  reports/mobile.html"

# Curative language is a legal risk for a non-medical wellbeing service.
# The disclaimer legitimately contains these words ("nem helyettesíti az orvosi
# kezelést"), so lines containing a negation are excluded from the scan.
# Sentence-aware, because HTML wraps prose across lines and a line-based grep
# separates a claim word from its qualifier. See tools/claims-check.py.
claims-check:
	@python3 tools/claims-check.py

variants:
	@for v in $(VARIANTS); do open "$(HOST)/variants/$$v/index.html"; done

audit: validate claims-check
	@echo "✓ Static checks passed. Run 'make serve' then 'make a11y' and 'make lighthouse'."

clean:
	@rm -rf reports
