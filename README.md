# Equity research and valuation report skills

Two independently installable Codex skills connect primary-source acquisition, financial reconciliation, research judgments, forecasting and valuation, reader-facing writing, and verifiable delivery.

The workflow is distilled from successive Changjiang Power drafts and human revisions. It emphasizes interpretable judgments from accurate evidence, without turning that report's numbers, sector model, or chapter count into universal defaults.

## Choose a version

- Chinese: `skills/equity-research-report-zh/SKILL.md`
- English: `skills/equity-research-report-en/SKILL.md`

Each folder contains five references and three standard-library Python helpers. Neither depends on the other. Copy the complete selected folder into your Codex skills directory.

Example request:

> Use $equity-research-report-en to complete a company research and valuation report as of the specified cutoff. Acquire official originals, follow the supplied template, deliver a reproducible model and report, and state clear judgments, dominant sensitivities, and conditions that would change the conclusion.

Specify company, timing, perimeter, audience, and outputs. Retrieval does not automatically admit evidence into a model. Helpers verify machine-checkable relationships; economic reasoning and page quality require substantive review.

## Contents

`data-research.md` covers originals, periods/versions, definitions, and judgments; `modeling.md` covers forecasting, capital costs, terminal value, and claims; `writing.md` addresses accumulated evidence and caveats; `delivery.md` defines registries and verification; `changjiang-case.md` documents historical strengths and residual weaknesses.

Helpers initialize a workspace, capture supplied public URLs including failed-attempt records, and check sources, numerical bindings, hashes, and review records. Commands are in each version's delivery reference. These are not a complete autonomous agent; they do not automatically search, value, or write the report.

## Local verification

```text
python -m unittest discover -s tests -v
```

Tests use temporary directories and a local HTTP server, without real issuer access or authenticated services. They do not establish unattended report production. Agent orchestration, integration, and real-case acceptance will be designed after the skill content is approved.

Publication contents exclude the full original report, private working papers, and source collection. The workspace-specific review/index is saved separately. This skill version was approved for publication on October 12, 2026. A local Python application for the full workflow is the next design stage.
