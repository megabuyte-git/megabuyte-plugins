---
name: megabuyte-buyer-universe
description: Likely buyers and investors for a UK tech company from the Megabuyte MCP, backed by deal evidence or stated acquisition intent. Use for who would buy, back or invest in a named or described business ("who would buy Bridewell?", "acquirers for a £20m payments software business"), exit options, trade vs PE buyers, buyer lists, or the most active investors in a space. Prefer megabuyte-target-screen for targets for a buyer, when installed.
---

# Megabuyte buyer universe

Builds a buyer list for a company or described business: trade buyers and private equity sponsors, each justified by deals Megabuyte has on record.

**Read `references/conventions.md` first.** 

## Workflow

1. **Plan.** Call `plan_query` with `intent: "buyer_universe"` (or `investor_activity` when the question is about investors themselves), the question as asked, the company in `companies`, and any sector word in `theme`. Follow the plan's calls and rules (conventions §2). For a described business with no named company, keep the user's description (size, capability, ownership) as the seed for steps 3b and 3c.

2. **Window.** Default to the last 60 months unless the user gives one, and say so.

3. **Deal evidence by all four routes** (conventions §11). Every route is required.
   - **a. Taxonomy:** `get_deals` over the subject's segment (the plan's leaves) and the window: `deal_category: "MA"` for trade buyers, and again with `"PrivateEquity"` for PE buyers. Platforms that PE firms now own and that buy in the space are trade buyers too. Page each call to the 100-row cap (conventions §10).
   - **b. Keywords:** first `guided_keywords: true` over the subject's leaves to read the capability vocabulary. Then `search_companies` with the 3–6 strongest capability `keywords`, `exclude_closed_profiles: true`, **no taxonomy filter** and **no `plan_id`** (conventions §2), then `get_deals` over those companies' ids with the window. This finds buyers active in the capability whose acquisitions are filed under other segments (e.g. MSPs and integrators buying cyber practices).
   - **c. Similar companies:** seed on the subject, and on 1–2 of the most comparable targets from step a. Use `find_similar_companies` (`limit: 15`) per seed, and `search_companies` with `similar_to` and no `plan_id` (for a described business, the user's description is the `similar_to` text). Then `get_deals` over all the lookalikes' ids with the window. Whoever bought or backed businesses like the subject is as relevant as whoever bought in its segment.
   - **d. Analyst commentary:** `semantic_search` across news, reports and Company Analysis, phrased to surface buyer names, e.g. "consolidators acquiring managed security businesses" or "most active acquirers of payments software". Use `tags: ["M&A","Private Equity"]` for news.
   - **e. Stated acquisition intent:** `semantic_search` with `sources: ["news","report","company_analysis"]`, a `since` within the last 24 months, and the subject's segments or capability, phrased for intent rather than completed deals. For example: "plans to make acquisitions in managed security", "buy-and-build strategy", "new investment to fund M&A", "debt facility for acquisitions", "looking for bolt-ons". Look especially at:
     - companies newly backed by PE in the last 24 months in or next to the subject's space (from step a's `"PrivateEquity"` deals), whose backing is often described as a buy-and-build mandate;
     - results and fundraising news where management states an M&A ambition;
     - the **corporate strategy section of Company Analyses** (passages headed "Corporate strategy"), which often states whether a company is pursuing bolt-ons and in which capabilities. Read the whole analysis with `get_analysis` when a passage looks relevant;
     - peer-group quarterlies' "M&A activity triggers" tables. Where a table has lost its company names in the text, use only the companies named in the surrounding prose.
     A company qualifies only when a dated Megabuyte passage states or clearly reports its acquisition intent, and that intent covers the subject's capability or segment. Record the source's linked title, its date, and a short summary of what it says, in your own words.
   - **f. Sponsor activity:** `search_investors` for the 3–5 most relevant sponsors, with `deal_from` the window start.

   Merge the buyers by group, recording which route(s) found each. A buyer found by several routes ranks higher. Widen up the taxonomy (to the peer group, then the sector) only if all four routes together are thin, and say so.

4. **Size fit.** One `search_companies` call with `company_ids` for the targets in the evidence, to compare each deal's size with the subject's revenue. Prefer buyers whose past targets are of similar scale, and say this is your judgement.

5. **Exclusions.** Never list the subject's own group, a closed or acquired company (`closed_profile`: name its new owner instead, if the deal shows one), a lender or an adviser as a buyer. Never present a similar company as a buyer unless it has its own deal.

6. **Check** with `check_answer`, then answer.

## Output structure

**Provenance labels** (conventions §4): Deals, holdings and sponsor activity are **Megabuyte data**; stated intent is **Megabuyte research (AI summary)**; "why relevant", size fit and the Read are **AI analysis**.

1. **Headline**: how many trade and PE buyers have deal evidence in the window, how many more have stated acquisition intent, and the window. Directly under it, the **Routes run** line (conventions §11).
2. **Trade buyers table** (completed deals in the window): buyer (linked to its profile), its relevant deals (date, target, value or "not disclosed"), deal count in the space, found via (taxonomy / keywords / similar / commentary), and why it's relevant (your judgement, labelled).
3. **PE buyers table**: sponsor, relevant deals, found via, its current platforms in the space where held, deals since the window start, and why relevant.
4. **Stated acquirers: intent, no completed deal in the window**: buyer (profile link), what the intent is and in which capability, the linked source and its date, ownership, and size fit with the subject. Keep this table separate from the completed-deal tables. Never imply a deal has happened, and drop intent statements older than 24 months unless the user asks.
5. **Most active in the space**: a short list from `search_investors`, ranked by recent activity.
6. **Read**: 2–3 sentences on the likely buyer pool, trade vs PE balance, size fit, and how strong the stated-intent evidence is. Mark it as your inference.
7. **Caveats** (always include): the universe is bounded by Megabuyte's UK tech corpus, so credible overseas or non-tech buyers with no recorded UK deal won't appear; buyer preferences, thesis and dry powder aren't held; "likely" is inference from past deals.
8. **Coverage notes**, then **Sources**.

## Watch-outs

- Only name a buyer that has a returned deal or holding, or a dated Megabuyte source stating its acquisition intent (step 3e). Nothing from general knowledge.
- On M&A records, the acquirer is recorded as the "investor".
- Classify a firm as PE or trade only from the deal category or its record.
