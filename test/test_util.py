from twisted.trial import unittest

from txpoloniex import util

class FormatFunctionTestCase(unittest.TestCase):

    def _test(self, name, expected):
        result = util.format_function(name)
        self.assertEqual(result, expected)
        
    def test_replace(self):
        self._test('returnTest', 'test')

    def test_same(self):
        self._test('test', 'test')
