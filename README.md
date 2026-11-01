<div align="center">

**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

# Equity Research Report Skills

### From primary sources to a reproducible valuation and a readable report

Two independent Codex skills for listed-company research, in Chinese and English.

[Quick start](#quick-start) · [Workflow](#workflow) · [Deliverables](#deliverables) · [FAQ](#faq) · [Verification](#verification)

</div>

## Quick start

1. Copy **one complete folder** into your Codex skills directory:
   - [English skill](skills/equity-research-report-en/)
   - [Chinese skill](skills/equity-research-report-zh/)
2. Restart Codex so it can discover the skill. Then supply the company, valuation date, information cutoff and time zone, audience, scope, and requested formats.
3. Ask, for example:

   > Use $equity-research-report-en to research and value the specified company as of the stated cutoff. Use official originals, follow my template, and deliver a reproducible model and report with key sensitivities and conditions that would change the conclusion.

The Japanese, Korean, and Arabic pages translate this introduction; the executable skill instructions themselves are available in English and Chinese.

## Workflow

1. Define the assignment and initialize a new workspace.
2. Acquire original sources, record their provenance, and reconcile financial facts and definitions.
3. Develop research judgments, choose suitable methods, and build a reproducible forecast and valuation.
4. Write the report and check its numerical bindings, supporting evidence, and rendered pages.
5. Deliver the requested report, model, inputs, source records, and review results, explaining material gaps and conditions.

The approach draws on research and human revisions of a Changjiang Power report. Its numbers, sector model, and chapter structure are not defaults for other companies.

## Deliverables

Each skill includes five references on research, modeling, writing, delivery, and the Changjiang Power case, plus three Python standard-library helpers. The helpers initialize a workspace, capture supplied public URLs and failed attempts, and check machine-verifiable relationships. Commands and registry formats are in each skill's `references/delivery.md`.

The helpers do **not** automatically search, value a company, or write a complete report. Source retrieval is not the same as verification or admission into a model; economic judgments and page quality require substantive review. The project has not established unattended end-to-end research production.

## FAQ

**Which skill should I install?** Choose the Chinese or English folder for the language of the skill instructions. They are independently installable and do not depend on one another.

**What should I provide?** At minimum, identify the company and intended use. A valuation date, information cutoff and time zone, audience, scope, template, and deliverable formats help define the assignment.

**Can the result be used without review?** No. Check sources, assumptions, calculations, judgments, and the final rendered report. A successful automated check does not prove an economic assumption or an investment conclusion.

## Verification

From the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests use temporary directories and a local HTTP server. They do not test access to real issuers or authenticated services, or establish unattended report production. The repository does not include the full original report, private working papers, or source collection.
