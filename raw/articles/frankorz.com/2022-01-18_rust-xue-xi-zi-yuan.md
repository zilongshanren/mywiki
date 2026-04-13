---
title: Rust 学习资源
url: http://frankorz.com/2022/01/18/rust-study-resource/
author: 文章作者 猫冬
published: '2022-01-18'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

博主发现咸鱼咸鱼着居然到 2022 年了，忽然良心不安，因此先从这篇比较水的资源总结开始吧！

这篇文章主要是总结下学 Rust 参考过的资料，会随着博主对 Rust 的关注随缘更新。

- 更新日志

2023/03/02 新增[noxasaxon/learning_rust.md](https://gist.github.com/noxasaxon/7bf5ebf930e281529161e51cd221cf8a)。

2023/01/06 新增 mouse 姐姐新书[《Rust Atomics and Locks: Low-Level Concurrency in Practice》](https://marabos.nl/atomics/)和STATE MACHINES。

2022/12/28 新增[Ray Tracing in One Week](https://misterdanb.github.io/raytracinginrust/)

2022/12/27 新增[LSM in a week](https://skyzh.github.io/mini-lsm/)

2022/12/25 新增[tfpk/macrokata](https://tfpk.github.io/macrokata)

2022/12/22 新增[Comprehensive Rust](https://google.github.io/comprehensive-rust/welcome.html)

2022/12/06 新增[night-cruise/async-rust](https://github.com/night-cruise/async-rust)

2022/11/28 新增[《dyn async traits》系列](https://smallcultfollowing.com/babysteps/)[中文版](https://zjp-cn.github.io/translation/dyn-async-traits.html)

2022/11/28 新增[Writing Interpreters in Rust: a Guide](https://rust-hosted-langs.github.io/book/introduction.html)[WebAssembly Compiler](https://www.bitfalter.com/webassembly-compiler-text-format-and-ast)

2022/11/15 新增[北京大学编译原理课程在线文档](https://pku-minic.github.io/online-doc/#/),[jondot/rust-how-do-i-start](https://github.com/jondot/rust-how-do-i-start)

2022/11/13 新增[Rust Game Series](https://www.jendrikillner.com/tags/rust/page/2/)

2022/10/17 新增[smallnest/concurrency-programming-via-rust 《Rust 并发编程实战课》](https://github.com/smallnest/concurrency-programming-via-rust)

2022/09/26 新增[Learn wgpu 中文版](https://jinleili.github.io/learn-wgpu-zh/),[Vulkan Tutorial(Rust)](https://kylemayes.github.io/vulkanalia/introduction.html)

2022/08/24 新增[Rust 源码剖析 中文版](https://github.com/awesome-kusion/rust-code-book)

2022/08/24 新增[Boshen/javascript-parser-in-rust](https://github.com/Boshen/javascript-parser-in-rust)[Writing a container in Rust](https://litchipi.github.io/series/container_in_rust)

2022/07/05 新增[Visualizing memory layout of Rust’s data types](https://www.youtube.com/watch?v=rDoqT-a6UFg)[2022年开源操作系统训练营](https://learningos.github.io/rust-based-os-comp2022/)

## 基础

[The Rust Programming Language](http://rust-lang.github.io/book/)- 堪称 Rust 的 “The Book”，是目前最权威的 Rust 系统教程，入门必读，最近也更新到了 2021 版本。
[中文版(经常更新)](https://kaisery.github.io/trpl-zh-cn/title-page.html)[rustwiki 中文版](https://rustwiki.org/zh-CN/book/)

[Rust by Example](https://rustwiki.org/zh-CN/rust-by-example/)- 实例化的讲解方法，通过一个个可实际运行的例子去介绍 Rust 的特性和用法，有的时候，代码是最好的老师。
[中文版](https://rustwiki.org/zh-CN/rust-by-example/)

[The Rust primer for beginners](https://github.com/rustcc/RustPrimer)- 给初学者的 Rust 中文教程。

[Rust入门秘籍](https://rust-book.junmajinlong.com/about.html)- 这是一本 Rust 的入门书籍，相比官方书籍《The Rust Programming Language》，本书要更详细、更具系统性，本书也尽量追求准确性。

[Rust First Steps](https://docs.microsoft.com/en-gb/learn/paths/rust-first-steps/)- 微软的 Rust 教程，简短精炼，适合初学者。
[官方中文](https://docs.microsoft.com/zh-cn/learn/paths/rust-first-steps/)

[Rust Cookbook](https://rust-lang-nursery.github.io/rust-cookbook/)- Rust 程序设计语言（
[Rust 官方教程简体中文版](https://rustwiki.org/zh-CN/book)）的简要实例示例集合：展示了在 Rust 生态系统中，使用各类 crate 来完成常见编程任务的良好实践。 [中文版](https://rustwiki.org/zh-CN/rust-cookbook/)

- Rust 程序设计语言（
[Rustlings](https://github.com/rust-lang/rustlings)- 官方出品，涵盖大量小练习，打怪通关学习 Rust。
- Jetbrains IDE 可以直接
[下载课程](https://plugins.jetbrains.com/plugin/16631-rustlings)，编辑器内写代码做练习。

[Learning Rust With Entirely Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/index.html)- 通过写双链表来学习 Rust

[Read Rust - Getting Started](https://readrust.net/getting-started)[Read Rust](https://readrust.net/)是一个集合了有价值的 Rust 文章/博客的网站，其中[Getting Started](https://readrust.net/getting-started)部分有各种 Rust 知识点相关的十分优秀的文章。

[Stanford CS 110L：Safety in Systems Programming](https://reberhardt.com/cs110l/spring-2020/handouts/course-information/)- This class is focused on safety and robustness in systems programming. We will use the Rust programming language as a vehicle to teach mental models and paradigms that have been shown to be helpful in preventing errors, and we will look at how these features have made their way back into C++.
[2020 年课程的 B 站中文字幕版](https://www.bilibili.com/video/BV1Ra411A7kN)[2021 年课程主页](https://reberhardt.com/cs110l/spring-2021/)、[2022 年课程主页](https://web.stanford.edu/class/cs110l/)

- Rust 语言圣经(Rust 教程 Rust Course)
[rust-course](https://github.com/sunface/rust-course)国人写的 Rust 教程，对Rust语言进行全面且深入的讲解，书中辅以生动的示例和习题。

[Rust 官方文档中文教程](https://rust.purewhite.io/)[rust-lang-cn 组织](https://github.com/rust-lang-cn)翻译的官方文档，另外这个组织也翻译了很多 Rust 相关的书籍。

[Visualizing memory layout of Rust’s data types](https://www.youtube.com/watch?v=rDoqT-a6UFg)- 可视化了 Rust 的类型在内存中的布局，入门必看。

[Rust 实践指南](https://rust-guide.budshome.com/)[zzy/rust-guide](https://github.com/zzy/rust-guide)《Rust 实践指南》，聚焦重要的主题，展示可能的解决方案。以开发中的实际问题为导向，以优雅的解决方案为目标，以完整的实例实践解决方案。

[Comprehensive Rust](https://google.github.io/comprehensive-rust/welcome.html)- Google Android 团队的四天 Rust 教程。

[Bilibili：软件工艺师](https://space.bilibili.com/361469957/video)- 微软 MVP，做了不少 C#、Go、Rust 的教程，其中 Rust 相关的有
[Rust编程语言入门教程](https://www.bilibili.com/video/BV1hp4y1k7SV)和[Rust Web 全栈开发教程](https://www.bilibili.com/video/BV1RP4y1G7KF)

- 微软 MVP，做了不少 C#、Go、Rust 的教程，其中 Rust 相关的有
[Rust Language Cheat Sheet](https://cheats.rs/)[quickref.me Rust cheatsheet](https://quickref.me/rust)[quickref.me](http://quickref.me)是一个汇聚了大部分语言的语法索引页, 其中也包含了 Rust, 可以帮助大家快速找到想用的语法。

[rust-lang/api-guidelines](https://github.com/rust-lang/api-guidelines)[中文版：Rust API 编写指南](https://zjp-cn.github.io/api-guidelines/about.html)这是一组关于如何设计和呈现 Rust APIs 的建议。 这些建议主要由 Rust library 团队编写， 总结了 Rust 生态下构建标准库和其他 crates 的经验。

[《Programming Rust, 2nd Edition》简单的翻译](https://blog.fudenglong.site/Programming-Rust/)- 第一版图灵社区有翻译：
[Rust程序设计](https://www.ituring.com.cn/book/2101)，第二版多了两章，可以考虑买第一版的电子版 pdf。

- 第一版图灵社区有翻译：
[rustlang-cn/Rustt](https://github.com/rustlang-cn/Rustt)- RustCn 翻译计划，翻译一些 Rust 的技术文章。

[suhanyujie/article-transfer-rs](https://github.com/suhanyujie/article-transfer-rs/)- 一些 Rust/Go 文章翻译


## 进阶

[Rust Standard Library Reference](https://doc.rust-lang.org/std/index.html)[The Rust Reference](https://doc.rust-lang.org/reference/index.html)- Rust 语言的 reference manual，你应该收藏好，以便于在对某个语言细节不清楚时在这里进行查阅。
[中文版](https://rustwiki.org/zh-CN/reference/)

[The unsafe Book](https://doc.rust-lang.org/nightly/unstable-book/index.html)[The Rustonomicon](https://doc.rust-lang.org/nomicon/)- Rust 死灵书主要讲 Rust 高级特性，如何使用 unsafe Rust。
[中文版](https://nomicon.purewhite.io/)

[The Little Book of Rust Macros](https://veykril.github.io/tlborm/introduction.html)- 对于 Rust 宏有详细的讲解，里面的注释很全面。
[中文版](https://zjp-cn.github.io/tlborm/)

[night-cruise/async-rust](https://github.com/night-cruise/async-rust)- 介绍 Rust 中 async/await 语法和异步运行时的原理和工作机制的电子书

[《dyn async traits》系列](https://smallcultfollowing.com/babysteps/)- Niko 是 Rust 语言诸多特性的设计者（比如 NLL）。这个系列主要探索在 trait 中支持 async fn，因此主要聚焦于思路梳理与原型设计。
[中文版](https://zjp-cn.github.io/translation/dyn-async-traits.html)

[smallnest/concurrency-programming-via-rust 《Rust 并发编程实战课》](https://github.com/smallnest/concurrency-programming-via-rust)- 《Go 并发编程实战课》的作者鸟窝系统整理的 Rust 的并发编程的相关资料。主要是从入门入手，让大家了解和熟悉这些并发原语，在工作中用起来。

[《Rust Atomics and Locks: Low-Level Concurrency in Practice》](https://marabos.nl/atomics/)- mouse 姐姐出版的关于 Rust 并发的书，可以在她博客免费阅读，亚马逊也可以购买：
[Amazon](https://www.amazon.com/Rust-Atomics-Locks-Low-Level-Concurrency/dp/1098119444)。

- mouse 姐姐出版的关于 Rust 并发的书，可以在她博客免费阅读，亚马逊也可以购买：
[Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/01_getting_started/01_chapter.html)[A Guide to Porting C/C++ to Rust](https://locka99.gitbooks.io/a-guide-to-porting-c-to-rust/content/)[The Rust FFI Omnibus](https://jakegoulding.com/rust-ffi-omnibus)- 使用 Rust 编写代码用到其他语言的示例集合.
[中文版](http://llever.com/rust-ffi-omnibus/)

[Jon Gjengset YouTube Channel](https://www.youtube.com/channel/UC_iD0xppBwwsrM9DegC5cQQ)([Crust of Rust Playlist](https://www.youtube.com/watch?v=rAl-9HwD858&list=PLqbS7AVVErFiWDOAVrPt7aYmnuuOLYvOa))[Rust Design Patterns](https://rust-unofficial.github.io/patterns/)- 有许多问题具有共同的形式。由于事实上 Rust 并不完全是面向对象的，设计模式也与其他面向对象的编程语言不同。 细节不同的同时，因为他们有相同的形式，他们可以用同样的基本方法解决。
[中文版](http://chuxiuhong.com/chuxiuhong-rust-patterns-zh/)

[The Rust Performance Book](https://nnethercote.github.io/perf-book/introduction.html)- 介绍很多优化 Rust 程序性能的工具、技巧、调试方法等方面的书。

[Problem-solving with algorithms and data structures using Rust](https://github.com/QMHTMY/RustBook)- 国人写的一本 Rust 书籍，包括算法分析，基本数据结构和算法，外加一些实战。

[Rust 源码剖析 中文版](https://github.com/awesome-kusion/rust-code-book)- 国人写的一本 Rust 书籍，针对 Rust 语言本身和开源库的代码进行分析。

[dtolnay/case-studies](https://github.com/dtolnay/case-studies)- dtolnay 是 anyhow, thiserror, cxx 等库的作者，这是他对一些 tricky Rust code 的分析。

[Bilibili：Databend](https://space.bilibili.com/275673537)- Databend 社区持续做了不少 Rust 的公开课。
[仓库地址](https://github.com/wubx/rust-in-databend/)

- Databend 社区持续做了不少 Rust 的公开课。
[Bilibili：爆米花胡了](https://space.bilibili.com/500416539/)- 这个 up 主做了很多 Rust 过程宏的视频教程。

[Bilibili：喜欢历史的程序君](https://space.bilibili.com/39222989)- 陈天在极客时间开了门 Rust 的课，同时也在持续输出一些 Rust 视频教程。

[KAIST CS431: Concurrent Programming](https://www.youtube.com/playlist?list=PL5aMzERQ_OZ9j40DJNlsem2qAGoFbfwb4)[Github repo](https://github.com/kaist-cp/cs431)- 本课程面向对并行计算机系统的现代理论和实践感兴趣的计算机科学（或相关学科）的高年级本科生（或研究生）。

[Rust for the Polyglot Programmer](https://www.chiark.greenend.org.uk/~ianmdlvl/rust-polyglot/index.html)- 面对有经验的程序员的 Rust 指南。

[High Assurance Rust: Developing Secure and Robust Software](https://highassurance.rs/landing.html)- 本书介绍了如何构建我们可以合理信任(justifiably trust)的高性能软件。这意味着有足够的数据来支持对我们代码的功能和安全性的信心。可信性是高安全性(high assurance)软件的一个标志。

[Warrenren/inside-rust-std-library](https://github.com/Warrenren/inside-rust-std-library)- 本书主要对 Rust 的标准库代码进行分析。按照内存相关，基本数据类型，ops Trait, Option 类型，Result 类型，Iterator，切片类型，智能指针类型等逐一进行源码分析。


## 有潜力的教程

[Rust 101 Lecture Series](https://www.youtube.com/watch?v=xOgdaL6A_AY&list=PL-zQguBgjr2O4d-B9g_b0WYh1fyXr6MMq)- 与伦敦帝国理工学院计算社会系合作的 Rust 系列讲座
[Rust Lecture Series with Imperial College London’s Department of Computing Society](https://www.reddit.com/r/rust/comments/smt5ef/rust_lecture_series_with_imperial_college_londons/)

[Effective Rust](https://lurklurk.org/effective-rust/intro.html)

## 练习实战的小项目

[知乎-学习Rust适合写什么练手项目？](https://www.zhihu.com/question/34665842)[Exercism.io](https://exercism.org/tracks/rust/exercises)[course-rs/tokio-course](https://github.com/course-rs/tokio-course)- 《Tokio 异步编程》翻译并扩展了 tokio 官网的教程， 深入讲述了如何编写 Rust 高并发异步程序

[Github: cfsamson](https://github.com/cfsamson?tab=repositories&q=&type=source&language=&sort=stargazers)- 这哥们喜欢用 Rust 实现一些小例子如：Futures、greenthreads、async、epoll 等。

- STATE MACHINES
[Part1](https://blog.yoshuawuyts.com/state-machines/)[Part2](https://blog.yoshuawuyts.com/state-machines-2/)[Part3](https://blog.yoshuawuyts.com/state-machines-3/)[2022.12]- 用 Rust 实现状态机

[LSM in a week](https://skyzh.github.io/mini-lsm/)[2022.12]- Build a simple LSM-Tree storage engine in Rust.
[Github](https://github.com/skyzh/mini-lsm)

- Build a simple LSM-Tree storage engine in Rust.
[tfpk/macrokata](https://tfpk.github.io/macrokata)[2022.12]- MacroKata, a set of exercises which you can use to learn how to write macros in Rust.
[Github](https://github.com/tfpk/macrokata)

- MacroKata, a set of exercises which you can use to learn how to write macros in Rust.
[Writing Interpreters in Rust: a Guide](https://rust-hosted-langs.github.io/book/introduction.html)[2022.11]- 用 Rust 写解释器，
[仓库](https://github.com/rust-hosted-langs/book)

- 用 Rust 写解释器，
[Boshen/javascript-parser-in-rust](https://github.com/Boshen/javascript-parser-in-rust)[2022.08]- A book on writing a JavaScript Parser in Rust

[2022年开源操作系统训练营](https://learningos.github.io/rust-based-os-comp2022/)[2022.07]- 教程共分为八章，主要展示如何从零开始，用 Rust 语言写一个基于 RISC-V 架构的类 Unix 内核。

[北京大学编译原理课程在线文档](https://pku-minic.github.io/online-doc/#/)[2022.06][Writing a container in Rust](https://litchipi.github.io/series/container_in_rust)[2022.05]- 用 Rust 写容器。

[Lisp interpreter in Rust](https://vishpat.github.io/lisp-rs/)[2022.05][lisp-rs](https://github.com/vishpat/lisp-rs)项目用 Rust 实现了一个解释器，用于 Scheme 的一个小子集，即 Lisp 方言。

[Implementing a size-bounded LRU cache with expiring entries for my DNS server (in Rust)](https://memo.barrucadu.co.uk/dns-cache.html)[2022.03]- 使用 Rust 实现一个有大小限制可过期的 LRU 缓存。

[Implementing and Optimizing a Wordle Solver in Rust](https://www.youtube.com/watch?v=doFowk4xj7Q)[2022.03]- Jon Gjengset 的六小时一镜到底视频流教程，这次是实现一个 Wordle 求解器。

[Writing a Programming Language (in Rust)](https://www.youtube.com/playlist?list=PLkpGh2gaaueyzEAn07jf44LdscDeWRyzy)[2022.02 updating][Implementing the NTFS filesystem in Rust](https://fosdem.org/2022/schedule/event/misc_ntfs_rust/)[2022.02][Rust Latam: procedural macros workshop](https://github.com/dtolnay/proc-macro-workshop)[2022.01 updating]- 实战学习写 Rust 过程宏。

[Rust Runtime 设计与实现](https://www.ihcblog.com/rust-runtime-design-1/)[2021.12]- 系列文章主要介绍如何设计和实现一个基于 io-uring 的 Thread-per-core 模型的 Runtime。

[Building a GUI app in Rust](https://www.youtube.com/watch?v=NtUkr_z7l84)[Building a web app in Rust](https://www.youtube.com/watch?v=NtUkr_z7l84)[2021.10]- 作者用 egui 库去实现了 newsapi 的客户端和网页端（WebAssembly）。

[Rust过程宏入门](https://frank-king.github.io/rustblog-zh/2021-01-proc-macro/00.html)[(Risp (in (Rust) (Lisp)))](https://stopachka.essay.dev/post/5/risp-in-rust-lisp)[2021.07]- Rust 实现 Lisp 解释器

[WebAssembly Compiler](https://www.bitfalter.com/webassembly-compiler-text-format-and-ast)[2021.05]- Rust 实现 WebAssembly Parser, Compiler and Runtime.

[Learning to Fly: Let’s simulate evolution in Rust! (pt 1)](https://pwy.io/en/posts/learning-to-fly-pt1/)[2021.01]- 利用神经网络和遗传算法创建一个进化模拟，并编译应用程序到 WebAssembly

[Ray Tracing in One Week](https://misterdanb.github.io/raytracinginrust/)[2020.12]- Ray Tracing in One Week 系列的 Rust 版本
[Github](https://github.com/misterdanb/raytracinginrust)

- Ray Tracing in One Week 系列的 Rust 版本
[Rust Game Series](https://www.jendrikillner.com/tags/rust/page/2/)[2020.11]- 用 Rust 和 winapi 来用 D3D11 写三消游戏

[Building a Pixel Editor in Rust & WebAssembly (and Javascript)](https://www.youtube.com/watch?v=rHRBJKWbbw0)[2020.08]- 作者用 Rust 和 WebAssembly 做了个网页端的简陋版像素画板。

[Writing NES Emulator in Rust](https://bugzmanov.github.io/nes_ebook/chapter_1.html)[2020.08]- Rust 实现 NES 模拟器，不过最后一章到现在还是 todo。

[Building a DNS server in Rust](https://github.com/EmilHernvall/dnsguide/blob/master/README.md)[2020.06][pingCAP/talent-plan](https://github.com/pingcap/talent-plan)[2020.05] Rust 网络编程[Writing an OS in Rust](https://os.phil-opp.com/)[部分中文版](https://os.phil-opp.com/zh-CN/)[2020.05][PNGme: An Intermediate Rust Project](https://picklenerd.github.io/pngme_book/)[2019.06][Implementing TCP](https://www.youtube.com/playlist?list=PLqbS7AVVErFivDY3iKAQk3_VAm8SXwt1X)[2019.05]- 强烈推荐！Jon Gjengset 通过 Linux TUN/TAP 来实现 TCP 协议。三个视频加起来共 16 小时。
- 这个 up 主视频风格独特，内容有深度，录像不剪辑，每集时间巨长，好处就是可以了解一个完整项目的开发过程和解决问题的思路。

[Learning Parser Combinators With Rust](https://bodil.lol/parser-combinators/)[2019.04][Build Your Own Shell using Rust](https://www.joshmcguigan.com/blog/build-your-own-shell-rust/)[2018.11][So You Want to Build a Language VM](https://blog.subnetzero.io/post/building-language-vm-part-00/)[2018.07]

## 游戏开发相关

[有哪些值得推荐的Rust游戏引擎或图形渲染库？](https://www.zhihu.com/question/511998329/answer/2314160111)[Rust GameDev WG](https://gamedev.rs/)[Vulkan Tutorial(Rust)](https://kylemayes.github.io/vulkanalia/introduction.html)- 这老哥给自己的 Vulkan Rust 绑定
[vulkanalia](https://github.com/KyleMayes/vulkanalia)参考[Vulkan Tutorial](https://vulkan-tutorial.com/)写的教程。 - 我们也可以用
[ash](https://github.com/ash-rs/ash)来参考着写，两个 Vulkan binding crate 语法很像。

- 这老哥给自己的 Vulkan Rust 绑定
[The Ray Tracer Challenge](https://github.com/jakobwesthoff/the_ray_tracer_challenge_in_rust)[2022.02 updating]- 这老哥用 Rust 从零写一个 Raytracer，并把 live coding 的过程也录制上传在
[系列视频链接](https://www.youtube.com/playlist?list=PLy68GuC77sUTyOUvDhVboQoOlHoa4XrSO)

- 这老哥用 Rust 从零写一个 Raytracer，并把 live coding 的过程也录制上传在
[Vulkan with Rust by example](https://nikitablack.github.io/post/vulkan_with_rust_by_example_0_introduction/)- 又是用 Rust 和
[ash](https://github.com/ash-rs/ash)crate 来写 Vulkan 的一系列博文。

- 又是用 Rust 和
[Ashen Aetna](https://hoj-senna.github.io/ashen-aetna/)[2022.01 updating][Unofficial Bevy Cheat Book](https://bevy-cheatbook.github.io/)- Rust 游戏引擎 Bevy 的书。
- 中文版：
[Bevy 游戏引擎开发指南](https://yiviv.com/bevy-cheatbook/introduction.html)

[Learn Wgpu](https://sotrh.github.io/learn-wgpu/)[中文版](https://jinleili.github.io/learn-wgpu-zh/)[Wgpu](https://github.com/gfx-rs/wgpu)是[WebGPU API](https://gpuweb.github.io/gpuweb/)规范的一个 Rust 实现。- WebGPU 是由 GPU for the Web Community Group 发布的一个规范。它的目的是允许网络代码以安全和可靠的方式访问 GPU 功能。
- 它通过模仿 Vulkan API，并将其转换为主机硬件使用的任何 API（DirectX、Metal、Vulkan）来实现。
- 很多 Rust 游戏引擎都基于这一层图形 HAL。

[Tutorial: Writing a Tiny Rust Game Engine for Web](https://ianjk.com/game-engine-in-rust/)[2022.01][Roguelike Tutorial in Rust + tcod](https://tomassedovic.github.io/roguelike-tutorial/)[2020.04][Adventures in Rust: A Basic 2D Game](https://a5huynh.github.io/posts/2018/adventures-in-rust/)[2018.02]

## 其他领域相关

[The CLI Book](https://rust-cli.github.io/book/index.html)[The WebAssembly Book](https://rustwasm.github.io/docs/book/)[The Embedded Book](https://doc.rust-lang.org/stable/embedded-book/)[An Experimental Course on Operating Systems](https://cs140e.sergio.bz/)[Zero to Production in Rust (Building Backend Services)](https://www.lpalmieri.com/posts/2020-05-24-zero-to-production-0-foreword/)

## Rust 动态

[This week in Rust Newsletter](https://this-week-in-rust.org/)- 每周更新一次，把最新的 Rust 资源推到你的邮箱，这是跟踪 Rust 最新技术与事件的好方法。

- Discord
- Telegram
- 飞书
[The Rust Sub Reddit](https://www.reddit.com/r/rust/)[Rust语言开源杂志（2021）月刊](https://rustmagazine.github.io/rust_magazine_2021/index.html)[Rust语言开源杂志（2022）季刊](https://rustmagazine.github.io/rust_magazine_2022/index.html)

## 各种汇总（Awesome 系列）

[Awesome Rust [A curated list of Rust code and resources]](https://github.com/rust-unofficial/awesome-rust)- 针对 Rust 语言的 awesome lists，这里面汇集了各种各样的 Rust 库和资源，去参与或学习开源项目是当你入门后最好的进阶方法。

[rust-learning](https://github.com/ctjhoa/rust-learning)- 一个由社区维护的关于学习 Rust 的资源的汇总。

[EthanYuan/Rust-Study-Resource](https://github.com/EthanYuan/Rust-Study-Resource)- 又是一个关于学习 Rust 的资源的汇总。

[The Little Book of Rust Books](https://lborb.github.io/book/title-page.html)- Rust 相关书籍的汇总。

[sger/RustBooks](https://github.com/sger/RustBooks)- Rust 相关书籍的汇总。

[sunface/fancy-rust](https://github.com/sunface/fancy-rust)- Rust酷库推荐。使用我们精心挑选的开源代码，让你的Rust项目Fancy起来!

[EvanLi/Github-Ranking](https://github.com/EvanLi/Github-Ranking/blob/master/Top100/Rust.md)- Github 中 Rust 库星星排名的 Top 100，每日刷新。

[35 Rust Learning Resources Every Beginner Should Know in 2022](https://apollolabsblog.hashnode.dev/35-rust-learning-resources-every-beginner-should-know-in-2022)- 一篇推荐新手资源的文章


## Podcast

[Rustacean Station Podcast](https://rustacean-station.org/)[RustTalk](https://rusttalk.github.io/podcast/000/)- 主播：写代码的西瓜
[Rust 语言中文社区](https://rustcc.cn/)是一个相比干货分享的地方，偏文字，RustTalk 更侧重“湿货”，不仅仅会介绍到 Rust 的设计理念，更多的回去挖掘 Rust 背后的奇人轶事。


## 博客

[https://llever.com/](https://llever.com/)- 包含很多 Rust 周报及相关博文的翻译，不过现在好像不更新了。

[芽之家](https://blog.budshome.com/)- 同样是包含很多 Rust 周报及相关博文的翻译，同样好像不更新了😓


## 博客 RSS

## 作为参考的学习路线

### 各种方法入门

### 路线1

作者在文中提供了两种学习路线。

### 路线2

-
通读

[Rust by Example](http://rustbyexample.com/)，把其中的例子都自己运行一遍，特别是对其中指出的错误用法也调试一遍。 -
通读

[The Rust Programming Language](http://rust-lang.github.io/book/)，在进行了第一步后，已经基本对 Rust 的常用概念有所了解了，这个时候再读这本官方教程，进一步理解某些细节。 -
行了，到这一步后你就可以尝试做一个项目了，然后在做项目的过程中你一定会需要各种各样的库，请到

[Crates](https://crates.io/)上搜索，寻找适合你需求的 crate，了解它们的用法，必要时查阅它们的源码。一开始写实际代码时，你肯定会很痛苦，Rust 编译器一定会不断地折磨你，这个时候不要放弃，返回去再看[Rust by Example](http://rustbyexample.com/)和[The Rust Programming Language](http://rust-lang.github.io/book/)，然后终有通过编译的那一刻，恭喜你，入坑了！

## 常用站点

[Crates](https://crates.io/)- Rust 类库

[Docs.rs](https://docs.rs/)- Rust 类库文档

[Are we game yet](http://arewegameyet.com/)- 关于游戏开发

[Are we web yet](http://www.arewewebyet.org/)- 关于 Web 开发

[Are we (I)DE yet](https://areweideyet.com/)- 关于 IDE

[rust-library-i18n](https://github.com/wtklbm/rust-library-i18n)- Rust 中文文档，可以在 IDE 中使用


## 其他资料

[The 10 books that helped me, as a hobbyist, on my journey to learn Rust to re-code a Django application](https://www.reddit.com/r/rust/comments/s3z7ek/the_10_books_that_helped_me_as_a_hobbyist_on_my/)[Rustnote](https://www.rustnote.com/)- 某个网友的个人笔记