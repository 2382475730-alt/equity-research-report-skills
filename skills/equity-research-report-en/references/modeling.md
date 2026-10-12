# Forecasting and valuation

## Methods and perimeter

Start from cash generation and economic ownership. Consider FCFF for nonfinancial operating companies with investment and debt. For banks/insurers, debt may be an operating input; do not force an enterprise-value-minus-debt model. Equity cash flow, residual income, or other suitable methods may apply. Asset/SOTP methods must reconcile operating perimeters and claims. Explain each method's purpose, assumptions, and relationship to the primary method.

Define currency, units, periods, and ownership before computing. Match cash flow and discount rates: FCFF/WACC and FCFE/Ke. Full-consolidation cash flows require corresponding minority claims; do not also multiply the same asset by its ownership percentage.

## Reproducible operating forecasts

1. Start with reconciled financial statements and business data. Lock disclosed interim actuals and forecast the remaining period separately. Doubling interim values is an identified simplification, never an actual fact.
2. Forecast segment revenue through economic drivers: sold electricity×net settlement price, effective project capacity×price×commissioning fraction, or customers/units×unit revenue. Reconcile segment and consolidation eliminations.
3. Separate cash costs, fixed/variable costs, depreciation, taxes, and nonoperating items. Explain whether growth reflects volume, price, acquisition, efficiency, or accounting.
4. Distinguish maintenance, replacement, and growth investment. Connect construction, commissioning, depreciation, project payables, and payment timing. Allocate investment and working capital to forecast growth.
5. Build financing/dividend budgets and show borrowing or repayment needs. Count interest and capitalized interest once in the appropriate places.
6. Reconcile profits, the balance sheet, cash changes, parent/minority ownership, EPS, and FCFF. Investigate residuals rather than balancing with unexplained “other” entries.

Common FCFF relationships:

`NOPAT = operating EBIT × (1 − operating tax rate)`

`FCFF = NOPAT + depreciation − cash capital expenditure − change in operating working capital`

Adapt cash, taxes, and capitalized items to the actual definitions. Do not double-count taxes, interest, or construction payables because a generic formula already contains a related item. Operating cash requirements must agree with working-capital definitions, cash bridges, and capital rolls.

## Timing, terminal value, and capital costs

Include cash occurring after the valuation date. At a September-end valuation, use annual forecasts for financial analysis but do not discount already elapsed cash again. Set timing for the remaining quarter and subsequent full years, explain year-end/midyear conventions, and distinguish terminal measurement time from explicit cash-flow timing.

Explain the currency/maturity of the risk-free rate, beta sample and dividend/adjustment treatment, ERP version, country risk, marginal debt cost, tax shields, and capital structure. Low beta or R² does not automatically invalidate CAPM or justify arbitrary premiums; test sample choices, alternative estimates, and value sensitivity.

A fixed WACC alongside forecast debt repayment can express a target capital structure. Explain it. When capital-structure change materially affects value, consider time-varying WACC or APV. Use justified alternatives rather than unexplained parameter replacement.

Terminal value requires sustainable operations and reinvestment, with `WACC > g`. Growth must reconcile with investment and marginal returns. A common relation is `reinvestment rate = g / ROIC`, giving `terminal FCFF = terminal NOPAT × (1 − g / ROIC)`. If ROIC equals WACC, growth alone creates no incremental excess value. Temporarily low maintenance relative to depreciation does not prove indefinitely low reinvestment.

Original methodology references: [cash flows](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/cashflows.htm), [growth and reinvestment](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/growth.htm), and [terminal value and excess returns](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/termvalueexreturns.htm).

## Bridge operating value to common equity

Build an explicit bridge: operating value + nonoperating assets excluded from operating cash + excess available cash − debt − minority claims − other net economic claims. Identify each item's date, perimeter, and measurement as disclosed book value, separate valuation, or research proxy.

Investment profit in forecast earnings does not justify including it in FCFF and adding the investment's value again. Reconcile dividends, accounting profits, and asset values. Restricted cash is not automatically additive. Minority book equity differs from minority cash claims. Address issuance, repurchases, treasury shares, dilution, and other equity allocations. Adding/subtracting peer basic EPS with differing weighted share counts is an approximation requiring explanation.

Keep genuinely undefined claims as symbols/nulls with an impact relationship, never zero. U is not a universal correction for all definition errors, nor proof of an additional liability. Correct identifiable investment/minority errors in their actual bridge items.

## Cross-checks, scenarios, and judgments

EVA requires a complete invested-capital roll, NOPAT, capital charges, terminal value, and equity bridge. Under shared assumptions, it should reconcile with FCFF. Equality is algebraic consistency, not independent economic evidence.

Peer/historical valuations should align dates, profit/share definitions, exceptional items, and business mix. Explain differences from DCF; do not assign arbitrary weights or select multiples to manufacture a favorable result.

Sensitivity identifies influential inputs; scenarios jointly change economically related variables; reverse valuation explains conditions implied by price. Specify affected periods, variable interactions, bridge effects, and what stays constant. Scenario endpoints are not confidence intervals or automatic probabilities.

Answer: what drives the result, which assumptions are weakest, which interpretable combination explains price, and what observation/threshold would overturn the conclusion? Define monitoring indicators, original release channels, observation frequency, and implications. Do not schedule ongoing monitoring unless requested.

## Numerical production and verification

Inputs/configuration → executable model → full-precision JSON/table outputs → report tables/figures and a number registry. Bind report numbers to output fields, units, and rounding. Recalculate formula workbooks and compare with independent calculations; CSV is not a recalculating workbook. Record paths and SHA256 for code, inputs, and outputs in `model/manifest.json`.

Independent checks should cover important historical ratios, main valuation, timing/terminal treatment, equity bridge, and the sensitivities most likely to reverse the conclusion. Add economic checks for funding sufficiency, growth investment, and duplicate claims. Rerunning the same function verifies reproduction rather than independence.
