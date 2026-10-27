---
name: megabuyte-deal-precedents
description: Build precedent transaction tables and sanity-check valuations for UK technology M&A and investment using the Megabuyte MCP. Use this whenever the user asks about deal multiples, precedent transactions, comparable deals, what companies in a sector sold for, EV/Revenue or EV/EBITDA ranges, whether a price or multiple is fair/in line/rich, how multiples have moved, M&A or PE activity in a sector or period, or a named company's deal and ownership history. Also use when they want the precedents exported to Word, PDF, Excel or slides.
---

# Megabuyte deal precedents

Lists and counts UK tech deals for a sector, theme, period or company, and judges a quoted multiple against disclosed precedents.

**Read `references/conventions.md` first.** For any file export, also read `references/brand.md` and run `scripts/brand_setup.py`.

## Pick the mode

| User asks | Mode | plan_query intent |
|---|---|---|
| "Precedents for MSP deals since 2023" / "how many cyber deals last year" | **Precedent table** | `sector_deals_multiples` |
| "Is 14x EBITDA fair for a £20m payments business?" / "have multiples moved?" | **Valuation check** | `valuation_check` |
| "What has X bought?" / "who owns X and when did they buy it?" | **Company record** | `company_deals_and_ownership` |

## Workflow

1. **Plan.** Call `plan_query` with the intent, the question as asked, `theme` (the user's sector word), `period`, and `disclosed: true` if they only want deals with multiples. The plan resolves the theme to exact taxonomy leaves, so use those, not your own guess.

2. **Pull deals** with `get_deals`, passing the plan's taxonomy exactly as resolved (one level only), the dates, and the plan_id.
   - **Counts:** run the full screen. Quote "N of M deals held for those companies", and say it is matched on the company's classification, so it is a lower bound.
   - **Multiples:** add `disclosed: ["ev_sales","ev_ebitda"]` for either multiple, or `["ev_ebitda"]` for EBITDA only. Never use `ev_*_min` to mean "disclosed".
   - Page with `offset` until `next_offset` is null before computing any statistic, up to 100 rows (conventions §10). If more match, narrow the window or the taxonomy level rather than pulling everything, and say so.
   - **Company record:** pass the company with no `role`. Split the results into acquisitions made, investments received and exits.

3. **Sort the rows by side.** A sector screen returns deals where the sector company is the **target**, the **acquirer** or the **seller**, and some of those targets are non-UK or outside the theme (e.g. Sophos→SecureWorks, NCC's Fox-IT disposal). For a precedent set that values a UK business, use UK targets in the theme as the core set. Show the other rows separately or flag them. Don't silently drop them.

4. **Thin evidence.** If the plan's default window gives fewer than 5 disclosed multiples, widen it one step at a time: 24 months, then 36 months, then since 2020. If still thin, add adjacent leaves the user would accept. State each widening. In Payments, for example, the last 24 months held one EV/EBITDA, and since 2020 held six.

5. **Establish each deal's basis.** Deal records don't store whether a value is reported or a Megabuyte estimate, or whether a multiple is trailing or forward (`ev_ebitda_basis: not_recorded`). For every deal in the core set, look for it in the deal's news coverage: `semantic_search` with `sources: ["news"]`, `tags: ["M&A","Private Equity","Venture & Growth Capital","Capital Markets"]`, the target in `deal_targets` or the question, and a `since` near the announcement date.
   - **Value basis:** *Reported* (announced or filed by the parties) or *Megabuyte estimate* (the article or analysis says "estimated", "we estimate" or similar). Otherwise *Not stated*.
   - **Multiple basis:** *Trailing* (historic or last-twelve-months earnings), *Forward* (current-year or next-year earnings, e.g. "13.1x forward CY26 EBITDA"). Otherwise *Not stated*.
   - Search in batches (several targets per query where possible), and stop once the core set is covered or the 100-row cap applies (conventions §10). Never guess a basis.

6. **Compute** the statistics yourself over the full paged set of core rows: n, lower quartile, median, upper quartile and range, for EV/Revenue and EV/EBITDA separately. Exclude rows above 50x EBITDA and rows with EV under £2m from headline medians, and show them as outliers. With n < 5, list the deals and don't quote a median. Label every statistic as your own arithmetic, with its n. Say how many multiples in each statistic are reported vs estimated, and trailing vs forward. Where forward and trailing multiples are mixed, show the median for each basis separately if n allows.

7. **Valuation check:** place the user's multiple in the disclosed range deal by deal, comparing like with like (a trailing ask against trailing precedents). Name the 2–3 closest precedents by size, date and type. Then add context from Megabuyte's writing on valuations in that sector:
   - news tagged M&A, Private Equity, Venture & Growth Capital and Capital Markets: `semantic_search` with `sources: ["news"]`, those `tags`, the plan's `sectors`, and `since` within about 3 years;
   - relevant reports: `semantic_search` with `sources: ["report"]`, `report_families: ["CorporateActivity","PeerGroupQuarterly"]` and the same `sectors`, for commentary on deal multiples and valuation trends.

   Summarise what they say about pricing in your own words, dated. Give a clear position (e.g. "toward the top of a thin range"), and frame it as a position, not a valuation. Never state "the market pays Nx" as a fact, and never bring in trading multiples or your own knowledge.

8. **Context (optional).** For "why" questions, use `semantic_search` with `sources: ["deal","report"]`. It samples and never counts.

9. **Check** with `check_answer`, then answer.

## Output structure

1. **Headline**: the count or verdict in one sentence, including n and the window.
2. **Multiples summary**: a small table with columns for metric, n, LQ, median, UQ and range.
3. **Precedent table**: date, target, acquirer/investor, type, value (£m), value basis (Reported / Megabuyte estimate / Not stated), EV/Revenue, EV/EBITDA, multiple basis (Trailing / Forward / Not stated). Newest first, or sorted by relevance in a valuation check. Use "—" for undisclosed.
4. **Read**: 2–4 sentences on the trend over time, PE vs trade, the size effect, and any notable outliers.
5. **Caveats** (always include): multiples come only from deals that disclose them, typically a minority; reported values and Megabuyte estimates are shown as such, and bases not stated in Megabuyte's coverage are marked "Not stated"; the EBITDA in a deal multiple may differ from Megabuyte's adjusted EBITDA for the company; rumoured, withdrawn and non-UK-tech deals aren't held; advisers and earn-outs aren't held.
6. **Coverage notes**, then **Sources**.

Excel exports should carry the raw precedent table with one row per deal, plus a summary tab, so users can re-cut it.

## Watch-outs

- Multiple bounds take multiples (`ev_ebitda_min: 10` means 10x). Value bounds take whole pounds (`min_value_gbp: 20000000` means £20m).
- `deal_type` labels must match exactly (`"Merger or acquisition"`, `"Secondary buy-out"`).
- Never infer a multiple from a value and a revenue figure. Quote only the disclosed multiples.
- A sector screen matches on the **company's** classification, not the deal's, so state that.
