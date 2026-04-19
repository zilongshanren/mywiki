---
tags: [rendering, shader, pipeline, post-processing]
date: 2026-04-19
sources: 1
---

# 合并 Shader vs. 多趟 Pass 的取舍

Xor 在 Combining Shaders 里给出一张判断表：什么时候把两个后处理 shader 塞进同一个 fragment shader，什么时候该老老实实走两遍 pass？这和 [[ping-pong-surfaces]] 的 multi-pass 讨论是一枚硬币的两面。

## 什么时候合并

按优先级 Xor 列了 5 个 checkpoint：

1. **Performance**：两者都昂贵 → 合并后通常不可行。单贵 + 单便宜可以考虑。
2. **Sample Count**：这是最容易踩坑的地方。8 tap outline + 32 tap blur，**朴素合并会变成 8×32=256 次采样**。采样数会相乘，不是相加。
3. **Coordinates**：是不是一个工作在 screen-space、另一个在 texel 或 world-space？转换可行但会引入杂乱代码。
4. **Textures**：纹理过滤方式（linear vs nearest）、边界行为（clamp / repeat / discard）、blend mode、alpha test——必须统一。
5. **Uniforms**：uniform 数量有硬上限，而且 attribute / varying 接口得对齐；好的一面是常能**复用** `resolution`、`time` 这些。

## 怎么合并

机械流程：

1. 每个 shader 改写成 `vec4 f(vec2 uv)` 之类的**函数**，把原本 `main` 做的事封进去。
2. uniform / macro 不用传参，它们在文件作用域内可见。
3. 把函数互相**嵌套**，让**内层函数先执行**。

```glsl
// grayscale -> chromatic aberration
vec4 col = chromatic_using(saturation);
```

顺序关键：**在 for-loop 里调用的那一层会被执行 N 次**。所以 Xor 的经验法则是 **「把采样多的放外层，把单采样的放内层」**，避免把昂贵代码塞进内循环。例子里，chromatic aberration 有 20 次循环采样，desaturation 只要 1 次——合并时**把 desaturation 的采样嵌进 chromatic 的 for-loop 内部**，每次循环就吃一次 desaturation，但这是故意的（要先去色再做 CA）；如果顺序相反，就要把 chromatic 嵌到 saturation 里，从而只做一次 CA。

## 和 Multi-pass 的对比

- Multi-pass 的优势：可分离核（比如 9×9 Gaussian → 9×1 + 1×9，见 [[separable-gaussian-blur]]）、mipmap 链、ping-pong。
- Multi-pass 的代价：额外 surface、draw call、显存、管线复杂度。
- 合并的优势：省 draw call 和中间纹理；劣势：采样数乘法爆炸、uniform 和坐标空间要对齐。

决策不玄学——过一遍上面那 5 项，如果都没翻车就合并，否则保持 multi-pass。

## Sources

- [[sources/xor-mini-combining-shaders]]
