"""已有领域规则的边界回归。"""
import json
from pathlib import Path
import unittest
from caseweight import domain
from caseweight.overview import summarize

class DomainTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.data = json.loads((root / 'data/release.json').read_text())
        self.request = json.loads((root / 'data/request.json').read_text())

    def test_business_rules(self):
        result = domain.quote(self.data, self.request)
        self.assertEqual(result['usable_kg'], 48.75)
        self.assertEqual(result['minimum_net_g'], 1800)
        self.assertEqual(domain.detail(self.data, {'crate': 'family', 'gross_g': 2000})['net_g'], 1920)

    def test_overview_counts(self):
        self.assertTrue(summarize(self.data))
        self.assertTrue(self.data['synthetic'])
        self.assertEqual(len({row['id'] for row in self.data['rows']}), len(self.data['rows']))

    def test_invalid_request(self):
        with self.assertRaises((ValueError, KeyError)):
            domain.quote(self.data, {})
