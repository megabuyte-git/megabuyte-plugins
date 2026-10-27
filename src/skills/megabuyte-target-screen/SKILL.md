---
name: megabuyte-target-screen
description: Screen and shortlist UK technology companies as acquisition targets or investment candidates using the Megabuyte MCP. Use this whenever the user wants bolt-on, add-on or buy-and-build targets for a buyer ("we're a £60m MSP looking for cyber bolt-ons", "targets for our platform"), a longlist or screen of companies on criteria (size, growth, margin, sector, region, ownership), or PE-backed companies that look due an exit. Also use when they want the screen exported to Excel. Not for mapping a whole sector's structure (megabuyte-market-map) or for who would buy a company (megabuyte-buyer-universe).
---

# Megabuyte target screen

Produces a ranked, sourced longlist of UK tech companies that meet the user's criteria, for a named or described buyer where there is one.

**Read `references/conventions.md` first.** It sets the data boundary, figure, citation, gap and licence rules every answer must follow. For any file export, also read `references/brand.md` and run `scripts/brand_setup.py`.

## Pick the mode

| User asks | Mode | plan_query intent |
|---|---|---|
| Bolt-ons or targets for a buyer ("we", "our client", a named platform) | **Buy-and-build** | `buy_and_build_screen` |
| Companies matching criteria, no buyer | **Screen** | `company_screen` |
| Backed companies held for N years or near a typical exit | **Exit-ready** | `exit_readiness_screen` |

## Workflow

1. **Plan.** Call `plan_query` with the intent, the question as asked, the buyer in `companies` if named, and the user's sector word in `theme`. Follow the plan's calls and its "MUST state" and "Do NOT" lines (conventions §2). Say what the sector word was read as before giving results.

2. **Criteria.** Map each criterion to a `search_companies` argument: size (`revenue_min`/`_max` in whole pounds, `employees_min`/`_max`), growth and margin bands (percent, 0–100), `ownership`, `postcode_district` for places, and taxonomy or `keywords` for capability.
   - List every criterion as **applied** or **not applied (not held)**, e.g. recurring revenue, "approached by PE", customers served.
   - If a criterion is vague ("profitable"), choose a concrete band, state it ("adjusted EBITDA margin above 0%"), and keep going.
   - If the question is too open to screen ("find me good targets"), ask one short question first.

3. **Buyer exclusions (buy-and-build).** Resolve the buyer, then exclude its own group and its past acquisition targets via `exclude_company_ids`, as the plan sets out. Say how many of each were excluded.

4. **Screen, using every route** (conventions §11). In parallel:
   - **Taxonomy:** `search_companies` with every criterion, `collapse_to_group: true`, `sort_by` revenue (or what the user ranks on), and `fields` for revenue, financial_year, ebitda_margin_pct, revenue_growth_pct, organic_growth_pct, ownership, investors and postcode. **Leave growth bands out of the call**: apply growth thresholds yourself to the returned annualised figures (conventions §3).
   - **Keywords:** the same size and ownership criteria, with `keywords` for the capability ("cyber security", "penetration testing"), across all sectors.
   - **Similar companies:** for "targets like X", or when a buyer's past targets show what it buys, `find_similar_companies` seeded on X or on 1–2 of those past targets, then filter to the criteria.
   - **Analyst commentary:** `semantic_search` for companies the analysts discuss in the buyer's context, e.g. "acquisition targets for MSPs in cyber security", or "owner-managed security consultancies".

   Merge by group with a "Found via" note per company. Page only to the 100-row cap (conventions §10). Quote `total_matched` for the taxonomy route.

5. **Availability check.** One `get_deals` call over the shortlist's ids with `role: "target"` and `announced_from` 5 years back. Flag any company bought or backed in that window, with the deal date and buyer.

6. **Rank and comment.**
   - Order the list by fit to the stated criteria.
   - Add a one-line rationale per company, built only from returned fields (segment, size, growth, margin, ownership). The "fit" judgement is yours, so say so.
   - Never claim capability depth, partner status or customer base; keywords are the company's self-description.

7. **Check** with `check_answer`, then answer.

## Output structure

1. **Headline**: N of M matched, what the screen applied, and the buyer exclusions.
2. **Shortlist table**: rank, company (trading name, linked to its Megabuyte profile), segment, town or city, revenue (£m, FY), revenue growth, organic growth, adjusted EBITDA (£m), adjusted EBITDA margin, ownership and owners, found via, recent deal flag, rationale. Use "—" for not held. Adjusted EBITDA is revenue × margin (conventions §3).
3. **Not applied**: each criterion that couldn't be screened, with the nearest proxy used, if any.
4. **Coverage notes**: e.g. "EBITDA is held for about 10% of companies, so a margin screen searches only those".
5. **Sources.**

Excel exports: the shortlist on one sheet, with every column above including adjusted EBITDA (£m) and the company name as a profile hyperlink. Criteria applied and not applied go on a second sheet.

## Watch-outs

- Name companies by trading name (`short_name`), not the filed bidco or holding entity.
- Growth bands drop companies whose growth the server withholds for a non-12-month period, though Megabuyte's growth is annualised; filter growth yourself (step 4).
- A margin or EBITDA band silently drops every company without the figure. When a margin screen leaves few results, rerun without it, show both counts, and mark which companies lacked the figure.
- Adjusted EBITDA margin is `ebitda_margin_pct` (conventions §3).
- Never present `investors` as the current owner; use the ownership label and dated deals.
