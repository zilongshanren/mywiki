---
title: 云风的 BLOG
url: https://blog.codingnow.com/2022/03/
published: '2022-03-29'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

我们的游戏引擎一开始是[自己实现的粒子系统](https://blog.codingnow.com/2020/11/ecs_particle_system.html) 。在实现完之后，做配套编辑工具的阶段，开发工具的同学建议换成其它开源的成熟系统，这样就不必花太多精力在维护一套工具了。

他推荐了 [Effekseer](https://effekseer.github.io/) ，并完成了 Effekseer 和我们引擎的整合工作。

最近，我在推特上看到有个同学也在寻找 bgfx 下的粒子系统的方案，他希望有一个比 bgfx 自带粒子演示更完善的东西，同时又表示整合 [popcorn](https://www.popcornfx.com/) 实在是过于麻烦。我向他推荐了 effekseer 。

集成 effekseer 其实有两个层面的工作。一是对接图形 API ，而是和引擎集成。后者包括和引擎的资源管理集成。bgfx 只是图形 API 的抽象层，可以看成是和 opengl directx metal 这些同级的 api 。光给 effekseer 写一个 bgfx api 的渲染器是不够的，粒子系统还包括了贴图、着色器、模块的加载和管理。如果只在图形 api 级别对接的话，就会让这些资源的加载和生命期管理同时存在游戏引擎和粒子系统两处各一份。这显然是不合理的。

我们在去年做整合的时候，活做的比较粗糙，把两者混在一起了。所以并不好直接拿给另一个基于 bgfx 渲染的项目用。我看了一下推特上那哥们的简历，他曾经是 Crytek 的 Principal R&D Programmer ，做过很多年的 AAA 游戏，相比能力不错，便劝他为自己的项目做 effekseer 的整合工作。他表示既然有人做过，就不要浪费精力了，愿意花钱买我们的代码参考。

我想了想，决定重新设计一下抽象层，把和 bgfx 相关的部分从我们的引擎中剥离出来，单独写一个 effekseer 的 bgfx renderer ，然后开源。和那哥们聊了一下，他也很愿意以后共同维护。想着这样可以白赚一个朋友一起维护一个子模块也不错，多一个项目用也更靠谱些。从上周开始，我就加班开干了。

项目在这里：[https://github.com/cloudwu/efkbgfx](https://github.com/cloudwu/efkbgfx/)

目前还在做，这一周下来有太多想吐槽的东西，以后慢慢写。今天先写一下这其中关于 shader 转译的工作。

effekseer 有 6 种内置的材质，可分别用于渲染粒子片（四边形 sprite）或是模型。sprite 和 model 渲染用的 vs 是不同的，但 fs 是共用的，所以一共有 18 个 shader 。

bgfx 用的 shader 有一些自定义的书写格式，不能直接把 effekseer 中的 shader 文件直接拿过来用。去年我们同事做的时候，就根据它里面 opengl 的版本手工转译了几个 shader （并未完全直接全部 6 种内置材质）。这个工作并不难做，花半天时间就能搞定。但去年的 effekseer 版本和目前的最新版本已有差异，去年的工作还需要更新。

我研究了一下 effekseer 的项目，发现它实现了从 DirectX9 到 12 ，OpenGL 2 到 3 ES ，还有 Vulkan Metal 等等很多图形 API 的版本，其实这些不同版本的 shader 都是从 DirectX11 的版本生成出来的。只有 DirectX11 那一版是人工维护。生成工具以 [glslang](https://github.com/KhronosGroup/glslang) 为基础做的一个专有工具。

理想情况下，我们应该扩展这个工具，让它可以自动生成 bgfx 的 shader 版本。但我评估了一下，这个工作量并不算小。关键是，这个工具并没有留下太好的扩展方法。等于我们需要 fork 其代码再改。那些日后这个 fork 版本的工具同样也有跟进上游的维护成本。还会增加我们项目的构建复杂度。

怎么才能低成本的做成这事呢？

我打算绕开 effekseer 的 shader 转换工具，自己用 lua 写一个。由于 bgfx 的 shader 是基于 glsl 语法的，所以，从它机器生成的 Vulkan 版本转换最为容易。由于，原始版本就是机器生成的，所以格式非常规整。我在实现转译器的时候，甚至没有动用 lpeg ，就用 lua 内置的字符串库就搞定了。前后只花了 4 个小时，[100 来行的 lua 程序](https://github.com/cloudwu/efkbgfx/blob/master/efkmatc/genbgfxshader.lua)。

为什么写这么一个简易的专有工具就够用了？因为，我们需要转换的只有十几个 shader 文件，并不需要做成通用工具。而且，并不需要没有构建项目的时候都去转换，而只需要在上游代码更新的时候转换，直接把转换结果放在仓库里即可。专有工具不需要考虑太多情况，能把目前的文件处理对就够了。但可以留下足够的检查，一旦发现日后的更新有无法理解的段落，就尽可能的报错，而不是尝试转换。

当未来版本升级时，转换工作是自动化进行，但是人工监督的。一旦发现工具不适用了，改善工具配合更新的工作量并不大。而且专有工具可以配合已经写好的 renderer 代码做更多的细节：比如校验 Uniform 的名字、Vertex Layout 是否和 renderer 代码是否保持一致。而不需要真的去生成 renderer 中的 C++ 代码。这样也简化了 renderer 的实现。