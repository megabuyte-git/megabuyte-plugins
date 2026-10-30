# Megabuyte MCP conventions

These rules apply to every skill in the Megabuyte suite. They exist because subscribers use these answers in pitch books, IC papers and client meetings, so a confident wrong number is far more costly than a stated gap.

## 1. Data boundary

- Answer only from the Megabuyte MCP tools (names containing `get_company`, `get_deals`, `search_companies` and so on, on the Megabuyte server).
- Do **not** blend in data from other financial connectors (S&P Global / Capital IQ / Kensho, PitchBook and similar), even if they are installed. Licensing differs, and mixed figures cannot be sourced cleanly. If the user explicitly asks for a comparison with another provider, keep the two in clearly separated, labelled sections.
- Do not fill gaps from general knowledge or the web. If Megabuyte doesn't hold it, say so (see §6).

## 2. The plan is authoritative

Call `plan_query` first, with the user's question in their own words (don't paraphrase it, because the wording drives the routing), the most specific `intent`, and `companies` / `theme` / `period` where given. Pass its `plan_id` to every later call. On a follow-up, pass `previous_plan_id`.

**Follow the plan's "Start with" calls, its "MUST state" lines and its "Do NOT" lines.** These come from the server and are kept current. The workflow in each skill is the default for when the plan is silent. Where they differ, the plan wins, and the skill's job is the output shape. Make independent calls in parallel, as the plan asks.

The server may also adjust your arguments, for example by replacing a peer group with the leaves a theme word resolved to. A `guard_notes` field says when it has. **Read `guard_notes` after every call**, and report the scope the server actually used.

**Calls that must leave the plan's scope go without the plan_id.** When a call is meant to search outside or narrower than the plan's resolved taxonomy, pass no `plan_id`, because the guard will otherwise put the plan's leaves back. This covers:
- keyword searches with no taxonomy filter;
- `similar_to` lookalike searches;
- single-segment calls in a market map;
- `get_deals` over a list of company ids found by those routes.

If a guard note shows the scope was changed anyway, re-run the call without the `plan_id` before using its results. Never count a route as run if the guard narrowed it back into the taxonomy.

**Resolution:**
- **If a name returns candidates:**
  - If one candidate is marked "Megabuyte company" and the others are "part of" it, they are one business. Pick the Megabuyte company yourself; don't ask.
  - If the candidates are separate businesses, ask the user to pick. Don't guess: UK tech has many near-duplicate names.
- Describe the business under its trading name, not a bidco or holding entity (see "Group, not entities" below).
- If a name also matches other entities (e.g. "Bytes"), name the one used and the others in one line.
- Say what a sector word was read as, with the stored groups and their counts, before giving results.

## 3. Figures

- Every figure carries its **period** (FY end) and **source**: "megabuyte" (analyst-reviewed) or "Companies House" (as filed). Example: *Revenue £42.1m (FY Mar-25, Megabuyte)*.
- Money: tools take and return whole pounds. Present in £m to one decimal place (£k for under £1m).
- Percentages: tools use 0–100. Twenty percent is `20`, never `0.2`.
- Never present an **estimated** revenue as filed, and don't compute growth across one without saying so.
- **Growth rates are annualised.** Megabuyte's growth figures (`revenue_growth_pct`, `organic_growth_pct`) are already on an annualised basis, so use them as given, even where the accounting period isn't 12 months. Note the period length beside the figure.
  - The server's growth *bands* (`revenue_growth_pct_min`, `organic_growth_pct_min`) silently drop companies whose growth it withholds for a short or long period. When a growth criterion matters, screen without the growth band, then apply the threshold yourself to the returned (annualised) figures. Say you did.
  - Other figures for a period that isn't 12 months are labelled with its days.
- **EBITDA means adjusted EBITDA.** On companies Megabuyte covers, `ebitda` / `ebitda_gbp` is Megabuyte's adjusted EBITDA, and `ebitda_basis` says so ("adjusted EBITDA (Megabuyte)"). Margins and growth rates are on the same adjusted figures.
  - Present it as **adjusted EBITDA**. The reported (statutory) figure is `reported_ebitda`; show it only if asked, labelled "reported".
  - On companies with only filed accounts, `ebitda_basis` reads "as filed". Label that figure **"EBITDA (as filed)"**, never adjusted.
  - Screens (`search_companies`) can mix Megabuyte-covered and filed-only companies without saying which is which. In a screen's table, head the column "EBITDA (adjusted where Megabuyte covers the company)".
  - If EBITDA isn't held, use the adjusted EBITDA reported in Megabuyte news for that period, with the article and date (`ebitda_in_news`). Otherwise say it isn't held.
  - In benchmarks, use `ebitda_margin_pct` distributions.
- **Organic growth:** show `organic_growth_pct` beside revenue growth wherever growth is shown.
- **Deal EV/EBITDA:** the multiple's EBITDA basis isn't recorded (`ev_ebitda_basis: not_recorded`); say so, unless the row says `recomputed`.
- **Closed profiles.** Screens can return companies Megabuyte has closed (`closed_profile: true`, e.g. "acquired"), whose figures are out of date. Pass `exclude_closed_profiles: true` on screens, maps, peer sets and buyer searches. If a closed company is relevant (e.g. a recent acquisition), name it as closed, with the reason, and never as a current player or buyer.
- **Company names.** Use the `short_name` or `display_name` where a row gives one. Otherwise tidy the registered name: drop "Limited", "Ltd", "Holdings Limited" or "plc", and use normal capitalisation ("PERFORMANTA LIMITED" → "Performanta", "KHIPU NETWORKS LIMITED" → "Khipu Networks"). Keep the original for any Companies House reference.
- **Group, not entities.** Describe a company as one business. Don't list its individual registered entities (bidcos, midcos, holding companies) or their numbers. Give the trading name and, once, the Companies House number of the entity the figures come from.
- Counts: quote `total_matched` (or the stated totals), never the number of rows on the page.
- **Withheld figures.** Some metrics come back null with a `*_withheld` reason (e.g. a margin whose sign disagrees with the EBITDA). Say "withheld" and don't place the company on that metric. You may quote a news-reported figure beside it, labelled with its article and date.
- **Stored vs news EBITDA.** When `ebitda_in_news` shows `differs_from_stored: true`, lead with the stored adjusted figure. Mention the news figure only if it covers the same period, with its article and date (news figures are often a different year or a forward view).
- **Revenue basis for resellers.** For VARs and distributors (e.g. Softcat, Bytes, Computacenter), the stored revenue can be gross invoiced income (GII), not statutory revenue: Softcat FY Jul-25 is stored at £3,617m against statutory revenue of £1,458m. The server holds only Megabuyte's own series for these companies, so take statutory revenue from the Company Analysis or results news for the same year, with the source. Label the stored line "GII (Megabuyte)". Don't compare margins across companies on different bases.
- **Deal multiples.** Quote multiples from the deal record, or as stated in Megabuyte's own text (news, Company Analysis, reports), always with the source. Never calculate one yourself. If the record and the commentary disagree on the same deal (e.g. 19.96x on record vs "~14x" in the analysis), the record leads in tables and statistics, and the commentary figure is noted once.
- **Ownership.** State the ownership type as one of: PE-backed, VC-backed, publicly listed, subsidiary, or owner-managed. Base it on the `ownership` label and the dated deal rows, not `ultimate_ownership`, which can contradict them. Then name the primary owners for that type:
  - **PE- or VC-backed:** the backing investors, lead investor first, with the deal that brought them in.
  - **Subsidiary:** the parent company.
  - **Owner-managed:** the founder(s) or individual owner(s), where held.
  - **Listed:** an investor or shareholder breakdown where Megabuyte holds one. Otherwise say "shareholder breakdown not held".
  - Don't describe ultimate parents or holding structures beyond this.

## 4. Citing

**Provenance: show what came from Megabuyte and what the AI produced.** Every part of an answer, and of any file the user asks for, falls into one of four kinds. Label them so a reader can tell them apart at a glance:

| Label | Use for |
|---|---|
| **Megabuyte data** | Figures, deals, people, ownership and classifications exactly as the Megabuyte MCP returned them |
| **Megabuyte research (AI summary)** | Megabuyte analysts' views (Company Analysis, Market Analysis, quarterlies, analyst comment in news), summarised in AI words |
| **AI calculation** | Numbers you computed from Megabuyte data: medians, means and quartiles of precedents, positions, derived adjusted EBITDA, growth you calculated, counts you tallied |
| **AI analysis** | Your own judgement: rankings, "fit", rationales, the "Read", verdicts, questions to probe, capability clusters, summaries and synthesis |

How to apply them:
- **Section headings** carry the label after a dot, e.g. "Financial trajectory · Megabuyte data", "Megabuyte view · Megabuyte research (AI summary)", "Read · AI analysis". A section that mixes kinds takes the label of its main content, and the other kinds are marked inline.
- **Tables:** Megabuyte data columns need no mark. Columns you computed or judged are headed with "(AI)", e.g. "Rank (AI)", "Rationale (AI)", "Median (AI calc.)", and the table's source note says "Source: Megabuyte www.megabuyte.com; columns marked (AI) are AI-generated from Megabuyte data".
- **Inline:** in running text, mark an AI judgement inside a Megabuyte-data paragraph with "(AI view)", and a computed figure with "(AI calc.)".
- **Never label AI output as Megabuyte's.** Never present an AI ranking, calculation or summary as a Megabuyte figure or view.
- **Closing lines** of every substantive answer, replacing a single source line:
  - **Source: Megabuyte www.megabuyte.com**: [what came from Megabuyte, e.g. "company financials, deal records and the 9 Jul 2025 Company Analysis via the Megabuyte MCP"].
  - **AI-generated:** [what the AI produced, e.g. "the ranking, rationales, precedent statistics and summaries"].

- Use each row's `Link:` exactly as returned. A row without a Link gets title and date only. The one exception is company profiles, below; never build any other megabuyte.com URL.
- **Research passages carry their link too.** `semantic_search` results give it inside the passage: `report.url` for reports (also in the `notes` as "read the report"), and the passage's own URL field for news and analyses. Link the title of every report, analysis or article you cite or list, using that URL exactly. A report without a URL gets title and date only.
- **Every cited piece of research is a linked title,** e.g. "[Quarterly Insight Report – IT Managed Services – Q3 2026](url) (30 Sep 2026)". Never cite research as title and date alone when the tool returned a link.
- **Link every company you name to its Megabuyte profile:** `https://www.megabuyte.com/app/companies/{mb_id}/alias`, using the company's `mb_id` from any tool result.
  - This is the only URL you may build. Show it as a markdown link on the company name.
  - A company without an `mb_id` is named without a link.
- **Location:** give a company's town or city, not a postcode area code. Use the post town of its registered-office postcode district (e.g. "Altrincham" for WA14). If you're unsure of the post town, use the place name the server attaches to the postcode (e.g. "Warrington area").
- Date every piece of research or analysis you cite ("Megabuyte Company Analysis, 14 May 2026"). A 2019 note is not a current view.
- Never show internal ids (company_id, deal_id, person_role_id) to the reader.
- Signed-out readers hit a login page on megabuyte.com links. That is the paywall, not a broken link.

## 5. Freshness flags

- **Board records lag the news.** If a tool flags the board as possibly out of date (`may_be_out_of_date`), or news after the board record reports a change, read the article. Report the change it describes (e.g. a new CEO), and say the board record hasn't caught up. Never present a departed or deceased executive as in post.
- **Analysis predates events.** A Company Analysis is dated. If newer news exists (`analysis.newer_news_articles`), put the news beside the analysis and say which is newer.
- If `semantic_search` reports `reranking_refused` or `lexicalOnly`, say once that the research passages are a coarser match.

## 6. Gaps are answers

Coverage is uneven by design, so treat empty results carefully:

| Result | Say | Don't say |
|---|---|---|
| No deals for a company | "Megabuyte records no deals for X" | "X has never done a deal" |
| No financials | "No accounts within two years are held" | "X has no revenue" |
| No people | "Board data isn't held for X" | "X has no CFO" |
| Not-held metric (ARR, churn, NRR, customers, TAM, share price, lenders, advisers, earn-outs) | "Megabuyte doesn't hold [metric]", then offer the nearest held proxy (e.g. gross margin or recurring-revenue mentions in analyst text for ARR) | An estimate |

If `plan_query` routes to a `not_held_*` intent, lead with that statement. Don't bury it.

Put a short **Coverage notes** line at the end of any substantive answer, listing what was thin or missing.

## 7. Accuracy check

Before sending anything number-heavy, call `check_answer` with the draft and fix whatever it lists.

## 8. Answers and files

**The Megabuyte skills answer in chat.** They provide no export tooling of their own: no Megabuyte templates, styling, logos or document scripts.
- Use concise prose, with tables where the data is tabular.
- **No export offers.** Don't end answers by offering a document.
- **If the user asks for a file** (a deck, report, spreadsheet or document of their own), that's fine: create it with Claude's standard file tools and skills, as for any other request.
  - Don't apply Megabuyte branding, logos or the Megabuyte "Prepared with Megabuyte data" lockup, and don't present the file as Megabuyte's work. It's the user's document.
  - Keep the attribution and provenance labels (§4): wherever Megabuyte data or research appears in the file, add **Source: Megabuyte www.megabuyte.com**, and mark AI-generated content the same way as in chat, e.g. as a footnote under each table or chart, or a source line on each slide.
- **Attribution in chat:** end every substantive answer with the two closing lines from §4: what came from Megabuyte, and what is AI-generated.
- **No disclaimers or terms talk, in chat or in files:**
  - Don't add "Not investment advice" or any other disclaimer.
  - Don't mention Megabuyte's terms and conditions, its Content Usage Guidelines, licences or sharing rules, and don't link them.
  - The only required line is the source attribution against Megabuyte data and content.
- **Megabuyte content only.** Every figure, name and view in the answer comes from the Megabuyte tools (§1). Your own reasoning (rankings, "fit", inferences) is labelled as AI analysis (§4), and nothing comes from general knowledge or the web.

## 9. Tone

Write for PE investors, corporate financiers and executives: direct, specific and unhyped. Lead with the answer. UK spelling.

## 10. Fetching sensibly

- **Financial history:** at most 5 periods unless the user asks for more. Use 2 for comps.
- **Results:** prefer counts, aggregates and population statistics (`total_matched`, `benchmark_financials`) over pulling every row.
- **Paging:** page when the answer needs the full set (every match in a route, or every disclosed multiple in a precedent set), up to 100 rows. If more match, narrow the scope (period, sub-peer group, size band, a tighter keyword expression) and say what was left out.
- **No repeats:** don't re-fetch what's already in the conversation, and don't fetch "just in case" sections the answer won't use.
- **Batch:** one call with several ids rather than one call per company.
- **Research in your own words:** summarise Megabuyte research rather than quoting it at length; a short phrase in quotes is fine.

## 11. Finding the right companies: use every route

Megabuyte's taxonomy files each company in one sub-peer group. Real markets, buyer pools and peer sets cut across it: payments players sit in Payments, Banking, Financing and software leaves. So whenever a skill has to *find* companies (targets, buyers, a market's players, peers, consolidators), run **all four routes**, at the same level, then merge the results. **All four are required, not optional.** An answer built from the taxonomy alone is incomplete, however good it looks:

1. **Taxonomy:** `search_companies` or `get_deals` over the leaves the plan resolved.
2. **Keywords:** `search_companies` with `keywords` (the company's own crawled terms). Use `guided_keywords: true` first to read which keywords exist, then screen on the 3–6 strongest. **`keywords` is one search expression, not a list:** quote each phrase and join them with OR (or AND / NOT), e.g. `"penetration testing" OR "managed SOC" OR "cyber security"`. Keep it within 200 characters; only letters, numbers, spaces, quotes, brackets and `.|&!` are allowed. This catches companies filed elsewhere that describe themselves in the theme's terms.
3. **Similar companies:** `find_similar_companies` seeded on the subject, or on the 2–3 leading companies the first two routes found; and `search_companies` with `similar_to` (companies whose own descriptions read like the seed), which can take size and ownership filters in the same call. These are the businesses that read like them, whatever their classification.
4. **Analyst commentary:** `semantic_search` across news, reports, Company Analysis and Market Analysis, phrased to surface *company names*, not background, for companies the analysts have discussed in this context (e.g. "consolidators in managed security", "likely acquirers of payments software businesses"). It samples, so treat it as evidence for inclusion, never as a count.

Then:
- **Merge and de-duplicate by group.** One row per business, under its trading name.
- **Record each company's route(s)** in a "Found via" column (taxonomy / keywords / similar / analyst commentary). A company found by several routes is a stronger fit, so say so.
- **Widen up the taxonomy** (sub-peer group → peer group → sector) only if all four routes together are thin, and say you widened.
- **Mark keyword and similarity matches as self-description, not verified capability.**
- **Review the whole match set, by paging.** Each call returns at most 25 rows. That is a page size, not a limit on the search. Page with `offset` until `next_offset` is null, up to 100 companies per route (§10). Never stop at the first page and never present a first page as the result.
- **If a route matches more than 100:** keep the *closest* matches, never the largest.
  - Lookalike searches: leave `sort_by` unset, so results come closest first (`find_similar_companies` is nearest-first; `search_companies` with `similar_to` is ordered by relevance when `sort_by` is omitted).
  - Keyword searches have no closeness order, so tighten the expression or add a size band until the set is 100 or fewer.
  - Never sort a discovery route by revenue (that ranks by size, not fit), except in a market map, whose point is the largest players.
- **Deal look-ups over many companies:** `get_deals` takes up to 200 company ids in one call, so pass every id from every route at once (in two batches if needed), then page the deals 25 at a time.
- **State the routes in the answer.** Directly under the headline, add one "Routes run" line giving each route's count, e.g. "Routes run: taxonomy 66 matched (all reviewed) · keywords 41 · similar companies 23 · analyst commentary 4 named · 112 unique after merging". If a route returned nothing or couldn't run, say so and why. Never present a list as complete when a route was skipped. A route whose scope the server changed (see `guard_notes`, §2) doesn't count as run until it has been re-run correctly. **Never decide on your own to skip a required route to keep the answer shorter.** If a skill's priority rules allow a skip, state it in the Routes run line at the top, not at the end.

## 12. Working alone

Each Megabuyte skill is complete on its own. Subscribers may switch some off, so never depend on another being installed.
- Everything a skill needs is in its own folder: these conventions.
- When a request also covers a neighbouring job (e.g. a brief that asks about deal multiples), do that part yourself, briefly, with the MCP tools and these rules. Don't tell the user to use, install or switch on another skill, and don't name skills to the user.
- Every rule here (figures, citations, sourcing) applies to every part of the answer, whichever skill is running.
