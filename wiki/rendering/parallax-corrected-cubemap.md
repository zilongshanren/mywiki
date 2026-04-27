---
tags: [渲染, 反射, 立方体贴图, 环境光照, ibl]
date: 2026-04-14
sources: 1
---

# 视差修正 Cubemap（Parallax-Corrected Cubemapping）

**Cubemap** 天然是「无穷远」的光源假设：shader 用反射向量采样它时，根本没传入位置信息，所以无论你走到房间的哪个角落，反射都像贴在天上一样跟着摄像机滑动——和场景完全脱节。**视差修正 cubemap** 解决这件事的办法很简单：给 cubemap 绑一个**包围盒**（AABB 或 OBB），shader 先沿反射方向跟包围盒求交，把交点当作「反射真正发生的位置」，再从 cubemap 中心到该交点重新取一个方向向量去采样。一下子反射就和场景里的墙、天花板、地板锚定在一起了。

Sébastien Lagarde 2012 年的 *Image-Based Lighting Approaches and Parallax-Corrected Cubemap* 把这套方法系统化；它从此成为游戏引擎处理 **局部反射探针** 的标准做法——Unreal 的 Reflection Capture、Unity 的 Reflection Probe、Frostbite 的 radiance volume，背后都是它。

## 核心代码

假设反射探针中心为 `CubemapPositionWS`，包围盒为 `[BoxMin, BoxMax]`，像素世界坐标为 `PositionWS`：

```glsl
float3 DirectionWS    = PositionWS - CameraWS;
float3 ReflDirWS      = reflect(DirectionWS, NormalWS);
float3 FirstHit       = (BoxMax - PositionWS) / ReflDirWS;
float3 SecondHit      = (BoxMin - PositionWS) / ReflDirWS;
float3 FurthestPlane  = max(FirstHit, SecondHit);
float  Distance       = min(min(FurthestPlane.x, FurthestPlane.y), FurthestPlane.z);
float3 IntersectPosWS = PositionWS + ReflDirWS * Distance;
ReflDirWS             = IntersectPosWS - CubemapPositionWS;
return texCUBE(envMap, ReflDirWS);
```

数学上就是「沿反射方向打一条射线，取与 AABB 的最远出射点」。因为除零会产生 `±inf`，取 `max`/`min` 的自然退化会把无效平面忽略掉——这是经典的 slab test 技巧。

## 泛用 cubemap 的小修正

Lagarde 的原版方案假设 cubemap 是**专门为这个空间烘焙**的——cubemap 自身已经被压缩到一个立方体，shader 里的公式再把它「解压」回 AABB 的实际尺寸。但在现实项目里经常只有一张**通用的模糊 cubemap**（比如引擎自带的、或者隔壁房间复用的），不是为当前房间烘焙的。这时候如果房间本身是非正方的（Kostas 的例子是 `z = 2x`、`y = 0.5x`），原版公式会把 cubemap 的坐标系以奇怪的比例拉伸，视觉上出现扭曲的反射。

[[kostas-anagnostou|Kostas Anagnostou]] 给出了一个 hack：先算包围盒三边里最小那条作为基准，再按三边的比值生成一个 `BoxScale`，最后把修正后的反射向量乘以它：

```glsl
float3 BoxDiff  = BoxMax - BoxMin;
float  minDim   = min(BoxDiff.z, min(BoxDiff.x, BoxDiff.y));
float3 BoxScale = minDim / BoxDiff;
ReflDirWS      *= BoxScale;
```

效果是把通用 cubemap 非均匀地「压回」包围盒。cubemap 的内容依然和场景不匹配（显然不匹配，毕竟不是为它烘焙的），但至少不再漂在空中——反射点的朝向跟上了摄像机的运动，这对玻璃、抛光金属这种辅助反射的用途已经够用了。

> 原作者 Lagarde 在评论里指出原版代码对**任意 AABB** 都是工作的，不局限于正方体；Kostas 也承认这一点，他的改动只针对「cubemap 非当前场景烘焙」这种 hack 场景。区分这两个语境是理解这条 trick 的关键。

## 相关

- [[environment-probe-placement]] — 反射探针的密度与摆放策略
- [[physically-based-shading]] — IBL 与 PBR 的关系
- [[deferred-rendering]] — 反射探针在 deferred 管线下的应用
- [[kostas-anagnostou]]
- [[envmap-ibl-approximation-errors]] — 包含视差修正引入的预过滤 footprint 扭曲、可见性误差等系统性分析

## Sources

- [[sources/interplay-parallax-corrected-cubemap]]
- [[sources/c0de517e-envmap-wrong]] — parallax correction 与预卷积假设矛盾的分析
- [[sources/c0de517e-parallax-corrected-followup]]
- [[sources/c0de517e-ggx-parallax-correction]] — Pesce：GGX 波瓣距离—粗糙度修正推导（2015 存档，2023 公开）
- [[sources/c0de517e-env-lighting-occlusion]] — Pesce：基于 diffuse probe 的 specular 上界 clamping，解决光泄漏
