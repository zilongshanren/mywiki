---
tags: [game-engines, shader, slang, nvidia, language]
date: 2026-04-19
sources: 1
---

# Slang 着色器语言

**Slang** 是 NVIDIA 发起、现已集成进 Vulkan SDK 的新一代着色器语言。和 HLSL/GLSL 相比，它最大的卖点是把**C++ 级别的抽象能力**带到 shader：泛型、模块、命名空间、成员函数、接口（`interface`）、组合式的伪多态（把 raycaster、tracer、illuminator 用模板参数组装成一个 `PathTracingRendererV2`）。gameknife 说自己一年前不敢相信那段 `namespace Bindless { ... }` 是 shader 代码，现在每天写的就是这个——"与其说是 shader，其实更像一个渲染器"。

技术特性：

- **跨平台编译**：能输出 SPIR-V、DXIL、Metal、WebGPU WGSL，一份源码全平台覆盖——这是 HLSL 在 Vulkan 侧靠 DXC 做的事，Slang 把它做得更完整。
- **自动微分**：内建 automatic differentiation，可微 shader 本身就能参与前向训练——给"渲染特征预训练"这类 ML × graphics 场景提供了一条不用额外 Python/PyTorch 管线的路径。
- **性能不降反升**：gameknife 把一整套 GLSL codebase 改写成 Slang 后，性能反而提高了一些——可能与 Slang 编译器在抽象展开后做了更激进的特化有关。

从引擎架构的角度看，Slang 直接改变了 shader codebase 的组织方式。传统 GLSL 的 `#include` 地狱（文件顺序敏感、宏污染、函数名冲突）被正式的模块系统替代；以前只能靠宏和预编译变体表达的"泛型"，现在是一等的 `<T>`。这对 [[zero-bind-gpu-resource-management|零 bind]] 这种高度自由的管线尤其重要——资源访问和算法组合都从"硬编码 descriptor 布局"升级为"库里的一个抽象层"。

## Sources

- [[sources/gameknife-modern-rendering-how-modern]]
- [[sources/alain-shader-languages-review]]
