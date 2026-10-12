"""Functional tests only: these fixtures are synthetic, not economic evidence."""
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT=Path(__file__).resolve().parents[1]

def module(path):
    spec=importlib.util.spec_from_file_location(path.stem+'_'+path.parent.parent.name.replace('-','_'),path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def hashed(root,relative):
    return {'path':relative,'sha256':hashlib.sha256((root/relative).read_bytes()).hexdigest()}

def fixture(root):
    for d in ['sources','evidence','model','report','qa']:
        (root/d).mkdir(parents=True)
    dump(root/'project.json',{
        'company':'Synthetic Utility','ticker':'SYNTHETIC',
        'valuation_as_of':'2026-09-30','information_cutoff_at':'2026-09-30T15:30:00+08:00',
        'audience':'Research reviewer','purpose':'Synthetic helper test',
        'business_perimeter':'One synthetic operating unit','forecast_horizon':'One test period',
        'materiality_policy':'Test only; not real financial acceptance',
        'methods':['Synthetic arithmetic'],'requested_formats':['md']})
    (root/'sources/original.txt').write_text('Synthetic original: volume=10; price=2.555',encoding='utf-8')
    dump(root/'evidence/sources.json',[{
        'id':'S1','title':'Synthetic original','publisher':'Test fixture','url':'https://issuer.example/source',
        'retrieved_at':'2026-10-12T00:00:00+00:00','published_date':'2026-09-29','published_date_utc_offset':'+08:00',
        'publication_evidence':'Synthetic prior-day announcement','version':'Fixture v1',
        'admission':'accepted','local_path':'sources/original.txt',
        'sha256':hashed(root,'sources/original.txt')['sha256']}])
    dump(root/'evidence/facts.json',[{
        'id':'F1','kind':'fact','label':'Volume','value':10,'unit':'units','period':'Test',
        'scope':'Fixture','locator':'Original line 1','source_ids':['S1']}])
    dump(root/'evidence/assumptions.json',[{
        'id':'A1','value':2.555,'unit':'Currency/unit','rationale':'Synthetic baseline',
        'basis_ids':['F1'],'model_fields':['price'],'alternatives':'Synthetic price scenario',
        'effect':'Revenue changes with price'}])
    dump(root/'evidence/claims.json',[{
        'id':'C1','judgment':'Revenue follows volume and price','evidence_ids':['F1','A1'],
        'mechanism':'Multiply quantity by price','model_treatment':'Revenue = volume * price',
        'counterevidence':'Volume may change','change_condition':'Revise when price or volume differs'}])
    dump(root/'evidence/gaps.json',[])
    (root/'model/run.py').write_text(
        "from pathlib import Path\nimport json\n"
        "r=Path(__file__).resolve().parents[1]\n"
        "f=json.loads((r/'evidence/facts.json').read_text())\n"
        "a=json.loads((r/'evidence/assumptions.json').read_text())\n"
        "out={'revenue':f[0]['value']*a[0]['value'],'baseline':{'per_share':a[0]['value']}}\n"
        "(r/'model/results.json').write_text(json.dumps(out))\n",encoding='utf-8')
    subprocess.run([sys.executable,str(root/'model/run.py')],check=True,capture_output=True)
    dump(root/'model/manifest.json',{
        'command':'python model/run.py','runtime':sys.version,
        'inputs':[hashed(root,p) for p in ['project.json','evidence/facts.json','evidence/assumptions.json']],
        'code':[hashed(root,'model/run.py')],'outputs':[hashed(root,'model/results.json')]})
    (root/'report/final.md').write_text('Synthetic report: rounded number = 2.56. Not an actual valuation.',encoding='utf-8')
    dump(root/'report/number_bindings.json',[{
        'label':'Rounded test output','model_path':'model/results.json',
        'pointer':'/baseline/per_share','value':2.56,'decimals':2,'scale':1,
        'report_location':'Synthetic sentence'}])
    dump(root/'report/manifest.json',{'deliverables':[hashed(root,'report/final.md')]})
    reviews={}
    for key in ['sources','independent_math','model_economics','narrative','layout']:
        (root/f'qa/{key}.md').write_text('Synthetic recorded review; tests verify record handling only.',encoding='utf-8')
        reviews[key]={'status':'passed','reviewer':'Synthetic fixture','reviewer_kind':'ai',
                      'scope':'Record validation only','evidence_path':f'qa/{key}.md'}
    dump(root/'qa/review.json',{'reviews':reviews,'reviewed_files':[
        hashed(root,p) for p in ['report/final.md','report/number_bindings.json',
                                'model/manifest.json','model/results.json']], 'pages':None})

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/missing':
            self.send_error(404)
            return
        body=b'%PDF-1.4\nSynthetic format envelope only' if self.path == '/pdf' else b'<html><body>not a PDF</body></html>'
        self.send_response(200)
        self.send_header('Content-Type','application/pdf' if self.path == '/pdf' else 'text/html')
        self.end_headers()
        self.wfile.write(body)
    def log_message(self,*args):
        pass

class HelperTests(unittest.TestCase):
    def each(self):
        for language in ['zh','en']:
            yield language,ROOT/'skills'/f'equity-research-report-{language}'/'scripts'

    def test_initializer_real_entrypoint_and_no_overwrite(self):
        for language,scripts in self.each():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                target=Path(tmp)/'fresh'
                args=[sys.executable,str(scripts/'init_workspace.py'),str(target),'--company','Synthetic',
                      '--ticker','TEST','--valuation-date','2026-09-30','--cutoff','2026-09-30T15:30:00+08:00',
                      '--language',language]
                first=subprocess.run(args,capture_output=True,text=True,cwd=tmp)
                self.assertEqual(first.returncode,0,first.stderr)
                before=(target/'project.json').read_bytes()
                second=subprocess.run(args,capture_output=True,text=True,cwd=tmp)
                self.assertNotEqual(second.returncode,0)
                self.assertEqual(before,(target/'project.json').read_bytes())

    def test_valid_delivery_from_executed_synthetic_model(self):
        for language,scripts in self.each():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);fixture(root)
                result=module(scripts/'check_bundle.py').check(root,'delivery')
                self.assertTrue(result['passed'],result['errors'])
                self.assertAlmostEqual(json.loads((root/'model/results.json').read_text())['revenue'],25.55)

    def test_rejects_late_or_same_day_date_only_source(self):
        for language,scripts in self.each():
            for pub in ['2026-09-30','2026-10-01']:
                with self.subTest(language=language,pub=pub),tempfile.TemporaryDirectory() as tmp:
                    root=Path(tmp);fixture(root)
                    rows=json.loads((root/'evidence/sources.json').read_text())
                    rows[0]['published_date']=pub;dump(root/'evidence/sources.json',rows)
                    result=module(scripts/'check_bundle.py').check(root,'data')
                    self.assertFalse(result['passed']);self.assertTrue(any('availability' in e for e in result['errors']))

    def test_rejects_unknown_zero_and_missing_original(self):
        for language,scripts in self.each():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);fixture(root)
                rows=json.loads((root/'evidence/facts.json').read_text())
                rows.append({'id':'F2','kind':'unknown','label':'Undefined claim','value':0,
                             'unit':'Currency','period':'Valuation date','scope':'Common equity',
                             'locator':'Unresolved','gap_id':'G1'})
                dump(root/'evidence/facts.json',rows)
                dump(root/'evidence/gaps.json',[{'id':'G1','issue':'Unknown claim','impact':'Conditional equity',
                     'treatment':'Keep null','affected_claims':['C1']}])
                (root/'sources/original.txt').unlink()
                result=module(scripts/'check_bundle.py').check(root,'data')
                self.assertFalse(result['passed'])
                self.assertTrue(any('never zero' in e for e in result['errors']))
                self.assertTrue(any('Missing file' in e for e in result['errors']))

    def test_date_only_previous_day_in_another_timezone_is_not_automatically_earlier(self):
        for language,scripts in self.each():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);fixture(root)
                rows=json.loads((root/'evidence/sources.json').read_text())
                rows[0]['published_date_utc_offset']='-10:00'
                dump(root/'evidence/sources.json',rows)
                result=module(scripts/'check_bundle.py').check(root,'data')
                self.assertFalse(result['passed'])
                self.assertTrue(any('availability' in e for e in result['errors']))

    def test_rejects_changed_input_after_model_run(self):
        for language,scripts in self.each():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);fixture(root)
                rows=json.loads((root/'evidence/assumptions.json').read_text());rows[0]['value']=3
                dump(root/'evidence/assumptions.json',rows)
                result=module(scripts/'check_bundle.py').check(root,'model')
                self.assertFalse(result['passed']);self.assertTrue(any('Stale' in e for e in result['errors']))

    def test_rejects_wrong_report_number_and_stale_review(self):
        for language,scripts in self.each():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);fixture(root)
                rows=json.loads((root/'report/number_bindings.json').read_text());rows[0]['value']=2.55
                dump(root/'report/number_bindings.json',rows)
                result=module(scripts/'check_bundle.py').check(root,'delivery')
                self.assertFalse(result['passed'])
                self.assertTrue(any('number mismatch' in e for e in result['errors']))
                self.assertTrue(any('Stale' in e for e in result['errors']))

    def test_rejects_paths_outside_workspace_and_invalid_schema(self):
        for language,scripts in self.each():
            checker=module(scripts/'check_bundle.py')
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);fixture(root)
                rows=json.loads((root/'evidence/sources.json').read_text());rows[0]['local_path']='../outside.txt'
                dump(root/'evidence/sources.json',rows)
                self.assertFalse(checker.check(root,'data')['passed'])
                fixture_root=root/'second';fixture(fixture_root)
                dump(fixture_root/'qa/review.json',{'reviews':[],'reviewed_files':[],'pages':None})
                self.assertFalse(checker.check(fixture_root,'delivery')['passed'])

    def test_capture_preserves_bytes_errors_and_unknown_publication(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        try:
            for language,scripts in self.each():
                cap=module(scripts/'capture_source.py')
                with self.subTest(language=language),tempfile.TemporaryDirectory() as tmp:
                    base=f'http://127.0.0.1:{server.server_port}'
                    path,ok=cap.capture(base+'/pdf',tmp,'pdf')
                    self.assertEqual(ok['status'],'captured_not_admitted')
                    self.assertIsNone(ok['published_at'])
                    self.assertEqual(ok['sha256'],hashlib.sha256((Path(tmp)/ok['file']).read_bytes()).hexdigest())
                    path2,bad=cap.capture(base+'/html',tmp,'pdf')
                    self.assertNotEqual(path,path2);self.assertEqual(bad['status'],'failed')
                    self.assertNotIn('file',bad);self.assertIn('Expected PDF',bad['error'])
                    _,missing=cap.capture(base+'/missing',tmp,'pdf')
                    self.assertEqual(missing['status'],'failed');self.assertIn('404',missing['error'])
        finally:
            server.shutdown();server.server_close();worker.join()

if __name__ == '__main__':
    unittest.main()
