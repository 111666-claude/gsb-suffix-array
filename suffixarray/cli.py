"""命令行入口：后缀数组相关信息。"""

import argparse
import json
import sys

from .build import longest_repeated, suffixes, substring_count, unique_suffixes
from .build import STATS


def build_parser():
    parser = argparse.ArgumentParser(prog="suffix-array", description="后缀数组")
    parser.add_argument("--text", help="要分析的文本")
    parser.add_argument("--pattern", help="统计这个模式串出现次数")
    parser.add_argument("--stats", action="store_true", help="打印后缀数、最长重复子串、不同子串数")
    parser.add_argument("--generate", type=int, default=0, help="生成这么长的文本再分析（不打印后缀数组）")
    parser.add_argument("--counters", action="store_true", help="打印复制与比较次数")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    text = args.text or ""
    if not text and args.generate == 0:
        print("错误：需要 --text 或 --generate", file=sys.stderr)
        return 2
    if args.generate > 0:
        state = 20260926
        chars = []
        for _ in range(args.generate):
            state = (state * 6364136223846793005 + 1442695040888963407) % (2 ** 64)
            chars.append("abcdefgh"[(state >> 61) % 8])
        text = "".join(chars)
        order = suffixes(text)
        print("n=%d suffixes=%d" % (len(text), len(order)))
        if args.counters:
            print("copied=%d compared=%d" % (STATS["copied"], STATS["compared"]))
        return 0
    if args.pattern is not None:
        print("count=%d" % substring_count(text, args.pattern))
        return 0
    order = suffixes(text)
    print(json.dumps(order))
    if args.stats:
        print("suffixes=%d" % len(order))
        print("longest_repeated=%s" % longest_repeated(text))
        print("unique_substrings=%d" % unique_suffixes(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
