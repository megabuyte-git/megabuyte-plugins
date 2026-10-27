---
name: megabuyte-company-brief
description: Build a sourced company brief on a UK technology company from the Megabuyte MCP — for meeting prep, pitch prep, first looks and "tell me about X" questions. Use this whenever the user names a UK tech company and wants a profile, overview, brief, background, snapshot, one-pager, "who are they", "what do we know about", "prep me for my call/meeting with", or Megabuyte's view of it, even if they don't say "brief". Also use when they ask for the brief as a Word doc, PDF or exportable document.
---

# Megabuyte company brief

Produces a one-company brief from Megabuyte data: what the company does, how it's performing, who owns and runs it, what it has bought or raised, what has changed recently, and what Megabuyte's analysts think.

**Read `references/conventions.md` first.** It sets the data boundary, figure, citation and gap rules every answer must follow. For any file export, also read `references/brand.md` and run `scripts/brand_setup.py`.

## Workflow

1. **Plan.** Call `plan_query` with `intent: "meeting_brief"` (or `company_profile` for a short or single-fact ask), the question as asked, and the company in `companies`. Resolve any candidates with the user first. Then follow the plan's "Start with" calls, made in parallel (see conventions §2).

2. **Typical call set** (the plan usually asks for these):
   - `get_company` once, with `sections: ["overview","financials","ownership","structure","news","people"]`. Add `deals` and `analysis` if the plan doesn't fetch them separately.
   - `get_financials` (`periods: 5`) for the trend. History often carries only revenue and headcount, so don't expect margins per year.
   - `get_analysis` (`analysis_type: "company"`) for Megabuyte's view, read whole.
   - `get_deals` over the company and its group, in one call.
   - `semantic_search` scoped to the company (news and company analysis) for trading, leverage and growth-strategy evidence (strategy, acquisitions, expansion, new markets).
   - `semantic_search` with `report_families: ["PeerGroupQuarterly"]` and the company name inside the question, to find sector quarterlies that mention it. These carry no company tags, so a company scope won't find them. Buy-and-build trackers in these reports often hold leverage and estimated exit-year lines worth quoting.

3. **Read before you write.** Open the 1–3 most material news articles in full with `article_id`. Results and trading pieces, and any article flagged by `may_be_out_of_date`, often hold the latest adjusted EBITDA, debt and management changes.

4. **Check.** Run `check_answer` on the draft. Fix anything it lists, and mark approximate figures or quote the held one.

5. **Answer in chat**, using the structure below. Then, in one line, offer to export it.

## Brief structure

Use these sections in this order, both in chat and in exports. Drop a section only when nothing is held for it, and note the gap in Coverage notes.

1. **Snapshot**: 2–3 sentences covering what it does, where it sits in Megabuyte's taxonomy (sector › peer group › sub-peer group), HQ postcode area, ownership label, latest revenue and headcount with FY and source.
2. **Financial trajectory**: a table of the last 3–5 periods with these rows: revenue, revenue growth, organic growth, gross margin, adjusted EBITDA, adjusted EBITDA margin, headcount. History usually holds only revenue and headcount per year, so the other rows are often filled for the latest year only, with "—" elsewhere. Add one or two sentences on the trend. Flag estimated or non-12-month periods. Use adjusted EBITDA per conventions §3.
3. **Ownership**: the ownership type and primary owners, as set out in conventions §3, in one or two lines. Describe the business as one group; don't list its registered entities.
4. **Growth strategy**: 3–5 sentences, in your own words, on how the company is growing. Cover organic vs acquisitive growth, the M&A pattern from its deal record, target markets, products or services being pushed, geographic expansion, and stated ambitions. Draw on the Company Analysis, recent news (results, M&A and contract wins) and the deal history. Date each source. Where Megabuyte holds little on strategy, say so rather than padding.
5. **Deal history**: a table with date, type, counterparty, role and disclosed value/multiple, newest first. State the total held.
6. **Leadership**: current execs and chair with positions and start dates. Reconcile against news: if a newer article reports a change, lead with it and say the board record hasn't caught up.
7. **Recent developments**: dated headlines with Links, written as one line each on why each matters.
8. **Megabuyte view**: a summary in your own words of the latest Company Analysis, with its date and link. Note anything material that has happened since it was published. If none is held, say "No Megabuyte Company Analysis is held for X." Then list sector quarterlies that mention the company separately, with title and date. These are mentions, not coverage of the company.
   If the user says the brief is going outside their organisation, offer a data-only version without this section (see conventions §10).
9. **Questions to probe** (meeting-prep requests only): 3–5 sharp questions that come out of the data, such as a margin dip, a recent CFO exit, or a stale last deal. Ground every question in a fact above.
10. **Coverage notes**, then **Sources**.

Keep the chat version tight. The full brief should fit on one screen per section. The export can carry the full tables.

## Examples of good phrasing

- "Revenue grew 18% (12% organic) to £42.1m in FY Mar-25 (Megabuyte), the third straight year of double-digit growth. Adjusted EBITDA margin slipped from 21% to 17%."
- "Megabuyte records no deals for Acme since its 2021 secondary buy-out by LDC."
- "Megabuyte doesn't hold ARR or customer numbers. Its analysis notes that recurring revenue is around 70% of sales (Company Analysis, May 2026)."

## Not this skill

- Several companies side by side → `megabuyte-peer-benchmark`.
- Deal multiples or a valuation question → `megabuyte-deal-precedents`.
