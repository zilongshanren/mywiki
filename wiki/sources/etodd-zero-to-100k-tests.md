---
tags: [source, testing, software-design, mocking, devops]
date: 2026-04-19
sources: 1
---

# Zero to One Hundred Thousand Tests（Evan Todd, 2025-01）

[[evan-todd]] 2025 年 1 月的博文，是 [[sources/etodd-waiting-on-tests]] 的续篇。StrongDM 从零测试做到超过 100,000 条测试、70% 代码覆盖之后，作者回过头反思：什么叫"好测试"？答案出人意料地"反覆盖率原教旨"。

## 摘要

作者先退后两步问根本问题："软件公司存在的目的是什么？" 答：赚钱。然后借 [xkcd 722](https://xkcd.com/722/) 把软件比作一盘灯：有些灯"赚钱"，有些"可能赚钱"，大部分根本没亮。由此抽出两个目标：

- **Goal #1**：让"赚钱"灯数量单调递增（不要出现 CrowdStrike 那种集体熄灭）。
- **Goal #2**：尽快把"可能赚钱"灯变成"赚钱"灯（即缩短 design → build → test → release 的环路）。

作者认为自动化测试对 Goal #1 是"超强技能卡"——一次写、无数次跑，回归测试是手工测试的降维打击。但对 Goal #2，自动化测试的性价比其实**不**高：新功能要靠手工测试和 beta 测试去发现"根本方向错了"的致命风险，因为自动化测试只能测你已经预想到的 case。

接着给出两条实践原则：

1. **System boundary**：测试边界应当围绕整个业务逻辑 + 数据访问层画一圈，而不是一层一层分别测。按层分，每一层都得 mock 下层，耦合极强、改动扩散范围极大。IO 边界是好边界（Postgres 在事务里真跑，测试结束 rollback）；"慢"才值得 mock，单纯"懒得搭场景"不值得——写一个 test helper 永远比 mock 划算。
2. **100% coverage 陷阱**：为了覆盖 Go 的 `if err != nil { return ... }` 分支，不得不大量 mock，产出一堆脆弱测试。这些测试其实可以被 linter 代替，作者主张直接删。

他给了一正一反两个例子：`TestCreateRoleDuplicateName` 正确的写法是从外部调用两次 `Create` 并检查 already-exists；错误写法则用 mock 把 `GetByName` 塞进去触发内部路径——这种测试连 `GetByName` 改个名都会编译失败，典型的"改一行业务代码 → 改 100 行 mock"的 change amplification。

## 关键要点

- 自动化测试核心价值 = 防回归（Goal #1），不是发现新 bug。
- 新功能风险用手工 / beta 测试覆盖更划算；自动化测试只能测你已经能预想的 case。
- 好边界画在整个业务逻辑外圈，mock 只给真正的 IO（或慢的东西）；其它场景宁可写 test helper。
- **100% 覆盖率不是目标**，目标是那两盏灯的动态。Go 错误分支的 mock 洪流可以用 linter 替代然后整体删除。
- 坏测试的信号：改一行业务代码，100 行测试跟着改（mock 把实现细节当 API）。
- 测试本身也在"Maybe zone"里占时间，过度测试会让产品错失方向，这是 Goal #1 和 Goal #2 的张力。

## 链接到的概念

- [[automated-test-philosophy]]
- [[ci-cost-optimization-asg]]
- [[change-amplification]]
- [[information-hiding]]

## 原文

- 链接：https://etodd.io/2025/01/06/zero-to-one-hundred-thousand-tests/
- 本地：`raw/articles/etodd.io/2025-01-06_zero-to-one-hundred-thousand-tests.md`
