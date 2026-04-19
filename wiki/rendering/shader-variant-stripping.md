---
tags: [unity, shader, 编译, 打包, ipreprocessshaders]
date: 2026-04-19
sources: 1
---

# Unity Shader Variant Stripping

Unity 打包 shader 时，每个 shader 的 `multi_compile` keyword 会在构建期组合成一棵**变体树**，项目稍大就会爆炸（几千到几十万变体是常态）。Unity 提供了 `IPreprocessShaders` 接口，让开发者在构建期**主动剥掉不需要的变体**——减小包体、缩短编译时间、省运行时内存。

## 钩子形态

`IPreprocessShaders` 放在 Editor 程序集，构建开始时 Unity 会对**每个 shader 的每个 snippet**（一个 pass、一个 stage 的编译单元）调一次 `OnProcessShader(Shader, ShaderSnippetData, IList<ShaderCompilerData>)`。列表里每一条是一个**具体变体**（keyword 集合 + 平台 + 图形 API）。删掉列表元素就把这个变体从最终包里剥掉。

`callbackOrder` 控制多个 preprocess 之间的顺序，URP 自带的剥离也走同一接口；自定义的一般写 99 之类的大数字排到后面。

## 惯用匹配模式

Ming Wai Chan 在 URP fog 排除（见 [[urp-shadergraph-fog-strip]]）里给的模板是最朴素的形态：把 `ShaderKeywordSet` 的所有 keyword 名拼成字符串，用 `shader.name == "..."` + `Contains("FOG_")` 双重判定，命中就 `data.RemoveAt(i)`。

几个容易踩的坑：

- **倒走索引**：列表删元素会让后续下标错位，必须 `--i` 或倒序遍历。
- **写错位置**：脚本**必须放在 Editor 目录**，否则 Player 运行时找不到 UnityEditor namespace 会直接编译失败。
- **剥太猛会丢变体**：如果某个 keyword 组合在运行时仍会被 `Shader.EnableKeyword` 动态开启，却被 stripping 剥掉了，运行时会走 **fallback variant** 或黑屏。
- **组合匹配而非单 keyword**：`ShaderCompilerData.shaderKeywordSet` 是一整套 keyword 的集合，条件要按集合语义写（"同时包含 A 且不包含 B"），不能把每次命中都删。

## 与 Shader Stripping 的全局开关的关系

URP 还在 *URP Global Settings* 里提供 checkbox 形式的批量剥离（Lighting、Post Processing 等分类），那套是 URP 自己的 `IPreprocessShaders` 实现。自定义 `IPreprocessShaders` 是**在这之外追加**，两者按 `callbackOrder` 串行执行。

## Sources

- [[sources/cmwdexint-urp-shadergraph-fog-disable]]
