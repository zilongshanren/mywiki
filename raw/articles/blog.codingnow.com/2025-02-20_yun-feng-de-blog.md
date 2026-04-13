---
title: 云风的 BLOG
url: https://blog.codingnow.com/2025/02/
published: '2025-02-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 2D 渲染管线的一点优化

考虑到我想做的独立游戏并不需要以画面效果吸引人，游戏是策略向的，所以 2D 表现就足够了。之前几年做的 3d 引擎对这个需求来说太复杂了，而且这次我也不打算主打移动平台，之前为移动平台做的考虑也没太大意义。所以，最近想花个把月重新搭一个 2d 游戏用的框架。当然，最重要的是：我太久没写代码了，而做这个非常有趣。

前天在 github 上开了一个新坑，[具体想法写在项目的讨论区了](https://github.com/cloudwu/soluna/discussions/1)。

虽说 2d 游戏在如今的硬件上，性能那是相当富裕。但在具体写代码时，还是忍不住想想怎么设计，性能会比较好。不然总是重复大家都有的东西也是无趣。

在现代 GPU 上实现一个最简单的 2d 管线，就是把它当成 3d 网格，一堆顶点数据填进去，绑定贴图，提交渲染即可。所谓 2d 图片，就是两个三角形，看成是 3d 世界里的一个面片即可。

所以，每个顶点的数据就是 vec2 pos ，要画一个矩形需要四个顶点，用 vertex buffer 传进去。

但是和 3d 游戏不同，2d 图片形状大多不规整，不是边长为 2 的幂的正方形，尺寸也不大。如果每张小图片（2d 游戏中通常称为 sprite）都构造一张贴图的话，会非常低效。通常我们会把很多 sprite 打包在同一张大的正方形的贴图上。这样，顶点数据中还需要定义绘制矩形对应在贴图上的区域，通常称之为 uv 坐标。至此，常规的实现方法中，每个顶点就是 4 个数据量：vec2 pos 和 vec2 uv 。因为 sprite 都在同一张贴图上，一次图形指令提交只画一个矩形就太浪费了，我们会把多个矩形的顶点放在一起，一次把整个顶点数组提交到 vertex buffer 中。

虽然 2d 游戏的大多数 sprite 只需要指定屏幕（画布）坐标渲染即可，画布可以整体缩放。sprite 单独缩放旋转的机会比较少，但也并非没有。用上面的方法怎么处理旋转和缩放呢？过去常见的方法是在 CPU 中计算好四个顶点，把结果填在顶点数据流中。btw, 很早以前，我在实现 ejoy2d 的初版时就是这么做的。这样最为灵活，CPU 计算一个 2x3 的矩阵也不慢（ejoy2d 使用了定点数，在早期的手机上性能更好）。而且，大多数 sprite 并不需要旋转和缩放，只需要做一次 vec2 的加法即可。

计算该怎么做？我们需要找到 sprite 的基准点。大多数情况下，这个基准点并不是图片的左上角。然后以这个点为坐标原点，对 sprite 的四个顶点依次做旋转和缩放变换再加上 sprite 的绘制位置。这一系列运算相当于乘一个 2x3 的矩阵。如果我们想把这个运算放在 GPU 该怎么做？顶点数据流中就不能直接放顶点计算结果的坐标了，而应该放针对 sprite 的基准点的相对坐标，以及一个 2x3 的变换矩阵。这样，顶点数据就变成了：vec2 offset ; vec2 uv ; mat2 sr; vec2 t; 一共是 10 个数据。

很明显，后面这个 mat2 sr; vec2 t; 在数据流中重复了 4 次（一个 sprite 的 4 个顶点有相同的 2x3 矩阵）。另一方面，绝大多数的 sprite 不需要旋转和缩放变换，这种情况下，mat2 sr 都是单位矩阵；即使有旋转变换，旋转角度也是有限的。整个数据流中必然存在大量重复的 mat2 sr 。怎么优化掉这些重复数据呢？我们可以用一个 storage buffer 保存唯一的 mat2 sr ，在顶点流中保存一个索引 index 即可。这样，顶点数据就剩下 vec2 offset; vec2 uv; index; vec2 t; 7 个数据。最后这个 vec2 t 不放在索引中是因为大多数 sprite 会有不同的位移坐标，而 2x2 的 SR 矩阵更容易合并。

接下来的问题是，index 和 vec2 t 还是重复了 4 次。为了去掉这个重复，我们可以采用 instance draw 或 indirect draw 。理论上用 indirect draw 更合适，但它对图形 api 版本要求高一些（如果想运行在 web 上，还是需要考虑这点），所以我选择用 instance draw 实现。

使用 instance draw 的一个额外好处是可以省掉 index buffer ，使用三角条带描述矩形即可。

但 instance draw 有个问题：它最初是为了把一组顶点数据重复渲染设计的。而这里，我们有很多不同的矩形需要同一批次渲染。即，vb 中每组数据 vec2 offset; vec2 uv; 有很多组。所以，我选择不使用顶点数据流，把这组数据放在另一格 storage buffer 中，然后在顶点着色器（vs）中通过 `gl_InstanceIndex`

和 `gl_VertexIndex`

索引它。

做到这里，我注意到：2d 游戏中的 sprite 矩形都是轴对齐的。所以，描述四个顶点并不需要 8 个量，而只需要 4 个，保存两个对角顶点即可。另外，offset 矩形和贴图上的 uv 矩形形状也是一致的，我们只是把贴图上的一个区域完整映射到画布上，这样还可以少两个重复信息。最终，我们只需要 3 对 vec2 就可以表达一个矩形以及 uv 。

而图片是以像素为单位的，贴图尺寸不会有几万像素大。这个坐标量使用 int16 足够了。所以在保存 sprite 元信息的这个 storage buffer 中，每个图元其实只需要 6 个 int16 ，也就是 12 字节足够了。最终，绘制每个 sprite 的数据为 6 short + 3 float ( x,y,index ) = 26 字节。

layout(binding=0) uniform vs_params { vec2 texsize; vec2 framesize; }; struct sr_mat { mat2 m; }; layout(binding=0) readonly buffer sr_lut { sr_mat sr[]; }; struct sprite { uint offset; uint u; uint v; }; layout(binding=1) readonly buffer sprite_buffer { sprite spr[]; }; in vec3 position; out vec2 uv; void main() { sprite s = spr[gl_InstanceIndex]; ivec2 u2 = ivec2(s.u >> 16 , s.u & 0xffff); ivec2 v2 = ivec2(s.v >> 16 , s.v & 0xffff); ivec2 off = ivec2(s.offset >> 16 , s.offset & 0xffff) - 0x8000; uv = vec2(u2[gl_VertexIndex % 2] , v2[gl_VertexIndex >> 1]); vec2 pos = uv - ( off + ivec2(u2[0], v2[0])); pos = (pos * sr[int(position.z)].m + position.xy) * framesize; gl_Position = vec4(pos.x - 1.0f, pos.y + 1.0f, 0, 1); uv = uv * texsize; }

再来看 CPU 侧的设计：

我这次使用了 sokol 做底层图形 api 。sokol api 不支持多线程，所有图形指令必须在同一个线程提交。所以我做了一个简单的中间层：绘图时不直接调用图形 api ，而是填充一个内存结构。这个结构被称为 batch ，不同的线程可以持有多个不同的 batch 。所有 batch 汇总到渲染线程后，渲染线程再将 batch 中的数据转换为图形指令以及所需的数据结构。

因为 2d 游戏据大多数情况都在处理图片，使用默认的渲染方式。我对这种默认材质做了特别优化。batch 是由这样的结构数组构成：

struct draw_primitive { int32_t x; // sign bit + 23 bits + 8 bits fix number int32_t y; uint32_t sr; // 20 bits scale + 12 bits rot int32_t sprite; // negative : material id };

其中，用两个顶点 32bit 整数表示 sprite 的画布坐标；一个 32bit 整数表示旋转和缩放量；一个 sprite id 。

渲染层会查表把 sprite id 翻译成对应的元信息（上面提到的 offset 和 uv ），当 sprite id 为负数时，表示这是一个非默认材质，batch 中的下一组数据是该材质的参数。例如，文本渲染就会用到额外材质，文本的 unicode 和颜色信息就放在接下来的数据中。