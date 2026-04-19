---
tags: [unity, urp, shader-graph, emissive, 渲染, 扫描]
date: 2026-04-19
sources: 1
---

# 世界空间扫描波（World Scan）

开放世界游戏里常见的"按一次按钮，一圈发光的环从某个点向外扩"的扫描效果（No Man's Sky、《地平线》、《死亡搁浅》的扫描模式），底层是**三四个节点就能做出来的 shader**。Ilett 把这个效果叠进自定义 Terrain 之上，作为 Shader Graph Basics Part 11 的第二个教学例子。

## 原理：两个 Step 夹出一圈

给定：

- `_ScanOrigin`（`float3`，世界空间的扫描中心，通常由 C# 脚本从射线点击处设置）；
- `_ScanDistance`（`float`，扫描已经走过的距离，`Time.deltaTime * speed` 在 C# 里累加）；
- `_ScanWidth`（`float`，发光圆环的厚度）；
- `_ScanColor`（`HDR Color`，发光颜色）。

每个片元计算：

```
d = distance(worldPos, _ScanOrigin)
inner = step(_ScanDistance, d)                        // 1 if d > scanDistance
outer = 1 - step(_ScanDistance + _ScanWidth, d)       // 1 if d < scanDistance + width
ring  = inner * outer                                 // 1 inside ring, 0 elsewhere
emissive = ring * _ScanColor
```

`inner * outer` 给出一个在 `[_ScanDistance, _ScanDistance + _ScanWidth]` 之间为 1 的环，乘以 HDR 颜色塞进 `Emissive` 输出即可。配合 URP 的 **Bloom** post-processing（阈值低于 color intensity 时像素会炸光），整个环就发光扩散。

## 为什么走 `Emissive` 而不是 `Base Color`

Emissive 不走光照路径，在阴影、夜间、室内都保持全亮——扫描波本质是"物体自发光"的 UI 化表达，Base Color 会被 diffuse lighting 衰减，做不出这个感觉。HDR 颜色强度调到 > 1.0 之后才能触发 Bloom 阈值，这也是为什么 `_ScanColor` 必须开 HDR 而不是普通 LDR。

## C# 一侧的交互

Ilett 的 `WorldScanner` MonoBehaviour 给出了最简接入：

```csharp
if (Input.GetMouseButtonDown(0) &&
    Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out var hit))
{
    terrainMaterial.SetVector("_ScanOrigin", hit.point);
    scanDistance = 0f;
}
scanDistance += Time.deltaTime * scanSpeed;
terrainMaterial.SetFloat("_ScanDistance", scanDistance);
```

`Material.SetVector` / `SetFloat` 的第一个参数字符串必须和 Shader Graph property 的 **Reference** 值**完全一致**——这是前面 Terrain 教程里也强调过的，保持「下划线前缀、无中间下划线」格式可以避免人类记忆负担（`_ScanOrigin` 而不是 `_Scan_Origin`）。

## 变体

这个骨架的外延很宽：

- **换成球壳** —— 用 `length(worldPos - origin)` 是球形环；换成某个平面投影（比如忽略 y 轴）就是圆柱形环，扫描线沿地面铺。
- **扫描线噪声** —— 在 `d` 基础上加一点 Perlin noise（见 [[classic-shader-noise]]）让环边缘有不规则形状。
- **多波并发** —— 改成 `distances[]` 数组在 shader 里循环，一次点击可以发多个环。
- **把 mesh 换成 Terrain 之外的普通物体** —— 完全通用，任何能进入 `Emissive` 的 shader 都能加。

## 相关

- [[terrain-splatmap-shader-graph]]
- [[bloom-threshold-blur-composite]]
- [[shader-graph-lighting-primer]]

## Sources
- [[sources/danielilett-shader-graph-terrains]]
- [[sources/danielilett-snapshot-pro-world-scan]] —— Snapshot Shaders Pro 的 Volume override 版 World Scan，含 ramp 纹理驱动的条带颜色过渡
