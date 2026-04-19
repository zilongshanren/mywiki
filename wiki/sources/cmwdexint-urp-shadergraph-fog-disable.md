---
tags: [source, unity, urp, shader-graph, fog, shader-variant]
date: 2026-04-19
sources: 1
---

# Disable Fog for URP Lit ShaderGraph（cmwdexint）

[[ming-wai-chan]] 发表于 2022 年 8 月的实战 hack：场景开了 Fog，但希望**某几个 ShaderGraph 材质不吃雾**。

## 摘要

URP 没给 ShaderGraph 一个直观的"关掉雾"开关，所以要从 shader keyword 层下手。方法分两段：**编辑器里**通过在 ShaderGraph 的 Blackboard 上声明 Reference 名严格匹配的三个 Boolean keyword（`FOG_LINEAR` / `FOG_EXP` / `FOG_EXP2`），然后在材质上取消勾选对应当前 fog mode 的 keyword，让 shader 编译期就把雾分支剔除。**打包时**则必须在 Editor 目录放一个 `IPreprocessShaders` 脚本，遍历每个 `ShaderCompilerData`，凡是目标 shader 名 + keyword 字符串包含 `FOG_` 的变体就直接从 list 里删掉——否则 Unity 可能把所有 keyword 组合都编译进 Player build、运行时选用。这是 URP 上对"排除特定 shader 的内置效果"的通用模板。

## 关键要点

- Unity 的 fog 由 multi_compile keyword `FOG_LINEAR` / `FOG_EXP` / `FOG_EXP2` 控制；shader 未声明时默认启用，显式声明后交给材质勾选位决定。
- 编辑器 hack：ShaderGraph Blackboard 加 Boolean keyword，reference 名必须完全一致，材质上取消勾选。
- Player build hack：`IPreprocessShaders.OnProcessShader` 里按 shader 名 + keyword 字符串过滤 `ShaderCompilerData`，`data.RemoveAt(i); --i;` 倒走删除。
- 脚本必须放 Editor 文件夹，否则依赖 UnityEditor 命名空间会导致运行时构建失败。
- `callbackOrder` 设大一点可让自定义 stripping 跑在 URP 内置 stripping 之后，是惯例。

## 链接到的概念

- [[urp-shadergraph-fog-strip]]
- [[shader-variant-stripping]]

## 原文

- 链接：https://cmwdexint.com/2022/08/24/turn-off-fog-for-urp-lit-shadergraph/
- 本地：`raw/articles/cmwdexint.com/2022-08-24_disable-fog-for-urp-lit-shadergraph.md`
