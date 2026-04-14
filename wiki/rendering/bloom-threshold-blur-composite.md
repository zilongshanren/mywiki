---
tags: [rendering, shader, post-processing, bloom, hdr, unity]
date: 2026-04-14
sources: 1
---

# 简易 Bloom：阈值 + 模糊 + 合成

**Bloom**（辉光）的物理动机是镜头在强光源周围会溢出一圈光晕——相机/眼睛的光学系统把高亮度能量扩散到邻域。实时渲染里最朴素的复刻方法只有三步：**提取亮部 → 模糊 → 和原图相加**。这三步构成一个"pass 链"，每一步都是一个全屏 [[unity-image-effect-basics|image effect]] pass，中间要用临时 `RenderTexture` 串起来。这种实现不涉及 HDR 管线，也不关心真实物理，只是一个"看起来像 bloom"的后处理合成。

## 三步拆解

**Step 1 — Threshold pass**：读原图，把亮度（`rgb2hsv` 的 value 分量，或者一个简单的 `max(r,g,b)`）和一个 `_Threshold` 参数比较。超过阈值的像素保留原色，其余像素写黑。这样就得到一张只有"光源"亮着的稀疏亮度图。shader 里用三目运算符 `(bright > thr) ? col : 0` 代替 `if`，避免分支分化。

**Step 2 — Blur pass**：对阈值图做一次高斯模糊。Ilett 在教程里用的技巧是 **UsePass**——直接复用之前 [[separable-gaussian-blur|可分离高斯 shader]] 里写过的那个 pass，不重新写模糊逻辑。语法是在当前 shader 里写 `UsePass "Path/To/Shader/PASSNAME"`（名字必须大写，因为 Unity 内部会把 pass 名 uppercase）。被引用的 pass 需要事先用 `Name "xxx"` 命名，且当前 shader 要**重新声明**它所用的 Properties 和 CGINCLUDE，不会自动继承。

**Step 3 — Composite pass**：把原图和模糊后的亮度图按分量相加（或 `lerp`）写回。注意这一步有两张输入纹理——一张是上一步的 blur 结果（走 `_MainTex`，`Graphics.Blit` 默认喂），另一张是最初的源图，需要额外声明一个 `sampler2D _SrcTex` 并用 `material.SetTexture("_SrcTex", src)` 显式绑进去。

## 在 C# 端编排

对应的 `ImageEffectBloom.cs` 要做的事：开两块临时 RT（一块 threshold、一块 blur），按 pass index 依次 `Graphics.Blit(src, tmp, mat, passId)`，每一步都记得 `RenderTexture.ReleaseTemporary`。Ilett 把"单 pass 高斯还是可分离多 pass"做成 `enum BlurMode` + `[SerializeField]` 开关，让同一个 script 能切换两种模糊策略。

这种"C# 脚本做编排、shader 做算法"的分工是 Unity built-in 管线 image effect 的典型写法——URP 的等价物是 `ScriptableRendererFeature` + 多个 `ScriptableRenderPass`，把同样的 pass 链放进 render graph。

## 为什么不够"真"bloom

真实的 HDR bloom 会在**线性 HDR 空间**做阈值（高于 1.0 的亮度才叫光源）、用**多级 mipmap 金字塔**（Dual Kawase 或 Unity post-processing v2 的 13-tap 双线）做跨尺度能量扩散，最后 tonemap 回 LDR。而这个"简易 bloom"：

- 在 LDR `[0,1]` 空间阈值化，本质是"把偏亮的颜色模糊一下"；
- 只用单级全分辨率高斯，半径有限，大范围光晕很难做出来；
- 不搭配 [[local-tonemapping|tonemapping]]，相加后很容易过曝。

它的价值不在保真度，而在**完整展示了 image effect 的 pass 编排机制**：临时 RT、UsePass、多纹理绑定、pass index 管理。把这套流程理顺了，再去看 `catlikecoding` 的完整 HDR bloom 或 URP 的 `UberPost` 只是把每一步替换成更讲究的版本而已。

## 相关

- [[unity-image-effect-basics]]
- [[separable-gaussian-blur]]
- [[sobel-edge-detection]] —— 前一步的边缘提取可以作为 bloom 阈值的替代
- [[image-effect-colour-transform]]
- [[local-tonemapping]] —— 真正的 HDR bloom 需要配合 tonemap
- [[chromatic-aberration-post]]

## Sources

- [[sources/danielilett-image-effects-edge-detection-bloom]]
