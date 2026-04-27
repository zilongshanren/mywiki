---
tags: [渲染, opengl, metal, vulkan, 坐标系, 帧缓冲]
date: 2026-04-27
sources: 1
---

# 帧缓冲坐标约定（OpenGL / Metal / Vulkan）

OpenGL、Metal、Vulkan 三套图形 API 在纹理 UV 原点和多边形绕序（winding order）上取得共识，但在**帧缓冲坐标（framebuffer coordinates）Y 轴方向**上各持一套约定，给跨 API 的代码共享带来了连环陷阱。

## 三套 API 达成一致的部分

- **内存布局原点**：三套 API 都将纹理和帧缓冲数据的"低地址"放在左上角，行方向向右递增，再向下换行。UV (0,0) 就是内存里最早的那个像素/纹素。
- **多边形绕序**：顺时针/逆时针的定义都在"最终呈现给用户的方向上"判断——只要渲染结果正确，绕序定义就是一致的。这意味着绕序设置不需要跨 API 调整（前提是 Y 轴方向已统一）。

## OpenGL：全局 Y 向上，内部自洽

OpenGL 的所有坐标系（Clip Space、NDC、帧缓冲坐标）都以**左下角为原点，Y 向上**。这与绝大多数窗口系统（Y 向下）相反，驱动会在最后一步悄悄翻转图像再送给 compositor。代价是与操作系统的约定格格不入；好处是整套坐标系极为一致，render-to-texture 后用相同的 UV 读回来方向天然正确。

## Metal：混合约定，内置 Y 翻转

Metal 采用"**Clip 空间 / NDC Y 向上，帧缓冲坐标 Y 向下**"的混合策略。Viewport 变换内置了一次 Y 翻转（无法关闭），因此对 D3D 程序员来说感觉自然。

然而 render-to-texture 场景下会触发连环问题：

1. 默认渲染到纹理时，Metal 将低内存放在左上角（天空 → 低地址），而 OpenGL 风格的代码期望天空在高地址。
2. 若像 X-Plane 一样主动在 transform stack 插入 Y-flip（让 Metal 的 render-to-texture 结果与 OpenGL 方向一致），则 viewport、scissors 参数需要调整，front-face winding order 也需要反转（镜像翻转了三角形的可见面）。
3. 使用 `[[position]]`（相当于 `gl_FragCoord`）重建世界坐标时，光栅化的像素 Y 坐标会上下颠倒，需要在 shader 或 C++ 端交换四角系数。

## Vulkan：全局 Y 向下，可选翻转

Vulkan 默认"**全部 Y 向下**"——Clip Space Y 方向与 OpenGL 相反，这是三套 API 里最一致但也最违反习惯的设计。好消息是：Vulkan 1.1 允许指定**负值 viewport height**，这等价于把 Y 轴翻转回来，从而与 Metal 和 D3D 对齐，之后只需处理上面 Metal 小节里的一套问题。

## 跨 API 适配的工程策略

X-Plane 的选择提供了一个参考方案：

- 以 OpenGL 坐标约定（Y 向上、天在高内存）作为**内部规范**；
- 对 Metal 主动注入 Y-flip，让 render-to-texture 结果符合内部规范；
- 这样所有采样现有磁盘纹理的着色器无需改动，只有 render-to-texture 的建立代码和使用 `[[position]]` 的少数着色器需要处理补偿逻辑。

替代策略是以"帧缓冲 Y 向下"为内部规范（与 Metal/Vulkan/DX 对齐），则磁盘纹理的 UV 需要全量翻转，工作量更大但 viewport/scissors 代码更简单。选哪个主要取决于项目里"磁盘纹理采样代码"和"render-to-texture 建立代码"谁的数量更多。

## 相关

- [[coordinate-spaces]] —— Clip Space、NDC、Screen Space 的通用定义
- [[mvp-transform]] —— 顶点变换流水线
- [[metal-api-overview]] —— Metal 渲染管线概要
- [[vulkan-explicit-performance]] —— Vulkan 显式控制的整体设计
- [[ben-supnik]]

## Sources

- [[sources/supnik-opengl-coordinate-conventions]]
