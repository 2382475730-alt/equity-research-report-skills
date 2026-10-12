# Delivery and verification

## Stage outputs

| Stage | Required result | Basis for continuing |
|---|---|---|
| Assignment | project.json, artifact index, research questions | Dates, perimeter, audience, and outputs established |
| Acquisition/reconciliation | Originals and source/fact/conflict registries | Important fields located with admissible timing and definitions |
| Research judgment | Claims, assumptions, gaps | Mechanisms, model treatment, and reversal conditions |
| Model | Executable code/formulas, inputs, results, manifest | Recomputable valuation and reconciled statements/cash/claims |
| Report | Narrative, selected tables/figures, numerical bindings | New readers understand judgments and reasons |
| Delivery | Requested formats, calculations/page reviews, index | Current numbers/versions and adequate material qualifications |

If the user requests one stage, perform that stage and necessary dependencies. A complete report request cannot end at source collection or a reusable prompt. Directory creation and passing helpers do not complete research.

The initializer creates `sources/`, `evidence/`, `model/`, `report/`, and `qa/`. Preserve historical artifacts where they are and link through an index. Do not delete failed work, conflicts, or earlier deliveries merely to tidy a workspace.

## Commands

Use an available Python3 runtime and substitute the target workspace.

```text
python scripts/init_workspace.py research_run --company "Example Company" --ticker EXAMPLE --valuation-date 2026-09-30 --cutoff 2026-09-30T15:30:00+08:00 --language en
python scripts/capture_source.py ORIGINAL_PUBLIC_URL --out research_run/sources --expect pdf
python scripts/check_bundle.py research_run --stage data
python scripts/check_bundle.py research_run --stage model
python scripts/check_bundle.py research_run --stage delivery --out research_run/qa/machine_check_01.json
```

Initialization rejects an existing directory. Capture preserves new files and failed-attempt metadata. Check logs cannot overwrite existing files. Acquisition only marks `captured_not_admitted`; establish publication timing from the original or announcement index. The checker does not execute a model, retrieve sources, or score prose.

## Registry formats

Registries are JSON arrays except `project.json`, manifests, and review records. Use stable IDs. Store detailed evidence once and link it through citations/output bindings.

Complete `project.json` fields `audience`, `purpose`, `business_perimeter`, `forecast_horizon`, `materiality_policy`, and `methods`. Adapt currency, units, and formats; initialization defaults are not decisions or facts. Materiality should reflect changes to judgments, drivers, or forecasts rather than a universally fixed percentage.

An admitted entry in `evidence/sources.json`:

```json
{
  "id": "S01", "title": "Annual report", "publisher": "Issuer",
  "url": "https://issuer.example/annual.pdf",
  "local_path": "sources/annual.pdf", "sha256": "ACTUAL_SHA256",
  "retrieved_at": "2026-10-12T10:00:00+08:00",
  "published_at": null, "published_date": "2026-04-30", "published_date_utc_offset": "+08:00",
  "publication_evidence": "Issuer announcement index dated 2026-04-30",
  "version": "Original disclosed annual report", "admission": "accepted"
}
```

`admission` is `accepted/excluded/unresolved`. Use timezone-qualified ISO `published_at`, or `published_date` with the original publication location's `published_date_utc_offset` for that date. The checker uses local end-of-day to establish whether the entire possible publication interval precedes the cutoff; do not compare calendar dates across timezones directly. If the interval cannot establish availability, admission fails. Publication evidence must have a real basis. Hashed paths must be workspace-relative.

A field in `facts.json`:

```json
{
  "id": "F01", "kind": "fact", "label": "Revenue",
  "value": 100, "unit": "RMB hundred million", "period": "2025",
  "scope": "Consolidated", "locator": "S01 PDF file page 10, row Revenue",
  "source_ids": ["S01"], "raw_value": 10000000000, "raw_unit": "CNY",
  "normalization_rule": "raw_value / 100000000"
}
```

`kind` is `fact/derived/unknown`. Derived entries add `calculation` and fact-ID `depends_on`. Unknowns have `value:null` and a registered `gap_id`. Add currency/tax/perimeter details as needed. The checker verifies structure/references; conversions and accounting definitions still need substantive review.

`assumptions.json`: `id,value,unit,rationale,basis_ids,model_fields,alternatives,effect`. Basis IDs refer to facts or admitted sources. Alternatives specify justified ranges/scenarios, or explain why a range cannot be established rather than inventing endpoints.

`claims.json`: `id,judgment,evidence_ids,mechanism,model_treatment,counterevidence,change_condition`. Evidence IDs can reference facts, assumptions, or sources. Record actual contrary evidence or the strongest alternative explanation. If a thesis remains descriptive, model treatment explains that decision.

`gaps.json`: `id,issue,impact,treatment,affected_claims`; optionally add priority and the next acquisition route. Use an empty array when no gaps exist; do not invent gaps to satisfy a form.

## Model and report bindings

`model/manifest.json`:

```json
{
  "command": "python model/run.py", "runtime": "Python version recorded",
  "inputs": [{"path":"project.json","sha256":"ACTUAL_SHA256"}],
  "code": [{"path":"model/run.py","sha256":"ACTUAL_SHA256"}],
  "outputs": [{"path":"model/results.json","sha256":"ACTUAL_SHA256"}]
}
```

Complete this abbreviated example with all actual inputs, including at least `project.json`, `evidence/facts.json`, and `evidence/assumptions.json`, plus configurations and other dependencies. Execute the model before hashing its run artifacts. The checker establishes file agreement with that recorded run, not calculation correctness.

An entry in `report/number_bindings.json`:

```json
{
  "label": "Baseline conditional value", "model_path": "model/results.json",
  "pointer": "/baseline/per_share", "value": 33.39,
  "decimals": 2, "scale": 1, "report_location": "Table 17 baseline row"
}
```

The number illustrates the format. Use JSON Pointer, numerical array indices, and `scale` for actual unit conversion. The checker uses decimal ROUND_HALF_UP. Register important table/prose numbers or use equivalent verifiable generation bindings. It checks registered values against outputs rather than automatically extracting every number from DOCX; substantively verify that the registry matches the final report.

`report/manifest.json` contains a `deliverables` array of `path,sha256`. Formats must satisfy `project.requested_formats`.

## Review records and completion boundaries

`qa/review.json`:

```json
{
  "reviews": {
    "sources": {"status":"passed","reviewer":"Reviewer name","reviewer_kind":"ai","scope":"Actual checked source scope","evidence_path":"qa/sources.md"}
  },
  "reviewed_files": [{"path":"report/final.docx","sha256":"ACTUAL_SHA256"}],
  "pages": {"pdf_path":"report/final.pdf","count":28,"reviewed":[1,2],"renderer":"Actual renderer and version"}
}
```

This abbreviated example is incomplete. Reviews must cover `sources,independent_math,model_economics,narrative,layout`. Record actual scope, reviewer, AI/human identity, and an evidence file. Reviewed-file hashes cover final reports, numerical bindings, the model manifest, and outputs. Changed input/code hashes require rerunning and revisiting affected reviews. Count actual PDF pages and list every inspected page.

Independent math uses a different implementation or direct original calculations and states coverage. Reviews need not automatically use multiple agents; consider delegation only when authorized and useful. Economic review covers growth/investment, cash/funding, capital structure, and ownership. Reader review covers judgments, coherence, and conditions. Layout review inspects actual rendered images.

After export, inspect heading hierarchy, contents pages, table numbering, fonts, numeric alignment, repeated headers, row heights, equations, citations, and pagination. For complex equations, use editable mathematics or a verified rendered representation; plain text is not native math. A reference style may use A4, clear black headings, consistent dark table headers, and pale alternating rows, but the user's template controls. Sample font sizes are not universal requirements.

If the preferred renderer is unavailable, diagnose and use an available alternative such as Word export plus PDF rasterization, recording the renderer. Without actual rendering/inspection, report layout as unverified rather than passing a file-existence check.

The delivery index identifies the report, execution command, inputs/results, major conditions, review coverage, and unfinished items. Distinguish verification, reproducibility, economic conclusions, human acceptance, and formal submission. Publication and ongoing monitoring require the user's authorization for those actions.
