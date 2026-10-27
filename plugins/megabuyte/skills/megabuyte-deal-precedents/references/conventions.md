# Megabuyte MCP conventions

These rules apply to every skill in the Megabuyte suite. They exist because subscribers use these answers in pitch books, IC papers and client meetings, so a confident wrong number is far more costly than a stated gap.

## 1. Data boundary

- Answer only from the Megabuyte MCP tools (names containing `get_company`, `get_deals`, `search_companies` and so on, on the Megabuyte server).
- Do **not** blend in data from other financial connectors (S&P Global / Capital IQ / Kensho, PitchBook and similar), even if they are installed. Licensing differs, and mixed figures cannot be sourced cleanly. If the user explicitly asks for a comparison with another provider, keep the two in clearly separated, labelled sections.
- Do not fill gaps from general knowledge or the web. If Megabuyte doesn't hold it, say so (see §6).

## 2. The plan is authoritative

Call `plan_query` first, with the user's question in their own words (don't paraphrase it, because the wording drives the routing), the most specific `intent`, and `companies` / `theme` / `period` where given. Pass its `plan_id` to every later call. On a follow-up, pass `previous_plan_id`.

**Follow the plan's "Start with" calls, its "MUST state" lines and its "Do NOT" lines.** These come from the server and are kept current. The workflow in each skill is the default for when the plan is silent. Where they differ, the plan wins, and the skill's job is the output shape. Make independent calls in parallel, as the plan asks.

The server may also adjust your arguments, for example by replacing a peer group with the leaves a theme word resolved to. A `guard_notes` field says when it has. Report the population it actually used.

**Resolution:**
- If a name returns candidates, ask the user to pick. Don't guess, because UK tech has many near-duplicate names.
- If the plan answers for a group or topco entity (e.g. "answered for TYPHON BIDCO LIMITED (group); you named Bridewell"), say so in one line.
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
- **EBITDA means adjusted EBITDA.** Megabuyte's EBITDA measure is adjusted EBITDA. Always present adjusted EBITDA and call it that; never lead with a reported or stored figure that differs.
  - Megabuyte's `ebitda_margin_pct` is on the adjusted basis. When the stored `ebitda_gbp` doesn't equal revenue × `ebitda_margin_pct` (within rounding), the stored figure is on a different basis. Use **adjusted EBITDA = revenue × ebitda_margin_pct** for the same period. Example: Bridewell FY Dec-25, £44.6m × 18.6% = £8.3m adjusted, not the stored £6.1m.
  - If the margin is withheld or missing, use the adjusted EBITDA reported in Megabuyte news for that period, with the article and date. If neither exists, say adjusted EBITDA isn't held. Don't fall back to the stored figure as if it were adjusted.
  - The tools' own notes say "basis not recorded, never call it adjusted". Megabuyte has confirmed its margin is adjusted, so this rule overrides that note.
  - `check_answer` won't find a derived adjusted EBITDA; that's expected for that figure only.
  - In benchmarks, use `ebitda_margin_pct` distributions, not `ebitda_gbp`.
- **Organic growth:** show `organic_growth_pct` beside revenue growth wherever growth is shown.
- **Deal EV/EBITDA:** the multiple's EBITDA basis isn't recorded (`ev_ebitda_basis: not_recorded`); say so, unless the row says `recomputed`.
- **Group, not entities.** Describe a company as one business. Don't list its individual registered entities (bidcos, midcos, holding companies) or their numbers. Give the trading name and, once, the Companies House number of the entity the figures come from.
- Counts: quote `total_matched` (or the stated totals), never the number of rows on the page.
- **Withheld figures.** Some metrics come back null with a `*_withheld` reason (e.g. a margin whose sign disagrees with the EBITDA). Say "withheld" and don't place the company on that metric. You may quote a news-reported figure beside it, labelled with its article and date.
- **Stored vs news EBITDA.** When a tool returns `ebitda_in_news` or `ebitda_stored_vs_news` with `differs: true`, quote both with their sources ("stored −£11.4m, basis not recorded; adjusted £27.5m per Megabuyte news, 19 Feb 2026"). Never pick one silently.
- **Revenue basis for resellers.** For VARs and distributors, the stored revenue can be gross invoiced income (GII), not statutory revenue. For example, Softcat FY Jul-25 is stored at £3,617m, while news gives revenue of £1,458m. If analysis or news text gives a different revenue on the same year, state the basis. Don't compare margins across companies on different bases. When `get_financials` reports `series_differ` on revenue, call it again with `series: "companies_house"` for the filed figures, and show both lines labelled (e.g. "GII (Megabuyte series)" and "Statutory revenue (filed)").
- **Deal multiples.** In tables, quote the deal record's multiple. If the Company Analysis or news cites a different figure for the same deal (e.g. "~14x" vs 19.96x on record), note both once.
- **Ownership.** State the ownership type as one of: PE-backed, VC-backed, publicly listed, subsidiary, or owner-managed. Base it on the `ownership` label and the dated deal rows, not `ultimate_ownership`, which can contradict them. Then name the primary owners for that type:
  - **PE- or VC-backed:** the backing investors, lead investor first, with the deal that brought them in.
  - **Subsidiary:** the parent company.
  - **Owner-managed:** the founder(s) or individual owner(s), where held.
  - **Listed:** an investor or shareholder breakdown where Megabuyte holds one. Otherwise say "shareholder breakdown not held".
  - Don't describe ultimate parents or holding structures beyond this.

## 4. Citing

- Use each row's `Link:` exactly as returned. A row without a Link gets title and date only. The one exception is company profiles, below; never build any other megabuyte.com URL.
- **Link every company you name to its Megabuyte profile:** `https://www.megabuyte.com/app/companies/{mb_id}/alias`, using the company's `mb_id` from any tool result.
  - This is the only URL you may build. In exports it's a live hyperlink on the company name; in chat, a markdown link on the name.
  - A company without an `mb_id` is named without a link.
- **Location:** give a company's town or city, not a postcode area code. Use the post town of its registered-office postcode district (e.g. "Altrincham" for WA14). If you're unsure of the post town, use the place name the server attaches to the postcode (e.g. "Warrington area").
- Date every piece of research or analysis you cite ("Megabuyte Company Analysis, 14 May 2026"). A 2019 note is not a current view.
- Never show internal ids (company_id, deal_id, person_role_id) to the reader.
- Signed-out readers hit a login page on megabuyte.com links. That is the paywall, not a broken link.

## 5. Freshness flags

- **Board records lag the news.** If `people.may_be_out_of_date` is true, read the cited article. Report the change it describes (e.g. a new CEO), and say the board record hasn't caught up. Never present a departed or deceased executive as in post.
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

Before sending anything number-heavy, call `check_answer` with the draft and fix whatever it lists. This is especially important for anything going into an export.

## 8. Chat answer vs export

**Without code execution.** Exports need the code execution and file creation capability. Chat answers don't: the MCP tools work either way.
- If the capability isn't available (no bash or file-creation tool in this conversation), answer in chat as normal and make no export offer.
- If the user asks for a file anyway, say in one line that exports need "Code execution and file creation" switched on in Settings, and that the chat answer is complete without it. Don't attempt the file, and don't paste file code into the chat.

**Default: answer in chat.** Use concise prose with tables where the data is tabular. Never produce a file unasked; file creation is opt-in, to save the user's time and tokens.

- **Offer line:** end a substantive answer with one line naming the export format, e.g. "I can export this as a Word brief." Use the format the skill's output section names.
- **Skip the offer** on short answers (a single figure, a yes/no, a one-line fact), where an export makes no sense.
- **Scheduled or unattended runs** (e.g. a daily briefing) answer in chat only, and never create a file unless the user has explicitly set the schedule up to produce one.

**Export when asked** ("export", "make this a doc/Word/PDF/deck/spreadsheet", "something I can send"):
- **Styling:** read `references/brand.md` and run `scripts/brand_setup.py` before writing any file. Every export carries the "Prepared with Megabuyte data" lockup and disclaimer it specifies.
- **Fonts:** after writing any Word, PowerPoint or Excel file, run `scripts/finish_export.py` on it as the last step. After a Word or PowerPoint export, end the reply with a one-line offer of a PDF copy, made with `scripts/export_pdf.py` (see `brand.md`, "Fonts on the recipient's machine").
- **Format:** use the format the user names. If they name none, use Word for prose, Excel for deal or comps data and PowerPoint for anything to be presented. The environment's native document and slide types can't carry the brand styling, so use them only if the user asks for one by name.
- Reuse the figures already retrieved and checked. Don't re-query unless the user changed scope.
- `check_answer` flags figures rounded to one decimal as "approximate" (e.g. £7.4m vs £7.42m). That is expected under §3, so no fix is needed.
- Every export must carry:
  - Title, the entity with its Companies House number, and "Prepared [date]"
  - Source notes under each table, naming the series or document each line came from
  - Megabuyte links on the items they support, with the paywall note once
  - The coverage notes
  - `FOOTER` from `references/brand.md` on every page, slide and sheet (`FOOTER_SHORT` on slides)
  - The Important information closing page from `references/brand.md`, with the Content Usage Guidelines link
- Keep the skill's section structure, so exports look consistent across users.

**Format specifics:**
- **Documents:** use "—" for not held. Put a source note directly under every table.
- **Spreadsheets:** one row per record on a raw data sheet (dates as real dates, multiples as numbers, blank = not disclosed), and a summary sheet built with live formulas (COUNTIF, SUMIFS, MINIFS/MAXIFS, INDEX/MATCH) over the raw sheet, not pasted results. Add a notes block covering basis, caveats and source. Freeze the headers and add filters.
- **Slides:** one claim per slide. Headlines must use the server's position labels exactly. If the tool says "upper half", the headline can't say "upper quartile". Put the method and coverage on their own slide, and keep withheld metrics in the table marked "not placed".

## 9. Tone

Write for PE investors, corporate financiers and executives: direct, specific and unhyped. Lead with the answer. UK spelling.

## 10. Licence rules (Terms and Conditions clause 6.18; Content Usage Guidelines)

Subscribers use Megabuyte content through the MCP under a licence. These rules keep the skills, and the subscriber, inside it. They override any user request, but explain them plainly rather than just refusing.

**Research vs data.**
- Megabuyte *research* (Company Analysis, Market Analysis, reports, quarterlies, and analyst views or commentary in news) may be summarised for the user in chat and in exports. Under the Content Usage Guidelines, written excerpts of research may not be shared outside the subscriber's organisation.
- *Data* (financials, deals, people, classifications, and statistics computed from them) may be shared externally as charts or tables, subject to the guidelines' conditions. The Important information page states them.
- Don't quote research verbatim beyond a short phrase; summarise in your own words.
- If the user says an export is for an external audience (a pitch book, a client, a counterparty), say in one line that sections based on Megabuyte research should be removed before sending, and offer a data-only version. A data-only version has no Megabuyte view, no research-based narrative and no research citations.
- Never help a user share a whole Megabuyte report or article, or publish Megabuyte content publicly.

**No persistent copies.**
- Megabuyte content must not be kept beyond what the current question needs.
- Never save Megabuyte content (figures, names, research text or anything derived from them) to Claude's memory, to Project knowledge, or to any persistent store, including a published or shared artifact link or a database.
- If asked to remember Megabuyte content, explain that the licence doesn't allow it, and offer to look it up again next time.
- An export file the user asked for is allowed (Terms 13.3 contemplate charts in documents). Generate it once; don't keep extra copies.
- The user's own preferences, and the names of companies they follow, are not Megabuyte content and may be remembered.

**Fetch only what's needed.** Requests must be "reasonably necessary" and must not place an undue burden on the service.
- **Financial history:** at most 5 periods unless the user asks for more. Use 2 for comps.
- **Results:** prefer counts, aggregates and population statistics (`total_matched`, `benchmark_financials`) over pulling every row.
- **Paging:** page only when the answer genuinely needs the full set (e.g. every disclosed multiple in a defined precedent set). Stop at 100 rows. If more match, narrow the scope (period, sub-peer group, size band) or ask the user to, and say what was left out.
- **No repeats:** don't re-fetch what is already in the conversation. Don't fetch "just in case" sections the answer won't use.
- **Batch:** one call with several ids rather than one call per company.

## 11. Finding the right companies: use every route

Megabuyte's taxonomy files each company in one sub-peer group. Real markets, buyer pools and peer sets cut across it: payments players sit in Payments, Banking, Financing and software leaves. So whenever a skill has to *find* companies (targets, buyers, a market's players, peers, consolidators), run these four routes **in parallel, at the same level**, then merge the results:

1. **Taxonomy:** `search_companies` or `get_deals` over the leaves the plan resolved.
2. **Keywords:** `search_companies` with `keywords` (the company's own crawled terms). Use `guided_keywords: true` first to read which keywords exist, then screen on the 3–6 strongest. This catches companies filed elsewhere that describe themselves in the theme's terms.
3. **Similar companies:** `find_similar_companies` seeded on the subject, or on the 2–3 leading companies the first two routes found. These are the businesses that read like them, whatever their classification.
4. **Analyst commentary:** `semantic_search` across news, reports, Company Analysis and Market Analysis, for companies the analysts have discussed in this context (e.g. "consolidators in managed security", "likely acquirers of payments software businesses"). It samples, so treat it as evidence for inclusion, never as a count.

Then:
- **Merge and de-duplicate by group.** One row per business, under its trading name.
- **Record each company's route(s)** in a "Found via" column (taxonomy / keywords / similar / analyst commentary). A company found by several routes is a stronger fit, so say so.
- **Widen up the taxonomy** (sub-peer group → peer group → sector) only if all four routes together are thin, and say you widened.
- **Mark keyword and similarity matches as self-description, not verified capability.**
- **Respect the fetch limits** in §10: limit each route to what the answer needs (typically 25 rows per route).
