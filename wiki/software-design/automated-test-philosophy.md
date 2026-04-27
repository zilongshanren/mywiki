---
tags: [测试, 软件工程, 架构]
date: 2026-04-19
sources: 1
---

# Automated Test Philosophy —— 防回归是本命，发现新 bug 是副业

[[evan-todd]] 在 StrongDM 把自动化测试从 0 做到 100,000+ 条之后写下的反思。核心观点：自动化测试的首要目的不是发现 bug，而是确保**已经赚钱的功能继续赚钱**。这个定位决定了怎么画测试边界、怎么看待覆盖率、什么样的测试是好的。

## 两盏灯的框架

软件系统可以想成一盘灯泡：**Money 灯**是稳定赚钱的功能，**Maybe 灯**是尚未验证是否赚钱的新功能，剩下的是没点亮的功能。软件公司的目标拆成两条：

- **Goal #1**：Money 灯数量单调递增，绝对不能让它们熄灭（CrowdStrike 事件是反例）。
- **Goal #2**：把 Maybe 灯尽快变成 Money 灯——即压缩 design → build → test → release → 回款 的循环时长。

自动化测试对 Goal #1 是压倒性胜利：写一次、跑无数次，回归测试覆盖了全部 Money 灯，人工不可能每次都全量回归。对 Goal #2 却帮助有限——你只能测自己**能预想到**的 case，而新功能最大的风险恰恰是"方向就错了"。所以作者主张新功能阶段的风险用手工测试 + beta 测试更划算，自动化测试留给防回归。

## 系统边界画在哪

坏边界：按层画。业务逻辑测一遍、数据访问层测一遍、每一层都要 mock 下一层。结果是改一行业务代码要改 100 行 mock，测试耦合实现细节，轻微重构就爆炸——典型的 [[change-amplification]]。

好边界：**把整个业务逻辑 + 数据访问层当成一个 system under test**，只有最外围的 IO 才 mock。StrongDM 的做法是让每条测试在真 Postgres 的独立事务里跑，结束 rollback，天然隔离、天然并发。这和 [[information-hiding]] 的 [[deep-modules]] 一致：测试应该通过稳定的外部接口验证行为，而不是抓着内部调用结构不放。

## 两条判据

- **只在真正的 IO 或真正慢的东西上 mock**。"懒得搭测试场景"不是理由——写一个 test helper 永远比 mock 划算，因为 helper 可以复用，mock 只会制造脆弱性。
- **100% 覆盖率不是目标**。StrongDM 为了覆盖 Go 错误分支 `if err != nil { return ... }` 写了上千条 mock 测试，其实可以用 linter 替代然后整体删除。覆盖率是手段，灯不熄才是目的。

## 好测试 vs 坏测试

一个具体例子：`TestCreateRoleDuplicateName`。

- **好版本**：创建一个 role，再用同名创建第二个，期望收到 already-exists 错误。改 `Create` 的内部实现完全不影响这条测试。
- **坏版本**：mock 掉 `GetByName` 让它返回假数据，触发冲突分支。改 `Create` 的调用顺序、或把 `GetByName` 改个名字——测试就全红。这是典型的"测试绑定实现，而不是行为"。

## 和 CI 加速的协同

好的 Goal #1 测试必须**快**——参见 [[ci-cost-optimization-asg]]，如果测试跑 15 分钟，开发闭环就被它拖死，Goal #2 也输了。所以 testing philosophy 和 CI infra 是配套工程。

## 相关

- [[ci-cost-optimization-asg]]
- [[change-amplification]]
- [[information-hiding]]
- [[deep-modules]]
- [[identity-problem-naming]]
- [[evan-todd]]
- [[render-integration-testing]] — 图形渲染器的像素级集成测试，idiff + Python 脚本方案

## Sources

- [[sources/etodd-zero-to-100k-tests]]
- [[sources/16bpp-methods-of-testing]]
