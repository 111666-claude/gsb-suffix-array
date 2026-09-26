# suffix-array

后缀数组（构建、LCP、最长重复子串、子串计数、不同子串数），只用 Python 标准库。

```
python3 -m suffixarray.cli --text banana --stats
python3 -m suffixarray.cli --text banana --pattern an
python3 -m suffixarray.cli --generate 2000 --counters
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **最长重复子串**是 LCP 数组的最大值对应的子串：`--text banana --stats` 必须是 `ana`
  （现在返回第一个非零 LCP，给 `a`）；`mississippi` 必须是 `issi`（现在给 `i`）。
- **构建不能用「切出每个后缀再排序」**：那是 O(n² log n) 时间、O(n²) 内存。
  `--generate 2000 --counters` 现在 `copied=2001000`，按口径应该与 O(n log n) 同阶（几万以内）。
- **计数要走后缀数组二分**，不要线性扫描：`--text banana --pattern an` 现在给 `count=2`（值是对的），
  但比较次数与文本长度成正比；口径要求对同一文本的多次查询摊还 O(m log n)。
- LCP 要利用上一对的结果（Kasai 式的均摊线性），不是每对都从 0 重新比。
- 不变量：后缀数组与「朴素排序」结果一致；`lcp_array` 长度等于后缀数减一；
  不同子串数等于 `n(n+1)/2` 减去 LCP 之和；空文本返回空结果。
- 规模：10 万字符的文本要在 O(n log n) 时间、O(n) 内存内建好后缀数组与 LCP。

## 现在的行为

- `suffixes` 切出全部后缀再 `sort()`：`--generate 2000` 的 `copied=2001000`，
  `--generate 20000` 的 `copied=200010000`（两亿），都是 O(n²)。
- `longest_repeated` 返回**第一个非零 LCP** 对应的子串，而不是最大值：`banana` 给 `a`、`mississippi` 给 `i`。
- `substring_count` 对每个起点做 `startswith`：值对，但比较次数是 O(n × 模式长度)。
- `unique_suffixes` 把所有子串塞进 `set`：O(n²) 内存。

## 计划新增的能力

```
--generate N    生成 N 个字符的确定性文本再分析
--counters      打印复制与比较次数
```

## 输出

```
[后缀起始下标…]
suffixes=… longest_repeated=… unique_substrings=…
count=…
n=… copied=… compared=…
```

## 目录

```
suffixarray/build.py   后缀数组、LCP、计数
suffixarray/cli.py     命令行入口
tests/                 unittest 用例
```
