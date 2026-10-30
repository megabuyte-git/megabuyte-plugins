---
name: megabuyte-target-screen
description: Shortlist UK tech acquisition targets or investment candidates from the Megabuyte MCP. Use for bolt-on, add-on or buy-and-build targets for a buyer ("we're a £60m MSP looking for cyber bolt-ons"), screens or longlists on size, growth, margin, sector, region or ownership, and PE-backed companies due an exit. Prefer megabuyte-market-map for mapping a sector and megabuyte-buyer-universe for who would buy, when installed.
---

# Megabuyte target screen

Produces a ranked, sourced longlist of UK tech companies that meet the user's criteria, for a named or described buyer where there is one.

**Read `references/conventions.md` first.** It sets the data boundary, figure, citation, gap and fetching rules every answer must follow. 

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

4. **Screen by all four routes** (conventions §11). Every route is required.
   - **a. Taxonomy and keywords, in parallel.**
     - *Taxonomy:* `search_companies` over the resolved leaves with every criterion, `collapse_to_group: true`, `exclude_closed_profiles: true`, `sort_by` revenue (or what the user ranks on), and `fields` for revenue, financial_year, ebitda_margin_pct, revenue_growth_pct, organic_growth_pct, ownership, investors and postcode. **Leave growth bands out of the call**, and apply growth thresholds yourself to the returned annualised figures (conventions §3). If 100 or fewer match, review all of them.
     - *Keywords:* first `guided_keywords: true` over the leaves to read the capability vocabulary. Then `search_companies` with the same size and ownership criteria, `keywords` set to the 3–6 strongest capability terms (e.g. "managed SOC", "penetration testing", "cyber essentials"), **no taxonomy filter** and **no `plan_id`** (conventions §2). This catches MSPs, integrators and consultancies filed under IT Managed Services or IT Consulting that have a real practice in the capability.
   - **b. Similar companies,** seeded on the 2–3 strongest companies from step a and, for buy-and-build, on 1–2 of the buyer's past targets. Use `find_similar_companies` for each seed, and `search_companies` with `similar_to`, the same size and ownership criteria, and no `plan_id`. Filter to the criteria.
   - **c. Analyst commentary:** `semantic_search` phrased to surface company names, e.g. "owner-managed cyber security consultancies acquired by MSPs" or "cyber businesses analysts flag as targets", across news, reports and Company Analysis. Add a company only if it meets the criteria (check with `search_companies` and `company_ids`).
   - **d. Merge** by group, with a "Found via" note per company. Companies found by several routes rank higher on fit. Quote `total_matched` per route.

5. **Availability check.** One `get_deals` call over the shortlist's ids with `role: "target"` and `announced_from` 5 years back. Flag any company bought or backed in that window, with the deal date and buyer.

6. **Rank and comment.**
   - Order the list by fit to the stated criteria.
   - Add a one-line rationale per company, built only from returned fields (segment, size, growth, margin, ownership). The "fit" judgement is yours, so say so.
   - Never claim capability depth, partner status or customer base; keywords are the company's self-description.

7. **Check** with `check_answer`, then answer.

## Output structure

**Provenance labels** (conventions §4): Company figures and deal flags are **Megabuyte data**; rank, rationale and fit are **AI analysis**.

1. **Headline**: N of M matched, what the screen applied, and the buyer exclusions. Directly under it, the **Routes run** line (conventions §11).
2. **Shortlist table**: rank, company (trading name, linked to its Megabuyte profile), segment, town or city, revenue (£m, FY), revenue growth, organic growth, EBITDA (£m) and margin (adjusted where Megabuyte covers the company, otherwise as filed), ownership and owners, found via, recent deal flag, rationale. Use "—" for not held.
3. **Not applied**: each criterion that couldn't be screened, with the nearest proxy used, if any.
4. **Coverage notes**: e.g. "EBITDA is held for about 10% of companies, so a margin screen searches only those".
5. **Sources.**

## Watch-outs

- Name companies by trading name (`short_name`), not the filed bidco or holding entity.
- Growth bands drop companies whose growth the server withholds for a non-12-month period, though Megabuyte's growth is annualised; filter growth yourself (step 4).
- A margin or EBITDA band silently drops every company without the figure. When a margin screen leaves few results, rerun without it, show both counts, and mark which companies lacked the figure.
- EBITDA and margin follow conventions §3 (adjusted where Megabuyte covers the company). Pass `exclude_closed_profiles: true` so acquired or closed companies aren't offered as targets.
- Never present `investors` as the current owner; use the ownership label and dated deals.
