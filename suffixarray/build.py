"""后缀数组：构建、LCP、最长重复子串、子串计数。只用标准库。

- 构建：前缀倍增（doubling + 排名），时间 O(n log n)、内存 O(n)。
- LCP：Kasai 式均摊线性，利用上一对的结果。
- 计数：后缀数组上二分，单次 O(m log n)。
- 不同子串数：n(n+1)/2 - sum(LCP)，内存 O(n)。
"""

STATS = {"copied": 0, "compared": 0}


def suffixes(text):
    """返回排好序的后缀起始下标（倍增法，O(n log n)）。"""
    n = len(text)
    if n == 0:
        return []
    alphabet = {ch: pos for pos, ch in enumerate(sorted(set(text)))}
    rank = [alphabet[ch] for ch in text]
    STATS["copied"] += n
    order = list(range(n))
    step = 1
    while step < n:
        order.sort(key=lambda i: (rank[i], rank[i + step] if i + step < n else -1))
        STATS["copied"] += n
        new_rank = [0] * n
        for pos in range(1, n):
            prev, cur = order[pos - 1], order[pos]
            prev_key = (rank[prev], rank[prev + step] if prev + step < n else -1)
            cur_key = (rank[cur], rank[cur + step] if cur + step < n else -1)
            new_rank[cur] = new_rank[prev] + (cur_key != prev_key)
        rank = new_rank
        if rank[order[-1]] == n - 1:
            break
        step <<= 1
    return order


def lcp_array(text, order):
    """相邻后缀的最长公共前缀长度（Kasai 式，均摊 O(n)）。"""
    n = len(order)
    if n < 2:
        return []
    rank = [0] * n
    for pos, start in enumerate(order):
        rank[start] = pos
    out = [0] * (n - 1)
    height = 0
    for start in range(n):
        pos = rank[start]
        if pos == 0:
            continue
        other = order[pos - 1]
        while (
            start + height < n
            and other + height < n
            and text[start + height] == text[other + height]
        ):
            STATS["compared"] += 1
            height += 1
        out[pos - 1] = height
        if height:
            height -= 1
    return out


def longest_repeated(text):
    """最长重复子串：LCP 数组最大值对应的子串。"""
    order = suffixes(text)
    heights = lcp_array(text, order)
    if not heights:
        return ""
    best = 0
    best_at = -1
    for pos, height in enumerate(heights):
        if height > best:
            best = height
            best_at = pos
    if best_at < 0:
        return ""
    start = order[best_at]
    return text[start:start + best]


def substring_count(text, pattern):
    """模式串出现次数：后缀数组上二分，单次 O(m log n)。"""
    order = suffixes(text)
    length = len(pattern)
    lo, hi = 0, len(order)
    while lo < hi:
        mid = (lo + hi) // 2
        STATS["compared"] += 1
        if text[order[mid]:order[mid] + length] < pattern:
            lo = mid + 1
        else:
            hi = mid
    left = lo
    lo, hi = left, len(order)
    while lo < hi:
        mid = (lo + hi) // 2
        STATS["compared"] += 1
        if text[order[mid]:order[mid] + length] <= pattern:
            lo = mid + 1
        else:
            hi = mid
    return lo - left


def unique_suffixes(text):
    """不同子串的个数：n(n+1)/2 - sum(LCP)，内存 O(n)。"""
    n = len(text)
    if n == 0:
        return 0
    order = suffixes(text)
    heights = lcp_array(text, order)
    return n * (n + 1) // 2 - sum(heights)
