---
tags: [source, unity, urp, hdrp, volume, scripting, c-sharp]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Scripting Guide（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Snapshot Shaders Pro* 撰写的 **三管线脚本接入指南**——如何用 C# 动态修改 Volume profile 上的后处理参数。

## 摘要

Snapshot Shaders Pro 支持 URP / HDRP / Built-in 三个管线，每个管线的 scripting API 都不一样，但是核心模式相同：**拿到 Volume，从 profile 里 TryGet 具体效果类，改 parameter 的 `.value`**。

- **URP**：`UnityEngine.Rendering.Volume` + `volume.profile.TryGet(out HalftoneSettings h)`。注意 URP 下所有效果类名都追加了 `Settings` 后缀（`Halftone` → `HalftoneSettings`）——这是 URP 独有的约定，HDRP 和 Built-in 都不加。修改例：`h.textureSize.value = 8`。
- **HDRP**：`UnityEngine.Rendering.Volume` + `volume.profile.TryGet(out Vortex v)`。效果类名直接就是效果名（没有 Settings 后缀）。HDRP 的 custom post process 是 out-of-the-box 支持的，不需要用户定义 Renderer Feature。
- **Built-in**：完全不同的命名空间 `UnityEngine.Rendering.PostProcessing`，类型是 `PostProcessVolume`（不是 `Volume`），API 是 `volume.profile.TryGetSettings(out OilPainting o)`（注意是 `TryGetSettings` 而非 `TryGet`）。这是 Post Processing Stack v2 的接口。

修改模式统一：拿到 effect 实例，找到想改的 **VolumeParameter 子类**（`FloatParameter` / `IntParameter` / `ColorParameter` / `TextureParameter` 等），**修改它的 `.value`** 字段（不是直接赋值整个参数）——这是 Volume 参数的"包装"设计：参数是一个对象而非原始值，`.value` 是实际数值。

## 关键要点

- **三管线 API 断层**是 Unity 后处理碎片化的具体体现——URP 加 `Settings` 后缀、HDRP 裸类名、Built-in 换命名空间和方法名
- `TryGet` / `TryGetSettings` 都返回 bool——profile 里没加这个效果时不写就走不到，脚本健壮性由调用者管
- `.value` 的包装设计（[[urp-volume-post-processing|PPv3 的 VolumeParameter]]）本质上是为了 Volume 混合引擎能追踪 override 状态——runtime 写 `.value` 等价于手工 override，写完下一帧混合才看到
- **URP 的 `Settings` 后缀**只对 pack 的自定义效果存在吗？原文没明说——URP 的 builtin 效果（Bloom、Vignette 等）是不加 Settings 的，这是 pack 的命名惯例而非 URP 规范
- 把 *volume* 字段暴露到 MonoBehaviour inspector 是常规做法——比 `FindObjectOfType<Volume>()` 更可控
- HDRP 的 "out-of-the-box custom post process" 是从 2020.2 的 HDRP 10 才完善——早期版本需要 CustomPassVolume 绕路
- 本指南虽然以 Snapshot Shaders Pro 为例，但**API 模式对任何 URP/HDRP 自定义 Volume effect 通用**——它是 [[volume-component-scripting|VolumeComponent 脚本化]] 的最小可运行示例

## 链接到的概念

- [[volume-component-scripting]]
- [[urp-volume-post-processing]]
- [[blit-render-feature]]

## 原文

- 链接：https://danielilett.com/snapshot-shaders-pro/scripting-guide/
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-scripting-guide.md`
