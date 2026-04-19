---
tags: [source, unity, dots, ecs, tween, performance]
date: 2026-04-19
sources: 1
---

# Unity DOTS Tween 系统案例（Ted Sie / 阿祥的开发日常）

[[ted-sie|Ted Sie]] 发表于 2020 年 5 月的文章，把传统 MonoBehaviour Tween 迁移到 Unity DOTS，给出完整实现、性能数据和工程坑。

## 摘要

在 50 万物体的测试环境下，DOTS 版 Tween 把 CPU 耗时从 614.5ms 降到 64.3ms（约 89.5% 提升）。实现分五层：`TweenBase` 通用 Component、`TweenBaseSystem` 更新时间与 lerp、`TweenFloat3/4` 带类型的 from/to/result、`TweenInterpolationSystem` 做 `math.lerp`、最终应用层（`TweenLocalRotationSystem` 等）借 `TransformAccessArray + IJobParallelForTransform + BurstCompile` 写回 Transform。Ease Function 通过 **标签 Component + `[UpdateAfter]`** 开关代码路径。对 Light 这类非 Transform 的 managed object，只能 `WithoutBurst() + Entities.ForEach` 同步访问，失去 Burst 收益，属下策。生命期管理靠 `EntityCommandBuffer` 延迟添加 `TweenComplete / TweenDestroy` 标签，分 System 处理销毁。文末评论指出 Tween 本属 UI 多发场景、规模小 DOTS 化收益有限——呼应"DOTS 收益与数据规模强相关"的一般规律。

## 关键要点

- 五层拆分：基础数据 / 时间更新 / 类型化插值数据 / lerp 计算 / Transform 写回。
- 标签 Component + `[UpdateAfter]` 是 DOTS 控制流的核心 idiom。
- `IJobParallelForTransform` 是 Unity 为 Transform 黑盒的特例；其他 managed object 只能退化为 `WithoutBurst`。
- `EntityCommandBuffer` 把结构性操作延迟到安全点；`entityInQueryIndex` 是保留参数名。
- 规模是 DOTS 的前提——小数据量 MonoBehaviour 够用。

## 链接到的概念

- [[unity-dots-tween-system]]
- [[ecs]]
- [[aos-vs-soa]]
- [[cache-friendliness]]

## 原文

- 链接：https://tedsieblog.wordpress.com/2020/05/07/unity-dots-a-case-study-of-tween-system/
- 本地：`raw/articles/tedsieblog.wordpress.com/2020-05-07_unity-dots-a-case-study-of-tween-system.md`
