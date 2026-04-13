---
title: 拯救你的Commit Log：Conventional Commits实践指南
url: https://tonybai.com/2025/04/24/conventional-commits-guide/
published: '2025-04-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 拯救你的Commit Log：Conventional Commits实践指南

![](../../assets/d73722cc86cb26a5.png)


[本文永久链接](https://tonybai.com/2025/04/24/conventional-commits-guide) – https://tonybai.com/2025/04/24/conventional-commits-guide

告别混乱Commit Log！用规范指引你写出有意义的提交！


大家好，我是Tony Bai。

Git的Commit Log (提交日志) 是项目演进的脉络，也是开发者之间沟通变更、追溯历史、理解代码演变的关键载体。然而，在实际开发中，我们常常面对杂乱无章、意义不明的提交信息——”fix bug”、”update code”、”wip” 等屡见不鲜。这些模糊的记录不仅让代码审查、问题排查和版本追溯变得异常困难，也阻碍了自动化流程的实施。[Conventional Commits (约定式提交) 规范](https://www.conventionalcommits.org/en/v1.0.0/)提供了一套清晰、简洁的指引，旨在将每一次提交都转化为有意义、结构化的信息单元，从而显著提升 Commit Log 的价值和可利用性。

在这篇文章中，我们将探讨Conventional Commits如何作为一项关键指引，帮助开发者和团队构建更清晰、更一致、更具信息量的提交历史。

## 1. Commit Log的困境：为何需要指引？

缺乏明确指引的Commit Log往往会陷入以下困境：

**信息熵高，有效信息少:**大量模糊、随意的提交信息混杂在一起，难以快速定位关键变更或理解特定提交的目的。**沟通效率低下:**团队成员需要花费额外时间去解读他人的提交意图，代码审查效率降低。**历史追溯困难:**当需要回溯某个功能或 Bug 的引入/修复历史时，无结构的日志如同大海捞针。**自动化阻碍:**不一致、不可预测的提交信息使得自动化生成 Changelog、语义化版本控制（SemVer）等流程难以实现。

面对这些普遍存在的困境，业界亟需一套行之有效的规范来引导开发者记录更有价值的提交信息。这正是 Conventional Commits 规范所要解决的核心问题，它通过引入一套简洁而强大的结构化指引来实现这一目标。Conventional Commits并非强制性的铁律，而是一套**强大的指引 (Guidance)**，它通过引入轻量级的结构化约定，引导开发者在提交时思考并明确表达变更的**性质、范围和影响**。

## 2. Conventional Commits 核心指引：结构化的力量

该规范的核心指引体现在其简洁的提交信息结构上(如下所示)：

```
<type>[optional scope]: <description>
[optional body]
[optional footer(s)]
```


遵循这项指引，每次提交都应包含以下关键要素：

-
**Type (类型):****[必须遵循的指引]**表明提交的性质。规范定义了基础类型：- fix:：修复 Bug (对应 SemVer PATCH)。
- feat:：引入新功能 (对应 SemVer MINOR)。
**鼓励扩展:**团队可以根据需要定义其他类型，如 build, chore(用于标记那些不涉及新特性或修复的常规维护工作，比如更新依赖项等), ci, docs, style, refactor, perf, test等，以适应具体工作流。这些扩展类型本身通常不直接影响版本号（除非包含破坏性变更）。

-
**Scope (范围):****[可选但推荐的指引]**明确提交影响的代码库区域或模块，用括号包裹，如 feat(api): 或 fix(parser):。这极大地增强了信息的可定位性。 -
**Description (描述):****[必须遵循的指引]**紧跟冒号和空格，用简洁的语言（推荐使用祈使句现在时）概括本次提交的核心变更内容。这是提交信息的“标题”。 -
**Body (正文):****[可选指引]**当简短描述不足以说明时，提供更详细的上下文、动机和实现细节。与 Description 之间需空一行。 -
**Footer(s) (脚注):****[可选指引]**提供元数据，如关联 Issue (Refs: #123)。特别重要的两个脚注指引：- BREAKING CHANGE:
：明确标示不兼容的 API 变更 (对应 SemVer MAJOR)。 - INITIAL STABLE RELEASE:
：标记项目从 0.y.z 进入 1.0.0。

- BREAKING CHANGE:

**强调重要变更的简化指引：** 规范还提供了 ! (紧跟 type 或 scope 之后) 和 !! 作为标记 BREAKING CHANGE 和 INITIAL STABLE RELEASE 的快捷方式，进一步简化遵循指引的实践。

为了更直观地理解这个结构，以下是一些典型的Conventional Commits示例：

**简单的 Bug 修复:**

```
fix: correct minor typos in documentation
```


**带范围的新功能:**

```
feat(lang): add Polish language support
```


**使用 ! 标记破坏性变更:**

```
refactor!(auth): remove deprecated JWT authentication method
```


注意：这里的 ! 表明这是一个破坏性变更，即使type是refactor。

**包含详细正文和脚注的提交:**

```
perf(api): improve user query performance significantly
Implemented a new indexing strategy for the users table and optimized
the SQL query execution plan. Initial tests show a 50% reduction
in average query latency under heavy load.
Reviewed-by: Alice <alice@example.com>
Refs: #456, #478
```


**使用 !! 标记首次稳定版发布:**

```
chore(release)!!: prepare for 1.0.0 stable release
Finalized documentation, updated dependencies, and ran comprehensive
end-to-end tests to ensure stability for the first major release.
INITIAL STABLE RELEASE: The project is now considered stable for production use.
```


通过遵循这些简单的指引，原本混乱的Commit Log就被转化为结构清晰、信息丰富的记录。

理解了 Conventional Commits 的核心结构和要素后，我们自然会问：遵循这项指引究竟能为开发者和团队带来哪些实实在在的好处？答案是多方面的，它能让原本静态、难以利用的 Commit Log “活”起来，释放出巨大的潜在价值。

首先，结构化的 type 和 scope 提升了可读性与可理解性，使团队能够快速筛选和定位信息，清晰的 description 和 body 阐述了变更的“什么”和“为什么”。

其次，一致的格式增强了团队沟通与协作，减少了误解，提高了代码审查和协作效率，使每一次提交都成为清晰的沟通。

此外，结构化的日志简化了历史追溯与问题排查，便于查找特定功能引入、Bug 修复或破坏性变更的源头。

最后，一个充满有意义提交的日志自然而然地成为自动化工具的理想输入，能够驱动自动化生成 CHANGELOG、自动化 SemVer 版本判断，以及基于提交类型触发不同的 CI/CD 流程。

认识到 Conventional Commits 带来的显著价值后，如何在日常开发中有效地遵循并最大化其效益，就成了一个关键问题。仅仅了解规范的语法是不够的，掌握一些最佳实践和深入的洞察，能帮助我们更好地将这项指引融入工作流。

## 3. 遵循指引的最佳实践与洞察

为了更好地应用Conventional Commits指引，以下几点值得关注：

-
**原子化提交:**我们鼓励将复杂的变更分解为多个逻辑上独立的、遵循单一type的提交。这本身就是一种良好的 Git 实践，很多大厂的git commit规范以及代码review规范也是这么要求的。Conventional Commits 进一步强化了这一点。 -
**选择最合适的Type:**当一次提交包含多种类型的变更时（虽然应尽量避免），选择最能代表其核心意图的 type，并在 Body 中详述其他变更。 -
**祈使句现在时:**推荐使用如 “Add feature”、”Fix bug” 的风格撰写 Description，简洁、直接，如同给代码库下达指令。 -
**利用工具辅助:**社区提供了丰富的工具（如[Commitizen](https://commitizen-tools.github.io/commitizen/),[commitlint](https://commitlint.js.org/)等）来帮助开发者遵循规范格式，并在提交前进行校验，降低遵循指引的负担。 -
**团队共识与逐步采纳:**引入规范需要团队达成共识。可以通过分享、讨论和使用工具逐步推广。

当然，良好实践的推广离不开工具的支持。幸运的是，围绕 Conventional Commits 已经形成了一个活跃的社区和丰富的工具生态系统，它们极大地降低了开发者遵循规范的门槛，让指引更容易落地。

## 4. 社区生态：工具让指引落地

Conventional Commits 的流行离不开活跃的社区和丰富的工具支持，它们帮助开发者轻松地将这项指引融入日常工作流：

**Commitizen:**交互式命令行工具，引导用户创建符合规范的提交信息。**Commitlint:**用于校验提交信息是否符合规范，常与 Git Hooks (如 husky) 集成。**IDE 插件:**主流 IDE (VS Code, JetBrains IDEs 等) 均有插件提供模板、补全和校验支持。**自动化版本与 Changelog 工具:**如[semantic-release](https://github.com/semantic-release/semantic-release),[goreleaser/chglog](https://github.com/goreleaser/chglog)等，它们消费符合规范的提交历史。

这两年基于大模型的辅助生成commit log的工具以及一些代码智能体应用(如Cursor等）也在规范git commit log方面起到了非常积极的作用，对于像我这样英语非母语但又喜欢以英文log提交的选手来说，这些工具大幅降低了我在纠结如何写commit log时的心智负担，给予了我很大的帮助。

## 5. 小结

总而言之，Conventional Commits 远不止一套冷冰冰的格式规则，它更像是一位**贴心的向导**，一项旨在**将每一次提交都转化为宝贵信息资产**的核心指引。它赋予我们结构化的力量，能够将困扰许多团队的**混乱、低效的Commit Log**，转变为**清晰、一致且富有洞察力**的项目演进历史——这对于提升代码可维护性、团队协作效率乃至自动化流程都至关重要。

现在，**就将这项指引融入你的日常开发吧！** 让每一次git commit不再是随意的记录，而是对项目演进负责任的、有意义的贡献。

**那么，你的团队是如何采纳和实践提交规范的？你在使用Conventional Commits或其他规范时，有什么独到的心得或踩过的“坑”吗？**

**非常期待在评论区看到你的分享与交流！**

如果这篇文章让你觉得“提交信息确实应该更有意义”，请分享给你的同事或团队，一起提升代码库的 Commit Log 质量吧!

别忘了**关注我**，持续获取更多提升研发效能的实用技巧与深度解析。

## 6. 参考资料

[Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/#specification)– https://www.conventionalcommits.org/en/v1.0.0/#specification

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论