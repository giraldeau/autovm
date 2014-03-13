#!/usr/bin/env python
# coding=utf-8

import unittest

from autovm.helpers import fn


class Test(unittest.TestCase):
    """Unit tests for utils.fn()"""

    def test_fn(self):
        """Test result"""
        value = True
        result = fn(value)
        self.assertEqual(value, result)

if __name__ == "__main__":
    unittest.main()
