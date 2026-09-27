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

## 实现方式

- `suffixes` 用前缀倍增（doubling + 排名）建后缀数组：O(n log n) 时间、O(n) 内存。
  `--generate 2000` 的 `copied` 在几万以内，`--generate 100000` 约 1.8e6（n log n 同阶）。
- `longest_repeated` 取 LCP 数组最大值对应的子串：`banana` 给 `ana`、`mississippi` 给 `issi`。
- `lcp_array` 用 Kasai 式均摊线性算法，相邻后缀比较利用上一对的结果。
- `substring_count` 在后缀数组上二分，单次 O(m log n)。
- `unique_suffixes` 用 `n(n+1)/2 - sum(LCP)`，内存 O(n)。
- `suffixarray/naive.py` 是朴素参考实现（切片排序 + 逐对重比 LCP），测试用它对
  样例与 1000 份随机文本逐项比对后缀数组、LCP、最长重复子串与计数。

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
suffixarray/naive.py   朴素参考实现（仅测试对照用）
tests/                 unittest 用例
```
