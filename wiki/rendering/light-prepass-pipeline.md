---
tags: [渲染, 光照, 管线, deferred, ni-no-kuni]
date: 2026-04-19
sources: 1
---

# Light Pre-Pass 管线

Light Pre-Pass 是 Wolfgang Engel 在 2009 年提出的一种「折中型」光照管线，介于 forward 和 deferred 之间。它先渲染 **深度 + 法线**，然后用一个单独的 pass 算出全屏的「光照累加结果（irradiance）」，再在主 color pass 里把这份光照作为输入，和材质贴图相乘，避免把完整的材质参数都写进 GBuffer。Adrian Courrèges 在 *Deus Ex: Human Revolution* 的帧分析里识别出过这套管线，[[thomas-poulet]] 在 [[sources/thomas-poulet-ninokuni-2-frame|Ni No Kuni 2 的帧分析]] 里给出了一个更完整的实例。

## 三步走

1. **Depth + Normal pre-pass**：把 opaque 物体写进一张屏幕尺寸的深度图和一张法线图，透明物体排除在外。Ni No Kuni 2 用的深度格式是 D24S8，但 stencil 实际不用；没有 reversed-Z，near/far = 0.1/1000，深度信息集中在最后 25% 的 [0,1] 区间里。
2. **Light map pass**：输入是上面两张图 + 灯光列表。**Ni No Kuni 2 把它做成一个 compute pipeline**，输出是屏幕大小的一张 buffer，存每像素的辐照度。把它放到 compute 上的好处是可以跟同时段的 light scattering pass 并发，[[thomas-poulet]] 猜测是为了打 GPU 的 async 空隙。
3. **Color pass**：正常跑一遍 forward，这时 depth write 还开着但已不需要（depth test 改 *Less Equal*），保证 0 overdraw 的重物料着色。着色器从 light map 里采样预算好的光照，和 albedo / 反射贴图合成。

## 和其他管线的对比

- 相比 [[deferred-rendering|deferred]]：GBuffer 小得多（只存 depth + normal），节省带宽，代价是材质参数每次都要重采；不容易支持太多材质变体的高级光照模型。
- 相比 forward / [[tiled-light-prepass|forward+]]：灯光计算集中在一个 pass 里，不用在每个 draw 里重复算，但 [[tiled-light-prepass|tiled]] 派更现代、更适合百千级灯光。
- 相比 [[unreal-frame-breakdown|UE 的 cluster + deferred]]：结构上 light pre-pass 可以看作 *没有 material ID 的 deferred 光照阶段* —— 把光算完就扔回 forward。

Ni No Kuni 2 的选择贴合它的视觉需求：只有环境光 + 少数动态光，没有 GI，没有阴影投射的局部光源，光的总数少，material 要和 **line-art / stylized shading** 紧紧耦合——所以不愿意让光照 pass 把 BRDF 选择固化下来。

## Sources

- [[sources/thomas-poulet-ninokuni-2-frame]]
