---
tags: [unity, urp, hdrp, volume, 脚本, c-sharp, 后处理]
date: 2026-04-19
sources: 1
---

# Volume Component 运行时脚本化（Volume Component Scripting）

通过 Volume 系统把后处理参数暴露给美术是 Unity 现代渲染管线的基本做法——但**从 C# 运行时修改**这些参数（比如：玩家受伤时把 Vignette 红度推到最大、出洞后把 Bloom 强度平滑过渡）需要额外的 scripting API。Daniel Ilett 的 *Snapshot Shaders Pro* scripting guide 给出了三管线（URP / HDRP / Built-in）各自的最小示例，反映了 Unity 后处理生态的 API 碎片化。

## 共通模式：Volume → Profile → TryGet → VolumeParameter.value

三管线都走一个等价流程：

1. 拿到 **Volume 对象引用**（通常用 `public Volume volume` 暴露到 Inspector，让美术拖进去）
2. 从 `volume.profile` 里 **TryGet** 出具体 effect 的实例
3. 修改该 effect 上某个 **VolumeParameter** 子类（`FloatParameter`、`IntParameter`、`ColorParameter`、`TextureParameter` 等）的 `.value` 字段

`.value` 这一层包装不是多余——[[urp-volume-post-processing|PPv3 Volume 系统]]需要知道哪些参数是用户"覆盖"过的（profile UI 里被勾选的那些），这个信息编码在 VolumeParameter 的 `overrideState` 字段上。直接写 `.value` 隐含地把这个参数当作"已覆盖"参与混合。

## 三管线的 API 差异

**URP**：`UnityEngine.Rendering` 命名空间、`Volume` 类型、`TryGet` 方法。**Snapshot 2 / Pro 的 URP 效果类名都有 `Settings` 后缀**（`Halftone` → `HalftoneSettings`）——这是 pack 作者的命名惯例，URP 的内建效果（`Bloom`、`Vignette`、`ColorAdjustments`）并不加。

```csharp
public Volume volume;
void Start() {
    if (volume.profile.TryGet(out HalftoneSettings h))
        h.textureSize.value = 8;
}
```

**HDRP**：同命名空间 `UnityEngine.Rendering`、同 `Volume` 类型、同 `TryGet` 方法，但**类名裸用**（`Vortex` 而非 `VortexSettings`）。HDRP 从 2020.2 起原生支持 custom post process，不需要用户注册 Renderer Feature。

```csharp
if (volume.profile.TryGet(out Vortex v))
    v.strength.value = 2.5f;
```

**Built-in**：这是 Post Processing Stack v2，完全不同的世界——命名空间 `UnityEngine.Rendering.PostProcessing`、类型 `PostProcessVolume`（不是 `Volume`）、方法 `TryGetSettings`（不是 `TryGet`）。

```csharp
using UnityEngine.Rendering.PostProcessing;
public PostProcessVolume volume;
void Start() {
    if (volume.profile.TryGetSettings(out OilPainting o))
        o.kernelSize.value = 27;
}
```

## 为什么 API 会这么乱

这是 Unity 后处理演化的历史伤疤：

- **Built-in** 走 Post Processing Stack v2（独立包，`UnityEngine.Rendering.PostProcessing`）
- **HDRP** 从头重做 Volume，用 `UnityEngine.Rendering` 命名空间
- **URP** 复用 HDRP 的 Volume 核心，但自定义 effect 的 API 细节有微调（类名 Settings 后缀是作者选择）

三个管线之间**没有统一的后处理 scripting abstraction**——想写跨管线的后处理控制代码就得 `#if UNITY_RENDER_PIPELINE_URP` / `#if UNITY_RENDER_PIPELINE_HDRP` 三套预编译分支。这也是为什么 asset store 上任何 cross-pipeline 的 post 包都要写**三份脚本**——Snapshot Shaders Pro 正是如此。

## Parameter 的类型识别

改值前要知道参数的类型：

- 数值：`FloatParameter`、`IntParameter`、`BoolParameter`、`MinFloatParameter`、`ClampedFloatParameter`、`MinIntParameter`、`ClampedIntParameter`
- 颜色：`ColorParameter`（可能带 HDR flag）
- 贴图：`TextureParameter`、`Texture2DParameter`、`CubemapParameter`
- 枚举：`EnumParameter<T>`
- 曲线 / 渐变：`AnimationCurveParameter`、`GradientParameter`、`TextureCurveParameter`

这些都继承自 `VolumeParameter` 基类，都有 `.value` 字段。

## 动画化参数：`Mathf.Lerp` + 外部驱动

由于 `VolumeParameter` 没有 tween 内建支持，常规做法是外部驱动：

```csharp
float t = (Time.time - startTime) / duration;
h.textureSize.value = Mathf.Lerp(4, 16, t);
```

或者用 DOTween / Unity animation 驱动脚本属性、脚本再写入 `.value`。

## 警告：profile 是 shared asset

`volume.profile` 返回的是共享资产——修改会影响所有用同一 profile 的 volume。如果只想改当前 volume 不影响其他，用 `volume.sharedProfile.Instantiate()` 或 `VolumeManager.instance.stack` 从 stack 层处理。这是 [[urp-volume-post-processing]] 原条目没细讲但实际项目里的高频坑。

## 相关

- [[urp-volume-post-processing]] —— Volume 系统本身
- [[volume-mask-layers]] —— 另一个运行时配置点
- [[blit-render-feature]]
- [[custom-srp]]

## Sources

- [[sources/danielilett-snapshot-pro-scripting]]
- [[sources/danielilett-blur-shaders-pro-scripting]]
