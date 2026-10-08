"""Offline invariants: routes, anchors, metadata, and protected assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=[]; self.tags=[]; self.title=False; self.description=False; self.canonical=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append(tag)
        if 'id' in attrs:self.ids.append(attrs['id'])
        for key in ['href','src']:
            if key in attrs:self.links.append(attrs[key])
        if tag=='title':self.title=True
        if tag=='meta' and attrs.get('name')=='description':self.description=True
        if tag=='link' and attrs.get('rel')=='canonical':self.canonical=True

def resolve(url,origin):
    parsed=urlparse(url)
    if parsed.scheme or parsed.netloc:return None,None
    path=unquote(parsed.path)
    target=ROOT/path.lstrip('/') if path.startswith('/') else origin.parent/path if path else origin
    if target.is_dir():target=target/'index.html'
    return target, parsed.fragment

class SiteTests(unittest.TestCase):
    def test_protected_bytes(self):
        for path,expected in json.loads((ROOT/'docs/preserved-assets.json').read_text()).items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),expected,path)
    def test_generated_structure_and_links(self):
        for entry in json.loads((ROOT/'docs/generated-pages.json').read_text()):
            path=ROOT/entry['path'];doc=Document();doc.feed(path.read_text())
            self.assertEqual(doc.tags.count('main'),1,str(path))
            self.assertEqual(doc.tags.count('h1'),1,str(path))
            self.assertEqual(len(doc.ids),len(set(doc.ids)),str(path))
            self.assertTrue(doc.title and doc.description and doc.canonical,str(path))
            self.assertIn('main',doc.ids,str(path))
            for link in doc.links:
                target,fragment=resolve(link,path)
                if target is None:continue
                self.assertTrue(target.exists(),f'{path.relative_to(ROOT)} → {link}')
                if fragment and target.suffix=='.html':
                    destination=Document();destination.feed(target.read_text())
                    self.assertIn(fragment,destination.ids,f'{path} → {link}')
    def test_original_routes_and_downloads_preserved(self):
        for row in json.loads((ROOT/'docs/original-route-inventory.json').read_text()):
            self.assertTrue((ROOT/row['path']).is_file(),row['path'])
        for path in json.loads((ROOT/'docs/original-asset-inventory.json').read_text()):
            self.assertTrue((ROOT/path).is_file(),path)
    def test_sitemap_contains_only_canonical_indexable_pages(self):
        rows=json.loads((ROOT/'docs/generated-pages.json').read_text())
        urls={x['url'] for x in rows if x['index']}
        sitemap=ET.parse(ROOT/'sitemap.xml');locs={i.text.replace('https://eshaanarora.com','') for i in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
        self.assertEqual(urls,locs)
if __name__=='__main__':unittest.main()
