---
tags: [game-engines, playcanvas, webgl, webgpu, semver, refactoring]
date: 2026-04-19
sources: 1
---

# PlayCanvas Engine 2.0：一次 major bump 的工程学

2024 年 8 月，[[will-eastcott|Will Eastcott]] 宣布 PlayCanvas Engine 跨到 **2.0.0**。距离 1.0.0 已经 6 年，中间跨了 73 个 minor 版本。对一款以"稳定优先、几乎不引入 breaking change"著称的商业 web 引擎来说，这次 major 版本号的用途只有一个——**给团队开一次"合法破坏"的窗口**，把长期 deprecated 的代码一次清掉。

## 为什么要大扫除

Eastcott 用了一个特意标注词典释义的词：**cruft**——"设计糟糕、过度复杂或无用的代码或软件"。引擎在 1.x 后期已经到了"cruft 多到拦住下一代 API 落地"的状态——具体是什么下一代 API？是 [[webgpu-intro|WebGPU]]。要给 WebGPU 搭新的资源绑定路径、新的渲染后端抽象、新的 shader 编译管线，老代码里那些为 WebGL 1 准备的兼容层、为 Scripts 1.0 准备的脚本执行器、废弃已久的 AudioSourceComponent，都在占用接口预算、牵制测试矩阵。一次性砍掉是最省力的解法。

被砍掉的三样东西各有决策依据：

- **WebGL 1**：终端用户占比已不足 2%，且单调下降。支持 WebGL 1 是 [[playcanvas-webgpu-editor|WebGPU 后端]]重写的最大负担，砍掉它才有精力去做新后端的 MRT、compute、timeline semaphore 这些。
- **Scripts 1.0**：2016 年 Scripts 2.0 上线即已 deprecated，8 年后还没砍只是因为没人敢在 minor 版里动。2.0 给了合法机会，顺便为即将到来的 **ESM-based 脚本系统**腾位置。
- **AudioSourceComponent**：`SoundComponent` 上位多年，留着是给历史项目兜底的。

## Semver 的真实价值

Semver 规则表面上讲的是"major = breaking / minor = feature / patch = fix"，本质上给的是一种**社会合同**：用户可以根据版本号判断升级风险。对引擎团队来说，这意味着 major bump 不是随便什么时候都能做——它必须是**积累够了需要清扫的旧债**之后才做一次；频繁的 major bump 会破坏用户对稳定性的信任。

PlayCanvas 的节奏很保守：1.0.0（2018）→ 2.0.0（2024），6 年一次。对比之下，Eastcott 自己也承认 1.0.0 本该更早——引擎从 2010 年就有了、2014 年开源，早就是稳定生产代码，只是团队一直没到"觉得值得 1.0"的时刻。这是很有普遍性的行业观察：**很多项目的版本号长期低于它的实际成熟度**，因为团队在"等一个完美时刻"而那个时刻永远不会来。

## 迁移策略

breaking change 发布出去，用户凭什么放心升级？PlayCanvas 给的答案是**分轨道迁移**：

1. **Engine-only 用户（npm）** 可以立即试；大多数项目无需改动。
2. **Editor 用户**在后续几周 opt-in 升级，旧项目保持 1.x；**Engine 1.x 在 Editor 里继续维护至少一年**。
3. **新项目**默认走 2.0。

这是"商业 web 引擎 major 升级"的教科书模板：用 npm 社区做尖锐测试，用 Editor 托管项目做慢迁移，用新项目默认值推动主流切换。这条路径里藏着一个核心前提——**Editor 形态的引擎有义务维持比 npm 长得多的兼容窗口**，因为托管项目的开发者不像 npm 用户那样随时能"自己选版本"。

## 新能力同步登场

2.0 不只是减法，也有加法——一批新示例标记出后续能力发力方向：

- **Custom shaders**（cross-hatching、Gooch 非真实感）——自定义 shader 管线的成熟度。
- **SSAO**——屏幕空间环境光遮蔽作为引擎内置后处理。
- **Hardware instancing**，包括 `EXT_mesh_gpu_instancing` glTF 扩展——draw call 预算下的大场景支持。

这些 example 的选择不是偶然——都是 draw call 密集或 compute 型工作负载，正是 [[webgpu-intro|WebGPU]] 相对 WebGL 能带来显著收益的场景。Engine 2.0 的存在，就是为了接下来能把这些能力推得更深。

## 启示

这次 major bump 揭示了**长期健康代码库的节律**：在稳定产品周期里按兵不动；在下一代 API 真正到来、旧代码开始拦路时，不要试图"绕过去"，而是接受一次 major bump 的社会成本，果断清扫，然后把腾出来的接口预算留给未来 6 年。

## 相关

- [[playcanvas-webgpu-editor]]
- [[webgpu-intro]]
- [[will-eastcott]]
- [[engine-evolution]]
- [[dependencies]]

## Sources

- [[sources/playcanvas-engine-2-release]]
