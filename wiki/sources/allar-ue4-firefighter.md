---
tags: [source, unreal-engine, engineering-practices, team-management]
date: 2026-04-19
sources: 1
---

# Confessions of an Unreal Engine 4 Engineering Firefighter（Michael Allar）

[[michael-allar]] 发表于 2018 年 3 月的长文，以"UE4 工程救火员"的外包顾问视角复盘洛杉矶地区游戏工作室反复踩的管理和工程坑。一句话总结：**绝大多数"紧急 UE4 技术问题"，本质是团队缺少资深工程师把关和管理层不听一线意见**。

## 摘要

Allar 做的是匿名白牌顾问——被叫进来的时候项目通常离上线只剩几周、团队已经烧光预算。他把反复遇到的问题分成两类：一是管理层故事（没有 senior/lead、公司文化让员工不敢提问题、用初级工程师干资深的活、不听下属反馈、和 publisher 签了不对等的合同），二是纯工程清单（缓存文件进了源码库导致引擎跳过必要的烘焙、Blueprint 意大利面、没人跑 profiler、VR 项目不用 forward、component 嵌套过深、4K 贴图满天飞、把警告当空气）。文章的核心论点不是"如何写更好的 UE4 代码"，而是"能不能准时上线的决定因素是：团队能不能在问题变成火灾之前识别它"。识别问题占他工作时间的 95%，真正修复只占 4%。

## 关键要点

- 高频起火原因：管理层请不到 senior 就"算了让现有团队扛"，然后项目在最后两周崩溃。
- 典型技术事故：Perforce 配置错误，把引擎缓存当项目资产同步，导致只有原作者能正常听到游戏音效——被误以为是外包音频团队交付问题，几乎引发诉讼。
- 工程师分级的判断维度：看他需要从哪里获得支持——上级（mid）、同级（senior/lead）、下级（entry）。Lead 不等于 senior：前者管人，后者解难题。
- 不听员工意见的团队可以由 7 人降到 2 人只花一个月；让所有人说话然后真的行动的团队，三年能翻 3 倍。
- "GDC War Story" 黑名单：公司对公事务在脱衣舞俱乐部搞、工位上吸毒、因为追员工配偶而招人/开人、长期拖欠工资等——都真实遇到过。

## 链接到的概念

- [[michael-allar]]
- [[ue4-common-perf-pitfalls]]

## 原文

- 链接：https://allarsblog.com/2018/03/17/confessions-of-an-unreal-engine-4-engineering-firefighter/
- 本地：`raw/articles/allarsblog.com/2018-03-17_confessions-of-an-unreal-engine-4-engineering-firefighter.md`
