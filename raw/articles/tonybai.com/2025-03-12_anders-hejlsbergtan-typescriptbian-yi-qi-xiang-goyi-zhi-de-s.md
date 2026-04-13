---
title: Anders Hejlsberg谈TypeScript编译器向Go移植的实践与规划
url: https://tonybai.com/2025/03/12/typescript-native-port-to-go/
published: '2025-03-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Anders Hejlsberg谈TypeScript编译器向Go移植的实践与规划

![](../../assets/2d3d889c55d50098.png)


[本文永久链接](https://tonybai.com/2025/03/12/typescript-native-port-to-go) – https://tonybai.com/2025/03/12/typescript-native-port-to-go

TypeScript、C#语言、Delphi语言之父

[Anders Hejlsberg]今日在Microsoft开发者博客宣布重大消息，[TypeScript编译器以及工具链将移植到Go语言]，性能提升高达10倍！这究竟是怎么回事？为什么要用Go？对开发者有什么影响？本文将为你深度解读。

## TypeScript迎来史诗级更新，性能提升10倍！

就在今天，TypeScript社区迎来了一颗重磅炸弹！微软技术院士、TypeScript首席架构师、C#、Delphi和Turbo Pascal的最初设计者——**Anders Hejlsberg**，亲自在微软开发者博客上宣布，TypeScript团队正在进行一项激动人心的计划：**将TypeScript编译器和相关工具链移植到Go语言！**

这一举动旨在解决TypeScript在大型代码库中性能瓶颈的问题，为开发者带来更流畅、更高效的开发体验。根据官方公布的数据，新的原生实现将带来以下惊人的改进：

**编辑器启动的项目加载速度提升8倍！****大多数构建时间缩短10倍！****内存使用量大幅减少！**

这意味着，开发者将告别漫长的加载和等待，享受“秒开”项目的快感，获得更流畅的代码编辑、智能提示、代码导航等体验。

## 实测数据说话，性能提升肉眼可见！

为了证明新版编译器的强大性能，TypeScript团队选取了GitHub上多个不同规模的热门TypeScript项目进行测试，以下是测试结果：

![](../../assets/1be47f4d384cb174.png)


从数据中我们可以清晰地看到，无论是大型项目如 VS Code，还是小型库如 rxjs，新版编译器都实现了 **10 倍左右的性能提升**！

![](../../assets/41835a550fbcc8d2.png)


Anders Hejlsberg 表示，这仅仅是开始，随着开发的深入，性能还将进一步优化。

## 为什么要移植到Go？

面对这一重大变革，很多开发者可能会疑惑：为什么选择Go语言？C#或者Rust不香吗？

对此，Anders Hejlsberg和TypeScript团队在[TypeScript GitHub仓库的讨论区](https://github.com/microsoft/typescript-go/discussions/411)进行了解释，主要原因有以下几点：

**代码结构相似性：**TypeScript 现有代码库采用函数式编程风格，很少使用类。而Go语言也以函数和数据结构为中心，与现有代码结构高度相似，这使得移植工作更加容易。**内存管理：**Go语言提供自动垃圾回收（GC），无需开发者手动管理内存，这大大简化了移植过程，降低了代码复杂度。同时，Go的GC对TypeScript编译器这类批处理任务影响很小。**内存布局控制：**Go语言允许对内存布局和分配进行精细控制，这对于优化性能至关重要。**图处理能力：**TypeScript编译器涉及大量的树遍历和多态节点处理，Go语言在这方面表现出色。

Anders Hejlsberg 强调，这是一次“移植”而非“重写”，目标是尽可能保留现有代码库的结构和语义，确保兼容性。Go语言的特性与TypeScript现有代码库的契合度最高，是“阻力最小”的路径。

**针对社区关心的为什么不选择C#，Anders Hejlsberg也做了专门回应：**

- Go是能同时做到原生性和自动垃圾收集的最低层级语言。
- C#是字节码优先的，虽然也有AOT编译，但有平台限制，且没有像Go一样经过长时间的生产环境验证。
- C#是重OOP范式的，TypeScript的JS代码库是高度函数式的。

## 版本路线图

TypeScript团队公布了明确的版本路线图：

- 当前版本为TypeScript 5.8，即将发布TypeScript 5.9。
- 基于JavaScript的代码库将继续开发到 6.x 系列，TypeScript 6.0 将引入一些弃用和破坏性更改，为原生代码库做准备。
- 当原生代码库达到与当前TypeScript相当的功能时，将发布
**TypeScript 7.0**。 - 为了保持清晰，TS团队将分别称之为TypeScript 6 (JS) 和 TypeScript 7 (native)。
- TypeScript 6 (JS) 将持续维护，直到 TypeScript 7+ 达到足够的成熟度和采用率。
- 内部讨论或代码注释中可能会出现“Strada” (TypeScript 原始代号)和“Corsa” (此次工作的代号)。

TypeScript团队预计在2025年中期发布一个能够进行命令行类型检查的原生tsc实现，并在年底发布一个功能完整的项目构建和语言服务解决方案。

## 开发者可以做什么？

**尝鲜体验：**你现在就可以从[typescript-go仓库](https://github.com/microsoft/typescript-go)构建和运行Go语言编写的代码，体验新版编译器的强大性能。**关注动态：**关注TypeScript团队的博客和GitHub仓库，获取最新进展。**参与讨论：**参与[TypeScript Community Discord](https://discord.gg/typescript)的 AMA 活动（太平洋时间 3 月 13 日上午 10 点 | UTC 时间下午 5 点），与 TypeScript 团队交流。

## 展望未来

10倍的性能提升，将为TypeScript和JavaScript开发体验带来巨大飞跃。曾经遥不可及的功能，如今触手可及。这不仅意味着更快的编译速度和更流畅的开发体验，还将为AI驱动的新一代开发工具奠定基础。

TypeScript的这次重大变革，再次证明了微软对开发者社区的承诺，以及对技术创新的不懈追求。让我们一起期待TypeScript的未来，迎接更高效、更智能的开发时代！

## 参考资料

[A 10x Faster TypeScript](https://devblogs.microsoft.com/typescript/typescript-native-port/)– https://devblogs.microsoft.com/typescript/typescript-native-port/[discussions: Why Go?](https://github.com/microsoft/typescript-go/discussions/411)– https://github.com/microsoft/typescript-go/discussions/411[TypeScript is being ported to Go | interview with Anders Hejlsberg](https://www.youtube.com/watch?v=10qowKUW82U)– https://www.youtube.com/watch?v=10qowKUW82U

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


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

翻了下原文，好像并没有提AOT的问题？这个来源是？

https://github.com/microsoft/typescript-go/discussions/411 官方讨论中有。

Anders的专访中也有提到：https://www.youtube.com/watch?v=10qowKUW82U

ts 7(native) 是指计划将ts直接native编译为二进制而非js吗？

不是的。全篇都在说ts的编译器tsc。ts7(native)我理解就是tsc-go（用go实现的版本）。tsc功能不会变，依然是将ts翻译为js。

运行时还是浏览器中js的引擎或node.js。