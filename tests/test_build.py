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


import random

from tests.reference import (
    naive_lcp_array,
    naive_longest_repeated,
    naive_substring_count,
    naive_suffixes,
    naive_unique_substrings,
)


class AgainstNaiveTest(unittest.TestCase):
    SAMPLES = ["", "a", "aa", "banana", "mississippi", "abracadabra", "aaaaaa", "abcabxabcd"]

    def check_text(self, text):
        order = suffixes(text)
        expected_order = naive_suffixes(text)
        self.assertEqual(order, expected_order)
        heights = lcp_array(text, order)
        self.assertEqual(heights, naive_lcp_array(text, expected_order))
        self.assertEqual(len(heights), max(0, len(order) - 1))
        self.assertEqual(longest_repeated(text), naive_longest_repeated(text))
        self.assertEqual(unique_suffixes(text), naive_unique_substrings(text))
        self.assertEqual(
            unique_suffixes(text),
            len(text) * (len(text) + 1) // 2 - sum(heights),
        )
        for pattern in ["a", "an", "zz", text[:2], text[-2:]]:
            self.assertEqual(
                substring_count(text, pattern),
                naive_substring_count(text, pattern),
            )

    def test_samples_against_naive(self):
        for text in self.SAMPLES:
            with self.subTest(text=text):
                self.check_text(text)

    def test_random_texts_against_naive(self):
        rng = random.Random(20260927)
        for trial in range(1000):
            length = rng.randint(0, 30)
            text = "".join(rng.choice("abcde") for _ in range(length))
            with self.subTest(trial=trial, text=text):
                self.check_text(text)

    def test_deterministic(self):
        text = "mississippibananabanana"
        self.assertEqual(suffixes(text), suffixes(text))
        self.assertEqual(longest_repeated(text), longest_repeated(text))


class ScaleTest(unittest.TestCase):
    def test_hundred_thousand_chars(self):
        state = 20260926
        chars = []
        for _ in range(100000):
            state = (state * 6364136223846793005 + 1442695040888963407) % (2 ** 64)
            chars.append("abcdefgh"[(state >> 61) % 8])
        text = "".join(chars)
        order = suffixes(text)
        self.assertEqual(len(order), 100000)
        self.assertEqual(order, sorted(order, key=lambda i: text[i:]))
        heights = lcp_array(text, order)
        self.assertEqual(len(heights), 99999)
        for step in range(1, len(order)):
            left, right = text[order[step - 1]:], text[order[step]:]
            common = 0
            while common < len(left) and common < len(right) and left[common] == right[common]:
                common += 1
            self.assertEqual(heights[step - 1], common)
