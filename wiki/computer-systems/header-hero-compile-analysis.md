---
tags: [cpp, compile-time, include-graph, profiling, build-system]
date: 2026-04-19
sources: 1
---

# Header Hero：C++ 编译时间的 include 图剖析工具

C++ 编译时间只会越来越糟——这是 [[niklas-frykholm]] 说的 C++ 程序热力学第二定律。有人加一个 `#include` 容易，很少有人会回头删。所以每隔一段时间就得出一个「hero」去把 header 依赖图砍平。2011 年他写了个叫 *Header Hero* 的 C# 小工具来帮这件事。

## 工具的核心指标：Blowup Factor

给它 `.cpp` 和 include 搜索路径，它会用一个非常简化的解析器（只找 `#include` 字符串，不跑 preprocessor）扫全工程，几秒钟就能算出：

- **Total Lines**：项目原始行数；
- **Total Parsed**：完整 rebuild 时编译器实际吃进去的行数——一个 header 被 N 个 `.cpp` include 就算 N 次；
- **Blowup Factor** = `Total Parsed / Total Lines`：每行平均被解析几次。

作者项目的例子里 blowup 是 35，也就是每行代码平均重复解析 35 次。这个数字有直觉价值：**blowup 是 include 卫生程度的体检指标**，和 unity build 对冲的也是它（参考 [[unity-build-macro-renaming]]）。

## 排序 + 双向展开定位元凶

按「contribution = file 行数 × 被 include 次数」排序，榜首通常是 `map / set / string / vector` 这类模板容器，合理。但 Frykholm 点出反直觉的例子：`shader.h`、`file_system.h` 这种「本不该到处传染」的具体模块排在前面——说明有中间 header 把它们引爆了。

工具提供一个详情视图：左列是「谁 include 我」、右列是「我 include 谁」，每一项后面跟着传染总数。作者追到 `data_compiler.h → set.h` 被 316 个文件间接吃进，砍掉这一条收益极大。

## 打破依赖的四招

1. **前向声明**替代 include；别忘了模板和 typedef 也能前向声明：
   ```cpp
   template <class T> class Vector;
   typedef int Id;
   ```
2. 前向声明只能用指针/引用，所以成员变量可能要换成 **pimpl**（[[information-hiding]] 的经典手法）或指针——代价是多一跳 indirection。
3. 指针带来的 cache 访问模式劣化，可以 **placement new 到内嵌的原始 buffer**：声明 `char _b_storage[SIZE_OF_B];` + `_b = new (_b_storage) B();`，`a.h` 完全不 include `b.h`。但可读性代价很大，文章说「只在绝望时用」。
4. 像 `matrix4x4.h` 这种「小 type + 大量 inline method」的文件，**拆成两个 header**：别的 header 只 include 类型定义，`.cpp` 再拉 inline 实现。

一天半优化下来，他的项目从 6M 行 Total Parsed 降到 4.3M，完整 rebuild 37 秒。

## 工具自身的取舍

简化的 `#include` 解析器（字符串匹配而非真 preprocessor）是性能关键：缓存 + 纯字符串让增量扫描在半秒内完成，从而把「改 header → 看效果」变成一个内循环。代价是 fancy preprocessor trick 会被漏掉，注释里的 `#include` 不会被识别成已注释掉——评论区确认了「注释掉不会生效，要真删」。评论还指出一个小 bug：同一 header 被自己的 `.cpp` include 会被多计一次，但 include guard 假设下不应该发生。

## 相关
- [[unity-build-macro-renaming]]
- [[header-file-vs-pub-export]]
- [[header-as-user-manual]]
- [[information-hiding]]
- [[orthodox-cpp]]
- [[dependencies]]
- [[types-h-data-code-separation]] —— Frykholm 对 include 传染的结构性解法

## Sources

- [[sources/bitsquid-header-hero]]
