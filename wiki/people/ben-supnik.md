---
tags: [人物, 作者, 图形, 游戏引擎]
date: 2026-04-19
sources: 33
---

# Ben Supnik

Benjamin Supnik，Laminar Research 的核心图形/引擎程序员，在模拟飞行产品 **X-Plane** 上持续工作约二十年。他的个人博客 *The Hacks of Life*（`hacksoflife.blogspot.com`）主题覆盖 OpenGL → Vulkan 迁移、GPU 驱动的渲染管线、C++ 新语法在实际引擎里的落地（C++20 coroutines / concepts），以及工程组织层面的设计原则。

文风特点是把硬核工程问题讲成短小随笔：标题常见半开玩笑（*This One Weird Trick…*、*We Never Needed Stackfull Coroutines*），内容却是真实生产代码里踩过的坑——例如如何在 X-Plane 里引入 C++20 coroutine 做 async I/O，而不付出 Fiber 保存完整 stack 的代价；又如他对 YAGNI 与「泛化陷阱」的多篇反思，全部源自 X-Plane 的特征排期。

他在工程观上是坚定的「解决更小的问题」派：反对虚假泛化、反对未经验证的 future-proofing，主张用领域特殊性换性能和清晰度。参见 [[cheat-by-solving-less]] 与 [[future-proofing-tests]]。

## 相关
- [[stackless-vs-stackful-coroutines]]
- [[coroutine-awaitable-pattern]]
- [[future-proofing-tests]]
- [[cheat-by-solving-less]]
- [[srgb-premultiplied-alpha-compression]]
- [[incremental-rearchitecting]]
- [[header-as-user-manual]]
- [[api-fast-path-design]]
- [[number-puzzle-tile-shader]]
- [[opengl-builtin-attribute-aliasing]]
- [[cpp-template-value-vs-type-parameter]]
- [[triangle-strips-vs-indexed-triangles]]
- [[stl-not-abstraction-prescription]]
- [[huge-world-coordinate-precision]]
- [[function-vs-data-pointer-portability]]
- [[texture2dgrad-explicit-derivatives]]
- [[uv-precision-derivative-loss]]
- [[alpha-blending-front-to-back]]
- [[vbo-double-buffering-orphaning]]
- [[agp-vs-vram-streaming]]
- [[glbuffersubdata-serialization]]
- [[opengl-extension-bucket-strategy]]
- [[gpu-embarrassingly-parallel-serial-dispatch]]
- [[cgal-exact-arithmetic-mantissa-growth]]
- [[cgal-arrangement-import-antennas]]
- [[message-queue-thread-ownership]]
- [[shared-library-soname-versioning]]
- [[floating-point-geometric-predicates]]
- [[premultiplied-alpha-bilinear-ring]]
- [[gpu-sliced-volumetric-shadows-limits]]
- [[cross-platform-openal-runtime-loader]]
- [[c-bitwise-operator-precedence-history]]
- [[linear-lighting-pipeline]] —— Gamma and Lighting 三部曲里关于光照累积三种路径的总结
- [[matrix-as-basis-vectors]] —— 2010 双篇 change-of-basis / basis-projection 合编
- [[optimization-leverage-ratio]] —— 「1% 算多吗」的 profile 判断框架
- [[semaphore-vs-condvar-latency]] —— X-Plane 10 worker 唤醒延迟优化
- [[xplane-gbuffer-format]] —— X-Plane 10 第一版延迟管线的 G-Buffer 布局（shadow/shine 浮点打包）
- [[encapsulation-over-polymorphism]] —— 90/10/0 OOP 三要素权重启发式
- [[glsl-compiler-optimization-reliance]] —— 2010 ShaderAnalyzer 观察驱动对 X-Plane 10 shader 组织的反向影响
- [[cas-refcount-lowbit-lock]] —— CAS+refcount 的低位自旋锁变体与 differential refcount 讨论
- [[compact-normal-encoding]] —— 2011 G-Buffer 法线用 Lambert azimuthal 2 通道编码解条带
- [[asset-exchange-format-strategy]] —— COLLADA 抉择：三条资源交换路线的权衡

## Sources
- [[sources/supnik-stackless-vs-stackful-coroutines]]
- [[sources/supnik-coroutine-as-awaitable]]
- [[sources/supnik-future-proof]]
- [[sources/supnik-beat-the-experts]]
- [[sources/supnik-srgb-premultiplied-alpha]]
- [[sources/supnik-when-to-rewrite]]
- [[sources/supnik-coding-for-two-audiences]]
- [[sources/supnik-fast-paths]]
- [[sources/supnik-tile-too-far]]
- [[sources/supnik-debugging-glsl]]
- [[sources/supnik-ive-got-the-blues]]
- [[sources/supnik-templating-functions]]
- [[sources/supnik-devil-in-details]]
- [[sources/supnik-to-strip-or-not-to-strip]]
- [[sources/supnik-stl-not-abstraction]]
- [[sources/supnik-scroll-opengl-world]]
- [[sources/supnik-glxgetprocaddressarb-syntax]]
- [[sources/supnik-change-uv-map-on-fly]]
- [[sources/supnik-running-out-of-derivative-res]]
- [[sources/supnik-alpha-front-to-back]]
- [[sources/supnik-double-buffering-vbos]]
- [[sources/supnik-agp-vs-vram]]
- [[sources/supnik-glbuffersubdata]]
- [[sources/supnik-value-of-granularity]]
- [[sources/supnik-santa-youre-an-idiot]]
- [[sources/supnik-cgal-mantissa]]
- [[sources/supnik-cgal-arrangements-import]]
- [[sources/supnik-fear-of-threading]]
- [[sources/supnik-vbo-really-double-buffered]]
- [[sources/supnik-race-condition-debug]]
- [[sources/supnik-openal-linux-part-27]]
- [[sources/supnik-when-good-floating-point-goes-bad]]
- [[sources/supnik-premultiplication-pros-cons]]
- [[sources/supnik-alpha-blending-lets-try-again]]
- [[sources/supnik-gpu-sliced-shadows-fail-clouds]]
- [[sources/supnik-openal-three-platforms]]
- [[sources/supnik-finding-mom-and-dad]]
- [[sources/supnik-c-seventies-technology]]
- [[sources/supnik-gamma-lighting-trilogy]]
- [[sources/supnik-more-stl-abstraction]]
- [[sources/supnik-change-of-basis-revisited]]
- [[sources/supnik-basis-projection]]
- [[sources/supnik-is-1-a-lot]]
- [[sources/supnik-semaphore-vs-condvar]]
- [[sources/supnik-semaphore-nptl]]
- [[sources/supnik-gbuffer-format]]
- [[sources/supnik-fmtt-glsl-edition]]
- [[sources/supnik-what-oop-isnt]]
- [[sources/supnik-glsl-compiler-observations]]
- [[sources/supnik-cas-reference-counting]]
- [[sources/supnik-derivatives-two-parts]]
- [[sources/supnik-derivatives-iii-ran-out-of-rez]]
- [[sources/supnik-is-collada-a-win]]
- [[sources/supnik-gbuffer-normals-revisited]]
