---
tags: [unity, urp, shader-graph, fog, shader-keyword, shader-variant]
date: 2026-04-19
sources: 1
---

# 给特定 ShaderGraph 材质关掉 URP 雾效

典型场景：场景里开启了 *Lighting Settings* 里的 Fog（因此所有 Lit 物体都吃雾），但某几个用 ShaderGraph 写的特殊物体**不想吃雾**。URP 没有在 ShaderGraph 上给"禁用雾效"的直观开关，Ming Wai Chan 的 hack 方案走 **shader keyword 反制 + [[shader-variant-stripping]]**。

## 编辑器内的 hack：声明 fog keyword 但不勾

URP 的 fog 是以三个 multi-compile keyword 控制：`FOG_LINEAR`、`FOG_EXP`、`FOG_EXP2`。**如果 shader 根本没声明这些 keyword**，Unity 会在编译这个 shader 时补上雾效代码（作为默认启用）。反过来，如果 ShaderGraph **显式声明了这些 Boolean keyword 并且 reference 名字完全匹配**，那具体材质要不要吃雾就由 keyword 的勾选状态决定。

做法：

1. Lighting Settings 里开 Fog；
2. 在 ShaderGraph 的 *Blackboard* 上添加三个 Boolean keyword，**Reference 必须严格写成** `FOG_LINEAR`、`FOG_EXP`、`FOG_EXP2`；
3. 新建材质挂这个 ShaderGraph，**取消勾选对应当前 fog mode 的 keyword**——比如项目用 Exponential Squared，就把 `FOG_EXP2` 取消（作者也提到只把 `FOG_LINEAR` 保留勾上也能生效，取决于 URP 版本的代码路径）。

原理是 ShaderGraph 生成的代码里，雾效分支由这些 keyword 包围；keyword 被材质关掉等于整段雾效代码编译时就被剔除。

## 打包后的 hack：shader variant stripping

Editor 的技巧**在 Player build 里不保险**——Unity 在打包时可能会把所有相关 keyword 组合都编译出来，运行时根据场景 fog 状态选用其中一个变体。这时需要在 Editor 目录放一个 `IPreprocessShaders` 实现，**主动剥掉想丢的 variant**：

```csharp
using UnityEditor.Build;
using UnityEditor.Rendering;
using UnityEngine.Rendering;

class StrippingExample_Shader : IPreprocessShaders {
    public int callbackOrder => 99;
    public void OnProcessShader(Shader shader, ShaderSnippetData snippet,
                                IList<ShaderCompilerData> data) {
        for (int i = 0; i < data.Count; ++i) {
            string keywords = "";
            foreach (var k in data[i].shaderKeywordSet.GetShaderKeywords())
                keywords += " " + k.name;

            if (shader.name == "Shader Graphs/ShaderGraphNoFog" &&
                keywords.Contains("FOG_")) {
                data.RemoveAt(i);
                --i;
            }
        }
    }
}
```

要点：

- 必须放在 *Editor/* 文件夹，否则运行时类型不存在会报错；
- `callbackOrder` 大一点能让自己的剥离发生在 Unity 内置剥离之后；
- 遍历 `ShaderCompilerData` 时**边删边倒回** `i`，标准 C# 列表倒走写法；
- 过滤条件用**shader 名 + keyword 名**双重约束，防止误伤其他 shader 的同名 keyword。

这其实是 URP 给"某个 shader 永远不要吃雾"这个需求的**通用模板**：ShaderGraph 层声明 keyword 控制默认行为 + 构建期变体剥离避免打包意外引入。

## Sources

- [[sources/cmwdexint-urp-shadergraph-fog-disable]]
