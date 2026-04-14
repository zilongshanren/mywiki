---
tags: [渲染, shader, shadertoy, gamemaker, glsl]
date: 2026-04-14
sources: 1
---

# ShaderToy 格式与移植到游戏引擎

[ShaderToy](https://www.shadertoy.com) 是 shader 社区事实上的标准游乐场——单一 fragment shader、预定义 uniform、即时编译，极其方便分享 demo。但 ShaderToy 的设计初衷是**浏览器里的 GLSL 演示**，它做了不少偷懒的假设：没有 vertex shader、所有纹理都是 standalone、alpha 不参与合成、可以自由用 WebGL 2 的新特性。把一段好看的 ShaderToy shader 搬进真实游戏引擎（GameMaker、Unity、Unreal、or custom），这些假设就会一个个露馅。[[xor-shader-artist|Xor]] 以 GameMaker 的视角整理了一份完整的移植清单——对任何做 2D/混合渲染的引擎都有参考价值。

## ShaderToy 的隐式约定

一段 ShaderToy shader 的「最小可运行单元」长这样：

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    fragColor = vec4(uv, 0.5 + 0.5*sin(iTime), 1.0);
}
```

它暗含：

- **没有 vertex shader**。ShaderToy 在内部渲染一个全屏 quad，fragment 里通过 `fragCoord`（像素坐标）和 `iResolution` 自己计算 NDC。对应的引擎里通常已经有了插值好的 `v_vTexcoord`。
- **入口函数叫 `mainImage`**，参数 `fragColor`（out）、`fragCoord`（in）——引擎的入口是 `main()`，输出写 `gl_FragColor`，像素坐标在 `gl_FragCoord.xy`。
- **uniform 以 `i*` 前缀命名**：`iResolution`（注意是 vec3，z 恒为 1）、`iTime`、`iTimeDelta`、`iMouse`、`iFrame`、`iChannel0..3`、`iChannelResolution[]`。
- **alpha 不参与合成**——ShaderToy 是 "paint fullscreen"，alpha 写不写都显示出颜色；但在引擎里如果开了 alpha blending，随手写 `fragColor.a = 0.5` 就会半透明。

## 移植的五个必改点

Xor 给的清单可以浓缩成五步：

1. **加 varying**：在 fragment shader 顶部加 `varying vec2 v_vTexcoord; varying vec4 v_vColour;`（如果引擎用这套命名）。
2. **改入口签名**：`void mainImage(out vec4 fragColor, in vec2 fragCoord)` → `void main()`，函数体里把 `fragColor` 全部替换为 `gl_FragColor`、`fragCoord` 替换为 `gl_FragCoord.xy`。
3. **显式设置 alpha**：很多 ShaderToy shader 让 `fragColor.a` 是未定义状态；引擎里要么 `gl_FragColor.a = 1.0`，要么根据游戏需要做出刻意选择。
4. **绑定 uniform**：每个 `i*` 都要在 CPU 侧有对应的 `shader_set_uniform_f`（或 `material.SetFloat` 等）。常用的映射表：
   - `iResolution` → `vec3(width, height, 1.0)`
   - `iTime` → `get_timer() / 1e6`（GM）/ `Time.time`（Unity）
   - `iTimeDelta` → `delta_time / 1e6` / `Time.deltaTime`
   - `iMouse` → `vec4(mouseX, mouseY, lastClickX, lastClickY)`；后两位带符号表示按压状态
   - `iFrame` → 自增计数器
   - `iChannelN` → sampler uniform；**每张贴图必须独占 texture page**（否则 UV 0–1 范围失效，见 [[two-texture-sampling-tricks]]）
5. **修 WebGL 2 → WebGL 1 / ES 3 → ES 2**：ShaderToy 已经默认 WebGL 2，而很多 2D 引擎（特别是 GameMaker）停在 ES 2 / WebGL 1 的兼容子集。常见修正：
   - `texture()` → `texture2D()`
   - 不支持位运算（`& | ^ << >>`）、`switch`、动态数组、非方矩阵
   - `round(x)` 不存在 → `floor(x + 0.5)`

## 多 buffer 的坑：float texture

ShaderToy 允许多 tab：`Buffer A/B/C/D` 各是一个独立的 pass，上一个 pass 的输出作为下一个 pass 的输入。`Common` tab 是共享代码。**每个 buffer 的中间纹理是 float**，意味着 `fragColor` 可以写 `vec4(2.0, -0.3, 1e4, 5)` 这种超出 0–1 的值（常见于 motion accumulators、HDR luminance、velocity fields）。

把这种 shader 搬到普通引擎时：

- **每个 buffer 对应一个 render target**——GM 里就是 surface，Unity 里是 RenderTexture。
- **中间纹理默认 8-bit unorm**——写进去的 `-0.3` 直接变 0、`1e4` 被 clamp 到 1。Xor 的警告直白：**先让 ShaderToy 里的 buffer 输出都落在 0–1 内，再移植**。Unity 里可以用 `RGBAFloat`/`RGBAHalf` 的 RenderTexture 绕开，GM 早期版本没有这选项。
- **`Common` tab 拷贝到每个 buffer shader 顶部**——没有 include 机制。

这个「中间纹理精度」问题是 ShaderToy 模拟退火、粒子、fluid simulation 类 demo 最常见的移植失败点，比 syntax 错误更难排查——因为它**编译通过、只是结果错**。

## 和 GM 的兼容性边界

Xor 专门点出 GameMaker 不支持：

- 位运算 —— 某些 hash 函数（[[pcg3d-hash]]、[[non-cryptographic-hash]]）会依赖这个，得改写成浮点版本或 floor/mod 实现
- `switch` —— 改成 if-else 链
- 动态数组 —— 必须编译期固定大小
- 非方矩阵（`mat2x4` 等）—— 改用 `vec4` 数组 + 手写乘法
- 3D 纹理 —— GM 只支持 2D sampler，`iChannelN` 是 3D 的 shader 得用 2D atlas 替代

对 Unity、Unreal 来说，大部分这些限制已经不存在（GLSL → HLSL 自动转换处理了其中一些），但 ShaderToy → HLSL 的 syntax 层面仍然有 `texture2D`、`vec2`、`mat2(...)` 构造函数等一堆替换。

## 许可与归属

Xor 在文末反复强调：**每段 ShaderToy 代码都有作者**。默认是 CC-BY-NC-SA 3.0，商业项目里随手用会踩坑。最佳实践：

- 保留原作者署名（注释里）
- 如果有明确 license header，**完整保留**
- 商业使用先联系原作者

这不只是法律问题也是社区问题——ShaderToy 生态的繁荣依赖于作者们愿意公开分享，尊重归属是让这个循环延续的基本纪律。

## 和其它 shader 起点的对比

- **ShaderToy** —— 浏览器、单 fragment、零 boilerplate，适合学算法和发 demo，**不适合**做产品。
- **Shader Graph / ASE** —— 节点化，有 PBR 前置，适合美术向，但复杂数学和循环不便写。
- **Custom HLSL / GLSL in-engine** —— 有完整 pipeline，是学完 ShaderToy 之后的下一步。

本页讲的其实就是**第一跳**：把你在 ShaderToy 上学到的东西接进真实引擎。

## 相关

- [[two-texture-sampling-tricks]] —— texture page 约束和 UV 归一化，是移植的前置条件
- [[fragment-shader]]
- [[shaderlab-hlsl-basics]]
- [[shader-code-golfing]] —— ShaderToy 风格的数学恒等式技巧
- [[ping-pong-surfaces]] —— 多 buffer / render target 的 GM 版本
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-shadertoy]]
