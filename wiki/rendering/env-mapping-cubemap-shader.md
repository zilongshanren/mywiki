---
tags: [渲染, shader, 环境贴图, hdri, 反射]
date: 2026-04-14
sources: 1
---

# 环境贴图：等距柱状 HDRI 的 shader 实现

**环境贴图**（environment map）是一张 360° 的全景纹理，用来代表场景周围的「远处光照和背景」。主流引擎用 **cubemap**——六张贴图拼一个立方体，硬件直接支持 `textureCube`；但在 GameMaker、WebGL1、以及一些老移动 GPU 上没有 cubemap 采样器。这时的标准替代是 **等距柱状投影**（equirectangular / HDRI）纹理，一张普通的 2D 贴图搞定，只是需要一点三角函数把方向向量映射回 UV。

[[xor-shader-artist|Xor]] 的 Mini: Environments 用这种方式把天空盒、反射球都做出来，本页提炼其中最关键的两个 shader 片段。

## 等距柱状格式的坐标含义

等距柱状贴图和世界地图是同一个数学：x 轴是 **偏航 yaw**（水平方向，0°→360°），y 轴是 **俯仰 pitch**（垂直方向，-90°→+90°）。给定一个归一化的三维方向向量 `dir`，可以用两次反三角函数拿到球极坐标：

```glsl
float yaw   = atan(dir.y, dir.x);                  // [-π, +π]
float pitch = asin(clamp(dir.z, -1.0, 1.0));       // [-π/2, +π/2]
vec2 sphere_uv = vec2(yaw / PI * 0.5 + 0.5,
                      pitch / PI + 0.5);
```

`clamp` 是为了防止 `dir.z` 由于浮点误差略超 1 导致 `asin` 输出 NaN——这类数值防御在所有反三角函数采样时都值得写上。这里 Xor 用的是 Z-up 的约定（`dir.z` 是 pitch），Y-up 场景需要把分量顺序换一下。

## Skybox：视向直接查表

最简单的用法是**天空盒**。从相机位置到当前着色点的方向就是「往天上看什么」：

```glsl
vec3 dir = normalize(v_world_pos.xyz - u_camera);
vec2 uv  = dir_to_sphere_uv(dir);
gl_FragColor = texture2D(uSky, uv);
```

注意 `v_world_pos` 必须从顶点着色器用世界矩阵算出来传下来，因为方向需要世界空间；camera 位置 `u_camera` 作为 uniform 传入。如果天空盒几何体是静止在相机上的一个大球或者 inverted cube，这一套可以直接绘制出全景背景。

## 反射：view vector + reflect()

从天空盒 shader 改成**反射物体**只要加一行 GLSL：

```glsl
vec3 ref_dir = reflect(dir, v_world_normal);
vec2 uv = dir_to_sphere_uv(ref_dir);
```

`reflect(I, N)` 把入射方向绕法线翻一下，这恰好是物理上的镜面反射方向。world-space 法线也要在顶点着色器里构造好：

```glsl
v_world_normal = normalize((gm_Matrices[MATRIX_WORLD] * vec4(in_Normal, 0.0)).xyz);
```

第四分量取 0 是因为法线是**方向**，不应受平移影响。严格地讲，非均匀缩放下这个写法不对——需要用 `inverse(transpose(model))`——但在匀速缩放场景里够用。

这是最古老的 **环境映射**（environment mapping）技巧之一：Blinn & Newell 1976，比 [[ibl-split-sum|IBL]] 早了几十年，却仍然是「简单引擎里把一个金属球体渲染得好看」最便宜的办法。

## 和 cubemap 的权衡

等距柱状贴图的优点是**不需要硬件 cubemap 支持**，缺点是：

- 两极 UV 严重密集，采样效率低；
- 需要两次反三角函数，比 `textureCube(dir)` 贵；
- 缺少硬件边缘过滤——cubemap 会在面交界处自动处理 seam，equirectangular 则会在 `u=0 / u=1` 接缝处闪烁。

所以凡是硬件支持 cubemap 的 3D API（D3D9+、OpenGL ES 3、WebGL2），都应该优先 cubemap；**等距柱状只在不支持 cubemap 或者只想存一张 PNG 分发时用**。反过来 HDRI 资源网站（如 PolyHaven）通常发等距柱状的 EXR/HDR，用之前最好预处理一次成 cubemap。

## 延伸方向

- 把 `reflect` 换成 `refract` 得到玻璃和水面折射；
- 从环境贴图里预积分出 diffuse irradiance map 与 specular prefiltered map，就是 PBR 中的 [[ibl-split-sum|image-based lighting split-sum]]；
- 对环境贴图做 mipmap 得到粗糙度导致的模糊反射；
- 动态环境贴图 = 每帧渲染一次 cubemap = 局部反射探针。

## 相关

- [[ibl-split-sum]] — 基于环境贴图的 PBR 预积分
- [[environment-probe-placement]] — 反射探针摆放策略
- [[parallax-corrected-cubemap]] — 让立方体探针近似盒形空间
- [[coordinate-spaces]] — 世界空间与模型空间的转换
- [[xor-shader-artist]]
- [[fragment-shader]]

## Sources

- [[sources/xor-mini-environments]]
