"""朴素参考实现：切片排序 + 逐对重比 LCP。仅用于测试对照。"""


def suffixes(text):
    return sorted(range(len(text)), key=lambda i: text[i:])


def lcp_array(text, order):
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
    order = suffixes(text)
    heights = lcp_array(text, order)
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
    return sum(1 for i in range(len(text)) if text.startswith(pattern, i))


def unique_substrings(text):
    return len({text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)})
