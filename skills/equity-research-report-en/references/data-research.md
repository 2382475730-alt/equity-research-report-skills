# Primary sources and research judgments

## Acquire against research questions

Map operating cash generation and economic ownership. The operating map covers volume, price, costs, taxes, investment, and working capital. The ownership map covers cash, investments, debt, minority interests, and other claims. Turn each question into an acquisition task: hypothesis, required fields, preferred originals, affected forecast variable, and the consequence of missing information. Prioritize evidence capable of changing the conclusion.

| Question | Preferred originals | Required research output |
|---|---|---|
| What actually earns the money? | Segment statements, operating disclosures, settlement information | Business perimeter and revenue/profit drivers without duplicating subsidiaries and segments |
| Does the advantage create economic value? | Peer disclosures, resources/permits, operating and customer information | Relative advantage, transmission into economics, and conditions |
| Can growth become earnings? | Approvals, budgets, construction progress, pricing mechanisms | Investment→commissioning→revenue→cash timeline and ownership |
| Does profit become shareholder cash? | Cash statements, debt, dividends, related parties, claims | Conversion, funding gaps, and distribution perimeter |
| What does the price imply? | Same-date prices, then-public earnings, original capital-cost inputs | Comparable valuation and market-implied assumptions |

Choose channels by jurisdiction and question. For Chinese issuers, use issuer IR, exchange/CNINFO filings, and original statistical/policy agencies. Trace overseas operations to their local issuer, regulator, or exchange. Vendors can be discovery aids or identified proxies, but cannot be relabeled as official. For US structured filings, see the [SEC's official API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces); check periods, units, and filing versions rather than treating every aggregate as a complete comparable segment disclosure.

## Acquisition and failures

Discover → open the original → preserve it → extract → reconcile → admit. For scans, perform OCR and visually compare important numbers with the page. Preserve original HTML, API responses, or PDF files with locators. Cache by source, version, and cutoff rather than downloading everything again each round.

The same URL can change. Preserve final response URL, retrieval time, SHA256, and version evidence. After a failed route, try the issuer's IR index, announcement identifier, regulatory mirror, or the user's local original. Record the specific missing input after proportionate attempts and continue independent tasks. Restricted access may require the user's existing access; do not claim acquisition that did not occur.

Successful retrieval does not verify a fact; verification does not establish suitability for a model. Assess source reliability, disclosure timing, field definition, and model use separately.

## Two temporal uses

- An operating trend as of the current cutoff may use the latest comparable restatement published before that cutoff, with version/perimeter disclosure.
- Historical point-in-time research, PE, or backtests must use what was public at each historical observation. Do not backfill later restatements or actual outcomes.
- Record reporting period, first publication time, and retrieval time separately. If a same-day publication lacks a time and admission before the cutoff cannot be established, leave it unresolved or excluded.
- A historical original retrieved later can be used when its earlier publication/version is established. A year in the title alone does not prove availability.

## Reconcile fields

Preserve field ID, raw value/unit, normalized value/unit, period, currency, consolidation perimeter, original source ID, and page/table row/clause. Distinguish PDF file page order from printed page labels.

Check generated versus sold electricity; gross versus net prices; group versus subsidiary; operations versus investments; parent versus minority; balances versus flows; project budget versus recognized costs versus remaining payments; and book versus fair value. Budget less construction book cost may proxy remaining construction, but is not automatically remaining cash payments.

Reconcile key fields with totals, cross-statement relationships, and original document review. For conflicts, retain both values, version differences, selection rationale, and affected outputs. Do not average conflicting definitions. Calculate unit conversions rather than editing headings: yuan/100 million→RMB hundred millions; MW×0.1→ten thousand kW; GWh/100→hundred million kWh. Verify conversion formulas independently.

## Turn evidence into judgment

For each thesis, maintain a working card: question; supporting/contrary evidence; mechanism; model variable; forecast direction/magnitude; scope; strongest alternative explanation; and observation that would change the judgment. The narrative need not reproduce the card's structure.

Example: demand growth supports electricity absorption, while water and dispatch constrain sales. Do not assign macro electricity growth directly to company revenue. Model price, sales volume, and utilization separately. Falling settlement prices can coexist with rising demand and lower profits.

Treat substantial gaps according to their effects:

1. Obtainable facts: find the original or reconcile definitions.
2. Estimable inputs: use a justified proxy/range and explain the baseline; do not misclassify it as a disclosed fact.
3. Conclusion-sensitive uncertainties: compute sensitivity, scenarios, or reversal thresholds and state when the conclusion changes.
4. Undefined claims/perimeter: preserve an unknown or conditional expression and limit conclusions to established coverage. Unknown does not mean zero or prove a liability exists.

Results can be clearly positive, neutral, negative, or “the operating advantage is supported, but the price offers insufficient margin of safety.” State the judgment and its rationale rather than merely announcing uncertainty. Do not invent probabilities, precise ranges, or thresholds without a basis.
