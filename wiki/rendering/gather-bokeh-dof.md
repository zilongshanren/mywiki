---
tags: [渲染, 后处理, 景深, bokeh, unreal, 移动端]
date: 2026-04-19
sources: 1
---

# Gather Bokeh DoF（向内采样式景深）

**[[scatter-bokeh-dof|Scatter bokeh]]**——每个源像素朝外"撒"一个精灵——在桌面 AAA 是物理对的一侧，但在 Tegra X1 这样的移动 GPU 上 1080p 要撒约 200 万 quad，带宽直接爆。**Gather bokeh** 是对偶方案：**每个输出像素向邻居要颜色**，按 bokeh 形状做 N 个 tap 的 weighted average——成本 O(N × 输出像素)，GPU 纹理 cache 擅长这种稠密读，可分离和半分辨率叠加后非常便宜。

[[adrian-courreges|Adrian Courrèges]] 在 [[sources/adrian-ue4-optimized-post-effects|UE4 优化补丁集]]里实现了 *GatherDOF*——作为 UE4 *BokehDOF* 的 drop-in 替代：保留 UE4 *BokehDOF* 的 CoC 计算（艺术家参数完全复用），换掉它的 scatter 主体。在大 bokeh 半径场景里比 *BokehDOF* 快到 **10×**。技术来自 DOOM 2016 和更早的 CryEngine 3。

## 形状映射：方形网格 → 任意多边形

Gather 的关键是"怎么在 shader 里生成一个覆盖 bokeh 形状的采样点云"。Courrèges 的做法走两步：

1. **方形 → 圆盘**（[Shirley 1997](https://pdfs.semanticscholar.org/4322/6a3916a85025acbb3a58c17f6dc0756b35ac.pdf) 的低失真映射）：把 `[-1,1]²` 均匀网格拉成极坐标，按象限分两段线性。
2. **圆盘 → n 边形**：给定极角 θ 时把半径乘一个收缩因子
   `r = cos(π/n) / cos((θ mod 2π/n) − π/n)`
   即可把点云"压"成正 n 边形。n=5 得五边形、n=6 六边形——对应物理相机的光圈叶片数。

两步都是 ALU-only，无 LUT、无 vertex fetch，可以完全内嵌进像素 shader。

## 降噪：McIntosh flood-fill

tap 数有限时 bokeh 盘里会残留明显噪点（尤其孤立亮点 + 大半径时）。暴力提 tap 数是一条路，更聪明的是一次 **flood-fill pass**——用 McIntosh 的 "max-filter" 思路：邻域里取最大亮度。意外地好使——黑色不连续被最亮值填平，bokeh 形状瞬间干净。

near-field 额外再把 CoC map 自己做 1/8 下采 + blur（取 tile 内的 max CoC），再拿这张下采过的 CoC 决定采样半径——这样 near / in-focus 分界处不会有硬跳变。far-field 不需要这套，直接用原 CoC。

## Pros / Cons

- **性能**：小半径下 *BokehDOF* 因为触碰像素少反而更快；大半径下 gather 一骑绝尘（文章里报了 15ms → 2ms 的对比，Tegra X1@768 MHz）。
- **噪声**：*BokehDOF* 采样最理想；Gather 在半径极大时会噪。
- **定制度**：*BokehDOF* 可以自定义 sprite + 色差；Gather 只能多边形无色差。
- **边缘伪影**：*BokehDOF* 有著名的"屏幕底部一条细边不模糊"bug（[Octopath Traveler](https://en.wikipedia.org/wiki/Octopath_Traveler) 的 tilt-shift trailer 里肉眼可见）；Gather 在 near-field 边缘会主动做 fade，更自然。

出货证明：《Dragon Quest XI S》Switch 版和《Pikmin 4》都用了这套 Gather DoF 的修改分支（Pikmin 4 的 miniature tilt-shift 效果是卖点）。

## 相关
- [[scatter-bokeh-dof]] — 物理对的另一侧，桌面高档效果
- [[mgs-v-fox-engine-frame]] — Fox Engine 的 DoF 是 scatter 的多级分辨率加强版
- [[thin-lens-model]] — CoC 推导
- [[chromatic-aberration-post]] — scatter 路线才能做"对的"色差
- [[separable-gaussian-blur]] — creamy bokeh 的低成本近似
- [[adrian-courreges]]
- [[circular-separable-dof]] —— Frostbite/EA 的复数可分离圆盘 gather 路线
- [[variable-size-gather-dof]] —— Scheuermann 2004 的早期 gather DoF，按 CoC 调整采样半径

## Sources

- [[sources/adrian-ue4-optimized-post-effects]]
