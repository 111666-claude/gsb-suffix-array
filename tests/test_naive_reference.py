"""与朴素参考实现逐项对照，外加口径要求的样例与不变量。"""

import random
import unittest

from suffixarray import build, naive


def reset_stats():
    build.STATS["copied"] = 0
    build.STATS["compared"] = 0


class SpecCaseTest(unittest.TestCase):
    def test_banana_longest_repeated(self):
        self.assertEqual(build.longest_repeated("banana"), "ana")

    def test_mississippi_longest_repeated(self):
        self.assertEqual(build.longest_repeated("mississippi"), "issi")

    def test_banana_count(self):
        self.assertEqual(build.substring_count("banana", "an"), 2)
        self.assertEqual(build.substring_count("banana", "zz"), 0)

    def test_empty_text(self):
        self.assertEqual(build.suffixes(""), [])
        self.assertEqual(build.lcp_array("", []), [])
        self.assertEqual(build.longest_repeated(""), "")
        self.assertEqual(build.unique_suffixes(""), 0)
        self.assertEqual(build.substring_count("", "a"), 0)

    def test_deterministic(self):
        text = "mississippi" * 20
        first = (build.suffixes(text), build.longest_repeated(text))
        second = (build.suffixes(text), build.longest_repeated(text))
        self.assertEqual(first, second)

    def test_build_counters_scale(self):
        reset_stats()
        text = "".join("abcdefgh"[((i * 6364136223846793005 + 1442695040888963407) >> 61) % 8] for i in range(2000))
        order = build.suffixes(text)
        self.assertEqual(len(order), 2000)
        self.assertLess(build.STATS["copied"], 100000)


class NaiveReferenceTest(unittest.TestCase):
    def test_random_texts_match_naive(self):
        rng = random.Random(20260928)
        for case in range(1000):
            n = rng.randrange(0, 61)
            text = "".join(rng.choice("aabc") for _ in range(n))
            order = build.suffixes(text)
            self.assertEqual(order, naive.suffixes(text), "suffixes: %r" % text)
            heights = build.lcp_array(text, order)
            self.assertEqual(heights, naive.lcp_array(text, order), "lcp: %r" % text)
            self.assertEqual(len(heights), max(0, n - 1))
            self.assertEqual(
                build.longest_repeated(text), naive.longest_repeated(text), "lrs: %r" % text
            )
            self.assertEqual(
                build.unique_suffixes(text), naive.unique_substrings(text), "unique: %r" % text
            )
            for _ in range(3):
                pattern = "".join(rng.choice("aabc") for _ in range(rng.randrange(1, 4)))
                self.assertEqual(
                    build.substring_count(text, pattern),
                    naive.substring_count(text, pattern),
                    "count: %r in %r" % (pattern, text),
                )


if __name__ == "__main__":
    unittest.main()
