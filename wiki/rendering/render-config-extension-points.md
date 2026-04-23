---
tags: [渲染, 引擎架构, 数据驱动, 插件, stingray, bitsquid, plugin-system]
date: 2026-04-19
sources: 1
---

# Render Config Extension Points（Stingray 1.5）

[[stingray-data-driven-render-config|Stingray 的 render pipeline 是一份 JSON config]]。2016 年 Stingray 1.5 出现一个新问题：**越来越多的 plugin（还有为非游戏行业定制的功能）需要把自己的 pass / resource 塞进主 pipeline**，但 Stingray 不想让每个 plugin 都去**整份 diff 或 fork 主 `render_config`**。Tobias Persson 的答案是 `render_config_extension`——一个带**命名注入点**的"渲染配置补丁系统"。

## 问题：不能整份复制

Plugin（比如 [[stingray-volumetric-clouds-plugin|Jp 的体积云 plugin]]）如果 fork 整份 `renderer.render_config` 就失去了跟随主 pipeline 升级的能力；如果要求用户手改主 config 就把 plugin 安装变成"每次都要跟主 pipeline 做三方合并"。**plugin 需要一个局部、声明式、可版本化的扩展接口**。

## `render_config_extension` 的结构

每个扩展文件有两个顶层 block：

### `append`：顺序无关的补充

```
append = {
  shader_libraries = [ "clouds-resources/clouds" ]
  render_settings  = { clouds_enabled = true  ... }
  global_resources = [ { name="clouds_result_texture1" ... } ]
  resource_generators = { ... }
  viewports = { ... }
  lookup_tables = [ ... ]
}
```

可以追加的主 config 根 block：
- `shader_libraries` — 挂新 shader 源文件。
- `render_settings` — 加品质档 / debug flag。
- `shader_pass_flags` — 给 shader system 开更多 pass 开关。
- `global_resources` — 声明 plugin 私有 GPU buffer（如云的三张 3D texture）。
- `resource_generators` / `viewports` / `lookup_tables` — 加 generator / viewport 模板 / 启动期执行的生成器。

**当前（1.5）没有命名冲突检查**——文档直接建议"用 plugin 前缀当 namespace"，这是一个**有意接受的工程债**。

### `insert_at`：精准插到命名 hook

```
insert_at = {
  post_processing_development = {
    modifiers = [
      { type="dynamic_branch" render_settings={ clouds_weather_data_visualization=true }
        pass = [ { type="fullscreen_pass" shader="debug_weather" ... } ]
      }
    ]
  }
  skydome = {
    layers = [
      { resource_generator="clouds_modifier" profiling_scope="clouds" }
    ]
  }
}
```

`insert_at` 的对象名必须对应主 `render_config`（或本 extension 之前已加载的另一个 extension）里**显式列出的 `extension_insertion_points`**。Tobias 的原话：

> "We've chosen not to allow extensions to inject anywhere they like (using line numbers or similar crazyness), instead we expose a bunch of extension hooks."

这就是这套系统的设计哲学——**主 pipeline 作者显式声明在哪里可以被扩展**，而不是让 extension 用 patch / sed / JSON-path 撞大运。这样重构主 pipeline 只要保住命名 hook 就不破坏 plugin 兼容性。

## 加载顺序由 boot ini 决定

```
render_config = "core/stingray_renderer/renderer"
render_config_extensions = ["clouds-resources/clouds", "prism/prism"]
```

数组顺序就是 extension 之间的依赖顺序——后面的 extension 能 `insert_at` 前面 extension 已加的 hook。这样 plugin 生态可以分层（比如一个基础大气 plugin + 一个依赖它的云 plugin）。

## 未决的工程债

作者自己列出来当时没做的东西：
- **版本号** — extension 应该能声明兼容的 Stingray 版本范围、甚至按版本走不同实现；
- **强制 namespace** — 现在 plugin 名冲突只能约定成俗；
- **更激进的 validation** — 提前发现 name collision / hook 不存在。

但 1.5 选择了"先发出去，解封 plugin 作者，再回头填"——和 [[engine-plugin-c-abi-versioned-api|Bitsquid 的 C-ABI plugin 系统]] 一致的工程节奏（**别为还没遇到的问题提前设计**）。

## 为什么这是"正确的"数据驱动扩展方式

对比三种 render pipeline 扩展策略：
1. **Fork 主 config** — 断更新；
2. **全局 patch / JSON merge** — 脆弱，主 config 一改 plugin 就废；
3. **命名插入点 + 追加补丁** — Stingray 选的这条。主 pipeline 作者对"哪里可扩展"负契约责任，plugin 作者对"扩展什么"负契约责任——**两边的契约都通过配置文件表达**，没有 C++ 代码耦合。

这跟 UE 的 material function override、Unity SRP 的 CustomRenderPass 在哲学上是同一个族谱，只是 Stingray 把一切都推到 config 层而不是 C# / C++ 类层次。

## 相关

- [[stingray-data-driven-render-config]]
- [[engine-plugin-c-abi-versioned-api]]
- [[stingray-volumetric-clouds-plugin]]
- [[data-driven-architecture]]
- [[tobias-persson]]
- [[niklas-frykholm]]

## Sources
- [[sources/bitsquid-render-config-extensions]]
- [[sources/bitsquid-renderer-walkthrough-7-data-driven]]
- [[sources/bitsquid-renderer-walkthrough-8-default-pipes]]
