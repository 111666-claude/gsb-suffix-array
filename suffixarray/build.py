"""后缀数组：构建、LCP、最长重复子串、子串计数。只用标准库。

构建用倍增法（前缀 doubling + 排名），时间 O(n log n)、内存 O(n)；
LCP 用 Kasai 式均摊线性算法；计数走后缀数组二分；
不同子串数用公式 n(n+1)/2 - sum(LCP)。
"""

STATS = {"copied": 0, "compared": 0}


def suffixes(text):
    """返回排好序的后缀起始下标。倍增法：每轮按 (rank[i], rank[i+k]) 排序。"""
    n = len(text)
    if n == 0:
        return []
    alphabet = sorted(set(text))
    code = {ch: idx for idx, ch in enumerate(alphabet)}
    rank = [code[ch] for ch in text]
    STATS["copied"] += n
    order = list(range(n))
    length = 1
    while True:
        order.sort(key=lambda i: (rank[i], rank[i + length] if i + length < n else -1))
        new_rank = [0] * n
        STATS["copied"] += n
        for step in range(1, n):
            prev, curr = order[step - 1], order[step]
            prev_key = (rank[prev], rank[prev + length] if prev + length < n else -1)
            curr_key = (rank[curr], rank[curr + length] if curr + length < n else -1)
            STATS["compared"] += 1
            new_rank[curr] = new_rank[prev] + (1 if curr_key != prev_key else 0)
        rank = new_rank
        if rank[order[-1]] == n - 1 or length >= n:
            break
        length *= 2
    return order


def lcp_array(text, order):
    """相邻后缀的最长公共前缀长度。Kasai：利用上一对的结果，均摊线性。"""
    n = len(text)
    if n < 2:
        return []
    rank = [0] * n
    for pos, start in enumerate(order):
        rank[start] = pos
    out = []
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
            height += 1
            STATS["compared"] += 1
        out.append((pos, height))
        if height > 0:
            height -= 1
    out.sort()
    return [value for _pos, value in out]


def longest_repeated(text):
    """最长重复子串（至少出现两次）：LCP 数组最大值对应的子串。"""
    order = suffixes(text)
    heights = lcp_array(text, order)
    if not heights:
        return ""
    best = max(heights)
    if best == 0:
        return ""
    step = heights.index(best)
    start = order[step + 1]
    return text[start:start + best]


def substring_count(text, pattern):
    """模式串出现次数：在后缀数组上二分上下界，单次 O(m log n)。"""
    if pattern == "":
        return 0
    order = suffixes(text)
    m = len(pattern)

    def compare(start):
        piece = text[start:start + m]
        STATS["compared"] += 1
        if piece < pattern:
            return -1
        if piece > pattern:
            return 1
        return 0

    lo, hi = 0, len(order)
    while lo < hi:
        mid = (lo + hi) // 2
        if compare(order[mid]) < 0:
            lo = mid + 1
        else:
            hi = mid
    lower = lo
    lo, hi = lower, len(order)
    while lo < hi:
        mid = (lo + hi) // 2
        if compare(order[mid]) <= 0:
            lo = mid + 1
        else:
            hi = mid
    return lo - lower


def unique_suffixes(text):
    """不同子串的个数：n(n+1)/2 - sum(LCP)，内存 O(n)。"""
    n = len(text)
    if n == 0:
        return 0
    order = suffixes(text)
    heights = lcp_array(text, order)
    return n * (n + 1) // 2 - sum(heights)
