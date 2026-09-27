"""朴素参考实现：切片排序 + 逐对比 LCP。只用于测试对照。"""


def naive_suffixes(text):
    return sorted(range(len(text)), key=lambda i: text[i:])


def naive_lcp_array(text, order):
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


def naive_longest_repeated(text):
    order = naive_suffixes(text)
    heights = naive_lcp_array(text, order)
    if not heights or max(heights) == 0:
        return ""
    step = heights.index(max(heights))
    start = order[step + 1]
    return text[start:start + max(heights)]


def naive_substring_count(text, pattern):
    if pattern == "":
        return 0
    return sum(1 for i in range(len(text)) if text.startswith(pattern, i))


def naive_unique_substrings(text):
    return len({text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)})
