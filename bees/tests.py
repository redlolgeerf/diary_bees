import json
from django.test import TestCase
from bees.models import DUser, History, Bees

class TestDUser(TestCase):
    def test_update(self):
        b = json.dumps({12345: 'asd', 134256: 'vvv'})
        n = [(12345, 'asd'), (134256, 'vvv'), (1342, 'abc')]
        d = DUser()
        d.save()
        d.bees = b
        d.update_bees(n)
        self.assertEqual(d.history_set.count(), 1)

class TestHistory(TestCase):
    def test_from_diff(self):
        diff = ('141', 'j', 'ccc')
        h = History.create_from_diff(diff)
        self.assertEqual(h.d_id, 141)
        self.assertEqual(h.action, 'j')
        self.assertEqual(h.d_name, 'ccc')

class TestBees(TestCase):
    def setUp(self):
        b = {12345: 'asd', 134256: 'vvv'}
        self.js = json.dumps(b)
        self.li = [(12345, 'asd'), (134256, 'vvv')]
        self.b = {str(k): v for k, v in b.items()}

    def tearDown(self):
        pass

    def test_from_json(self):
        bees = Bees(self.js)
        self.assertJSONEqual(bees.to_json(), self.js)
        self.assertDictEqual(bees._bees_dict, self.b)

    def test_from_json_blank(self):
        bees = Bees('')
        self.assertJSONEqual(bees.to_json(), "{}")
        self.assertDictEqual(bees._bees_dict, {})

    def test_from_list(self):
        bees = Bees(self.li)
        self.assertDictEqual(bees._bees_dict, self.b)
        self.assertJSONEqual(bees.to_json(), self.js)

    def test_from_list_blank(self):
        bees = Bees([])
        self.assertDictEqual(bees._bees_dict, {})
        self.assertJSONEqual(bees.to_json(), "{}")

    def test_comparision(self):
        bees = Bees(self.js)
        other_bees = Bees(self.js)
        self.assertTrue(bees == other_bees)

        other_bees = Bees(json.dumps({12345: 'asd', 134256: 'vvk'}))
        self.assertFalse(bees == other_bees)

    def test_diff(self):
        bees = Bees(self.js)
        other_bees = Bees(self.js)
        self.assertEqual(bees.diff(other_bees), [])

        other_bees = Bees(json.dumps({12345: 'asd', 134256: 'vvk'}))
        expected = [('134256', 'r', 'vvv', 'vvk')]
        self.assertEqual(bees.diff(other_bees), expected)

        other_bees = Bees(json.dumps({12345: 'asd'}))
        expected = [('134256', 'l', 'vvv')]
        self.assertEqual(bees.diff(other_bees), expected)

        other_bees = Bees(json.dumps({12345: 'asd', 134256: 'vvv', 141: 'ccc'}))
        expected = [('141', 'j', 'ccc')]
        self.assertEqual(bees.diff(other_bees), expected)
