---
tags: [rendering, 可微渲染, 自动微分, 优化, 机器学习, 光栅化]
date: 2026-04-27
sources: 1
---

# 可微渲染（Differentiable Rendering）

可微渲染是指将渲染管线设计为关于场景参数（几何、材质、光照等）**可微分**的函数，从而可以用梯度下降等数值优化方法，针对给定目标图像反向求解场景参数。[[angelo-pesce]] 以一种"非主流"（SDF 光线行进）路线实验了这一思想，并记录了实用经验与踩坑。

## 基本原理

若将渲染器视为从参数向量到图像的映射 `f(θ) → I`，则给定参考图像 `I_ref`，可以定义误差 `L = ||f(θ) - I_ref||²`，再通过自动微分（[[automatic-differentiation]]）计算 `∂L/∂θ`，用梯度下降迭代优化。

**间断性问题**是可微渲染的核心挑战。标准渲染器充满不连续性：三角形边缘处覆盖关系突变，深度测试产生硬性遮挡切换。主流解法是在边缘处引入"软化"——让每像素保存多个片元候选，再加权混合。典型实现有 nvdiffrast 和 PyTorch3D。

## SDF 光线行进路线

Pesce 采用了一条"天然软"的替代路径——**SDF sphere tracing**：由于 SDF raymarcher 在接近表面边缘时自然减速（步长变小），其深度缓冲本身就是连续的，无需额外软化即可求导。具体做法：

1. 在 ShaderToy 中实现 SDF raymarcher，去除大多数分支，保持固定迭代步数（等价于展开，不含 control flow 间断）；
2. 把需要优化的场景参数（球的位置、半径）提取为参数数组；
3. 用 LLM 将 GLSL 翻译成 Python/JAX；
4. 接入 JAX 的自动微分，定义深度误差函数，梯度下降收敛。

这一方案的优势：不需要存储多片元，内存占用低；天然支持从任意视角稀疏采样；缺点是仅能处理几何形状（深度），不支持着色，且"软化效应"导致优化出的基元比真实尺寸偏小。

## JAX vs PyTorch

JAX 总是编译到原生代码（经 LLVM IR），对长而复杂的程序（如 raymarcher）性能远优于 PyTorch（后者持续解释中间层）。主要注意事项：

- JAX 不能用 Python `if` 对被追踪的数组做条件分支，需改用 `jnp.where`（条件移动语义）；
- Python `for` 循环会被展开进 JAX IR，循环过长会导致编译超时，改用 `jax.lax.scan` 或 `vmap`；
- 标准 NumPy 线性代数函数（如 `jnp.linalg.norm`）针对大矩阵优化，对 3D 图形的小向量会产生不必要的代码膨胀。

## 全局优化与层次分割

**梯度下降是局部优化器**，对含多个极小值的问题（如用有限数量的基元拟合复杂形状）必须辅以全局策略：

- **遗传编程（GP）交叉**：维护一个候选解种群，每代用少量梯度步骤快速优化各候选解，再用交叉算子生成下一代。符合"积木假说"（Building Block Hypothesis）——已收敛到好区域的基元是可重用模块。与纯 GP 相比，GP + 梯度的组合速度快得多。
- **层次分割（Hierarchical Splits）**：从 1 个基元开始，梯度下降只有一个全局极小值，收敛可靠；收敛后找误差最大的基元沿最长轴一分为二，逐步增加基元数量。结果质量远优于一次性用全部基元初始化。

这两个模式都对应 Gaussian Splatting 的实践（先用点云初始化再做梯度优化，以及自适应 densification / pruning）。

## 应用前景

Pesce 给出的潜在用例：

- **遮挡网格自动生成**：用可微渲染寻找能最大化遮挡的保守近似几何，比手工制作简单得多；
- **几何 LOD 联合优化**：与纹理联合优化，参见已有的 NVIDIA 外观驱动模型简化工作；
- **Shader 参数自动调优**：将 Shader 视为可微程序，对质量和性能指标做多目标优化（"Auto-Jorge"愿景）。

## 相关概念

- [[automatic-differentiation]] — JAX/PyTorch 背后的自动微分机制
- [[neural-graphics-primitives]] — NeRF/Gaussian Splatting 也属于可微体积渲染
- [[rasterization]] — 标准光栅化管线
- [[gaussian-splatting-web]] — 同样依赖可微渲染思路做优化

## Sources

- [[sources/c0de517e-differentiable-rasterize]]
