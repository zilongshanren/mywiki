---
tags: [strategy-pattern, switch-statement, refactoring, 代码坏味道, 可扩展性]
date: 2026-04-14
sources: 1
---

# Strategy 对决 Switch

有一种非常常见的代码结构：一个类根据某个"类型码"分支到不同行为。用 `switch` 实现最直接，但 Martin Fowler 在《Refactoring》里把它列为经典的**代码坏味道（code smell）**，并提出对应的重构手法 "Replace Type Code with State / Strategy"。[[allen-chou|Allen Chou]] 写 Bunnyhill 2D 渲染引擎的 blend mode 时亲自做过一次这种重构，留下了一个小而完整的对照案例。

## Switch 版本

最初的做法是：用一组字符串常量表示 blend mode，`RenderEngine.setBlendMode(value)` 里面一个 `switch` 展开三种情况：

```
class BlendMode {
    static const ADD = "add";
    static const ALPHA = "alpha";
    static const NORMAL = "normal";
}

class RenderEngine {
    setBlendMode(value: String) {
        switch (value) {
            case BlendMode.ADD:    /* 配置 add */   break;
            case BlendMode.ALPHA:  /* 配置 alpha */ break;
            case BlendMode.NORMAL: /* 配置 normal */break;
        }
    }
}
```

看起来挺清楚。但一旦要加第四种 blend mode，你必须**同时改两个地方**：`BlendMode` 里加新常量、`RenderEngine` 里加新 `case`。这正是 [[change-amplification|Change Amplification]]——一个逻辑变更被放大成多处物理改动。

## Strategy 版本

重构的做法是把每一种 blend mode 变成实现同一个接口的**策略对象**：

```
interface IBlendMode {
    setupBlendMode(engine: IRenderEngine): void;
}

class BlendMode {
    static const ADD    = new Add();
    static const ALPHA  = new Alpha();
    static const NORMAL = new Normal();
}

class RenderEngine {
    setBlendMode(value: IBlendMode) {
        value.setupBlendMode(this);
    }
}
```

对调用方来说写法完全相同（`renderEngine.blendMode = BlendMode.ADD`），但扩展代价变了：**新增一种 blend mode 只需要写一个新类**，`RenderEngine` 和既有策略对象一行都不用动。这是 [[modular-design|模块化设计]]想要的结果——每个"新功能"被局限在一个独立单元里。

## 什么时候不该这么做

Chou 在评论区被读者追问"是不是 strategy 总比 switch 好"，他的回答很务实：

> 永远有 trade-off。Strategy 未必比 switch 跑得快。如果这段代码不是性能瓶颈（run once vs 每帧 10000 次的区别），而 strategy 能让代码更干净，那就用。

也就是说，选择取决于两个问题：

1. **这段分支是否真的会扩展？** 如果永远只有那么几种、而且未来不会加——例如平台标记或协议版本号——`switch` 可能更直观，不值得引入一个类层级。
2. **是否在热路径上？** 虚函数调用、对象分配、缓存命中都会有额外成本；极端的紧内层循环里 `switch`（编译器经常能展开成跳转表）往往更快。[[cpp-multi-paradigm-discipline|C++ 多范式纪律]]里提过类似取舍——"抽象要为运行时成本买单"。

换句话说，Strategy 模式解决的是**代码演化**问题，而不是性能问题。它是写给"未来要加第 N 种 case 的那个人"看的，不是为了让 CPU 更开心。

## 相关

- [[change-amplification]]
- [[modular-design]]
- [[dependencies]]
- [[cpp-multi-paradigm-discipline]]
- [[composite-command-pattern]] —— 同样把分支展开为对象层级的另一种模式
- [[allen-chou]]

## Sources

- [[sources/allenchou-switch-vs-strategy]]
