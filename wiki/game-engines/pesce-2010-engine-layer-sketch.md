---
tags: [游戏引擎, 架构, 分层, 历史]
date: 2026-04-19
sources: 1
---

# Pesce 2010 引擎分层草图

[[angelo-pesce]] 2010 年发起的协作实验产出的引擎分层清单，是 **2010 年前后 AAA 图形程序员对「理想引擎」的共识快照**。与 [[engine-layering|Gregory 的教科书分层]] 相比，它更工程化，也更具时代指纹——把 CI、Code Review、编码规范写进 Layer -1，把 DX11 风格的无状态 device 抽象作为 Layer 2 的起点。

## 六层结构

```
Layer -1  Prerequisites            编码规范 / 构建 / CI / 静态检查 / 版本控制 / Code Review
Layer  0  Language Extensions      编译器抽象 / 栈回溯 / 模块服务 / 根对象 / 内存分配器 / 生命周期
Layer  1  Core Libraries           多线程 / 资源层 / 反射 / 数学 / 容器 / 参数系统 / 网络 / 日志 / 序列化
Layer  2  Low-level Rendering      Device 抽象 / Debug 渲染 / GUI / Effect / 参数编辑 / 资源加载
Layer  3  User-level Libraries     脚本绑定（代码生成自反射） / 还缺蒙皮 / 顶点处理 / LOD / 阴影 / 后处理
External  Tools                    反射 inspector / 自动化测试
```

把 **Layer -1** 摆进分层图是这份草图最特别的地方——它主张「工程流程本身就是架构的一部分」，而不是附属品。Pesce 引用的价值观也很鲜明：**「Fuck C++ OOP. Data is the king. Keep compile times low.」**——这与后来 [[data-driven-architecture|数据驱动架构]] 与 [[dots-ecs-programming-patterns|DOTS/ECS]] 路线的兴起一脉相承。

## 几个有辨识度的主张

- **模块服务系统而非全局单例**：每个模块把接口实例注册到 `(name, pointer)` hashmap；模块可以声明对其他模块的依赖，加载失败即拒载，卸载时通知订阅者。类似后来的 service locator，但强调静态链接接口 + 动态发现实例。
- **反射走 PDB 解析路线**：在编译步骤里把 PDB 调试数据库转成反射 DB，按需加载。优点是避开宏/模板魔法、能对第三方库生效、可用来做代码度量与覆盖率分析；缺点是自定义 attribute 与反射函数调用需要编译器特定技巧。这与 [[cpp-runtime-reflection]] 的讨论形成对照——2010 年的 Pesce 投票给「离线分析 PDB」，2020+ 年的讨论更多偏向 C++20 反射提案与 libclang/AST 路线。
- **Job scheduler 的五类依赖**：normal（纯同步）/ data（写一块内存，下游读）/ data-parallel（数组拆分）/ buffered（循环缓冲，下游读上一帧）/ streamed（数组元素级流水）。这套分类比主流 job system 常见的「任务依赖 DAG」更细，隐含了今天 [[render-graph|render graph]] 的一些雏形。
- **渲染设备走 DX11 风格**：无直接单 state 写入、块上传、支持多 device 与 command buffer 录制；stateless 或支持 state flush/invalidate。2010 年这是前瞻立场，之后被 DX12/Vulkan 彻底接收。
- **STL 不适合引擎**：不好对齐、不好暴露在接口里、实现差异大、难调试、与反射冲突。自建 `vector / fixed_vector / hash_map / lockless_queue / bloom filter` 等容器——这个立场后来在 EASTL / Bitsquid 容器 / [[rpp-stl-replacement]] 等实践里被反复复制。
- **全局参数系统的四类 section**：`external` 只读外链 DB、`shared` 走 spinlock、`thread` 限定线程、`threadmessage` 支持 onChange 回调。对应到今天的 CVar / ConsoleVariable 系统，但粒度更细。

## 未解 dilemma

Pesce 在文末留下一个没想清楚的问题：**引擎数据层是统一走「反射 + 序列化」，还是分裂成「参数数据库（材质、shader 参数）+ 专用文件格式（mesh、texture）」？** 他说「两套代码都得写，但这仍是一个架构决定」。2010 年之后主流工业答案更偏向「两者并存 + 用反射生成工具链」——Unreal 的 `UPROPERTY` + uasset 是典型。

## 与后续文献的对话

- 与 [[engine-layering|Gregory 的分层]] 对比：Gregory 偏教学、层次更粗；Pesce 偏工程、层次更细并把 DevOps 抬到最底层。
- 与 [[bitsquid-managing-coupling|Bitsquid 的解耦文章]] 对比：Pesce 的模块服务系统思路与 Bitsquid 的 service locator 风格接近，但 Bitsquid 2011+ 更明确地把「尽量少的共享状态」写在首位。
- 与 [[scene-graph-unnecessary-in-engine]]（Pesce 本人 2012+ 的观点）对比：2010 的草图里还没有明确抛弃场景图，但 Layer 3 已经留出「未达成共识」的空洞——这与他后来的立场一致。

## 相关

- [[angelo-pesce]]
- [[engine-layering]]
- [[game-engine]]
- [[data-driven-architecture]]
- [[cpp-runtime-reflection]]
- [[render-graph]]

## Sources

- [[sources/c0de517e-collaborative-engine-design]]
