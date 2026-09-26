import unittest

from suffixarray.build import lcp_array, longest_repeated, substring_count, suffixes, unique_suffixes


class SuffixTest(unittest.TestCase):
    def test_banana_suffix_array(self):
        self.assertEqual(suffixes("banana"), [5, 3, 1, 0, 4, 2])

    def test_empty_text(self):
        self.assertEqual(suffixes(""), [])

    def test_single_char(self):
        self.assertEqual(suffixes("a"), [0])


class LcpTest(unittest.TestCase):
    def test_lcp_lengths(self):
        order = suffixes("banana")
        self.assertEqual(lcp_array("banana", order), [1, 3, 0, 0, 2])

    def test_lcp_of_single_suffix(self):
        self.assertEqual(lcp_array("a", [0]), [])


class CountTest(unittest.TestCase):
    def test_substring_count(self):
        self.assertEqual(substring_count("banana", "an"), 2)

    def test_substring_count_missing(self):
        self.assertEqual(substring_count("banana", "zz"), 0)

    def test_unique_substrings(self):
        self.assertEqual(unique_suffixes("banana"), 15)

    def test_unique_substrings_empty(self):
        self.assertEqual(unique_suffixes(""), 0)

    def test_longest_repeated_type(self):
        self.assertIsInstance(longest_repeated("banana"), str)
