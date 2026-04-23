---
tags: [人物, 作者, 图形, 游戏引擎]
date: 2026-04-19
sources: 10
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
