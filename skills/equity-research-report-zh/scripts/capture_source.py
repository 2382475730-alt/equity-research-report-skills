"""Capture a supplied public URL and provenance. Publication is never inferred."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import uuid

def capture(url, directory, expected='any', user_agent='EquityResearchSourceCapture/1.0', timeout=30, max_bytes=50_000_000):
    if urlsplit(url).scheme not in ('http', 'https'):
        raise ValueError('Only HTTP/HTTPS public URLs are supported')
    if urlsplit(url).username or urlsplit(url).password:
        raise ValueError('Do not embed credentials in source URLs')
    if expected not in ('any', 'pdf', 'json', 'html'):
        raise ValueError('Invalid expected content type')
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    stem = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8]
    meta = {'requested_url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat(),
            'published_at': None, 'published_date': None, 'publication_evidence': None,
            'status': 'failed'}
    try:
        with urlopen(Request(url, headers={'User-Agent': user_agent}), timeout=timeout) as r:
            data = r.read(max_bytes+1)
            if len(data) > max_bytes:
                raise ValueError('Response exceeds maximum size')
            if not data:
                raise ValueError('Empty response')
            meta.update({'final_url': r.geturl(), 'http_status': r.status,
                         'content_type': r.headers.get('Content-Type'),
                         'etag': r.headers.get('ETag'), 'last_modified': r.headers.get('Last-Modified')})
        if expected == 'pdf' and not data.lstrip().startswith(b'%PDF-'):
            raise ValueError('Expected PDF; response may be an HTML error/login page')
        if expected == 'json':
            json.loads(data)
        if expected == 'html' and b'<html' not in data[:4096].lower() and b'<!doctype html' not in data[:4096].lower():
            raise ValueError('Expected HTML document')
        suffix = {'pdf': '.pdf', 'json': '.json', 'html': '.html', 'any': '.bin'}[expected]
        target = directory/(stem+suffix)
        with target.open('xb') as f:
            f.write(data)
        meta.update({'status': 'captured_not_admitted', 'file': target.name,
                     'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    except Exception as e:
        meta['error'] = f'{type(e).__name__}: {e}'
    metadata_path = directory/(stem+'.capture.json')
    with metadata_path.open('x', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return metadata_path, meta

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('url')
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--expect', choices=['any','pdf','json','html'], default='any')
    p.add_argument('--user-agent', default='EquityResearchSourceCapture/1.0')
    a = p.parse_args()
    path, meta = capture(a.url, a.out, a.expect, a.user_agent)
    print(json.dumps({'metadata':str(path),'status':meta['status'],'error':meta.get('error')}, ensure_ascii=False))
    raise SystemExit(0 if meta['status'] == 'captured_not_admitted' else 1)

if __name__ == '__main__':
    main()
