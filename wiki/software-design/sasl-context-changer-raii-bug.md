---
tags: [raii, cpp, 调试, openal, 临时对象]
date: 2026-04-19
sources: 1
---

# SASL 的 ContextChanger：一条 RAII 命名陷阱与 OpenAL 崩溃

X-Plane 用户在升级 macOS El Capitan 后遇到一条奇怪的崩溃：只要用户从 SASL 插件驱动的飞机切换到 X-Plane 自带飞机就 abort。[[ben-supnik|Supnik]] 不得不自己复盘，调查不属于他代码的 bug——顺带给出一条值得每个 C++ 开发者警惕的临时对象命名陷阱。

## 两条独立的 bug 叠加

崩溃是 **Apple OpenAL + SASL** 各一条 bug 的合成：

### Apple OpenAL 侧

`alcDestroyContext` 对"**仍有播放声源 + 是 device 的唯一 context + 未使用 effect**"的 context 会从析构里抛出 `AudioUnits` 错误码。在 C++98 行为下外层 catch 住、转成 ALC 错误码返回——对应用无感。El Capitan 升级 Xcode 工具链 → C++11 隐式 `noexcept` 析构 → 抛出即 [[throwing-destructor-noexcept-terminate|std::terminate]]。

Supnik 的判断是公平的：OpenAL 规范本身是**灾难级**的写法，"删除正在播放声源的 context 是否合法"这种角落里连规范都没说清楚；没有任何清醒 app 会跳过 stop-sound 直接 destroy context——所以这个 bug 在规范外的边缘行为上，长期没触发。

### SASL 侧：RAII 的临时对象命名陷阱

SASL 想用经典 RAII 在切换 OpenAL context：

```cpp
// 正确写法
ContextChanger changer(sound->context);
// 作用域末尾析构恢复 old context
```

实际 SASL 的 cleanup 代码写的是：

```cpp
// 永远不工作
ContextChanger(sound->context);
```

后者是**完全合法的 C++**：它构造一个匿名临时对象、立刻在语句结束析构，相当于瞬间 make + immediately revert——等同于什么都没做。Supnik 承认自己也写过这种 bug。

后果：cleanup 阶段 SASL **没有切到自己的 context**，于是按自己 context 的源名字列表去 X-Plane 的 context 里删声源——大概率失败并被 OpenAL 记下 `AL_INVALID_NAME`，或删掉了 X-Plane 的无辜声源（"not cool man, not cool!"）；然后它 destroy 自己的 context，而自己的声源因为 cleanup 没真跑还在响——正好踩进 Apple 的 bug 触发条件。

## 为什么这次 bug 六年没被发现

Supnik 愤怒的点不是匿名临时——任何人都可能写错；而是**它一次都没工作过**，却过了六年没被抓出来。原因有两条：

1. `ContextChanger(ctx)` 构造时做了 `alGetError()` **不检查直接丢弃**——相当于主动抹掉 OpenAL 的错误累积。后续 cleanup 调用即便全部返回 `AL_INVALID_NAME`，SASL 也不会看到。
2. cleanup 代码的行为不是用户可见的——没人能观察到"X-Plane 的声源被错删了"，因为 X-Plane 接着重载 plane 时这些声源无论如何都会被重建。

这是一条经典的 [[good-software-no-double-check|自检盲区]]：静默丢弃错误码 + 不直接用户可见 = 永远不会自然爆出来，直到平台把"刚好够宽容"的边界再收紧一点。

## 三条教训

Supnik 在帖尾总结的设计原则，相当于 [[performance-by-design|performance by design]] 的质量对偶：

1. **返回码是 debug 时的断言来源**：OpenAL / OpenGL 的 `glGetError` / `alGetError` 不是异常通道，而是"程序员写错了"的自检信号。debug build 里该把它们转成 assert。
2. **不能靠用户眼睛验证**：行为对就不代表正确。没人看着正常 → 没 bug，这不成立。
3. **非用户可见的代码（所有 cleanup / 资源回收）必须带可调试性设计**：log、assert、test、debugger attach——这些不是"有空加"，是功能需求的一部分。

这一条"21 年前那位资深工程师教我的事"，和 [[future-proofing-tests]]、[[good-software-no-double-check]] 是同一棵树的不同枝。

## 相关
- [[throwing-destructor-noexcept-terminate]] —— Apple 侧 bug 的语言机制根因
- [[cross-platform-openal-runtime-loader]]
- [[good-software-no-double-check]]
- [[crash-on-unexpected-errors]] —— Boris 的「真错误要立刻爆」原则
- [[minimize-points-and-types-of-failure]]
- [[performance-by-design]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-sasl-crash-el-capitan]]
