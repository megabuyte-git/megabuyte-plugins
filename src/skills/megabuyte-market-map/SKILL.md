---
name: megabuyte-market-map
description: Map the structure of a UK technology sector or market using the Megabuyte MCP — its segments, the main players in each by size, who owns them, and recent deal activity. Use this whenever the user asks to map, landscape or lay out a sector ("map the UK cyber security sector", "who are the main players in UK payments", "how is the MSP market structured", "market map", "competitive landscape", "who's in this space"). Also use when they want the map as slides or a spreadsheet. Not for what Megabuyte thinks about a theme or trend (megabuyte-market-trends) or for a filtered target shortlist (megabuyte-target-screen).
---

# Megabuyte market map

Lays out who is in a UK tech market and how it is structured: segments, leading players by size, ownership and recent deal activity, with a short Megabuyte view.

**Read `references/conventions.md` first.** For any file export, also read `references/brand.md` and run `scripts/brand_setup.py`.

## Workflow

1. **Plan.** Call `plan_query` with `intent: "company_screen"`, the question as asked (including the word "map"), and the user's sector word in `theme`. The plan resolves the theme to segments (sub-peer groups) with company counts. Start the answer by stating what the word was read as, e.g. "'cyber security' read as six segments, 1,074 companies". If the theme has no taxonomy home, say the map is a best-effort keyword map.

2. **Segment statistics.** One `benchmark_financials` call with `sub_peer_group` set to all the segments and `group_by: "sub_peer_group"`, for company counts and median revenue, growth and adjusted EBITDA margin per segment.

3. **Find the market's players by every route** (conventions §11). A market is rarely one taxonomy branch: payments players also sit in Banking, Financing and software leaves. In parallel:
   - **Taxonomy:** one `search_companies` call per resolved segment, with `sub_peer_group: [that segment]`, `collapse_to_group: true`, `sort_by: "revenue"`, `limit: 10`, and `fields` for revenue, financial_year, organic_growth_pct, ebitda_margin_pct, ownership, investors, postcode and keywords.
     - **Do not pass the plan_id on these calls.** The plan widens a single-segment call back to the whole theme; check `guard_notes`, and re-call without the plan_id if it happened.
   - **Keywords:** `guided_keywords: true` over the theme's leaves to read the capability vocabulary. Then `search_companies` with the 3–6 strongest `keywords` across all sectors, `sort_by: "revenue"`, for players filed elsewhere.
   - **Similar companies:** `find_similar_companies` seeded on the 2–3 largest players found, for businesses that read like them.
   - **Analyst commentary:** `semantic_search` on the market across reports, Market Analysis and news, for players the analysts discuss as part of it.

4. **Build the groupings, in more than one dimension.** De-duplicate by group, then organise the players:
   - **By segment:** the taxonomy leaves, plus a "Filed elsewhere" group for players found by the other routes.
   - **By capability:** clusters from the keywords the players share (e.g. in payments: acquiring and merchant services, payment gateways, embedded payments, B2B payables, open banking). Name each cluster from the keyword evidence, and say that the clusters are your grouping.
   - **By ownership and scale:** the ownership type × revenue band.

   Each player shows which route(s) found it.

5. **Deal activity.** One `get_deals` call over all the segments for the last 24 months: quote the total, the split by deal category (M&A, PE, VC) where the answer gives it, and the 3–5 largest deals with dates and parties.

6. **Megabuyte view.** One paragraph, in your own words, from the newest Market Analysis (`get_analysis`, `analysis_type: "market"`, the peer group) or the newest peer-group quarterly (`get_reports`, `report_family: "PeerGroupQuarterly"`). Date it. Keep it brief; a deeper thematic view is the market trends skill's job.

7. **Check** with `check_answer`, then answer.

## Output structure

1. **Headline**: the sector as read, the number of segments and companies, and the snapshot date.
2. **Segment overview table**: segment, companies held, median revenue, median organic growth, median adjusted EBITDA margin, with n per metric.
3. **Leading players by segment**: for each segment (and "Filed elsewhere"), a table of rank, company (trading name, profile link), revenue (£m, FY), organic growth, adjusted EBITDA margin, ownership and owners, town or city, found via.
4. **Capability map**: the capability clusters, each with its players and the keywords that define it. A player can sit in more than one cluster.
5. **Ownership and scale**: a grid of ownership type × revenue band, counting the players shown, labelled as covering the players found, not the whole market.
6. **Deal activity**: count and largest deals in the last 24 months.
7. **Megabuyte view**: one dated paragraph.
8. **Coverage notes**, then **Sources**.

**Exports:**
- **PowerPoint:** an opening map slide (a grid of capability clusters or segments with their leading players), then one slide per segment, a capability slide, an ownership-and-scale slide and a deal activity slide.
- **Excel:** the full player list.

## Watch-outs

- Rank by revenue held. Companies without a revenue figure won't appear, so say so in the coverage notes.
- Overseas-headquartered groups with UK entities (e.g. a US parent's UK subsidiary) appear on their UK filings; note it where it explains an outlier.
- Short or long accounting periods are annualised by the server; flag any company whose growth is withheld because of that.
- Use trading names (`short_name`), never bidco or holding entities.
