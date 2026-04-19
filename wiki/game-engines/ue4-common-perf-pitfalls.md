---
tags: [unreal-engine, performance, engineering-practices, vr]
date: 2026-04-19
sources: 1
---

# UE4 项目反复出现的工程陷阱清单

[[michael-allar]] 把他做 UE4 "救火"顾问时反复碰到的低级问题整理了一份清单。大部分和"高级工程技巧"没关系，只是纪律。记录在这里当 checklist 用。

## 源码管理与构建

- **任何缓存文件都不该进源码服务器**。UE4 引擎会检测某些缓存（如音频烘焙缓存）存在与否来决定要不要重建数据——如果错误地把别人机器上的缓存同步过来，引擎会以为"已经烘焙过了"而跳过步骤，导致只有原作者机器上能听到声音，其他所有人都是哑的。这类 bug 追起来极痛苦，却可以用一条正确的 `.gitignore` / `p4ignore` 避免。
- **小批量提交 + 写清 commit 信息**。把 2GB、2000 个文件塞进一条 "did some work" 的提交里，事后想 bisect 等于没救。
- **从第一周开始做自动化 build 并跑 playtest**。不要到上线前两个月才第一次做打包测试。
- **在目标硬件上测**。VR 项目定了最低 GPU 是 GTX 960 还拖到 11 个月后才第一次在 960 上跑，是洛杉矶地区每三个月发生一次的事。

## 代码与资源纪律

- **警告当错误处理**。"那个 warning 挂了几个月了可以忽略"是大多数问题的起点。
- **不要做 Blueprint 意大利面**。[blueprintsfromhell.tumblr.com](https://blueprintsfromhell.tumblr.com/) 收集了典型反例。
- **原型转生产要留时间重写**。赶工拼出来的系统不能直接进 production，否则整个项目都会开始长蜘蛛网。
- **遵循风格指南**。项目内一致就行，没有就用 Allar 的 [ue4.style](http://ue4.style/)。不一致的代码/资产命名会让每个新人都多烧 1-2 周。
- **多人游戏要从第一天就上网络**。"加上 multiplayer" 不是一个可加的功能。
- **真的去跑 profiler**。打开 GPU / game thread profiler 马上能看到某个 Blueprint 花了 100ms 而不是 1ms 的情况非常常见。
- **"在我机器上能跑"先做 file diff**。90% 的情况下 diff 一开就是答案。
- **大概率不是编译器 bug**——是你。

## 资产与渲染

- **不需要所有贴图都 4K**。按 texel density 规划。
- **不要堆几千个 dynamic shadow casting 灯**。3 FPS 的渲染再好看也不是游戏。
- **用 LOD**。没时间手做至少开自动生成。
- **岩石不该有 12 个 material slot**。PBR 时代的制作思路和十年前不一样。
- **Component 比想象中贵**。场景里任何会动的 `USceneComponent`，它本身动一下就要递归处理所有子 component 的 transform 更新，嵌套深的层级是性能黑洞。

## VR 专项

- **VR 不要滥用平面反射**。20 个 2048 分辨率的实时平面反射根本跑不到 HMD 需要的帧率。
- **VR 默认用 forward**。如果团队里没人说得清 deferred 和 forward 的差别，又在做 VR，立刻切 forward——Allar 的原话是"飞到客户办公室，改成 forward，然后回家"。
- **VR 不要落后引擎版本超过 2 个**。每个版本都在修 VR 性能，落后 = 白送帧率。

## 团队配置

- **缺 lead / senior engineer 本身就是问题**。小问题在项目初期被 senior 随手指出来的成本，远远低于在上线前两周请"救火队"。

## 相关

- [[unity-vs-unreal]]
- [[umg-user-widget-lifecycle]]
- [[ue4-editor-battery-throttle]]

## Sources

- [[sources/allar-ue4-firefighter]]
