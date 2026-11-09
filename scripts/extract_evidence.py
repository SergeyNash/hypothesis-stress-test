#!/usr/bin/env python3
"""Bounded local text extraction. JSON to stdout; no interpretation or writes.

Optional readers: pypdf, python-docx, openpyxl (see requirements-evidence.txt).
Never executes macros, formulas, hyperlinks, OCR or embedded content.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from discover_sources import discover

TEXT = {'.md', '.markdown', '.txt', '.log', '.csv', '.srt', '.vtt'}


class TextHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in {'script', 'style'} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())


def check_archive(path):
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if len(entries) > 5000 or sum(x.file_size for x in entries) > 50 * 1024 * 1024:
            raise ValueError('archive_expansion_limit')


def units(path):
    ext = path.suffix.lower()
    if ext in TEXT:
        kind = 'transcript' if ext in {'.srt', '.vtt'} else ('markdown' if ext in {'.md', '.markdown'} else 'text')
        for n, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            if line.strip():
                yield kind, f'line:{n}', line
    elif ext in {'.html', '.htm'}:
        parser = TextHTML()
        parser.feed(path.read_text(encoding='utf-8-sig'))
        for n, part in enumerate(parser.parts, 1):
            yield 'html', f'text_block:{n}', part
    elif ext == '.pdf':
        from pypdf import PdfReader
        reader = PdfReader(path)
        if reader.is_encrypted:
            raise ValueError('encrypted_pdf')
        for n, page in enumerate(reader.pages, 1):
            if n > 100:
                raise ValueError('page_limit')
            text = page.extract_text() or ''
            if text.strip():
                yield 'pdf', f'page:{n}', text
    elif ext == '.docx':
        check_archive(path)
        from docx import Document
        document = Document(path)
        for n, paragraph in enumerate(document.paragraphs, 1):
            if paragraph.text.strip():
                yield 'docx', f'paragraph:{n}', paragraph.text
        for t, table in enumerate(document.tables, 1):
            for r, row in enumerate(table.rows, 1):
                for c, cell in enumerate(row.cells, 1):
                    if cell.text.strip():
                        yield 'docx', f'table:{t}/row:{r}/cell:{c}', cell.text
    elif ext == '.xlsx':
        check_archive(path)
        from openpyxl import load_workbook
        workbook = load_workbook(path, read_only=True, data_only=False, keep_links=False)
        try:
            visited = 0
            for sheet in workbook:
                if (sheet.max_row or 0) > 100000 or (sheet.max_column or 0) > 1000:
                    raise ValueError('worksheet_dimension_limit')
                for row in sheet:
                    for cell in row:
                        visited += 1
                        if visited > 200000:
                            raise ValueError('worksheet_cell_limit')
                        if cell.value is not None:
                            text = str(cell.value)
                            if cell.data_type == 'f':
                                text = 'formula_not_evaluated: ' + text
                            yield 'xlsx', f'sheet:{sheet.title}/cell:{cell.coordinate}', text
        finally:
            workbook.close()
    else:
        raise ValueError('unsupported_extension')


def extract(path, root, *, max_file_size=2 * 1024 * 1024, max_units=1000, max_chars=100000):
    path, root = Path(path), Path(root).resolve()
    result = {'source_path': str(path), 'status': 'skipped', 'units': [], 'limit_reached': False}
    try:
        # A directory symlink must not let the recursive scan escape the chosen KB.
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            raise ValueError('outside_root')
        result['source_path'] = resolved.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError('symlink')
        if not path.is_file():
            raise ValueError('not_a_file')
        if path.stat().st_size > max_file_size:
            raise ValueError('file_size_limit')
        used = 0
        for kind, location, text in units(path):
            if len(result['units']) >= max_units or used + len(text) > max_chars:
                result['limit_reached'] = True
                break
            result['units'].append({'source_kind': kind, 'location': location, 'text': text})
            used += len(text)
        if result['units']:
            result['status'] = 'partial' if result['limit_reached'] else 'extracted'
        else:
            result['reason'] = 'extraction_limit' if result['limit_reached'] else 'no_extractable_text'
    except ImportError as error:
        result['reason'] = 'missing_reader:' + (error.name or 'unknown')
    except Exception as error:
        # Keep a bounded partial result with its failure; never present it as complete.
        result['reason'] = str(error)[:200] or type(error).__name__
        if result['units']:
            result['status'] = 'partial'
        if str(error).endswith('_limit'):
            result['limit_reached'] = True
    return result


def candidates(root, query=''):
    for item in discover(root, query)['files']:
        if item['reader'] == 'document':
            yield Path(root) / item['path']


def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('must be positive')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', help='Files under --root; without paths scan root')
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--query', default='', help='Topic terms for automatic candidate ordering')
    parser.add_argument('--max-files', type=positive, default=200)
    parser.add_argument('--max-file-size', type=positive, default=2 * 1024 * 1024)
    parser.add_argument('--max-units', type=positive, default=1000)
    parser.add_argument('--max-chars', type=positive, default=100000)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error('--root must be an existing directory')
    catalog = None if args.paths else discover(root, args.query)
    paths = ((root / p for p in args.paths) if args.paths else
             (root / item['path'] for item in catalog['files'] if item['reader'] == 'document'))
    output = {'root': str(root), 'limits': vars(args).copy(), 'files': [], 'limit_reached': False}
    output['limits'].pop('root')
    output['limits'].pop('paths')
    if catalog is not None:
        output['discovery'] = catalog
        output['limit_reached'] = catalog['limit_reached']
    for n, path in enumerate(paths):
        if n >= args.max_files:
            output['limit_reached'] = True
            break
        result = extract(path, root, max_file_size=args.max_file_size,
                         max_units=args.max_units, max_chars=args.max_chars)
        output['files'].append(result)
        output['limit_reached'] |= result['limit_reached']
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
