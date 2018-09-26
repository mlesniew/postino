import unittest

import postino.address


class AddressParser(unittest.TestCase):
    def test_tuple(self):
        addr = postino.address.parse_address(('Foo', 'foo@bar.com'))
        self.assertTrue(isinstance(addr, str))
        self.assertEqual(addr, 'Foo <foo@bar.com>')

    def test_tuple_unicode(self):
        addr = postino.address.parse_address(('Foo', 'foo@bar.com'))
        self.assertTrue(isinstance(addr, str))
        self.assertEqual(addr, 'Foo <foo@bar.com>')

    def test_string(self):
        addr = postino.address.parse_address('Foo <foo@bar.com>')
        self.assertTrue(isinstance(addr, str))
        self.assertEqual(addr, 'Foo <foo@bar.com>')

    def test_unicode(self):
        addr = postino.address.parse_address('Foo <foo@bar.com>')
        self.assertTrue(isinstance(addr, str))
        self.assertEqual(addr, 'Foo <foo@bar.com>')

    def test_string_no_name(self):
        addr = postino.address.parse_address('foo@bar.com')
        self.assertTrue(isinstance(addr, str))
        self.assertEqual(addr, 'foo@bar.com')

    def test_unicode_no_name(self):
        addr = postino.address.parse_address('foo@bar.com')
        self.assertTrue(isinstance(addr, str))
        self.assertEqual(addr, 'foo@bar.com')

    def test_short_tuple(self):
        with self.assertRaises(ValueError):
            postino.address.parse_address(('foo@bar.com',))

    def test_long_tuple(self):
        with self.assertRaises(ValueError):
            postino.address.parse_address(('Foo', 'foo@bar.com', 'z'))

    def test_object(self):
        with self.assertRaises(ValueError):
            postino.address.parse_address(object())
