---
title: 用 Rust 实现简单的光线追踪
url: http://frankorz.com/2021/05/05/rust-raytrace/
author: 文章作者 猫冬
published: '2021-05-05'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

学 Rust 十来天了，自己被这个语言惊艳到，就跟着教程 [Ray Tracing in One Weekend](https://raytracing.github.io/books/RayTracingInOneWeekend.html) 写了个很简陋的光线追踪示例练习，项目在 [Latias94/rust_raytracing](https://github.com/Latias94/rust_raytracing)。

学这门语言的时候，感觉就是上手容易遇到很多新概念，容易学不下去，跟编译器作斗争…不过作为一个还很新的系统编程语言，工具链如文章、包管理、格式化、编译器等很完善，官方教程很棒，社区也很活跃。

学 Rust 的契机其实是在 V2EX 上看到有人在纠结学 Go 还是 Rust，底下的帖子也有不少夸 Rust 语言的，因此自己也开始关注 Rust 语言。后来发现 Rust 的用武之地非常广，Github 上还能找到不少 Rust 做的游戏引擎，其中一部分主打 ECS 功能，例如：[bevyengine/bevy](https://github.com/bevyengine/bevy) 、[Ralith/hecs](https://github.com/Ralith/hecs) 等。

学习 Rust 语言，其实也是在了解一个现代化的语言该有的样子，了解 C++ 或其他语言部分设计上的不足，以及 Rust 是打算如何从根源解决这些问题的。这部分我作为一个初学者，不打算展开讲。大家有空可以了解一下 Rust 语言，看看官方的教程[《Rust 程序设计语言》](https://kaisery.github.io/trpl-zh-cn/title-page.html)。

总而言之，我觉得光线追踪的教程可以作为学一门新语言后**严肃学习**的项目，做完成就感也满满！

顺便推荐一篇好文：[新技术学习不完全指北：以 Rust 为例](https://juejin.cn/post/6898953413250252814)。

最后放下示例的渲染图：

![1200*800 渲染图](../../assets/ff61b09524fdbb9d.png)


五一劳动节快乐！