from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from extract_evidence import extract


class Extraction(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_text_anchors(self):
        p=self.root/'log.txt'; p.write_text('first\n\nthird\n')
        result=extract(p,self.root)
        self.assertEqual('extracted',result['status'])
        self.assertEqual(['line:1','line:3'],[x['location'] for x in result['units']])

    def test_html_does_not_extract_script(self):
        p=self.root/'page.html';p.write_text('<h1>Visible</h1><script>danger()</script><style>hidden</style>body')
        texts=[x['text'] for x in extract(p,self.root)['units']]
        self.assertEqual(['Visible','body'],texts)

    def test_size_limit(self):
        p=self.root/'large.txt';p.write_text('123456')
        result=extract(p,self.root,max_file_size=2)
        self.assertEqual('file_size_limit',result['reason'])
        self.assertTrue(result['limit_reached'])

    def test_units_limit(self):
        p=self.root/'lines.txt';p.write_text('first\nsecond')
        result=extract(p,self.root,max_units=1)
        self.assertEqual('partial',result['status'])
        self.assertTrue(result['limit_reached'])

    def test_symlink_escape_rejected(self):
        p=self.root/'outside.txt';p.symlink_to(ROOT/'VERSION')
        self.assertEqual('outside_root',extract(p,self.root)['reason'])

    def test_unsupported_file_is_gap(self):
        p=self.root/'file.bin';p.write_bytes(b'123')
        self.assertEqual('unsupported_extension',extract(p,self.root)['reason'])

    def test_missing_pdf_reader_is_explicit_gap(self):
        p=self.root/'document.pdf';p.write_bytes(b'%PDF')
        with patch.dict(sys.modules, {'pypdf': None}):
            result=extract(p,self.root)
        self.assertEqual('skipped',result['status'])
        self.assertEqual('missing_reader:pypdf',result['reason'])

    def test_scan_excludes_generated_examples(self):
        (self.root/'examples').mkdir();(self.root/'examples/false.txt').write_text('must not be evidence')
        (self.root/'fact.txt').write_text('raw')
        output=subprocess.check_output([sys.executable,str(ROOT/'scripts/extract_evidence.py'),'--root',str(self.root)])
        self.assertEqual(['fact.txt'],[x['source_path'] for x in json.loads(output)['files']])

    def test_cli_max_files_reports_limit(self):
        for name in ['one.txt','two.txt']:(self.root/name).write_text(name)
        output=subprocess.check_output([sys.executable,str(ROOT/'scripts/extract_evidence.py'),'--root',str(self.root),'--max-files','1'])
        result=json.loads(output)
        self.assertTrue(result['limit_reached']);self.assertEqual(1,len(result['files']))

    @unittest.skipUnless(importlib.util.find_spec('docx'),'optional python-docx missing')
    def test_docx_text_and_table(self):
        from docx import Document
        document=Document();document.add_paragraph('Support promise')
        document.add_table(rows=1, cols=1).cell(0,0).text='Customer approval'
        p=self.root/'contract.docx';document.save(p)
        result=extract(p,self.root)
        self.assertEqual('extracted',result['status'])
        self.assertEqual(['paragraph:1','table:1/row:1/cell:1'],[x['location'] for x in result['units']])

    @unittest.skipUnless(importlib.util.find_spec('openpyxl'),'optional openpyxl missing')
    def test_xlsx_values_formulas_and_cell_anchors(self):
        from openpyxl import Workbook
        workbook=Workbook();sheet=workbook.active;sheet.title='Costs';sheet['A1']=90000;sheet['B1']='=A1-75000'
        p=self.root/'costs.xlsx';workbook.save(p);workbook.close()
        result=extract(p,self.root)
        self.assertEqual('sheet:Costs/cell:A1',result['units'][0]['location'])
        self.assertEqual('formula_not_evaluated: =A1-75000',result['units'][1]['text'])

    @unittest.skipUnless(importlib.util.find_spec('openpyxl'),'optional openpyxl missing')
    def test_sparse_worksheet_dimension_is_bounded(self):
        from openpyxl import Workbook
        workbook=Workbook();workbook.active['A1000000']='outlier'
        p=self.root/'sparse.xlsx';workbook.save(p);workbook.close()
        result=extract(p,self.root)
        self.assertEqual('worksheet_dimension_limit',result['reason'])
        self.assertTrue(result['limit_reached'])

    @unittest.skipUnless(importlib.util.find_spec('pypdf'),'optional pypdf missing')
    def test_pdf_text_page_anchor(self):
        from pypdf import PdfWriter
        from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject
        writer=PdfWriter();page=writer.add_blank_page(width=600,height=800)
        font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        stream=DecodedStreamObject();stream.set_data(b'BT /F1 12 Tf 20 700 Td (Service boundary) Tj ET')
        page[NameObject('/Contents')]=writer._add_object(stream)
        p=self.root/'promise.pdf';writer.write(p)
        result=extract(p,self.root)
        self.assertEqual('page:1',result['units'][0]['location'])
        self.assertIn('Service boundary',result['units'][0]['text'])

    @unittest.skipUnless(importlib.util.find_spec('pypdf'),'optional pypdf missing')
    def test_pdf_without_text_and_encrypted_pdf_are_gaps(self):
        from pypdf import PdfWriter
        writer=PdfWriter();writer.add_blank_page(width=100,height=100)
        p=self.root/'scan.pdf';writer.write(p)
        self.assertEqual('no_extractable_text',extract(p,self.root)['reason'])
        writer.encrypt('password');p=self.root/'encrypted.pdf';writer.write(p)
        self.assertEqual('encrypted_pdf',extract(p,self.root)['reason'])


if __name__ == '__main__':
    unittest.main()
