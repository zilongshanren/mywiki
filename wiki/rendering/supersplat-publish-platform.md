---
tags: [渲染, gaussian-splatting, supersplat, webxr, 发布平台, 视频, 开源]
date: 2026-04-19
sources: 3
---

# SuperSplat 从编辑器到发布平台

2024 年下半年，[[supersplat-pwa|SuperSplat]] 还只是一个 3DGS 编辑器——你把原始 PLY 拖进去，清掉飞点、对齐坐标、导出压缩 PLY，剩下的"怎么托管、怎么给人看"得自己想办法。从 2025 年 2 月到 4 月，PlayCanvas 团队用三个版本（2.0 / 2.2 / viewer 开源）把它扩张成一个完整的**编辑 + 发布 + 托管 + 社区**一体化平台——3DGS 版的 Sketchfab 雏形。这条路径揭示的是 3DGS 这种新型 3D 表示从"研究输出"走向"消费级内容"所必需的基础设施清单。

## 发布流水线：从 PLY 到 URL

SuperSplat 2.0（2025-02-13）的核心变化是 **`File > Publish`**：登录 PlayCanvas 账号、填基本信息、点 Publish、拿到一条 URL。底层 stack 是——开源的[[gaussian-splatting-web|压缩 PLY]] 格式（节省下载和显存）+ [[playcanvas-webgpu-editor|PlayCanvas 引擎]]驱动的 HTML viewer + PlayCanvas 的托管服务。发布出来的 splat 默认在 `superspl.at` 公共 gallery 里露出，也可以设为 unlisted 保留私域 URL。域名从 `playcanvas.com/supersplat` 单独迁到 `superspl.at`，信号是这个产品线已经大到值得独立品牌。

## Timeline：让 splat 有镜头脚本

2.0 同时引入 **Timeline 关键帧相机动画**：在时间线上选帧 → 移相机 → 打 keyframe，连成一条完整 flythrough。这个功能的意义不在"让 splat 动起来"——splat 本身就是静态的，动的是观察它的相机——而在于**把 3DGS 从"可交互 3D 资产"升级到"有镜头语言的视觉内容"**。对于博物馆、房地产、产品展示这类业务场景，观众更习惯被"带着看一圈"而不是自己拖拽相机。

## 视频渲染与竖屏

SuperSplat 2.2（2025-03-13）把 Timeline 接上视频输出管线：`Render` 菜单里选分辨率、码率，甚至直出竖屏比例。编码"impressively fast"——暗示走的是浏览器侧硬件加速路径（WebCodecs 或类似）。竖屏预设是个很小但方向性强的细节——3DGS 工具首次主动适配移动端短视频平台（TikTok、小红书、Reels）的分发形态。

这一步把 SuperSplat 接进了**现代内容生产的主流管线**：不仅可以分享一个 3D URL 给会点开链接的朋友，也可以直接生成一段可贴进任意社交平台的短视频。对创作者来说，这降低了"让 splat 被看见"的门槛。

## 项目文件：`.ssproj`

Timeline 让 SuperSplat 项目变复杂——多个 splat、一串关键帧、相机参数、清洗历史——这些信息需要跨会话保存。2.0 引入的 **`.ssproj`** 就是这个持久化容器：一个 ZIP 壳，里面装 JSON 元数据 + 多个 PLY 文件。这个设计思路很经典：

- **ZIP 作为容器**：所有主流操作系统默认支持，且可以用任意 ZIP 工具直接窥探结构。
- **JSON 存项目级元数据**：项目设置、时间线关键帧、图层信息。
- **PLY 存 splat 数据**：复用已有格式，不为项目格式发明新的二进制结构。

同时 `File` 菜单语义被重新梳理：**`Open/Save/SaveAs` 只吃 `.ssproj`**，**`Import/Export` 处理 `.ply` / `.splat`** 等交换格式。这避免了新手把"导入 PLY"当成"打开项目"的路径混淆——这种路径混淆在很多 DCC 工具里反复出现过，干净的语义分离很值钱。

## WebXR：AR / VR 一等公民

发布的 viewer 自带 WebXR 支持——点 viewer 的 AR 按钮就能把 splat 放进真实房间；戴 VR 头显可以直接沉浸进场景。团队测试过的设备包括 Meta Quest 2/3、Apple Vision Pro、Android 智能手机。这是 3DGS 相对传统照片/视频的核心差异点：**同一份数据，既能在平面屏幕看，也能在混合现实里看**。一次内容生产对应多种消费形态。

## Embed：把 splat 贴到任意网页

2.2 引入的 **splat embed** 让 3DGS 从"点链接看"升级到"嵌入任意网页里的可交互模块"——类似 YouTube 视频但内容是**可交互**的 3D splat 而不是 iframe 视频。对产品展示页、博客文章、在线杂志，这是真的有替代 2D 产品图的潜力。

## 社区层

2.2 同步上线了 **user pages**（每个创作者有自己的展示页）、**评论**、**社交分享**（X / LinkedIn / Slack / email）。这些功能堆在一起就是一套迷你社交平台。引用的创作者像 tipatat（食物 splat）、Studio Duckbill（日本风景）、Christoph Schindelar 展示了早期社区的广度——3DGS 的应用边界已经从"科研 demo"扩到食物、风景、产品等日常内容。

## Viewer 开源：链路最后一块补齐

2025 年 4 月 9 日，**SuperSplat Viewer** 也以 MIT 协议开源。至此 SuperSplat 全链路——编辑器、引擎、viewer——**三段都是开源的**。用户可以选 superspl.at 托管（省心），也可以下载 viewer 代码自部署（可控）。两条路径跑的是同一份代码、体验一致。这种"**托管 + 自托管共享代码**"的开源策略给了创作者实际的议价权：不喜欢平台策略随时可以搬家，但搬家不意味着重写 viewer。

Eastcott 同时预告了 viewer 的下一个大功能——**annotations**，即在 splat 场景里放置信息面板，像 Matterport 的 tag 但嵌在 3DGS 里。这是 3DGS 走向"可交互沉浸内容"（导览、教学、产品说明、展馆）的下一步。

## 视角：3DGS 需要什么样的基础设施

把 SuperSplat 这三个版本拼起来，可以画出**3DGS 从研究走向消费的最小基础设施清单**：

1. **格式**：能压缩的 PLY + 能序列化的项目 ZIP。
2. **编辑**：清洗、对齐、瘦身。
3. **镜头**：关键帧相机动画。
4. **输出**：Web URL、视频文件、embed 代码。
5. **沉浸**：WebXR AR/VR。
6. **托管 + 社区**：统一域名、user page、评论、分享。
7. **viewer 开源**：创作者议价权。

少任何一项，3DGS 都还只是"技术 demo"。凑齐这 7 项，3DGS 才真正具备**作为一种新媒体形态被消费**的条件。PlayCanvas 团队 2 个月内把 7 项凑齐的节奏很快，也解释了为什么 SuperSplat 在 3DGS 创作者里迅速站住了位置。

## 相关

- [[supersplat-pwa]]
- [[gaussian-splatting-web]]
- [[playcanvas-webgpu-editor]]
- [[webgpu-intro]]
- [[will-eastcott]]
- [[volumetric-video-playback]]

## Sources

- [[sources/playcanvas-supersplat-2-0-publish]]
- [[sources/playcanvas-supersplat-2-2-video]]
- [[sources/playcanvas-supersplat-viewer-oss]]
