---
tags: [渲染, opengl, 驱动, 性能]
date: 2026-04-19
sources: 1
---

# OpenGL 状态切换是延迟生效的

**任何生产级 OpenGL 驱动里，`glBindBuffer` / `glVertexAttribPointer` / `glEnable` 等状态切换的真正工作都不在函数返回时完成——它只是在 context 里记下「脏位」**。真正把硬件寄存器同步过去的工作推迟到**下一次 [[draw-call]]**（`glDrawArrays` / `glDrawElements` 等）。这解释了为什么 profile 总显示状态函数「很快」而 draw 调用「很慢」——CPU 时间实际上是在 draw 开始前由驱动补齐的。

## 为什么驱动必须延迟

因为**单独一次状态函数不够决定最终硬件配置**。以 vertex format 为例：

```c
glBindBuffer(my_buffer);
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, (char*) 0);
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, (char*) 12);
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, (char*) 24);
```

现代 GPU（尤其是 GCN 以后的 AMD）需要**在 vertex shader 前置生成 fetch 代码**（见 [[opengl-hardware-impedance-mismatch]]）。如果驱动在第一次 `glVertexAttribPointer` 就去 patch shader，剩下两个调用进来时之前的工作就作废——而且驱动**根本不知道你什么时候叫停**（没有 `glDoneScrewingAroundWithVertexAttribPointer`）。唯一可靠的同步点是 draw call——这时驱动可以确定「你就是要这个配置」，一次性把所有脏位落到硬件。

## 驱动侧的典型结构

```c
void glBlendFunc(GLenum s, GLenum d) {
    context* c = get_thread_context();
    c->blend.sfactor = s;
    c->blend.dfactor = d;
    c->dirty_bits |= bit_blend_mode;   // 只做记账
}

void glDrawArrays(GLenum m, GLint f, GLsizei n) {
    context* c = get_thread_context();
    if (c->dirty_bits & bit_blend_mode)
        sync_blend_mode_with_hardware(&c->blend);  // 这里才贵
    /* … 其余脏位同步 … */
    c->dirty_bits = 0;
    /* 真正 draw（相对便宜） */
}
```

Apple 的 GL 栈拆成多个 dylib，Instruments 里能看到 `sync_*` 这类子程序名——可以直接看到 draw call 时的状态同步。Windows 的 GL 栈是 monolithic + stripped，看不到 back-trace，同样的热点就很难定位。

## 推论：无意义的冗余状态切换仍会拖慢 draw

```c
for (int i = 0; i < 1000; ++i) {
    glEnable(GL_BLEND);               // 看起来「免费」
    glDrawArrays(GL_TRIANGLES, i*12, 12);
}
```

`glEnable` 每次都让 blend 脏位置位，即便值没变；**下一次 draw 都会重新跑一遍 blend 同步路径**。驱动不会替你去重——它假设「你改了状态就是要改」。因此：

- 不必要的状态切换**即便函数单独看起来 O(0)**，仍然在**拉高每个 draw call 的实际成本**。
- 正确做法：在状态不变时根本不要调，或者用 [[gl-draw-accumulator-batching|累加器]] 在上层合并状态变化。

## 对 profile 的影响

profile 上常见误读：*「glDrawArrays 占 80% CPU，所以要减少 draw」*——对，但不完全对。

真正问题是 **draw 之前累积的脏位太多**。同样是 1000 个 draw call：如果状态稳定，80% 可能掉到 15%；如果每次 draw 前都有 20 次状态切换，不管 draw 本身多小，这 20 次脏位同步都会落在下一次 draw 上。**减少脏位比减少 draw 更直接**。

## 相关
- [[draw-call]]
- [[opengl-hardware-impedance-mismatch]]
- [[gl-draw-accumulator-batching]]
- [[batching]]
- [[opengl-hint-bit-irrelevance]]
- [[mtl-render-pipeline-state]] —— Metal 用 immutable PSO 把这份「延迟同步」明确化

## Sources
- [[sources/supnik-gl-state-deferred]]
