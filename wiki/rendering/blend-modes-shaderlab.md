---
tags: [shader, urp, shaderlab, blend, 透明, alpha]
date: 2026-04-19
sources: 1
---

# ShaderLab 的 Blend 命令与混合模式

ShaderLab 里的 `Blend` 命令是半透明、叠加发光、乘法色板等一切 **src/dst 线性组合**效果的唯一入口。它放在 `Pass` 块顶部（不是 HLSL 里），语法 `Blend <srcFactor> <dstFactor>`——GPU 会把当前像素写的颜色当 source、屏幕已有的颜色当 destination，各自乘因子再相加。公式 `输出 = 源 × srcFactor + 目标 × dstFactor`。默认（不写）等同 `Blend Off`（不混合、直接覆盖，配 `ZWrite On` 就是 opaque shader）。

## 11 个可选因子

对应 Unity 的 `UnityEngine.Rendering.BlendMode` 枚举（整数值是它在枚举里的索引）：

| 值 | 名称 | 含义 |
|---|---|---|
| 0 | `Zero` | 清零 |
| 1 | `One` | 原样通过 |
| 2 | `DstColor` | 逐通道乘目标颜色 |
| 3 | `SrcColor` | 逐通道乘源颜色 |
| 4 | `OneMinusDstColor` | 1 - 目标色 |
| 5 | `SrcAlpha` | 乘源 alpha |
| 6 | `OneMinusSrcColor` | 1 - 源色 |
| 7 | `DstAlpha` | 乘目标 alpha |
| 8 | `OneMinusDstAlpha` | 1 - 目标 alpha |
| 9 | `SrcAlphaSaturate` | `min(SrcAlpha, OneMinusDstAlpha)`（用于顺序无关透明的近似） |
| 10 | `OneMinusSrcAlpha` | 1 - 源 alpha |

Ilett 吐槽这张表"顺序没有规律"——用时只能查文档。

## 三种常见 blend 模式

| 效果 | srcFactor | dstFactor | 数学含义 |
|---|---|---|---|
| **Alpha blending** | `SrcAlpha` | `OneMinusSrcAlpha` | 标准半透明；`α·src + (1-α)·dst` |
| **Additive（发光）** | `SrcAlpha` | `One` | 加亮不减暗；粒子光点、全息效果常用 |
| **Multiply（色板）** | `DstColor` | `Zero` | `src · dst`；乘法调色、阴影叠印 |

*Premultiplied alpha* 则是 `One` `OneMinusSrcAlpha`——前提是源颜色本身已经被 alpha 乘过（纹理导入设置里勾选 Premultiplied），避免透明边缘发黑的著名问题。（参见 [[alpha-compositing]]）

## 把因子暴露成面板参数

通用的 transparency shader 常把 src/dst 做成 Property：

```shaderlab
Properties
{
    [Enum(UnityEngine.Rendering.BlendMode)] _SrcBlend("Src Blend", Integer) = 5
    [Enum(UnityEngine.Rendering.BlendMode)] _DstBlend("Dst Blend", Integer) = 10
}
SubShader
{
    Pass
    {
        Blend [_SrcBlend] [_DstBlend]
        ZWrite Off
        ...
    }
}
```

两个关键技巧：

- **`[Enum(...)]` 属性**——把 Integer Property 渲染成下拉菜单，`UnityEngine.Rendering.BlendMode` 是完整的 C# 命名空间名。
- **`Blend [_Prop] [_Prop]`**——方括号引用 Property，**不需要在 HLSL 里声明**这个变量（它是 ShaderLab-only 的，和 HLSL 互不影响）。这是少数 Property 不走 HLSL 的例子之一。

合上这两点，一个 shader 就能在 Inspector 里切换 alpha / additive / multiply，而无需写多份 shader。URP Lit 自己也用同样的套路（只是它额外暴露了 Surface Options 把模式打包）。

## 透明队列与 depth write

`Blend` 必须配合正确的 Queue 和 ZWrite：

- **`RenderType = Transparent` + `Queue = Transparent` + `Blend Src Dst` + `ZWrite Off`** —— 半透明标准组合。
- **`Queue = AlphaTest` + `Blend Off` + `ZWrite On`** —— [[dither-alpha-clipping|alpha clip]] 路径，仍算 opaque。
- `ZWrite Off` 的理由：透明物体相互重叠时用 back-to-front 排序、depth buffer 不写入能避免排序错误导致后面的透明物被当前这个"挡住"。打开 `ZWrite On` 仅在非常特殊的深度裁剪场景下做。

## 与 Blend Op 的关系

默认 `BlendOp` 是 `Add`，即 src·f + dst·f。可以换成 `Sub` / `RevSub` / `Min` / `Max`——`Max` 在做 occluded glow 之类"最亮者胜"的累积时很便利。工业 PBR shader 和主流透明 shader 通常不需要动 BlendOp。

## 相关

- [[alpha-blending]] —— 数学细节
- [[alpha-compositing]] —— premultiplied alpha 的工程深坑
- [[dither-alpha-clipping]] —— AlphaTest 路径的替代方案
- [[shaderlab-hlsl-basics]] —— Pass 和 Property 在骨架里的位置

## Sources

- [[sources/danielilett-shader-code-transparency]]
