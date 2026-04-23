---
tags: [游戏引擎, plugin, c-abi, api-versioning, bitsquid, dll]
date: 2026-04-19
sources: 1
---

# 引擎 Plugin 系统的 C-ABI 版本化 API

[[niklas-frykholm|Niklas]] 2014 年 4 月给 Bitsquid 设计 plugin 系统时，总结出一条容易被忽视的观察：**plugin 架构其实同时要设计两套 API**，而绝大多数失败的 plugin 系统都只想着其中一套。

## 两个 API，不是一个

**Plugin-exposed API**：plugin 暴露给引擎调用的入口，通常是 `init/update/shutdown` 这种定时被调的回调。这套简单，真正难的是第二套。

**Engine-exposed API**：引擎暴露给 plugin 调用的服务面——生成 unit、播声音、渲 mesh……plugin 要做事，就得能回调引擎。这一套的难点是**耦合管理**：plugin 需要多少引擎能力、API 面就扩多大；API 面扩大一次、plugin ABI 破一次。

Niklas 列了两条常见但不理想的做法：

- **共享 DLL**：把公共接口放进一个 DLL，引擎和 plugin 都链接它。结果 DLL 越长越大、最后半个引擎塞进去，和"简洁 API"的初衷背道而驰——任何内部改动都震到所有 plugin。
- **脚本语言桥接**：所有 plugin → 引擎调用走 Lua。对某些应用合适，但对 C++ plugin 来说：一是很多底层能力本来就不在 Lua 面上；二是 marshal 到 Lua 又回来纯粹是多此一举的 overhead，而且等于把引擎内核全部暴露给 Lua。

## Interface Querying：版本化 C API 表

Bitsquid 选的路是 **C-based、data-oriented、极简**——明确不用 C++ 接口，因为 C++ ABI 在不同编译器甚至同编译器不同版本之间都不兼容，plugin 用了就是锁定编译器。

最朴素的版本是：`EngineApi` 结构体里装一堆函数指针，`init(EngineApi *api)` 时一次性递给 plugin。问题是**不能改**——一旦要给 `spawn_unit` 加个旋转参数，所有 plugin 就破了。

Niklas 的解法是**引入查询函数 + 版本号 + 模块 ID**：

```c
#define WORLD_API_ID 0
#define LUA_API_ID 1

typedef struct WorldApi_v0 {
  void (*spawn_unit)(World *w, const char *name, float pos[3]);
} WorldApi_v0;

typedef struct WorldApi_v1 {
  void (*spawn_unit)(World *w, const char *name, float pos[3], float rot[4]);
} WorldApi_v1;

typedef void *(*GetApiFunction)(unsigned api, unsigned version);
```

引擎把 `get_engine_api(api_id, version)` 传给 plugin。plugin 在 init 里按需索取：`_world_api = (WorldApi_v1*)get_engine_api(WORLD_API_ID, 1);`。只要引擎愿意继续返回 `WorldApi_v0`，老 plugin 就永远不会坏——**老接口是可以无限"躺着"的**，加新接口只是新增一个 version，不是替换。

这个做法同时解决了三件事：

1. **ABI 稳定**：plugin 不 link 任何 DLL，只靠一个 header 和一个函数指针表——从 header 里包括什么都完全由 plugin 决定。
2. **可破坏地演进**：要修改 API？新开一个 v1，让 v0 作为 compatibility shim 存续。
3. **模块化**：API 自然拆成 WorldApi、LuaApi、RenderApi……plugin 只拿自己真正要用的那几个。

## Plugin 侧对称使用同一把钥匙

查询机制一旦引入，Niklas 顺手把**plugin 自己也改成同样形态**——plugin 不再 export `init/update/shutdown` 一串符号，而是只 export 一个 `get_plugin_api(api_id, version)`。这样 plugin API 本身也能演进：加一个"plugin 卸载前要做的清理"函数？新开 `PluginApi_v1`，老 plugin 返回 v0 仍然可用。**对称**让两边都可以独立演进。

## 选择 C 不是情怀

评论区有人问为什么不干脆用 C++ 虚函数表——逻辑上和函数指针 struct 等价、语法更顺眼。Niklas 直答：**C++ ABI 在不同编译器甚至同编译器不同版本之间不兼容，plugin 用了就是锁定编译器**。plugin 内部想写 C++ 没问题，接口层保持 C 是为了让 plugin 作者**自由选工具链**——这和 [[middleware-vs-open-source|middleware vs open-source]] 背后的 ABI 自由意志是同一件事。

## 和数据导向的天然契合

这个 plugin 模型的"纯函数指针表 + 版本号 + 模块 ID"造型和 [[data-driven-architecture|数据导向设计]]几乎是同构的——API 本质上是**一组可调用操作的数据描述**，不是一棵继承树上的方法分派。这也是为什么 Bitsquid 的 plugin 系统能无缝接上后来的 [[bitsquid-data-oriented-entity-system|ECS]]：plugin 想给 entity 加新组件？注册一个新的 ComponentManager、在 EngineApi 里暴露对应的 WorldApi 函数即可——不需要继承，不需要反射。

## 相关

- [[bitsquid-data-oriented-entity-system]] — plugin 系统是 ECS 的直接诱因
- [[middleware-vs-open-source]] — ABI 自由和 plugin 的中立性
- [[c-interface-oop]] — 用 C 做多态接口的一般做法
- [[c-opaque-struct-modules]] — 不透明 struct + 函数表的模块风格
- [[custom-allocator-interface]] — Bitsquid 另一套 "接口即函数指针表" 的实例
- [[api-fast-path-design]] — API 设计的另一维度：hot path 与 cold path
- [[playcanvas-esm-scripts]] — 对比：PlayCanvas 把 script 扩展从 class-based 迁到 ESM-based

## Sources

- [[sources/bitsquid-engine-plugin-system]]
