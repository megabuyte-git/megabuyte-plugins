---
name: megabuyte-deal-precedents
description: Precedent deals and valuation checks for UK tech M&A and investment from the Megabuyte MCP. Use for deal multiples, precedent or comparable transactions, what companies in a sector sold for, EV/Revenue or EV/EBITDA ranges, whether a price is fair or rich, how multiples or deal volumes have moved, or a company's deal and ownership history. Prefer megabuyte-buyer-universe for who would buy a company, when installed.
---

# Megabuyte deal precedents

Lists and counts UK tech deals for a sector, theme, period or company, and judges a quoted multiple against disclosed precedents.

**Read `references/conventions.md` first.** 

## Pick the mode

| User asks | Mode | plan_query intent |
|---|---|---|
| "Precedents for MSP deals since 2023" / "how many cyber deals last year" | **Precedent table** | `sector_deals_multiples` |
| "Is 14x EBITDA fair for a £20m payments business?" / "have multiples moved?" | **Valuation check** | `valuation_check` |
| "What has X bought?" / "who owns X and when did they buy it?" | **Company record** | `company_deals_and_ownership` |

## Workflow

### Priority order and budget (precedent tables and valuation checks)

Work through the searches in this order. **Priorities 1–4 are never skipped for brevity**: a precedent set without them is incomplete by this skill's standard, however reasonable it looks.

| # | Search | Rule |
|---|---|---|
| 1 | Sector deals in the window (step 2), fully paged | Always |
| 2 | Lookalikes as targets (step 2b) | Always; closest first |
| 3 | Keyword route (step 2b) | Always; one tight expression |
| 4 | Each statistic deal's own article (step 5) | Always, for deals entering the statistics; about 1,200 characters each |
| 5 | Lookalikes' own acquisitions (step 2b) | May be skipped if priorities 1–3 already give 15 or more trailing multiples in the window |
| 6 | Valuation commentary (step 7) and context (step 8) | May be shortened to one search each |

**Keeping it efficient, without dropping anything:**
- On routes 2, 3 and 5, fetch only priced deals (`disclosed: ["ev_sales","ev_ebitda"]`): only those feed the statistics.
- Use `detail: "compact"` throughout, and read article text only for deals entering the statistics.
- Aim for about 20 tool calls.

**If something has to give,** it's priority 6, then 5, never 1–4. Say so **at the top of the answer**, in the Routes run line (e.g. "lookalikes' acquisitions: not run, because 18 multiples were already held"), and offer to run it. Never skip a search silently, and never decide on your own to shorten a run without stating it up front.

1. **Plan.** Call `plan_query` with the intent, the question as asked, `theme` (the user's sector word), `period`, and `disclosed: true` if they only want deals with multiples. The plan resolves the theme to exact taxonomy leaves, so use those, not your own guess.

2. **Pull deals: taxonomy route.** Call `get_deals`, passing the plan's taxonomy exactly as resolved (one level only), the dates, and the plan_id.
   - **Counts:** run the full screen. Quote "N of M deals held for those companies", and say it is matched on the company's classification, so it is a lower bound.
   - **Multiples:** add `disclosed: ["ev_sales","ev_ebitda"]` for either multiple, or `["ev_ebitda"]` for EBITDA only. Never use `ev_*_min` to mean "disclosed".
   - Page with `offset` until `next_offset` is null before computing any statistic, up to 100 rows (conventions §10). If more match, narrow the window or the taxonomy level rather than pulling everything, and say so.
   - **Company record:** pass the company with no `role`. Split the results into acquisitions made, investments received and exits.

2b. **Add comparable deals by lookalike and keyword routes** (conventions §11), for precedent tables and valuation checks; not for counts or a single company's record. Run these in parallel with step 2:
   - **Seeds:** for a valuation check, the subject (or, for a described business, the user's description). For a sector question, the 2–3 largest targets in step 2 that have disclosed multiples.
   - **Lookalikes as targets** (priority 2): `search_companies` with `similar_to` (the seed's name or description), no `plan_id`, a size band around the subject (about 0.33x–3x revenue, or the user's size) and **no `sort_by`**, so the closest come first. Page to every match, up to 100 (conventions §11). Lookalike searches always leave out closed profiles, so acquired lookalikes come through the keyword and taxonomy routes, not this one. Then `get_deals` over all their ids with `role: "target"`, the window, `disclosed: ["ev_sales","ev_ebitda"]` and `detail: "compact"`.
   - **Lookalikes' own acquisitions** (priority 5): `find_similar_companies` per named seed (`limit: 25`, paged to every neighbour, up to 100). It returns only live companies, so they will rarely be targets, but their acquisitions often are comparable. `get_deals` over their ids with `role: "investor"` and the window. Keep a deal only where the **target** does what the subject does (e.g. FluidOne's purchase of SureCloud Cyber Services as a cyber precedent). The comparability is your judgement, so label it, and drop the rest.
   - **Keywords** (priority 3): `guided_keywords: true` over the leaves, then `search_companies` with the 3–6 strongest capability `keywords` as one expression, no taxonomy filter, `exclude_closed_profiles: false` (acquired companies are often closed profiles) and **no `plan_id`** (conventions §2). Page to every match. Above 100, tighten the expression or the size band, never truncate by revenue. Then `get_deals` over all their ids with `role: "target"`, `disclosed: ["ev_sales","ev_ebitda"]` and `detail: "compact"`. This catches targets filed in other segments.
   - **Merge** with step 2's deals, de-duplicating by deal, and record "found via" (taxonomy / lookalike target / lookalike's acquisition / keywords) per deal.

3. **Sort the rows by side.** A sector screen returns deals where the sector company is the **target**, the **acquirer** or the **seller**, and some of those targets are non-UK or outside the theme (e.g. Sophos→SecureWorks, NCC's Fox-IT disposal). For a precedent set that values a UK business, use UK targets in the theme as the core set. Show the other rows separately or flag them. Don't silently drop them.

4. **Thin evidence.** If all routes together (steps 2 and 2b, plus trailing multiples stated in Megabuyte commentary, from step 5) give fewer than 5 multiples, widen the window one step at a time: 24 months, then 36 months, then since 2020. If still thin, add adjacent leaves the user would accept. Prefer more comparable deals from the same period over older ones, so run every route before widening the window. State each widening. In Payments, for example, the last 24 months held one EV/EBITDA, and since 2020 held six.

5. **Establish each deal's basis.** Deal records don't store whether a value is reported or a Megabuyte estimate. Their multiples are trailing by definition, but the EBITDA basis behind EV/EBITDA isn't recorded. **Read each priced deal's own article,** not just a general search. Cover every deal that will enter the statistics or the precedent table:
   - **Batch the reads:** `get_news_articles` with up to 20 targets per call: `company_id` as a list (or `company_name` as a list for targets with no id; articles are matched on the newsroom's names), `tag: "M&A"`, `published_since`/`published_until` spanning the deals' announcement dates, and `max_text_chars` about 1,200. Match each article to its deal by parties and date (within about six weeks of the announcement).
   - **Still missing:** for any deal with no article found that way, try `semantic_search` with `deal_targets: ["<target name>"]`, `sources: ["news"]`, and `since`/`until` around the announcement.
   - Read the text for the value's basis ("we estimate", "estimated at", "consideration of", "announced", "according to the accounts") and any stated multiple.
   - **Value basis:** *Reported* (announced or filed by the parties) or *Megabuyte estimate* (the article or analysis says "estimated", "we estimate" or similar). *Not stated* only after the deal's own article has been read, or none was found. In the coverage notes, say how many deals had their article read, and how many had no article.
   - **Multiple basis:** every multiple on a deal record is **trailing**: EV over the target's latest financial-year revenue or EBITDA (the server defines it this way). Multiples stated in Megabuyte's text carry whatever basis the text gives: *trailing* (historic or last-year earnings), *forward* (e.g. "13.1x forward CY26 EBITDA"), or *not stated*.
   - **Multiples in commentary:** while reading each deal's coverage, capture any multiple the text states (EV/Revenue or EV/EBITDA, reported or estimated), especially for deals whose record has none. Record it with its basis, whether it's reported or a Megabuyte estimate, and the linked article.
   - Search in batches (several targets per query where possible), and stop once the core set is covered or the 100-row cap applies (conventions §10). Never guess a basis.

6. **Compute** the statistics yourself over the full paged set of core rows: n, lower quartile, median, mean, upper quartile and range, for EV/Revenue and EV/EBITDA separately. Exclude rows above 50x EBITDA and rows with EV under £2m from headline medians, and show them as outliers. With n < 5, list the deals and don't quote a median or a mean. The mean uses exactly the same rows as the median, after the outlier exclusions. The **median is the headline figure**. If the mean differs from the median by more than about 20%, say the set is skewed and name the deals pulling it. Label every statistic as your own arithmetic, with its n. Say how many values behind each statistic are reported vs estimated. Which multiples go into the statistics:
   - **In:** deal-record multiples, plus trailing multiples stated in Megabuyte commentary for deals whose record has none.
   - **Split the n:** state how many came from each source, e.g. "n = 14: 11 deal records, 3 Megabuyte commentary".
   - **Out:** forward multiples, and multiples whose basis isn't stated. List them beside the statistic, never mixed in.
   - **Sensitivity:** when the lookalike and keyword routes added multiples, also give the taxonomy-only median and mean with its n, so the user can see what the wider set changed.
   - **Conflicts:** where a deal record and commentary disagree on the same deal, the record goes into the statistic and the commentary figure is noted (conventions §3).

7. **Valuation check:** place the user's multiple in the disclosed range deal by deal, comparing like with like (a trailing ask against trailing precedents). Name the 2–3 closest precedents by size, date and type. Then add context from Megabuyte's writing on valuations in that sector:
   - news tagged M&A, Private Equity, Venture & Growth Capital and Capital Markets: `semantic_search` with `sources: ["news"]`, those `tags`, the plan's `sectors`, and `since` within about 3 years;
   - relevant reports: `semantic_search` with `sources: ["report"]`, `report_families: ["CorporateActivity","PeerGroupQuarterly"]` and the same `sectors`, for commentary on deal multiples and valuation trends.

   Summarise what they say about pricing in your own words, dated. Give a clear position (e.g. "toward the top of a thin range"), and frame it as a position, not a valuation. Never state "the market pays Nx" as a fact, and never bring in trading multiples or your own knowledge.

8. **Context (optional).** For "why" questions, use `semantic_search` with `sources: ["deal","report"]`. It samples and never counts.

9. **Check** with `check_answer`, then answer.

## Output structure

**Provenance labels** (conventions §4): Deal rows and their multiples are **Megabuyte data** (multiples from commentary are marked as such); n, medians, means, quartiles and ranges are **AI calculations**; comparability judgements, the valuation position and the Read are **AI analysis**.

1. **Headline**: the count or verdict in one sentence, including n and the window. Directly under it, the **Routes run** line (conventions §11) for precedent tables and valuation checks.
2. **Multiples summary**: a small table with columns for metric, n, LQ, median, mean, UQ and range.
3. **Precedent table**: date, target, acquirer/investor, type, value (£m), value basis (Reported / Megabuyte estimate / Not stated), EV/Revenue, EV/EBITDA, multiple source (Deal record / Megabuyte commentary, with link), multiple basis (Trailing / Forward / Not stated), found via (taxonomy / lookalike target / lookalike's acquisition / keywords). Newest first, or sorted by relevance in a valuation check. Use "—" for undisclosed.
4. **Read**: 2–4 sentences on the trend over time, PE vs trade, the size effect, and any notable outliers.
5. **Caveats** (always include): multiples come only from deals that disclose them, typically a minority; reported values and Megabuyte estimates are shown as such, and bases not stated in Megabuyte's coverage are marked "Not stated"; the EBITDA in a deal multiple may differ from Megabuyte's adjusted EBITDA for the company; rumoured, withdrawn and non-UK-tech deals aren't held; advisers and earn-outs aren't held.
6. **Coverage notes**, then **Sources**.

## Watch-outs

- Multiple bounds take multiples (`ev_ebitda_min: 10` means 10x). Value bounds take whole pounds (`min_value_gbp: 20000000` means £20m).
- `deal_type` labels must match exactly (`"Merger or acquisition"`, `"Secondary buy-out"`).
- **Two quotable sources of multiples, both Megabuyte's:** the deal record, and multiples stated in Megabuyte's own text (news, Company Analysis, reports), e.g. "13.1x forward CY26 EBITDA" or "an estimated 14x EBITDA". Quote both, each with its source.
- **Never calculate a multiple yourself,** e.g. by dividing a deal value by a revenue or EBITDA figure. If neither source states one, the multiple is "not disclosed".
- A sector screen matches on the **company's** classification, not the deal's, so state that.
