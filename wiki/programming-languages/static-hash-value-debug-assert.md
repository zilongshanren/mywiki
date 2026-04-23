---
tags: [哈希, 编译期, cpp, bitsquid, 工程技巧]
date: 2026-04-19
sources: 1
---

# 静态 Hash + Debug Assert

游戏引擎里很常见的小问题：代码中频繁要判 `name == "root_point"`，但 name 实际上被 hash 成了 32-bit id。若每次都 `murmur("root_point")`，不是太慢就是代码里散落 `static unsigned` 带 init-once 分支。

[[niklas-frykholm|Niklas Frykholm]] 2010 年对比了三种解法：

1. **Code-gen pre-build pass**：扫 `H("str", 0)` 这样的标记，把第二参数替换成 hash 值。Julien、Phil 代表这一派。
2. **Preprocessor hash**：`HASH_STR_10('r','o','o','t','_','p','o','i','n','t')` 用宏递归把 MurmurHash 展开成常量表达式。作者写过，觉得"智力好玩，代码巨丑"。
3. **手写常量 + wrapper 做 debug 断言**：写死 `0x5e43bd96` 当然 scary，但套个宏就不 scary 了——

```cpp
#ifdef _DEBUG
inline unsigned static_hash(const char *s, unsigned value) {
    assert(murmur_hash(s, strlen(s), 0) == value);
    return value;
}
#else
#define static_hash(s, v) (v)
#endif

if (object.name() == static_hash("root_point", 0x5e43bd96)) ...
```

作者选的是第三条。release 里这就是 immediate 常量比较，零成本；debug 里每次都复算一遍并校验，保证"人眼写的 hash"和"真 hash"一致。

## 各方案的权衡

- **可读性**：第 3 种最好（源码里能看见字符串）；preprocessor 版最差；code-gen 居中但需要同步源码和生成物。
- **零成本**：第 2、3 种都在 release 里是常量；方案 1 若 hash 被替换成立即数也成立，若存成定义则多一层符号。
- **漏检查风险**：Phil 认为方案 3 依赖 debug build 的代码覆盖，万一这行代码在 debug 里没执行，release 里也不会抓到不一致。作者回应：hash mismatch 会使 release 行为也错，比较一定会触发错误分支、很容易暴露。
- **C++0x constexpr**：2013 年有人贴出 constexpr 版，这是所有问题的"未来答案"，但 2010 年 MSVC 还没支持。
- **template meta-programming**：Humus / Ignacio Castaño 等人试过，VS2005/2008 会把 `static_murmurhash("literal")` 折成 32-bit immediate，但受"编译器不肯无限内联"限制，长度 ≈ 23 字符；而且 `switch case` 不能用（`"s"[0]` 不是常量表达式）；编译时间剧增。
- **static initializer**：`unsigned root_id = murmur("root");` 可以躲开 init-once，但作者**坚决不用 static init**——不仅是初始化顺序问题，也是 startup 时间不可 profile。

## 关键收获

- **"硬编码 + 断言校验"是简单到被低估的解**：只要有 debug 路径复算，scary 的魔法数字立刻变成可信常量；
- `static_hash("str", val)` 还有个额外好处：grep 它就能**列出所有硬编码的 hash 出现点**，自动化改算法时有地图；
- 在没有 `constexpr` 的年代，工程解法往往比语言解法更省事。

## 相关
- [[non-cryptographic-hash]] — MurmurHash、FNV 等家族
- [[flow-graph-data-oriented-runtime]] — Bitsquid 里大量用 32-bit string hash 做事件名
- [[offset-based-resource-blobs]] — 跨资源引用用 hash(name) 解析
- [[string-handling-game-runtime]] —— 为什么运行时用 hash ID 取代字符串名、以及反查表/嵌入 debug_name 的补救做法
- [[murmur-hash-inverse]] — MurmurHash2 32/64 位的 inverse，用于反查 ≤ bucket 长度的 pre-image

## Sources

- [[sources/bitsquid-static-hash-values]]
