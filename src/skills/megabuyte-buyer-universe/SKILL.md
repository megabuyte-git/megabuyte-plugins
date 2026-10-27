---
name: megabuyte-buyer-universe
description: Identify likely buyers and investors for a UK technology company using the Megabuyte MCP, each backed by deal evidence. Use this whenever the user asks who would buy, back or invest in a named company or a described business ("who would buy Bridewell?", "potential acquirers for a £20m payments software business", "exit options", "trade vs PE buyers", "buyer list for an IM"), or which investors are most active in a space. Also use when they want the buyer list exported. Not for finding targets for a buyer (megabuyte-target-screen) or for deal multiples (megabuyte-deal-precedents).
---

# Megabuyte buyer universe

Builds a buyer list for a company or described business: trade buyers and private equity sponsors, each justified by deals Megabuyte has on record.

**Read `references/conventions.md` first.** For any file export, also read `references/brand.md` and run `scripts/brand_setup.py`.

## Workflow

1. **Plan.** Call `plan_query` with `intent: "buyer_universe"` (or `investor_activity` when the question is about investors themselves), the question as asked, the company in `companies`, and any sector word in `theme`. Follow the plan's calls and rules (conventions §2). If the plan answers for a group entity, say so in one line.

2. **Window.** Default to the last 60 months unless the user gives one, and say so.

3. **Deal evidence, using every route at the same level** (conventions §11). In parallel:
   - **Taxonomy:** `get_deals` over the subject's segment (the plan's leaves) with the window: `deal_category: "MA"` for trade buyers, and again with `"PrivateEquity"` for PE buyers. Platforms PE firms now own that buy in the space are trade buyers too.
   - **Similar companies:** `find_similar_companies` for the subject (`limit: 15`), then one `get_deals` call over those peers' ids with the window. Whoever bought or backed businesses like the subject is as relevant as whoever bought in its segment.
   - **Keywords:** `search_companies` with `keywords` for the subject's capability (from its own keywords or description), then one `get_deals` call over those ids. This catches buyers active in the capability but filed under other segments.
   - **Analyst commentary:** `semantic_search` across news, reports and Company Analysis for who the analysts name as consolidators, active acquirers or likely buyers in this space. Use `tags: ["M&A","Private Equity"]` for news. A buyer named here still needs a recorded deal or holding to be listed; otherwise mention it as "named in commentary" with the source.
   - **Sponsor activity:** `search_investors` for the 3–5 most relevant sponsors, with `deal_from` the window start.

   Merge the buyers, recording which route(s) found each. Widen up the taxonomy (to the peer group, then the sector) only if all routes together are thin, and say so.

4. **Size fit.** One `search_companies` call with `company_ids` for the targets in the evidence, to compare each deal's size with the subject's revenue. Prefer buyers whose past targets are of similar scale, and say this is your judgement.

5. **Exclusions.** Never list the subject's own group, a closed company, a lender or an adviser as a buyer. Never present a similar company as a buyer unless it has its own deal.

6. **Check** with `check_answer`, then answer.

## Output structure

1. **Headline**: how many trade and PE buyers have deal evidence in the window, and the window.
2. **Trade buyers table**: buyer (linked to its profile), its relevant deals (date, target, value or "not disclosed"), deal count in the space, found via, and why it's relevant (your judgement, labelled).
3. **PE buyers table**: sponsor, relevant deals, found via, its current platforms in the space where held, deals since the window start, and why relevant.
4. **Most active in the space**: a short list from `search_investors`, ranked by recent activity.
5. **Read**: 2–3 sentences on the likely buyer pool, trade vs PE balance, and size fit. Mark it as your inference.
6. **Caveats** (always include): the universe is bounded by Megabuyte's UK tech corpus, so credible overseas or non-tech buyers with no recorded UK deal won't appear; buyer preferences, thesis and dry powder aren't held; "likely" is inference from past deals.
7. **Coverage notes**, then **Sources**.

## Watch-outs

- Only name a buyer that has a returned deal or holding. Nothing from general knowledge.
- On M&A records, the acquirer is recorded as the "investor".
- Classify a firm as PE or trade only from the deal category or its record.
