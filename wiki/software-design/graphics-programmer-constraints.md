---
tags: [graphics, career, software-design, constraints]
date: 2026-04-19
sources: 1
---

# 图形程序员的硬约束

[[emilio-lopez-ros]] 的 *Life and Death of a Graphics Programmer* 把图形/游戏程序员与其它行业程序员的差异一次说透：**性能是正确性的一部分**。这一约束塑造了这个行业一切技术选择，从语言偏好到 clean code 立场。

## 三类程序员世界观

| 维度 | 游戏 / 嵌入式 | UI 软件（浏览器、IDE） | HFT / 航天 |
|---|---|---|---|
| 延迟要求 | 硬实时 16/33 ms | 软实时（事件驱动） | 硬实时但领域窄 |
| 正确性 | 对玩家友好、可容忍小 bug | 中等 | 近乎零容忍 |
| 安全性 | 低（除了在线游戏） | 高（浏览器沙箱、OS） | 极高（生命、金钱） |
| 发布模式 | 版本冻结 + hotfix | 持续发布 | 强认证 |
| 常用 C++ | 自研容器、avoid STL | 标准 STL + boost | 子集严格静态检查 |

**游戏这一列对性能的「视正确性一部分」的坚持，让很多在其它行业很自然的做法在这里不适用**——例如 clean code 推荐的小函数深继承、iterator-heavy STL 链、exceptions + RTTI。这不是品味差异，是需求不同。

## 硬约束清单

1. **帧预算 16/33 ms 全程责任**——任何子系统不能假设自己可以 skip 帧；
2. **编译时间是开发速度的瓶颈**——AAA 全量 rebuild 十几分钟，所以 PCH/Unity/forward declaration 全是工程活；
3. **debug build 必须能真跑** 15-25 fps 可玩，否则程序员会改 release build，真 bug 抓不到；
4. **工具性能是同事的时间**——美术的烘焙、LOD、navmesh 慢一小时 = 一天只能跑 8 次；
5. **NDA 知识密度高**——console SDK、GPU 驱动怪事、特定团队的 buffer 管理方式，在公开资料里找不到。

## 为什么这一行偏爱自研 STL

EA 的 EASTL、许多 3A 厂的自研容器不是 NIH 而是被逼：

- STL 容器都 heap 分配，游戏要 `fixed_vector`、`fixed_string` 来避免分配；
- SSO 阈值不标准导致跨平台行为漂移；
- STL 的编译时间与 debug build 性能对 AAA 都偏慢；
- STL 升级绑 C++ 版本，但平台工具链演进慢，不能等；
- 缺 intrusive pointer、intrusive list 等游戏常用模式。

## 这一页在 wiki 中的位置

这是对 [[clean-code-critique]] 的背景铺垫。两篇合看就能理解：**不是 clean code 错，是 clean code 的默认好处（可读、抽象、可维护）在图形/游戏领域的权重排序不同**——我们愿意牺牲若干层抽象换 debug build 速度、换 codegen 可预测、换美术迭代时间。

## Sources

- [[sources/elopezr-graphics-programmer-life]]
