---
tags: [字符串, utf-8, 哈希, 游戏引擎, bitsquid]
date: 2026-04-19
sources: 1
---

# 游戏运行时的字符串处理：UTF-8 + 无 string class + hash ID

[[niklas-frykholm|Niklas Frykholm]] 2011 年在 Bitsquid 博客里留下的一篇"strings redux"是**游戏引擎字符串哲学**的集中陈述。三句话总结他的主张：**内外都用 UTF-8、别做 string class、runtime 不要字符串**。每一条都反直觉但经得起推敲。

## 1. UTF-8 everywhere（内存里和盘上都是）

作者面试题喜欢问字符串编码，因为这是区分"懂数据本体 vs 懂某种表示"的试金石。但自己写代码时只用一种编码：**UTF-8**。

优点是压倒性的：只要做一次全项目约定"非 UTF-8 就是 wrong"，就再也没有"这份数据什么编码"的困惑；C 的 `char *` / `char []` 直接用，整套处理 ASCII 字符串的函数不改一行就能吃 UTF-8（continuation byte 恒为 `10xxxxxx`，ASCII 0–127 与 UTF-8 完全兼容）；所有 parser、`strchr`、`printf` 都天然工作。

常见的两个"UTF-8 劣势"都站不住：

- **浪费内存**？日文用 UTF-8 确实比 Shift-JIS 大，但游戏里字符串占总内存比例极小（如果不是，那是另一个 bug）；真要省，直接压缩，信息熵与编码无关，压缩后体积几乎一样。
- **O(n) 随机索引第 i 个 glyph**？真实代码里几乎从不做这件事。拼接、解析、比较都不碰 glyph；渲染是**顺序遍历**——UTF-8 顺序遍历和 UTF-32 一样快，只有随机访问慢。作者在评论区挑战读者给出一个真实场景，反例基本都是 Boyer-Moore 之类的高级子串搜索——那确实要 glyph 随机访问。

## 2. 别做 string class

作者的判断更激进：**string class 对两类场景都不好**。

游戏里字符串的用法泾渭分明：

- **静态字符串**——解析、数据编译、脚本 callback 的 key。数量占绝大多数。这时候参数该写 `const char *` 而不是 `const string &`：前者让调用者自由持有内存，不会因为穿过 API 就被强制转换成 string 对象。
- **动态字符串**——格式化、log。数量少得多。

对静态路径没意义，对动态路径也不够——经典的 `for i in 0..10000: a += "xxx"` 能让某些 string 实现变成 O(n²)。作者的替代是 `vector<char>` + 一组 `string::append(v, "xxx")` 函数。看起来退回原始，但**区分"能长大"（vector<char>）和"不能长大"（char *）的类型**，并把 amortized O(n) 的代价露在眼前。问自己一句话："你知道自己 string class 长大一次要多少开销吗？"

## 3. 运行时里几乎不要字符串

变长字符串慢、费内存、需要 alloc/free，还逼得工具里名字必须短；定长字符串要么更浪费，要么让设计师抱怨名字写不全。两头不讨好。

Bitsquid 把 runtime 里允许出现字符串的场景压到两类：**UI 文本**（必定走本地化管道，以 hash 过的 key 去查 localizer，`"menu_file_open" → IdString64`）、**debug build 专用**（format 字符串、log、assert）。**其余所有命名——resource、object、parameter、bone 名——在数据编译阶段就被 hash 成整数**：

- 全局名（texture、entity）用 **64-bit hash**（murmur64），碰撞被当作编译错误，据作者"还没发生过一次"；
- 局部名（bone、材质 slot）用 **32-bit hash**，因为作用域小、概率可控。

用 hash 胜过 enum：enum 要求跨模块全局协作避重；hash 只要 key space 足够大就无需协作。这正是 [[flow-graph-data-oriented-runtime|Flow]] 选 32-bit string hash 作为事件总线命名的理由。

### Debug 时怎么看 hash

`resource 0x3e728af10245bc71 报错`——这不是给人看的。两个补救：

- **反查表**：数据编译时顺手生成 `hash → original_string` 表，不进 runtime、给 console 工具用。游戏控制台输出自动把 hash 翻回 `vegetation/trees/larch_3.mesh`。
- **资源内嵌 debug_name[32]**：直接在资源 struct 里塞 32 字节人类可读名（通常是原 path 的末 32 字符）。资源本身普遍远大于 32 字节，这点开销不心疼；但在调试器和内存 dump 里一眼能认出，省一趟开反查工具。

这种**"hash 为主、debug name 为辅"**的二元设计是很多商业引擎的共同模式；对比 [[static-hash-value-debug-assert]]，那篇处理的是"代码里出现的硬编码 hash"如何安全写出来，本篇处理的是"引擎里大规模用 hash 代替字符串"的原则。

## 作者的源码约定

评论区有人问怎么保证 C++ 源文件真的是 UTF-8。作者的做法很朴素：**C++ 源文件严格 7-bit ASCII clean**，不放任何非 ASCII 字符；所有真正要本地化的字符串通过本地化工具编辑，输出 UTF-8 的 JSON，数据编译时拉进来。这样就不需要 `u8""` 前缀或者编辑器魔法，源码层面根本不存在编码问题。

## 相关

- [[static-hash-value-debug-assert]] —— 代码里硬编码 hash 的 debug 断言技巧
- [[non-cryptographic-hash]] —— MurmurHash 家族
- [[flow-graph-data-oriented-runtime]] —— 事件名用 32-bit hash 的典型例子
- [[offset-based-resource-blobs]] —— 资源里内嵌 debug_name 与 hash 引用的共用底座
- [[game-monitoring-event-buffer]] —— 监控系统里"字符串字面量地址即 intern ID"的极简玩法

## Sources

- [[sources/bitsquid-strings-redux]]
