---
tags: [渲染, frame-analysis, fox-engine, mgs-v, deferred-rendering, 后处理]
date: 2026-04-19
sources: 1
---

# Metal Gear Solid V / Fox Engine 一帧的全流程

[[adrian-courreges|Adrian Courrèges]] 2017 年用他定制的 [[sources/adrian-mgs-v-graphics-study|ReShade 分支]]把《MGS V: The Phantom Pain》PC 版一帧拆开——因为原版 ReShade 注入会触发 Fox Engine 的反调试自杀，Courrèges 自己 fork 了 ReShade 加 hook，导出中间 buffer、DXBC 着色器字节码。这帧是医院序章 Snake 和"Man on Fire"的镜头，总计 **2331 draw call / 623 纹理 / 73 render target**。

Fox Engine 是一套 [[deferred-rendering|deferred]] 渲染器，但有几个与同世代 AAA 同行不同的选择，非常值得单独记录。

## 流水线主线

1. **Depth pre-pass**：只画地形，从 heightmap（16-bit float 顶点 shader 读高度）生成；在开放世界（阿富汗山脉）里地形是绝佳 occluder，early-Z 拒掉被山挡住的建筑 / 士兵 / 树——闭室场景 pre-pass 收益小。
2. **G-Buffer**：**只 3 张 B8G8R8A8 + 32-bit depth**，非常"轻"。albedo / normal / specular(roughness + specular + material-ID + SSS 透射)。**reverse-Z**（近平面=1）保远距离精度。
3. **Velocity map**：先画动态 mesh（红通道做 mask、速度写 B/A），再 compose 静态几何的 reprojected velocity——静态部分完全从 depth + 前后 projection matrix 推出来。Snake 和士兵虽然技术上是动画 mesh，但引擎判定"动得太慢"直接按静态处理，省了一次 skinning（cost 可观）。
4. **双 SSAO 组合**：**LISSAO**（Toy Story 3 的"线积分"法，5 tap 低频粗阴影，把球形体积切成线形子体积做深度单次采样的加权和）+ **Scalable Ambient Obscurance 变体**（11 tap 高频细节，不用 depth mip、直接读 normal map、half-res）——各自半分辨率 + depth-aware blur，最后 compute shader 合成。两种算法对不同几何频率响应互补，SAO 参数被特意调得对角色腿部等高频变化更敏感。
5. **Irradiance spherical maps**：关卡按区域烘 [[spherical-harmonics|SH 系数]]，运行时每帧从 SH 重建小球映射，塞进 **16×16 tile 的 HDR atlas**——9 float vs 完整 cubemap 6 面，省大量带宽和内存。
6. **双 lighting pass**：先 non-shadow light（一个灯一个 volume 画 diffuse + specular 两张 RT），再按 shadow map 画 shadow-casting light（4k×4k per spot）。
7. **早 tonemap**：这是 Fox Engine 的**特殊选择**——tonemap + gamma 矫正**在 emissive/transparent/SSR/DoF 之前**就完成了，后续所有透明、反射、景深都在 **LDR** 域进行。alpha 通道保留 **pre-tonemap HDR luminance** 供 bloom 的 bright-pass 用。现代主流 HDR 管线通常反过来——tonemap 放最后。
8. **Emissive + transparency + reflection probe**：玻璃反射从 256×256 baked HDR cubemap 取——每个位置存 **sunny / cloudy / rainy / stormy × 一天各时刻**的多个版本，permutation 量惊人。
9. **SSR**：半分辨率 depth raymarch（4 tap per ray），alpha 用屏幕边缘 fade 隐藏"屏幕外物体"缺失，最后 Gaussian blur + 合成。
10. **Heat distortion**：对整帧**多次 copy**主 RT 做局部 stretch——典型的"每次 distortion 都要 resolve 一次"的高带宽做法。
11. **Bloom**：1/4 下采 + bright-pass（依赖 alpha 里存的 HDR luminance）+ 程序化 lens flare / chromatic aberration + 4 次 [[kawase-blur|Kawase blur]] 替代 Gaussian。
12. **DoF（sprite scatter）**：half-res near + far 两张场；但为控 overdraw，又拆出 1/4、1/8、1/16 **多级分辨率 buffer**——每个 sprite 按 CoC 只画进一级，vertex shader 把不属于本级的 sprite 顶点推到视锥外丢掉。这是 [[scatter-bokeh-dof|scatter bokeh]] 的一种工业级多层实现，也是 UE4 *BokehDOF* 的同族技术。
13. **Lens dirt + 额外 anamorphic lens flare**：精灵驱动。
14. **Motion blur**：MHBO 2012 算法——tile-max velocity + 沿速度方向局部 stretch。
15. **Color grading**：256×16 的 [[color-lut|3D LUT]]（16 slice × 16×16）走 trilinear，美工工作流是"场景截图里嵌 neutral LUT → 美工在 Photoshop 里调 → 提取修改后的 LUT 喂回引擎"。
16. **FXAA** 替代 MSAA（deferred 固有限制）。
17. **Final touch**：美工还能在最后贴 sprite 做局部调亮 / 压暗——"美工控制贯穿到最后一刻"是 Fox Engine 的设计哲学之一。

## 技术口味

把 Fox Engine 和同世代 deferred 对比，几个签名性的选择：

- **尽早 tonemap 到 LDR**——和 Frostbite / UE 主流做法相反，目的是让透明 / SSR / DoF 全部在 LDR 压缩过的色彩里跑，带宽省，但对 HDR 叠加（emissive 粒子、反射到高光处）会有一定精度损失；Fox 靠在 alpha 里留 pre-tonemap luminance 给 bloom 挽回。
- **双 SSAO**：LISSAO + SAO 组合而不是单一 HBAO / GTAO；频率响应互补，但总成本也翻倍。
- **小 G-Buffer**（3 × 32-bit + depth）：逼迫 specular channel 把 roughness / specular / material-ID / SSS 压在一起——和小 G-Buffer 派（Frostbite、id Tech 6）同一取向。
- **reverse-Z 深度 + velocity mask 小技巧**：开放世界高视距时这两者基本是标配，MGS V 把它们做得很干净。

## 相关

- [[adrian-courreges]]
- [[deferred-rendering]]
- [[unreal-frame-breakdown]] — [[kostas-anagnostou]] 的 UE4 版对照
- [[sources/thomas-poulet-anno-1800-frame]] — Anno 引擎（forward+ 路线的对比样本）
- [[spherical-harmonics]]
- [[scatter-bokeh-dof]] — MGS V 的 DoF 是这技术的分级实现
- [[kawase-blur]]
- [[bloom-threshold-blur-composite]]
- [[color-lut]]
- [[chromatic-aberration-post]]
- [[shadow-mapping-basics]]
- [[msaa-ssaa]]
- [[hbao-interleaved-sampling]]

## Sources

- [[sources/adrian-mgs-v-graphics-study]]
