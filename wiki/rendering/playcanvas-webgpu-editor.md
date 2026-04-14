---
tags: [渲染, webgpu, playcanvas, 引擎, compute, 跨平台]
date: 2026-04-14
sources: 1
---

# PlayCanvas 的 WebGPU 适配与 Editor 集成

2024 年 4 月，PlayCanvas 宣布 **WebGPU 支持正式落地到 Editor**，标志着这款面向 web 的老牌 3D 引擎从"WebGL + WebGL2"时代正式进入 [[webgpu-intro|WebGPU]] 时代。对了解 PlayCanvas 这家公司的人这并不突然——他们 2017 年就和 Mozilla 合作推了 WebGL 2.0 的首发支持，踩着"web 图形新 API 就推首发"的节奏。这次 WebGPU 的切换一样是一场计划很久的基建升级。

## 为什么要切 WebGPU

PlayCanvas 给出的动机里，对普通用户最直接的承诺是**"肉眼看不出差别"**：团队为了确保既有 WebGL 项目切到 WebGPU 后渲染结果完全一致花了大量精力。这种保守的"兼容第一"策略是商业引擎和 research 项目的本质区别——用户场景里有几万行业务代码，不允许"切换 API 顺便变了个画风"。但承诺之后真正的动力在下一层：

- **降低驱动开销**：WebGPU 的显式 pipeline、bind group、command encoder 让 draw call 路径远短于 WebGL 时代的 state patching。对 draw call 密集型场景（UI 多、物体多、材质切换频繁）长期会显著提速。
- **compute shader 原生**：这是 WebGPU 相对 WebGL 最大的能力跃迁。Engine v1.70.0 落地了 compute shader 支持，官方演示跑了 **GPU 上 100 万粒子**的示例。这类工作量在 WebGL 时代要靠 [[gpgpu-json-parsing|fragment shader GPGPU]] 之类 workaround 去凑。
- **splat 处理重写**：v1.71.0 借助 compute 重写了 3DGS 的 GPU 处理路径，把 [[supersplat-pwa|SuperSplat]] 的 bike 场景 GPU 耗时从 32ms 压到 13.5ms——超过 2 倍的提升。这条线最终喂养了 [[gaussian-splatting-web]] 的整套工作流。

## Beta 门与开关

WebGPU 在 PlayCanvas 里仍是 **beta** 状态。团队提示**运行时 lightmapper** 等少量功能还没移植，因此默认关闭，用户需要主动到项目设置里把 `Graphics Devices` 勾上 `WebGPU (beta)`。这种"先开后不后兼容再默认"的推进方式和 Chrome 当年给 WebGPU 加 flag 的策略几乎一致：用真实生产流量去把剩下 20% 的兼容性 bug 暴露出来。

## 行业节奏

文章引用 Web3D Survey 的数据：**截至 2024 年 4 月，62.19% 的终端用户可以跑 WebGPU**——主要是 Chrome 113+ 的贡献。Firefox 和 Safari 的 WebGPU 落地则被排在"不久之后"。作者预期随着两大浏览器陆续支持，这个数字会在 2024 年之内显著上升。对引擎作者来说意味着什么？意味着**可以开始把 WebGPU 当成"生产目标"而非"实验路径"规划未来 12–24 个月的路线图**——新功能（compute heavy 的粒子、流体、splat）可以直接挑 WebGPU 独占，WebGL 只维持向下兼容。

## 启示

PlayCanvas 这次发布揭示的不是"新 API 来了"，而是**商业 web 引擎切换图形后端的工程路径**：

1. **视觉一致性优先**：不允许切后端顺便"升级"或"回归"画面。
2. **分阶段启用**：beta flag → 手动 opt-in → 默认启用。
3. **先解决老 workaround**：把 GLSL GPGPU 时代凑出来的技巧换成 compute shader 的"正统实现"，释放性能。
4. **借新能力推出新产品**：用 compute 改写 splat 管线，然后基于它做 SuperSplat 和 Editor 的 3DGS 集成——一次性把 API 升级变成业务差异化。

这种"基建升级 → 业务落地"的紧密连接是 PlayCanvas 的一贯风格。

## 相关

- [[webgpu-intro]] —— WebGPU/WGSL 的背景与设计原理
- [[gaussian-splatting-web]] —— WebGPU compute 的第一个消费级应用
- [[supersplat-pwa]]
- [[compute-vs-raster-points]]
- [[d3d12-resource-binding]]
- [[will-eastcott]]

## Sources

- [[sources/playcanvas-webgpu-editor]]
