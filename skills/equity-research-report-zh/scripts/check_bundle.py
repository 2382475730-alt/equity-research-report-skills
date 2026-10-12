"""Validate traceability and artifact freshness; not an economic or prose audit."""
import argparse
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math
from pathlib import Path

class Checker:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.errors = []

    def require(self, condition, message):
        if not condition:
            self.errors.append(message)

    def read(self, relative):
        return json.loads(self.path(relative).read_text(encoding='utf-8-sig'))

    def path(self, relative):
        raw = Path(relative)
        if raw.is_absolute():
            raise ValueError(f'Path must be workspace-relative: {relative}')
        resolved = (self.root/raw).resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError(f'Path escapes workspace: {relative}')
        return resolved

    def hashed(self, item):
        p = self.path(item['path'])
        self.require(p.is_file(), f'Missing file: {item["path"]}')
        if p.is_file():
            self.require(hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256'],
                         f'Stale or incorrect hash: {item["path"]}')

    def ids(self, rows, label):
        ids = [r['id'] for r in rows]
        self.require(len(set(ids)) == len(ids), f'Duplicate IDs: {label}')
        return {r['id']:r for r in rows}

    def run(self, stage):
        project = self.read('project.json')
        cutoff = datetime.fromisoformat(project['information_cutoff_at'])
        self.require(cutoff.utcoffset() is not None, 'Cutoff requires timezone')
        date.fromisoformat(project['valuation_as_of'])
        for k in ['company','ticker','audience','purpose','business_perimeter','forecast_horizon','materiality_policy']:
            self.require(bool(project.get(k)), f'Complete project.{k}')
        sources = self.ids(self.read('evidence/sources.json'), 'sources')
        facts = self.ids(self.read('evidence/facts.json'), 'facts')
        assumptions = self.ids(self.read('evidence/assumptions.json'), 'assumptions')
        claims = self.ids(self.read('evidence/claims.json'), 'claims')
        gaps = self.ids(self.read('evidence/gaps.json'), 'gaps')
        self.require(bool(sources) and bool(facts) and bool(claims), 'Sources, facts, and claims must be nonempty')
        accepted = set()
        for sid, s in sources.items():
            self.require(s.get('admission') in ['accepted','excluded','unresolved'], f'{sid}: invalid admission')
            if s.get('admission') != 'accepted':
                continue
            accepted.add(sid)
            for k in ['title','publisher','url','retrieved_at','version','publication_evidence']:
                self.require(bool(s.get(k)), f'{sid}: missing {k}')
            retrieved = datetime.fromisoformat(s['retrieved_at'])
            self.require(retrieved.utcoffset() is not None, f'{sid}: retrieval needs timezone')
            if s.get('published_at'):
                pub = datetime.fromisoformat(s['published_at'])
                self.require(pub.utcoffset() is not None, f'{sid}: publication needs timezone')
                if pub.utcoffset() is not None and cutoff.utcoffset() is not None:
                    self.require(pub <= cutoff, f'{sid}: publication after cutoff')
            elif s.get('published_date'):
                pubdate=date.fromisoformat(s['published_date'])
                offset=s.get('published_date_utc_offset')
                self.require(bool(offset), f'{sid}: date-only publication needs its original UTC offset')
                if offset:
                    latest=datetime.fromisoformat(f'{pubdate.isoformat()}T23:59:59.999999{offset}')
                    self.require(latest.utcoffset() is not None, f'{sid}: invalid date-only UTC offset')
                    if latest.utcoffset() is not None and cutoff.utcoffset() is not None:
                        self.require(latest <= cutoff, f'{sid}: date-only interval cannot establish before-cutoff availability')
            else:
                self.require(False, f'{sid}: publication timing missing')
            self.hashed({'path':s['local_path'],'sha256':s['sha256']})
        for fid, f in facts.items():
            kind = f.get('kind')
            self.require(kind in ['fact','derived','unknown'], f'{fid}: invalid kind')
            for k in ['label','unit','period','scope','locator']:
                self.require(bool(f.get(k)), f'{fid}: missing {k}')
            if kind == 'unknown':
                self.require(f.get('value') is None, f'{fid}: unknown must be null, never zero')
                self.require(f.get('gap_id') in gaps, f'{fid}: unknown needs a registered gap')
            else:
                self.require(f.get('value') is not None, f'{fid}: known value cannot be null')
            if isinstance(f.get('value'), float):
                self.require(math.isfinite(f['value']), f'{fid}: nonfinite value')
            if kind == 'fact':
                refs=f.get('source_ids',[])
                self.require(bool(refs) and all(x in accepted for x in refs), f'{fid}: fact requires admitted originals')
            if kind == 'derived':
                self.require(bool(f.get('calculation')), f'{fid}: derived value needs calculation')
                self.require(bool(f.get('depends_on')) and all(x in facts for x in f['depends_on']), f'{fid}: invalid dependencies')
        for aid,a in assumptions.items():
            for k in ['rationale','basis_ids','model_fields','alternatives','effect']:
                self.require(bool(a.get(k)), f'{aid}: missing {k}')
            self.require(all(x in facts or x in accepted for x in a.get('basis_ids',[])), f'{aid}: invalid basis IDs')
            self.require(a.get('value') is not None, f'{aid}: unknown belongs in gaps, not an assumption')
        for cid,c in claims.items():
            for k in ['judgment','evidence_ids','mechanism','model_treatment','counterevidence','change_condition']:
                self.require(bool(c.get(k)), f'{cid}: missing {k}')
            self.require(all(x in facts or x in assumptions or x in accepted for x in c.get('evidence_ids',[])), f'{cid}: invalid evidence IDs')
        for gid,g in gaps.items():
            for k in ['issue','impact','treatment','affected_claims']:
                self.require(bool(g.get(k)), f'{gid}: missing {k}')
            self.require(all(x in claims for x in g.get('affected_claims',[])), f'{gid}: invalid claims')
        if stage == 'data':
            return
        self.require(bool(project.get('methods')), 'Select and explain valuation methods')
        manifest = self.read('model/manifest.json')
        self.require(bool(manifest.get('command')) and bool(manifest.get('runtime')), 'Record execution command/runtime')
        for group in ['inputs','code','outputs']:
            self.require(bool(manifest.get(group)), f'Model manifest needs {group}')
            for item in manifest.get(group,[]):
                self.hashed(item)
        input_paths={i['path'] for i in manifest.get('inputs',[])}
        self.require({'project.json','evidence/facts.json','evidence/assumptions.json'} <= input_paths,
                     'Model inputs must hash project, facts, and assumptions registries')
        if stage == 'model':
            return
        binds = self.read('report/number_bindings.json')
        self.require(bool(binds), 'Report number bindings must be nonempty')
        output_paths={i['path'] for i in manifest.get('outputs',[])}
        for b in binds:
            self.require(bool(b.get('report_location')), f'{b.get("label")}: missing report location')
            self.require(b['model_path'] in output_paths, f'{b.get("label")}: number must bind a hashed model output')
            value=self.read(b['model_path'])
            pointer=b['pointer']
            if pointer and not pointer.startswith('/'):
                raise ValueError('Use JSON Pointer for number bindings')
            for part in pointer.split('/')[1:] if pointer else []:
                key=part.replace('~1','/').replace('~0','~')
                if isinstance(value,list):
                    if not key.isdigit():
                        raise ValueError('JSON Pointer array indices must be nonnegative integers')
                    value=value[int(key)]
                else:
                    value=value[key]
            if value is None or isinstance(value,bool):
                self.require(False, f'{b.get("label")}: bound value is not numeric')
                continue
            quantum=Decimal(1).scaleb(-int(b['decimals']))
            expected=(Decimal(str(value))*Decimal(str(b.get('scale',1)))).quantize(quantum,rounding=ROUND_HALF_UP)
            self.require(expected == Decimal(str(b['value'])), f'{b.get("label")}: displayed number mismatch')
        reports = self.read('report/manifest.json')['deliverables']
        self.require(bool(reports), 'Report deliverables missing')
        formats={Path(r['path']).suffix.lstrip('.') for r in reports}
        self.require(set(project['requested_formats']) <= formats, 'Requested report formats missing')
        for r in reports:
            self.hashed(r)
        qa = self.read('qa/review.json')
        for k in ['sources','independent_math','model_economics','narrative','layout']:
            record=qa['reviews'].get(k,{})
            self.require(record.get('status') == 'passed' and bool(record.get('reviewer')) and
                         record.get('reviewer_kind') in ['ai','human'] and bool(record.get('scope')),
                         f'Substantive review incomplete: {k}')
            if record.get('evidence_path'):
                self.require(self.path(record['evidence_path']).is_file(), f'{k}: review evidence missing')
            else:
                self.require(False, f'{k}: review evidence path required')
        reviewed=qa['reviewed_files']
        for r in reviewed:
            self.hashed(r)
        required={r['path'] for r in reports}|{'report/number_bindings.json','model/manifest.json'}|output_paths
        self.require(required <= {r['path'] for r in reviewed}, 'QA hashes omit report/bindings/model manifest/outputs')
        if 'pdf' in formats:
            pages=qa.get('pages') or {}
            count=pages.get('count',0)
            self.require(isinstance(count,int) and count>0, 'Record actual PDF page count')
            self.require(set(pages.get('reviewed',[])) == set(range(1,count+1)), 'Page coverage incomplete')
            self.require(bool(pages.get('renderer')) and pages.get('pdf_path') in {r['path'] for r in reports}, 'PDF renderer/path missing')

def check(root,stage):
    c=Checker(root)
    try:
        c.run(stage)
    except (KeyError, IndexError, AttributeError, ValueError, TypeError, OSError, ArithmeticError) as e:
        c.errors.append(f'Invalid registry or artifact: {type(e).__name__}: {e}')
    return {'stage':stage,'passed':not c.errors,'errors':c.errors,
            'scope':'Traceability, numeric bindings, hashes, and recorded review coverage only'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace',type=Path)
    p.add_argument('--stage',choices=['data','model','delivery'],default='delivery')
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    result=check(a.workspace,a.stage)
    rendered=json.dumps(result,ensure_ascii=False,indent=2)
    if a.out:
        # Prevent a check log from replacing an input, model, or report artifact.
        target=a.out.resolve()
        if target.exists():
            p.error('--out must be a new file')
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(rendered+'\n',encoding='utf-8')
    print(rendered)
    raise SystemExit(0 if result['passed'] else 1)

if __name__ == '__main__':
    main()
