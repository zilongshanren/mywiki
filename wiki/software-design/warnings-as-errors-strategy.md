---
tags: [error-handling, warnings, deprecation, tooling, bitsquid]
date: 2026-04-19
sources: 1
---

# Warning 治理：分类、升级为 error、与 deprecation 的出路

Warning 的本质矛盾：**我们同时希望它 hard-to-ignore 和 easy-to-ignore**——否则要么淹没在噪声里没人看，要么占用大家每次启动时手动忽略的精力。[[niklas-frykholm]] 在 2012 年《Sensible Error Handling》第 3 篇里给出 Bitsquid 的治理方案。

## 先分类再动手

Bitsquid 把 warning 分三类：

- **Performance warning**——做了对性能潜在不利的事。没 mipmap 的纹理、300 MB 塞进内存的音频。
- **Suspicion warning**——"你真的要这么做吗？"。空 glyph 的字体、0 粒子的 particle effect。
- **Deprecation warning**——**这本该是 error**，只因为历史数据太多没来得及强制。两个节点重名、mesh 命名不统一之类。

分类的意义在于每类有不同的出路。

## 治理的主战术：把 warning 升格为 error

error 比 warning 好对付得多——它不是判断题，一出现就必须修，而且不修你根本进不了下一步。Warning 会累积、腐烂、最终变成无人理会的灰色泥潭。所以**能升格就升格**：两节点重名→error；同时受动画和物理驱动→error。 这和 [[zero-tolerance]] 的纪律完全一致。

阻碍升格的只有一个：deprecation——老数据不干净，不能立刻硬报错。Niklas 按「从好到差」给出四档方案。

### 1. 写转换脚本

把老数据按规则机械迁移到新格式。这需要源数据本身是脚本友好的（[[minimal-markup-pipeline|可读文本]]、JSON 之类）。**避免二元思维**——即使脚本只能处理 98%，也把美术的三周工作量压到 2.5 小时，完全值得。

### 2. 脚本 override

当要废弃的是脚本 API（例如 `AudioWorld.set_listener(pos)` 换成 `set_listeners(table)`），最干净的做法是用**新接口在脚本层重新实现旧接口**：

```lua
function AudioWorld.set_listener(pos)
    AudioWorld.set_listeners({pos})
end
```

引擎层彻底移除，gameplay 侧按自己节奏迁移。

### 3. Doomsday clock

没有自动化路径、必须手工改数据时，在 warning 里写死到期日："This warning will become a hard error on the 1st of May, 2012."。前提是制作人支持；否则 deadline 会被一推再推。

### 4. 投降但封住新入口

没时间治理存量，那至少别让增量继续恶化：在源数据里加一个 `bad_name_is_error = true` 的 flag，新工具创建的资源一律打上这个标记并按 error 处理；老数据保持 warning。效果是**止血**。

## 工具里而不是运行时

Warning 最有用的时机是**正在编辑某个对象时**——那时你对这个对象的上下文最清楚，修改成本最低。因此 warning 应该长在编辑器里，而不是等游戏跑起来才飘到 console。每个编辑器挂一个 warning 图标显示当前对象的 warning 数；保存前甚至可以要求用户逐条「我真的要这样」打勾。运行时 warning 只作第二道防线。

## Review 工具

另一个有价值的时机是项目 review——性能 review 就看所有 performance warning，按类别排序（`>2000 粒子`、`贴在地下的 unit`）。Review 工具允许制作人把「确实 OK」的 warning 打勾屏蔽——实现可以粗糙到「hash(对象名 + 消息)」然后记忆表。一个更激进的 idea：**新 warning 默认就是 error，除非被显式 silenced**——这样老问题被 grandfather，但新问题无法混入。

## 另一条心法：让工具不产生 warning

Warning 统计其实揭露了一件事——用户一直在做你没预期到的事。[[niklas-frykholm]] 说：每出现一类 warning，都应该反思能不能改工具让用户表达 intent 更容易。比如大量粒子 overdraw 警告→在 particle editor 里加实时 overdraw 可视化。把"指责用户"翻译成"升级工具"。这也是 [[intent-vs-state|intent vs state]] 的一种体现。

## 相关

- [[crash-on-unexpected-errors]]
- [[minimize-points-and-types-of-failure]]
- [[zero-tolerance]]
- [[intent-vs-state]]
- [[dependency-checker-tool]]

## Sources

- [[sources/bitsquid-sensible-error-handling-part-3]]
