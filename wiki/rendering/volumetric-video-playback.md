---
tags: [volumetric-video, webxr, ar-vr, streaming, mesh-streaming]
date: 2026-04-14
sources: 1
---

# 体积视频回放

体积视频（volumetric video）又称全息视频，是把真实人物或表演以动态几何 + 贴图的形式录制下来的技术，观众可以在 AR、VR 或 2D 屏幕中自由移动视角观看。Microsoft Mixed Reality Capture Studios（MRCS）从 2010 年起就在推进这一方向，其核心产物是一种 `.hcap` 格式的流式资源——内部按帧序列打包了变化的网格几何与纹理，需要运行时一边拉取数据、一边生成 mesh 与 material 喂给渲染管线。

在 Web 端集成体积视频面临两个工程现实。第一，数据量巨大：一段几十秒的全息视频动辄数百兆，必须放在 CDN（例如 Azure CDN）后面独立托管，而不能和引擎资源捆在一起；PlayCanvas 的做法是让 `holo-video-player.js` 接收一个外部 URL，由 MRCS 的 devkit 库 `holo-video-object-umd.js` 负责流式解码并在运行时创建网格。第二，回放脚本必须适配引擎的实体/组件模型——把解码出的动态 geometry 包装成标准的 render component，才能和 [[shadow-mapping-basics]]、灯光、后处理等既有管线无缝协作。

真正复杂的是**跨设备的统一发布**：同一个 URL 必须同时支持桌面浏览器的轨道相机、移动端 WebXR 的 AR 透视模式、以及 Oculus Quest 这类 6DOF VR 头显。为此需要一个 XR manager 脚本统一协调：根据设备能力决定显示 AR 按钮还是 VR 按钮，进入 AR 时切换到透明画布的第二相机、关闭天空盒层、把带 `ar-relative` 标签的实体移到用户正前方；退出会话时再恢复。VR 分支复用既有的传送/拾取/手部渲染代码，并把播放控制 UI 放到世界空间中、用 pivot 实体保持始终面向用户——世界空间 UI 是 VR 里唯一合理的做法，因为屏幕空间在头显中不存在。

两个值得记下的小技巧：一是**投影天空盒**（projected skybox），通过一个自定义 shader 把 cubemap 投影到平面地板上，免去建模就得到了"无限延展的地板 + 背景"效果；二是**阴影接收器材质**（shadow catcher），采样阴影贴图后把没有阴影的区域置为全透明，让投影地板也能接收角色投下的软阴影——这是在平面占位几何上伪造接触阴影的常见做法。

文中也坦白两个未解 bug 值得留意：VR 下启用 clustered lighting 的阴影会严重掉帧（规避方法是只保留定向光阴影）；进入 AR 后 screen-to-world 的投影仍用相机组件的 FOV，而引擎实际替换的是投影矩阵，导致 UI 命中不准——作者在第一帧从投影矩阵反解相机参数再写回组件来绕过。两者都暗示了 WebXR 引擎中"相机组件 vs 实际 projection matrix"的抽象接缝尚未打磨平整。

## Sources

- [[sources/playcanvas-volumetric-video]]
