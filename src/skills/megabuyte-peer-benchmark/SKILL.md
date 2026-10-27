---
name: megabuyte-peer-benchmark
description: Benchmark a UK technology company against its peers, or build a comps table, using the Megabuyte MCP. Use this whenever the user asks how a company compares, stacks up or ranks against peers/competitors/the sector, wants a peer set, lookalikes, "who else is like X", a comparables/comps table, median or quartile positioning, or describes their own business ("we're a £30m MSP at 15% EBITDA — how do we compare?"). Also use when they want the benchmark exported as a document or slides.
---

# Megabuyte peer benchmark

Places one company (named or described) against a defensible peer set and Megabuyte's population statistics, or lays out several named companies side by side.

**Read `references/conventions.md` first.** For any file export, also read `references/brand.md` and run `scripts/brand_setup.py`.

## Pick the mode

| User asks | Mode | plan_query intent |
|---|---|---|
| "How does X compare?" / "where does X sit?" | **Position** | `peer_benchmark` |
| "Comps table for A, B, C" / "our closest comparators" | **Comps** | `comps_table` |
| "Who is like X?" / "find X's peers" | **Peer set** | `similar_companies` |
| A described business, not a named one | **Position** (described) | `peer_benchmark` |

## Workflow

1. **Plan.** Call `plan_query` with the intent above, the company or companies, and `theme` if the user named a sector word. For a described business, keep their size, margin and growth wording in `question`. Then follow the plan's calls (conventions §2).

2. **Position mode: the population comes first.** Call `benchmark_financials` with `company_number` or `company_name` (never `company_id`) and the peer group the plan names, keeping the default size band. This returns the subject's figures, its quartile position on each metric, and n per metric, with the subject's own group already excluded. Use that as the headline. Don't build the headline from a similarity list.

3. **Described business.** Use the theme leaves the plan resolved, with `revenue_min`/`revenue_max` at roughly half to double their revenue. The server may split the result by sub-peer group. If the theme word pulled in leaves that plainly don't fit (e.g. "MSP" resolving to Print Services or Data Centres), show the leaves that fit and say which you set aside. If more than one leaf fits, place them against each fitting leaf, or ask which one describes them. Placement of a described business is your own reading, so say so.

4. **Peer set** (Peer set mode, or named peers in Position mode): call `find_similar_companies` (`limit: 15`) and read which engine ran.
   - Website-similarity scores are often tightly clustered, and the list can include micro companies or other peer groups. Keep peers that are in the same peer group and within roughly 0.33x–3x revenue. Say how many you dropped and why.
   - State the engine and its date or band.

5. **Comps mode.** Read every company in **one** `search_companies` call (`company_ids: [...]`, with `fields` covering revenue, growth, organic growth, gross margin, EBITDA, EBITDA margin, employees, financial_year and revenue_estimated). Use `get_financials` only when the user asks for several years.

6. **Check** with `check_answer`, then answer.

## Output structure

1. **Headline**: one sentence on where the subject sits. Example: "Acme is upper-quartile on growth (24% vs a 9% median) but below median on EBITDA margin (11% vs 15%) among 40 IT managed services peers of £15–150m revenue."
2. **Positioning table**: one row per metric with columns for subject, lower quartile, median, upper quartile, n, and the subject's quartile. Always show n, because EBITDA n is usually much smaller than revenue n.
3. **Comps table**: company, revenue, growth, gross margin, EBITDA margin and headcount, each with FY. Sort by revenue. Mark estimated revenue with "(est.)" and leave blanks as "—", never 0.
4. **Read-across**: 2–4 sentences on what explains the gaps (mix, scale, investment phase), based only on held data or Megabuyte analysis.
5. **Method**: which engine built the peer set, the size band, the taxonomy level, and any peers removed and why.
6. **Coverage notes**, then **Sources**.

For slide exports, put the positioning table on one slide and the comps table on another, each with its method footnote.

## Watch-outs

- EBITDA is always adjusted EBITDA (conventions §3). In comps tables, show adjusted EBITDA as revenue × `ebitda_margin_pct` and label the column "Adj. EBITDA". Position companies on `ebitda_margin_pct`, never on `ebitda_gbp`.
- Show organic growth beside revenue growth where held.
- Percentages are 0–100. A user's "15% margin" is `15`.
- Don't rank on a metric held for fewer than 5 peers. Report the count instead.
- Group-vs-entity accounts can distort comparisons, so flag it where the structure section shows a mix.
- Similarity scores are often tightly clustered, so don't over-read the order.
- A metric marked withheld (e.g. a margin whose sign disagrees with the EBITDA) gets no quartile position. Say so, and quote the news-reported figure beside it if one is held.
- For resellers, check the revenue basis before comparing margins (conventions §3). For example, Softcat, Bytes and Computacenter are stored on a gross invoiced basis, so their margins look thin against other peer groups.
