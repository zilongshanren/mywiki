---
tags: [渲染, 资源系统, 本地化, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 资源覆盖与后缀规则（替代旧 property 系统）

Niklas Frykholm 2016 年给 Stingray 重写本地化/平台变体系统时放弃了"文件名点号分段 = property"的旧设计，换成一套**resource override + suffix 规则**组合。这是一次用"更数据驱动 + 更动态"去替代"魔法文件名"的教科书式重构。

## 旧 property 系统为什么不够用

旧方案里，`trees/larch_03.fr.unit`、`trees/larch_03.ps4.unit` 通过文件名中的 `.fr`、`.ps4` 分段指代语言/平台变体，`.ps4` 类 platform property 编译期解析，`.fr` 类 runtime property 由脚本设定的 preference order 在加载时解析。实际使用堆积出来的问题：

- **文件名不能带点**——DCC 与外部工具常生成带 `.` 的文件名，手工改名常常破坏交叉引用。
- **切换语言必须重新加载包**——现代硬件内存宽裕，字符串按语言全量驻留才是常识。
- **只分平台太粗**——移动端同一个 `android` 有低端到中端的大跨度，真正该区分的是 `low-quality`/`high-quality`。
- **编辑器对 property 极其不友好**——Windows 上编辑 `.ps4` 变体、或显示 `.win32` 默认版的歧义都很难讲清楚。

## 新机制：override 为核、suffix 为糖

**第一层：资源替换由引擎显式知道**。对文本这种天然本地化的资源，`.strings` 直接变多语种 map，`Localizer.set_language("fr")` 即时切换、全语言常驻内存。

**第二层：通用资源走 override**。去掉文件名魔法，任何资源替换都可以在运行时注册：

```lua
Application.set_resource_override("unit", "trees/larch_03", "trees/larch_03_ps4")
```

引擎在加载 `trees/larch_03.unit` 时会替换成 `trees/larch_03_ps4.unit`。override 可以基于运行时信号（实测 CPU/GPU 性能、玩家血腥度设置）动态改写，甚至能被"滥用"做夜景/致幻版关卡切换。

**第三层：包管理器必须静态可见**。动态 override 有个致命问题——packaging 系统自动走依赖图时看不见运行时替换，会把 `_ps4` 变体漏打或把 iOS 版塞进不相关的大资源。Niklas 补了一层**静态 override 表**：

```
resource_overrides = [
    { suffix = "_ps4", platforms = ["ps4"] }
    { suffix = "_fr",  flags = ["fr"] }
    { suffix = "_4k",  flags = ["4K"] }
    { suffix = "_noblood", flags = ["noblood", "PG-13"] }
]
```

任何满足"同名 + 该后缀"的资源会被 packaging 系统识别为 override 候选。flag 可在编译期通过 `--resource-flag-true 4K` 静态解析（只打进 4K 变体），或通过 `--resource-flag-runtime noblood` 注入 runtime 选择（两份都打进包，`Application.set_resource_flag("noblood", true)` 热切换）。

## 设计取舍

- **override 不保证语义一致**。脚本可能查找 `larch_03.unit` 上的节点 `branch_43`，而 `larch_03_ps4.unit` 里没有。引擎不管这种脚本级错误——只有游戏代码自己知道两个资源是不是"够像"。这一点与旧 property 系统一样。
- **override 的解析时机目前只有两档**（编译期 / 运行时）。Niklas 在原文讨论了是否再加一档 "package load time"（两份打进磁盘、只加载一份、切换需重载包），最终为了保持简单而搁置——典型的 KISS 立场。
- **可向后兼容**。把 suffix 设成 `.fr`/`.ps4` 就能把旧 property 规则"转译"进新机制，旧项目不用改文件名。

## 与其他 Stingray 机制的联系

- [[stingray-data-driven-render-config]] —— 同一思路在 render pipeline 层的体现：把"硬编码分支"换成"数据驱动表"。
- [[stingray-package-manager]] —— Stingray 的 build/packaging 工具链是 override 静态部分的实际消费者。
- [[asset-exchange-format-strategy]] —— 资源系统对外接口的另一个维度。

Niklas 自己承认："对 name matching 驱动系统这件事我还是略有不适——name matching 是一种最容易走偏的实践"，但因为匹配规则完全由用户显式控制（不是引擎偷偷约定），这个折中在可用性和纯净性之间找到了合理的平衡点。

## Sources

- [[sources/bitsquid-stingray-localization-system]]
