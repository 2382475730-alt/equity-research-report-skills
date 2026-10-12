---
name: equity-research-report-en
description: Produce a complete listed-company research and valuation report from primary-source acquisition and financial reconciliation through research judgments, forecasting, reproducible valuation, and reader-facing delivery. Use for deep equity research or a systematic report rebuild, rather than isolated copyediting, a quote lookup, or trading strategies.
---

# End-to-end equity research and valuation reports

Deliver a report that stands alone, reaches clear judgments, traces its numbers to evidence, and includes a reproducible model. Start with original information, analyze economic mechanisms, choose and implement the model, and finish with valuation implications, monitoring indicators, and conditions that would overturn the conclusions. Writing is one part of this process.

## Start the assignment

1. Read the requested report, template, original information, current model, and latest editing instructions. Identify the purpose and version of each artifact. Preserve earlier work and use a new delivery directory.
2. Establish company/security, audience/purpose, valuation date, information cutoff with timezone, business/equity perimeter, forecast horizon, language/units, and deliverable formats. Ask only about missing choices that materially affect conclusions or prevent progress. State reasonable assumptions for other choices and continue.
3. Frame the research questions: how does the company earn, where does growth come from, who receives the cash, what does the market price imply, and what would change the judgment? Acquire information against these questions.
4. Initialize a fresh workspace with `scripts/init_workspace.py` and complete `project.json`. This utility creates the evidence and delivery structure; it does not perform research or implement a forecast model.

## Acquire and reconcile evidence

Follow [Primary sources and research judgments](references/data-research.md). Prioritize issuer filings, exchanges, regulators/statistical agencies, project approvals, and original methodology publications. Use search snippets to locate original material.

- Retrieve information and record publication time, reporting period, version, retrieval time, original locator, and file hash. `scripts/capture_source.py` snapshots a supplied public URL. Use available tools for APIs, restricted services, or local files, while maintaining the same registry.
- Extract from originals and reconcile units, currency, tax treatment, consolidation, restatements, and ownership. Calculate at original precision and round for presentation.
- Evidence suitable for a current description may be unsuitable for a historical test. Do not backfill with information published after the cutoff. Successful retrieval, verified evidence, and model admission are separate decisions.
- Maintain `evidence/sources.json`, `facts.json`, `assumptions.json`, `claims.json`, and `gaps.json`. They support the research and its checks; do not paste these registries into the narrative.

## Reach judgments and build the model

Connect important facts into causal explanations before applying [Forecasting and valuation](references/modeling.md). For each core judgment, record focused evidence → economic mechanism → revenue/profit/cash/equity effect → model treatment → contrary evidence and conditions that would change the judgment.

- Reach directional conclusions where the evidence supports them. Material uncertainty controls the strength of the language; incomplete data does not justify hedging every conclusion.
- Address missing inputs through additional original sources, reproducible derivation, justified ranges/proxies, scenarios, and reverse valuation. If a material gap remains, report a conditional result or narrow the conclusion. Do not invent range endpoints.
- Choose methods appropriate to the business. FCFF is a candidate for nonfinancial operating companies; financial institutions, unusual financing structures, or asset-led businesses may require different methods. Explain the choice.
- Use one reproducible system for forecasts, funding budgets, valuation, and report numbers. Distinguish historical facts, research assumptions, and computed outputs. An earlier result does not constrain a revised conclusion.
- Explain differences between methods. FCFF and EVA under shared assumptions establish computational consistency; PE provides a different market observation. Correlated outputs are not independent votes and should not be arbitrarily averaged.
- When evidence, definitions, or methods change, update affected calculations, tables, charts, narrative conclusions, and checks.

## Write and format the report

Follow [Writing for the reader](references/writing.md) and [Delivery and verification](references/delivery.md). A useful path is business and cash sources → industry constraints and advantages → earnings forecasts → valuation and market price → risks and conditions that change the judgment. Follow the user's actual template.

- Use connected prose for reasoning and selected tables for comparison and results. Put detailed sources, complete forecasts, checking procedures, and failed attempts in appendices or working papers.
- Explain a limitation where it is defined. Repeat it only when it changes the current judgment. Remove reminders that add no information and retain material qualifications.
- Without a prescribed structure, lead with a short summary of the conclusion, value range/conditions, dominant drivers, and most important reversal conditions. A required template overrides this default.
- Keep conditional valuation labels consistent in headings, table notes, the summary, and final conclusions. Do not display an apparently unconditional baseline while burying its substantive conditions later.
- Generate numerical tables from model outputs. Verify the model-to-report bindings and numbers embedded in prose.
- Give tables a specific purpose, sequential captions, periods/units/perimeter, actual-versus-forecast labels, necessary sources, and a brief interpretation. Write narrative reasoning as prose.
- Follow the user's reference style with semantic headings and an updatable contents field. Render the final DOCX/PDF and inspect pages, equations, repeated table headers, headings, and references. XML inspection or successful file generation does not establish visual quality.

## Completion

Run `scripts/check_bundle.py WORKSPACE --stage delivery` for machine-checkable consistency, then finish substantive review. Registry formats and commands are defined in the delivery reference.

Deliver the requested report, runnable model and inputs, necessary originals and registries, independent calculations/page review records, and conclusions with monitoring conditions. Explain which findings are verified, which rely on estimates, and which conditions matter most. Passing assistant checks does not prove economic assumptions.

If one acquisition channel fails, try a proportionate alternative and continue independent work. Explain the specific effect of material unresolved gaps. Do not replace judgment with generic caveats or label partial completion as a complete workflow.

## Optional references

- Read [The Changjiang Power case](references/changjiang-case.md) when the request needs the workflow's provenance, rewriting examples, or hydropower drivers. Case parameters are not defaults for another company.
- Helpers use the Python standard library and do not require a particular search connector, Word installation, or the other language version. Use suitable document/spreadsheet tools when available; otherwise choose verifiable alternatives and record limitations.
- Execute the current user's authorized research and local delivery. Publication, repository creation, pushing, and uploading follow the user's authorization for that action. This skill is not an already validated unattended research agent.
