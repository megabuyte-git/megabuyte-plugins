---
name: megabuyte-company-brief
description: Sourced brief on a UK tech company from the Megabuyte MCP. Use when the user names a UK tech company and wants a profile, overview, brief, snapshot, one-pager, background, "what do we know about", "prep me for my meeting with", or Megabuyte's view of it, even without saying "brief". Prefer megabuyte-peer-benchmark for comparing companies and megabuyte-deal-precedents for multiples, when installed.
---

# Megabuyte company brief

Produces a one-company brief from Megabuyte data: what the company does, how it's performing, who owns and runs it, what it has bought or raised, what has changed recently, and what Megabuyte's analysts think.

**Read `references/conventions.md` first.** It sets the data boundary, figure, citation and gap rules every answer must follow. 

## Workflow

1. **Plan.** Call `plan_query` with `intent: "meeting_brief"` (or `company_profile` for a short or single-fact ask), the question as asked, and the company in `companies`. Resolve any candidates with the user first. Then follow the plan's "Start with" calls, made in parallel (see conventions §2).

2. **Typical call set** (the plan usually asks for these):
   - `get_company` once, with `sections: ["overview","financials","ownership","structure","news","people"]`. Add `deals` and `analysis` if the plan doesn't fetch them separately.
   - `get_financials` (`periods: 5`) for the trend. History often carries only revenue and headcount, so don't expect margins per year.
   - `get_analysis` (`analysis_type: "company"`) for Megabuyte's view, read whole.
   - `get_deals` over the company and its group, in one call.
   - `semantic_search` scoped to the company (news and company analysis) for trading, leverage and growth-strategy evidence (strategy, acquisitions, expansion, new markets).
   - `semantic_search` with `report_families: ["PeerGroupQuarterly"]` and the company name inside the question, to find sector quarterlies that mention it. These carry no company tags, so a company scope won't find them. Buy-and-build trackers in these reports often hold leverage and estimated exit-year lines worth quoting. Keep each result's `report.url` and `published_on` for the citation.

3. **Read before you write.** Open the 1–3 most material news articles in full with `article_id`. Results and trading pieces, and any article flagged by `may_be_out_of_date`, often hold the latest adjusted EBITDA, debt and management changes.

4. **Check.** Run `check_answer` on the draft. Fix anything it lists, and mark approximate figures or quote the held one.

5. **Answer in chat**, using the structure below.

## Brief structure

**Provenance labels** (conventions §4): Snapshot, trajectory, ownership, deal history, leadership and recent developments are **Megabuyte data**; Growth strategy and Megabuyte view are **Megabuyte research (AI summary)**; Questions to probe are **AI analysis**.

Use these sections in this order. Drop a section only when nothing is held for it, and note the gap in Coverage notes.

1. **Snapshot**: 2–3 sentences covering what it does, where it sits in Megabuyte's taxonomy (sector › peer group › sub-peer group), HQ postcode area, ownership label, latest revenue and headcount with FY and source.
2. **Financial trajectory**: a table of the last 3–5 periods with these rows: revenue, revenue growth, organic growth, gross margin, adjusted EBITDA, adjusted EBITDA margin, headcount. History usually holds only revenue and headcount per year, so the other rows are often filled for the latest year only, with "—" elsewhere. Add one or two sentences on the trend. Flag estimated or non-12-month periods. Use adjusted EBITDA per conventions §3.
3. **Ownership**: the ownership type and primary owners, as set out in conventions §3, in one or two lines. Describe the business as one group; don't list its registered entities.
4. **Growth strategy**: 3–5 sentences, in your own words, on how the company is growing. Cover organic vs acquisitive growth, the M&A pattern from its deal record, target markets, products or services being pushed, geographic expansion, and stated ambitions. Draw on the Company Analysis, recent news (results, M&A and contract wins) and the deal history. Date each source. Where Megabuyte holds little on strategy, say so rather than padding.
5. **Deal history**: a table with date, type, counterparty, role and disclosed value/multiple, newest first. State the total held.
6. **Leadership**: current execs and chair with positions and start dates. Reconcile against news: if a newer article reports a change, lead with it and say the board record hasn't caught up.
7. **Recent developments**: dated headlines with Links, written as one line each on why each matters.
8. **Megabuyte view**: a summary in your own words of the latest Company Analysis, with its date and link. Note anything material that has happened since it was published. If none is held, say "No Megabuyte Company Analysis is held for X." Then list the sector quarterlies that mention the company separately: each as its title linked to `report.url` from the search result, with its date and one line on what it says about the company (e.g. "lists Node4 with bank debt at 9.6x EBITDA and an estimated exit in 2028"). These are mentions, not coverage of the company.
9. **Questions to probe** (meeting-prep requests only): 3–5 sharp questions that come out of the data, such as a margin dip, a recent CFO exit, or a stale last deal. Ground every question in a fact above.
10. **Coverage notes**, then **Sources**.

Keep the chat version tight. The full brief should fit on one screen per section.

## Examples of good phrasing

- "Revenue grew 18% (12% organic) to £42.1m in FY Mar-25 (Megabuyte), the third straight year of double-digit growth. Adjusted EBITDA margin slipped from 21% to 17%."
- "Megabuyte records no deals for Acme since its 2021 secondary buy-out by LDC."
- "Megabuyte doesn't hold ARR or customer numbers. Its analysis notes that recurring revenue is around 70% of sales (Company Analysis, May 2026)."

## Beyond a single-company brief

If the request also asks for a comparison with peers or for deal multiples, answer that part yourself, briefly, with the MCP tools and the conventions:
- **Peers:** `benchmark_financials` with the company name, giving its position on revenue, growth and margin with n.
- **Multiples:** `get_deals` over its sub-peer group with `disclosed: ["ev_sales","ev_ebitda"]`, giving the median and range with n.

Don't send the user to another skill or name one. A dedicated skill, if installed, will be picked for those requests on its own.
