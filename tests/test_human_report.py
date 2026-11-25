"""Offline acceptance of model-authored reports. Also accepts an unpacked field run."""
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


FIXTURES = Path(__file__).resolve().parents[1] / 'examples/acceptance/human-report'


class Navigation(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])


class ReportTests(unittest.TestCase):
    def check_run(self, run):
        out = run / 'outputs'
        documents = {p.resolve() for p in run.rglob('*.md')}
        inventory = (out / 'evidence_inventory.md').read_text(encoding='utf-8')
        entries = set(re.findall(r'^## (EVID-\d+)\.', inventory, re.M))
        summaries = {}
        for ext in ('md', 'html'):
            report = out / ('human_report.' + ext)
            body = report.read_text(encoding='utf-8')
            summaries[ext] = body
            nav = Navigation()
            nav.feed(body)
            if ext == 'md':
                nav.links.extend(re.findall(r'\]\(([^)]+)\)', body))
            self.assertEqual(len(nav.ids), len(set(nav.ids)))
            self.assertEqual(entries, {i for i in nav.ids if i.startswith('EVID-')})
            reached = set()
            for link in nav.links:
                url = urlsplit(link)
                if url.scheme in ('https', 'http'):
                    continue
                self.assertFalse(url.scheme or url.netloc or url.path.startswith('/'), link)
                dest = (out / unquote(url.path)).resolve() if url.path else report.resolve()
                self.assertIn(run.resolve(), dest.parents, link)
                self.assertTrue(dest.is_file(), link)
                if url.fragment:
                    target = Navigation()
                    target.feed(dest.read_text(encoding='utf-8'))
                    self.assertIn(unquote(url.fragment), target.ids, link)
                reached.add(dest)
            self.assertEqual(documents, {p for p in reached | {report.resolve()} if p.suffix == '.md'})
        return summaries

    def test_night_service(self):
        for body in self.check_run(FIXTURES / 'night-service').values():
            for fact in ['Сервис Север', '69,1%', 'точность классификации в соседнем проекте',
                         '8/8', 'роли — 5', 'интервью — 0', 'реестра — 20',
                         'Предложенная выборка — 300', 'инцидент, вызванный действиями агента',
                         'только как поисковые фрагменты', 'Длительность — не зафиксировано']:
                self.assertIn(fact, body)

    def test_product_with_partial_metadata(self):
        for body in self.check_run(FIXTURES / 'product-search').values():
            for fact in ['Каталог', '3/8', 'роли — 1', 'интервью — не зафиксировано', 'реестра — 1']:
                self.assertIn(fact, body)
            self.assertNotIn('Сервис Север', body)
            self.assertNotIn('ДИРС3', body)


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--run':
        ReportTests().check_run(Path(sys.argv[2]))
        print('Оба формата: все документы, записи EVID и локальные ссылки сверены.')
    else:
        unittest.main()
