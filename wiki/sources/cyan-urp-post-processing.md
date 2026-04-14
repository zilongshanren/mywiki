---
tags: [source, unity, urp, 后处理, shader]
date: 2026-04-14
sources: 1
---

# Post Processing in the Universal RP（Cyan）

[[cyanilux|Cyan]] 2020 年 6 月发表的文章，系统地介绍了 Unity **Universal Render Pipeline（URP）** 的后处理体系——从它和旧 Post Processing Stack V2（PPv2）的关系，到集成式 Volume 系统（PPv3）的使用方法，再到 Volume 不支持自定义效果时的绕路方案：写一个 `ScriptableRendererFeature` 做 Blit。

## 摘要

文章首先厘清 PPv2 和 PPv3 的历史：PPv2 是通过 Package Manager 提供的旧包，只支持 Unity 2019.4 LTS + URP v7.2-7.4 左右的版本；URP v8 之后只剩集成式 Volume 系统，没有自动迁移路径。随后讲解 Volume 组件的两种形态（Global / Local）、Priority/Weight/Blend Distance 的混合规则、Profile 与 Override 机制、以及 Camera 上必须手动打开 Post Processing 才能看到效果的坑。关于 Volume Mask / Volume Trigger 的解释澄清了很多人不清楚的"相机依赖哪个 Transform 来判定 Local Volume"的问题。最后给出一份完整的 `Blit.cs` 源码——这是 URP 社区早期自定义后处理的标准模板。

## 关键要点

- Volume 后处理（PPv3）是基于体积叠加、按 Priority/Weight 混合参数的系统，而不是像 PPv2 那样的"链式后处理 stack"。
- URP 早期的 Volume 系统不开放自定义效果扩展点——必须用 `ScriptableRendererFeature` + Blit 绕路（Unity 2022 才内置 Fullscreen Graph 组件）。
- Blit 的 shader 必须使用 **Unlit Master** 节点，且必须把 `blitShaderPassIndex` 显式设为 `0`——否则 Shader Graph 生成的 shadow caster pass 会被用作 Blit 源，屏幕被砸出黑色矩形。
- URP v8 时代没有 Ambient Occlusion、部分 Motion Blur / TAA 缺失。
- Ambient Occlusion、自定义效果、和 PPv2 的迁移路径都在 Unity 的 roadmap 上。

## 链接到的概念

- [[urp-volume-post-processing]]
- [[blit-render-feature]]
- [[scriptable-render-pipeline]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2020/06/22/urp-post-processing/
- 本地：`raw/articles/cyangamedev.wordpress.com/2020-06-22_post-processing-in-the-universal-rp.md`
