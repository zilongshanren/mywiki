---
tags: [software-design, cpp, performance, debate]
date: 2026-04-19
sources: 1
---

# Clean Code 批判：游戏程序员的视角

[[emilio-lopez-ros]] 在 *Life and Death of a Graphics Programmer* 中对「clean code」运动提出了系统性反对。他的立场不是「代码不要清楚」，而是**当 clean code 的规则（小函数、深继承、iterator-heavy STL、RTTI/exceptions）被作为无条件准则推广时，游戏/系统这一端的性能与可读性都会真实受损**。这是一篇把 Casey Muratori、Jonathan Blow、Jason Booth 观点汇合的典型发声。

## 他的核心论点

1. **代码不是画作（code is a tool, not a painting）**：写代码不是审美活动而是给机器+同事传达意图，过度装饰反而损害两者。
2. **「简短函数」+「深继承」+「STL 算法链」的组合让 debug build 慢 25-57%**，release 等价，而 debug build 是日常工作环境；牺牲 debug 速度换 release 无收益的「清洁」是错误贸易。
3. **抽象有成本**——每层 accessor、每个 iterator、每个 lambda 都让 watch window 多跳一层、stack frame 多压一层。
4. **不要类型炫技**——SFINAE、CRTP、各种 fold expression，在 9/10 次看起来聪明，读它的人（包括未来的你）只会骂娘。

## 具体例子：`std::transform` vs 手写 for

```cpp
std::string str = "Hello String";
// 标准 for
for (size_t i = 0, size = str.size(); i != size; ++i)
    str[i] = toupper(str[i]);
// Ranged-for（最清晰）
for (char& c : str) c = toupper(c);
// std::transform
std::transform(str.begin(), str.end(), str.begin(), toupper);
```

实测 Clang 下：

| 版本 | debug | release |
|---|---|---|
| 标准 for | 1.00× | 1.000× |
| iterator | 1.28× | 1.004× |
| ranged-for | 1.13× | 1.002× |
| std::transform | 1.57× | 1.003× |
| std::for_each | 1.42× | 1.000× |

release 差不多，debug 差 57%。多数业内观察者（Elopez、Muratori、Booth）的结论是 ranged-for 或标准 for 通常是最佳默认。

## 他给出的实用准则

- **花时间起名**——命名是 NP 难问题之一，acronym 救不了你；
- **别写复杂调用栈**——调 bug 时每多一层 F11 就是一次注意力断裂；
- **别因 SOLID 造类继承树**——只在真正需要时抽象；
- **变量不复用**——注释掉中间一段的风险；
- **别为节一行省去花括号或空格**——读者的调试时间比你键盘的寿命贵；
- **注释说 why、代码说 what**——`// initialize i` 是噪声；
- **Pythagoras 不在乎**：如果 `3.1415f` vs `<math.h>` 要拉进头文件的代价，宁可 copy-paste。

## 与 Ousterhout / Norvig 的对比

- [[john-ousterhout]] 的 [[deep-modules|deep module]] 立场和 Elopez 有大量重合：**把复杂藏在好接口后**，反对 shallow module 堆叠。
- 但 Ousterhout 更偏「长期架构」，Elopez 更偏「编译+调试+性能」——两人对「何时该抽象」的阈值相近，对「STL 算法是否算抽象成本」有分歧。
- Casey Muratori 的 *Clean Code, Horrible Performance* 是最直接的同源发声。
- Jason Booth 的 *OOP, AoS vs SoA* 的实测也在这一派。

## 这不是「永远不写抽象」

游戏引擎里 render graph、asset pipeline、ECS 本身都是大量抽象。区别在于：

- **抽象要换到对应的性能/维护代价**；
- **抽象的边界要清楚**（per-frame 的 particle update 不该戴继承帽子，mesh loader 可以）；
- **默认怀疑新抽象**，而不是默认推崇。

## 相关
- [[graphics-programmer-constraints]]
- [[tactical-programming]]
- [[strategic-programming]]
- [[aos-vs-soa]]
- [[cognitive-load]]
- [[cleaning-bad-code]] — Frykholm 的遗留代码清理操作手册（9 条）

## Sources

- [[sources/elopezr-graphics-programmer-life]]
