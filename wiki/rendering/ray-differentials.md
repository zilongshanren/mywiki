---
tags: [渲染, 路径追踪, mipmap, 纹理, 滤波, ray-differentials]
date: 2026-04-19
sources: 1
---

# 光线微分（Ray Differentials）

**光线微分（ray differentials，Igehy 1999）** 是路径追踪器里给 mipmap level 选择用的「屏幕空间导数代用品」。光栅化时 GPU 天然有 2×2 quad 可以算 `dudx/dudy`；路径追踪只有一条条独立 ray，因此必须另外构造：每条相机 ray 额外携带两条「邻居 ray 的方向偏移」，在命中点和切平面求交，反解出对应的 `dudx/dvdx/dudy/dvdy`，再走 [[mipmap-generation-sampling]] 的标准公式拿 LOD。

## 为什么需要它

没有 ray differentials，所有二级反射/折射 ray 只能**退回到 level 0 点采样**——纹理缓存（tiled + lazy load）瞬间失效，production 场景百 GB 级贴图就跑不动。Arnold、Vray、Corona、RenderMan、Hyperion、Manuka 都在这个问题上有自己的一套 hack，没有一家走纯 Suykens & Willems 2001 的 path differential（理论通用但复杂度随路径长度平方增长）。

## 四种实用方案对照

[[yining-karl-li]] 2018 年在自家 hobby renderer **Takua Renderer** 里梳理了四种主流工程做法：

1. **Igehy 1999 纯 ray differentials**：只对镜面/折射事件有严格公式；glossy 和 diffuse 都需要启发式扩宽 footprint。PBRT、Mitsuba、Solid Angle Arnold 的相机 ray 都是这一派。
2. **SPI Arnold 累计粗糙度**（Kulla et al. 2018）：跟踪 ray 沿途累计粗糙度，一旦累计值足够高或碰到 diffuse event，直接跳到最高 mip level；极其激进的 filtering，换来极佳的纹理访问模式。配合 OSL 上自动微分（dual arithmetic，Piponi 2004）——JIT 地把导数计算织进 shader 执行路径。
3. **RenderMan 单 float 简化 ray differential**（Christensen et al. 2018）：每条 ray 只携带 origin width + unit spread 两个 float——信息量比 Igehy 少得多，但 path tracer 本来就在每像素做 supersampling，这个简化够用了。[[hyperion-renderer]] 用的方案类似。
4. **Weta Manuka unified roughness**（Fascione et al. 2018）：从 shading 系统里统一估 mean cosine 驱动 ray differential 宽度；独一份。

Matt Pharr 在 PBRTv3 实验分支里另有一条更简单的经验路线：diffuse event 给 hemisphere 的 1/25、glossy event 给 1/100，就够用。

## Path differentials 与 covariance tracing

- **Path differentials**（Suykens & Willems 2001）：对每个 scattering event 沿 BSDF lobe 取偏导，最终构造一个多边形 footprint；通用但贵，没人用在生产。
- **Covariance tracing**（Belcour et al. 2013 / 2017）：把 transport/occlusion/roughness 全部编码成 5D 协方差矩阵，沿 path 只需携带单个矩阵，复杂度线性。它相对 path differentials 更关键的优势是——**可以从光源端出发做**，这一点正是解决 BDPT 的钥匙。

## 双向路径追踪的难题

Igehy ray differentials 的定义要求「相对于屏幕空间像素 footprint 求导」，但**光路径的最后一条 ray 才到相机**，完整 path 构造完之前根本没有 screen space 可供参考。更糟的是，就算能给光源端起一个初始 differential，其宽度也不能像相机 path 那样可以随意扩宽——因为光路径随时可能连向相机，footprint 必须始终 ≤ 1 像素。

这导致绝大多数支持双向技术（BDPT / progressive photon mapping / VCM）的生产渲染器，对光路径**干脆不算 ray differential**，全部退回 level 0 点采样——这就在整个引入 tiled texture cache 的意义上打了个洞。Manuka 团队隐晦地提到用 ray differential 控制 photon map gather 宽度，但细节不公开。

## Manuka 的 shade-before-hit 与绕过它的办法

Manuka 的 **shade-before-hit** 架构在渲染启动阶段就把几何细分成 micropolygon grid 并完成所有 pattern generation，BSDF 参数烘到顶点上；path sampling 时不再做 texture lookup——**于是整个 BDPT mip level 问题被架构级地绕过**。代价是启动时间很长，而且在相机正前方放放大镜头的场景下会失灵（全局预烘没法针对放大后的像素 footprint）。

## Takua 的 camera-based mip level selection

Yining 不愿意把 Takua 改成 shade-before-hit（他追求第一批样本出来得快），也不愿意把 BDPT 的光路径 mip level 吞了，于是设计了一个「只依赖世界空间到相机距离」的折中方案：

1. 启动时对相机每个像素计算一条 ray differential，求所有像素里最窄的 dx 和 dy。
2. 每次 ray 命中时计算 differential surface（dpdu/dpdv——对三角形是 vertex position 和 uv 的线性解）。
3. 构造一条「假 ray」：从相机 origin 指向当前命中点，带上步骤 1 求出的最窄 differential。
4. 用这条假 ray 走标准流程求 dudx/dvdx/dudy/dvdy，再求 mip level。

这样所有 path（包括光路径）的 mip level 只由空间位置决定，天然一致——BDPT 的不同 camera↔light vertex connection 拿到相同 mip level，不再偏差。语义上它跟 Manuka 的 shade-before-hit 一样，但发生在路径构造时，启动开销几乎为零。

论文里的实测：1920×1080 / 16 spp forest 场景，总 tile 数 745k：

- 无 mipmap（退化为全量访问）：unidir 42.18%，bdpt 42.32%
- Ray-based（incident ray 启发式）：unidir 13.84%，bdpt 27.30%
- **Camera-based（Takua）：unidir 14.05%，bdpt 14.07%**

对 BDPT 而言，camera-based 的 tile 访问量和 unidir 相当，比 ray-based 几乎便宜一半。已知的失效场景是**相机前放大透镜**——折射把世界空间 footprint 放大了，但 camera-based metric 看不到，可能选到过高 mip 导致贴图糊掉，和 shade-before-hit 的失效场景同源。

## 延伸

- Takua 的这套方案只用 point sampling 就直接用（不做 bilinear filtering），理由是「path tracer 本来每像素就几百上千 sample，texture filtering 的抗锯齿由 supersampling 兜底」——Moonray 团队（Lee et al. 2017）独立得出同样的结论并作为生产默认。
- 长远看作者倾向 covariance tracing 方向，因为 filtering 重要性在 glinty microfacet 等效果上会再上一个台阶，而 covariance tracing 是当前已知能同时覆盖 path space filtering、又能在 camera/light 两端都工作的技术。

## 相关

- [[mipmap-generation-sampling]]
- [[hyperion-renderer]]
- [[wavefront-path-tracing]]
- [[path-guiding-production]]
- [[ptex-gpu-streaming]]
- [[yining-karl-li]]

## Sources

- [[sources/yiningkarlli-mipmap-bidirectional]]
