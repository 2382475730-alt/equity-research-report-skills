"""Create a fresh research workspace; never overwrite an existing directory."""
import argparse
import json
from pathlib import Path

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace', type=Path)
    p.add_argument('--company', required=True)
    p.add_argument('--ticker', required=True)
    p.add_argument('--valuation-date', required=True)
    p.add_argument('--cutoff', required=True, help='ISO8601 timestamp with UTC offset')
    p.add_argument('--language', choices=['zh', 'en'], default='zh')
    a = p.parse_args()
    from datetime import date, datetime
    date.fromisoformat(a.valuation_date)
    if datetime.fromisoformat(a.cutoff).utcoffset() is None:
        p.error('--cutoff requires an explicit UTC offset')
    a.workspace.mkdir(parents=True, exist_ok=False)
    for d in ['sources', 'evidence', 'model', 'report', 'qa']:
        (a.workspace/d).mkdir()
    write_json(a.workspace/'project.json', {
        'company': a.company, 'ticker': a.ticker,
        'valuation_as_of': a.valuation_date, 'information_cutoff_at': a.cutoff,
        'language': a.language, 'currency': 'CNY', 'presentation_unit': 'RMB hundred million',
        'audience': None, 'purpose': None, 'business_perimeter': None,
        'forecast_horizon': None, 'methods': [], 'requested_formats': ['docx', 'pdf'],
        'materiality_policy': None
    })
    for n in ['sources', 'facts', 'assumptions', 'claims', 'gaps']:
        write_json(a.workspace/'evidence'/f'{n}.json', [])
    write_json(a.workspace/'model/manifest.json', {'command': None, 'runtime': None,
                                                'inputs': [], 'code': [], 'outputs': []})
    write_json(a.workspace/'report/number_bindings.json', [])
    write_json(a.workspace/'report/manifest.json', {'deliverables': []})
    write_json(a.workspace/'qa/review.json', {'reviews': {}, 'reviewed_files': [], 'pages': None})
    print(a.workspace.resolve())

if __name__ == '__main__':
    main()
