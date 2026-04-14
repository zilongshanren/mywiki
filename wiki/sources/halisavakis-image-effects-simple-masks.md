---
tags: [source, 渲染, unity, shader, 后处理, mask]
date: 2026-04-14
sources: 1
---

# My take on shaders: Simple masks (Harry Alisavakis)

[[harry-alisavakis]] 在 *My take on shaders* 系列的第三篇（2017-05-03）继续 image effect 教程线，主题是「怎么让一个全屏后处理只作用在画面的一块区域上」。

## 摘要

文章把第一篇教过的「[[unity-image-effect-basics|image effect 骨架]] + 反色」这个 hello-world 升级成「只在屏幕中心一个圆形区域反色」。手段是引入第二张纹理 `_MaskTex` 作为灰度遮罩：黑色像素保留原图、白色像素出特效、灰色按比例混合。fragment shader 关键就一行 `(1 - col) * mask + col * (1 - mask)`，等价于一次 lerp。Alisavakis 强调这种朴素遮罩的两个限制：遮罩贴图必须和屏幕同宽高比（否则圆会被拉成椭圆），且无法在运行时动态变形——后续教程会用 in-shader 自定义遮罩来解决。文末他提到这个看似过于简单的概念是他当年「敢动手实验 shader」的转折点。

## 关键要点

- 全屏后处理 + 遮罩 = 局部特效；公式是 `lerp(原图, 处理图, mask)`。
- 遮罩纹理按 `i.uv` 采样，所以必须匹配屏幕纵横比。
- 黑色 = 不变，白色 = 全特效，灰色 = 部分混合，几乎与 Photoshop 蒙版同构。
- 这是 image effect 学习路径的「第二级台阶」：第一级是写 fragment shader 一行返回 `1 - col`，第二级是知道用 mask 把它限制到目标区域。
- 局限引出后续课题：用 [[sdf-2d-primitives|2D SDF]] 在 shader 内部实时算遮罩，以解锁动态参数。

## 链接到的概念

- [[image-effect-mask-blend]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-simple-masks-introduction-to-image-effects-part-iii/>
- 本地：`raw/articles/halisavakis.com/2017-05-03_my-take-on-shaders-simple-masks-introduction-to-image-effect.md`
