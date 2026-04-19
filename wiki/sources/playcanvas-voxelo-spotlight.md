---
tags: [source, playcanvas, gaussian-splatting, ai, 电商, ug3d, 3dgs]
date: 2026-04-19
sources: 1
---

# AI-Powered 3DGS Product Visualization - Developer Spotlight on Voxelo（Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2026-01-22 发布于 blog.playcanvas.com 的 Developer Spotlight 第六期：采访 Voxelo.ai（英国团队，创始人含 Kaedim 前 CTO）。Voxelo 的卖点是**上传一段 3-4 分钟产品视频，输出可嵌入电商页的 3DGS + AR 体验**，他们称之为 UG3D（user-generated 3D）。

## 摘要

Voxelo 的工作流：用户拍一段 3-4 分钟的产品视频（手机或 DSLR 都行），上传后 Voxelo 用 AI 重建成 3DGS 数字孪生，输出 web-ready 3D + AR + 生活化 lifestyle 图 + 品牌产品图——"一次捕获，多种内容产出"。目标客群是中小电商（鞋服、家具、家居），后来发现大品牌兴趣更大（Cosatto、SportShoes.com 等）。性能方面，他们早期用 PlayCanvas React 做原型验证，但"wrapper 不直接暴露的底层功能需要自写脚本接入 engine"——对于 AR viewer 和 splat editor 这类深度功能，他们直接用 **native PlayCanvas app 再 embed 进 React 主站**，绕开 React 包装层提升性能和开发速度。关键数字：迁到 PlayCanvas 后帧率 2×+；切 [[sog-compression-format|SOG]] 后文件是"之前已压缩格式"的 1/3，相对原始 AI 重建的 PLY 减 95%+；"关闭 anti-aliasing" 这样的小 flag 对 Gaussian splat 渲染有明显的性能收益。展望：把 input 继续简化（视频越来越短）、扩 AI 生成内容的维度、嵌到 PDP 里看用户在产品上停留在哪——"3D 会像图片视频一样成为标配"。

## 关键要点

- **AI → 3DGS 的路径**：短视频 → AI 重建 → 3DGS 数字孪生 → 多种内容衍生（3D viewer / AR / lifestyle 图 / 产品图）。
- **UG3D 概念**：User-Generated 3D，强调从"需要 DSLR + 专家" 降门槛到"手机 + 几步点击"。
- **PlayCanvas React 的边界**：原型化好用，但深度定制（AR、splat editor）选择绕过 React 包装直接用 native。
- **性能实测**：帧率 2×、SOG 文件 1/3 之前格式、相对原 PLY 减 95%+。
- **小 flag 大影响**：关 AA 对 splat 渲染的帧率有明显收益——作者强调"认真读文档"这件事。
- **商业视角**：创始人预期 3D 在电商成为"像图片视频一样的标配内容层"。

## 链接到的概念

- [[sog-compression-format]]
- [[gaussian-splatting-web]]
- [[playcanvas-react-declarative]]

## 原文

- 链接：<https://blog.playcanvas.com/ai-powered-3dgs-product-visualization-developer-spotlight-on-voxelo>
- 本地：`raw/articles/blog.playcanvas.com/2026-01-22_ai-powered-3dgs-product-visualization-developer-spotlight-on.md`
