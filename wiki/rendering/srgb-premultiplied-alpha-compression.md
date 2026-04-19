---
tags: [渲染, srgb, alpha, 纹理压缩, 颜色]
date: 2026-04-19
sources: 1
---

# sRGB、预乘 Alpha 与压缩纹理的三方关系

美术工作流里有一个容易出错的三角：**[[gamma-correction-srgb|sRGB 色彩空间]]**、**[[alpha-compositing|预乘 alpha]]** 和**纹理压缩**（BC / ASTC 等）。任意两者配合都容易出问题，三者同时出现时更是灾区。Ben Supnik 的笔记把它们之间的数学讲清楚，给出在 shader / 资产管线里的正确顺序。

## 预先澄清术语

- **sRGB encoded**：纹理的 RGB 以 sRGB 曲线存储；好处是 8 bit 的精度预算"花在暗部"——人眼在暗部最敏感，linearly 分布 8 bit 会在暗部出现肉眼可见的色带。
- **Linear 纹理**：RGB 直接是线性光，通常 >= 16 bit（HDR 或高精度工作空间）。
- **Alpha 永远是线性的**：无论纹理标不标 sRGB flag，alpha 通道按线性解读。50% 透明就是 0x7F (或 0x80，看 IHV)。
- **Linear blending（gamma-correct）**：shader 先把 sRGB texel `decode` 成 linear，计算/混合在 linear 域完成，最后 `encode` 回 sRGB 输出。现代 HDR 管线必须如此。
- **sRGB blending**：保留 8-bit sRGB 不 decode，直接在 sRGB 值上做 `a + (1-a)*b`。数学上错误——红加绿会出现闷闷的土黄色——但**有时候美术真的想要**：(1) "Photoshop 默认就这样"；(2) 模拟 **partial coverage**（锈迹漆料："这个像素 50% 有漆 50% 没漆"），在感知空间里混合让覆盖率感觉"对"。

## 预乘 Alpha 的两个收益

- **节省乘法**：从 `C = A*src + (1-A)*dst` 缩减为 `C = src' + (1-A)*dst`（`src'` 已经是 `A * src`）。上世纪 NeXT 在 CPU 上做实时合成时，这半数 multiply 的节省是关键；今天 GPU 上算力不是问题，但公式的简洁仍有价值。
- **滤波与 mipmap 不产生边缘 bug**：预乘纹理里 alpha=0 的像素，RGB 也已乘成 0，和邻居 bilinear 混出来"更透明的正确颜色"。非预乘纹理则必须在工具链里给 alpha=0 的像素**"填色"**（把周围可见色摊进去），否则降分辨率时 alpha 边缘会出现原本不该存在的色带。

这是 [[mipmap-generation-sampling|mipmap 预乘是默认]] 的根本原因。

## 预乘 × sRGB：正确的运算顺序

Supnik 明确的步骤：

1. **decode 到 linear**（并用 > 8 bit 保存中间结果）。
2. **linear 颜色 × alpha**。
3. **re-encode 回 sRGB**。

换句话说：**预乘必须在 linear 空间里做**。如果你在 sRGB 8-bit 纹理里直接写 `RGB *= A`，你相当于在非线性曲线上做乘法——暗部会被过度压缩、边缘看起来偏灰。资产管线（Photoshop 导出、DCC 工具、texconv 等）默认做的就是错的；需要显式打开 "linear premultiply" 选项。

## 压缩纹理的陷阱

BC1/BC3/BC7、ASTC 这些[[bc7-solid-color-blocks|块压缩格式]]把一个 4×4 块压进少量比特。块压缩内部假设**输入值域是线性的**——它会在块内插值（端点 + index），插值在哪个空间做**不受你控制**。

交互后果：

- 如果你拿一张 **sRGB 纹理 + non-linear 预乘 alpha** 直接喂进压缩器，压缩器在 sRGB 数值上做内插，重建时 GPU 又用 sRGB decode 硬件乘一次——误差 **双重累积**，边缘偏灰或变脏的色带。
- 正确做法是**先 linear 化 → 线性预乘 → 再送压缩器**；或者让压缩器明确支持 sRGB-aware 内插（BC7 / ASTC 支持 sRGB 视作 linear 的 approximation）。

> 一句话原则：**预乘和压缩必须发生在线性域；sRGB encoding 是最后一步**。

## 实践 checklist

- albedo 纹理：sRGB flag **开**，工具里做 linear premultiply，压缩选 BC7 sRGB 或 ASTC HDR。
- 法线 / roughness / mask：sRGB flag **关**——这些通道本来就是线性数据，不能被硬件 gamma 解码踩一脚。
- UI / sprite 需要 sRGB blending："刻意违反正确性"的场景，blend state 写死在 sRGB，美术工具也按 sRGB 预乘——内部保持一致，避免 mismatched pipeline 里半 correct 半不 correct。
- HDR 粒子：全链路 linear 不走 sRGB；如果用 R11G11B10F 等 packed float，注意精度塌陷点。

## 与其他概念的关系

- 基础 decode/encode：[[gamma-correction-srgb]]
- 预乘 alpha 的数学：[[alpha-compositing]]
- 硬件 blend state：[[alpha-blending]]
- 色彩空间 TRC：[[color-space]]
- 块压缩细节：[[bc7-solid-color-blocks]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-srgb-premultiplied-alpha]]
