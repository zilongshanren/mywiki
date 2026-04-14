---
tags: [source, 渲染, shader, 环境贴图, hdri, 反射]
date: 2026-04-14
sources: 1
---

# Mini: Environments（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 11 月 24 日的一篇，主题是**环境贴图**——在没有 cubemap 的 GameMaker 里用**等距柱状投影（equirectangular / HDRI）**纹理做天空盒和反射球。核心概念抽到 [[env-mapping-cubemap-shader]]。

## 摘要

文章以「GameMaker 不支持 cubemap」作为起点，指出等距柱状贴图是通用替代：x 轴是 yaw（0°→360°），y 轴是 pitch（-90°→+90°），和世界地图是同一个投影。给定一个三维方向向量，可以用 `atan(dir.y, dir.x)` 和 `asin(clamp(dir.z,-1,1))` 分别取出 yaw / pitch，再归一化到 `[0,1]` 做 UV。天空盒的做法是用 `normalize(v_world_pos - u_camera)` 算视向方向，直接查环境贴图；反射物体只需在此基础上加一行 `reflect(dir, v_world_normal)`，把视向绕法线翻转作为采样方向。顶点着色器里 `v_world_normal = normalize((gm_Matrices[MATRIX_WORLD] * vec4(in_Normal, 0)).xyz)` 是常见写法，注意第 4 分量取 0 让平移不作用到方向向量上。作者顺带推荐 PolyHaven 作为免费 CC0 HDRI 资源站，并提到 GM 当前不支持 HDR 数据，需要先用 GIMP 转 PNG。Shadertoy 上有配套的可跑 demo。

## 关键要点

- **等距柱状公式**：`uv = vec2(atan(y,x)/PI*0.5 + 0.5, asin(clamp(z,-1,1))/PI + 0.5)`，`clamp` 防 asin NaN。
- **天空盒视向**：`normalize(v_world_pos - u_camera)` 得到「从相机指向当前像素」的世界方向。
- **反射一行字**：`reflect(view_dir, world_normal)` = 镜面反射方向，PBR 时代看似基础，1976 年就在用。
- **世界法线的向量化法**：`(world_matrix * vec4(normal, 0)).xyz` 再 normalize；严格讲非均匀缩放下应该用逆转置。
- **等距柱状的缺点**：两极采样密度高、接缝处没有硬件 seam 修复、两次反三角函数比 `textureCube` 贵——优先 cubemap。
- **资源建议**：PolyHaven CC0 HDRI；GM 不支持 HDR 需要离线转 8-bit PNG，会损失 range。
- **同样方法可做折射**：把 `reflect` 换 `refract` 即可，IOR 做 uniform。

## 链接到的概念

- [[env-mapping-cubemap-shader]]
- [[ibl-split-sum]]
- [[environment-probe-placement]]
- [[parallax-corrected-cubemap]]
- [[coordinate-spaces]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-environments-1475397
- 本地：`raw/articles/mini.gmshaders.com/2022-11-24_mini-environments.md`
