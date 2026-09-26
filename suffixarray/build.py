"""后缀数组：构建、最长重复子串、子串计数。只用标准库。"""

STATS = {"copied": 0, "compared": 0}


def suffixes(text):
    """返回排好序的后缀起始下标。缺陷：直接对每个后缀做字符串切片再排序。

    复杂度 O(n^2 log n)，而且每次比较都要复制子串。
    """
    items = []
    for index in range(len(text)):
        piece = text[index:]
        STATS["copied"] += len(piece)
        items.append((piece, index))
    items.sort()
    return [index for _suffix, index in items]


def lcp_array(text, order):
    """相邻后缀的最长公共前缀长度。缺陷：逐字符比较时从 0 开始，不看前一个的结论。"""
    out = []
    for step in range(1, len(order)):
        left, right = order[step - 1], order[step]
        length = 0
        while (
            left + length < len(text)
            and right + length < len(text)
            and text[left + length] == text[right + length]
        ):
            length += 1
        out.append(length)
    return out


def longest_repeated(text):
    """最长重复子串（至少出现两次）。缺陷：返回第一个非零 LCP，而不是最大的那个。"""
    order = suffixes(text)
    heights = lcp_array(text, order)
    if not heights:
        return ""
    for step, height in enumerate(heights):
        if height > 0:
            start = order[step]
            return text[start:start + height]
    return ""


def substring_count(text, pattern):
    """模式串出现次数。缺陷：线性扫描每个位置比较，不用后缀数组二分。"""
    count = 0
    for index in range(len(text)):
        STATS["compared"] += 1
        if text.startswith(pattern, index):
            count += 1
    return count


def unique_suffixes(text):
    """不同子串的个数。缺陷：把所有子串塞进 set，O(n^2) 内存。"""
    seen = set()
    for start in range(len(text)):
        for end in range(start + 1, len(text) + 1):
            STATS["copied"] += end - start
            seen.add(text[start:end])
    return len(seen)
