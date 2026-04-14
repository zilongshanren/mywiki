---
tags: [source, 渲染, 工具链, unity, shader]
date: 2026-04-14
sources: 1
---

# Using Unity as an FX Composer Replacement for Shader Prototyping（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 2 月的长文，系统比较 Unity 免费版与 FX Composer 在 shader 原型场景下的功能覆盖与工作流。

## 摘要

起因是他准备一场**物理基础渲染（PBR）**的讲演，需要在 FX Composer 里加载 Stanford Dragon 来做反射模型对比，但 FX Composer 加载屡屡失败。他换到 Unity，两次拖放就拿到想要的结果，于是决定做一次完整评测。文章逐项对比：Unity 有更强的内容管线（FBX / OBJ 自动导入、Cubemap 拖 6 张图就成）、更现代的场景编辑器、material Inspector、shader 保存即编译；支持 Cg / HLSL、Hull / Domain shader 所以能做 tessellation，这是 FX Composer 做不到的。限制也明确：Unity 不支持 `.fx` 文件格式；免费版没 render-to-texture，复杂多 pass 受限；`SubShader`+`Pass` 没有 `Technique` 的概念，不能跨 pass 共用 vertex shader 函数；Unity 的 `Properties` 块里的属性必须在 shader 代码里显式声明变量才能访问，不像 FX Composer 自动绑定。作者最后给了**归一化 Blinn-Phong + Fresnel + 简单 HDR tonemap** 的完整 Unity shader 代码作为起手模板，并表态他本人已经切换到 Unity。评论里有读者补充：把 `Range` 属性复制一份改成 `float` 就能同时显示滑块和数值。

## 关键要点

- Unity 内容管线完胜：drag-and-drop 加载模型 / 贴图 / cubemap
- shader 保存即自动编译（FX Composer 要手动触发）
- 支持 Hull / Domain shader → 能做 tessellation
- 受限：无 `.fx` 支持、免费版无 RTT、无 `Technique`、`Properties` 需要显式声明
- 作者给出归一化 Blinn + Fresnel shader 模板
- 结论：技术美术 / 图形程序员转 Unity 即可；纯美术可能更喜欢 FX Composer 的 Maya 式界面

## 链接到的概念

- [[shader-prototyping-tools]]
- [[unity-surface-shaders]]
- [[microfacet-brdf]]
- [[kostas-anagnostou]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2013/02/04/unity-as-an-fx-composer-replacement-for-shader-prototyping/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-02-04_using-unity-as-an-fx-composer-replacement-for-shader-prototy.md`
