---
tags: [source, engine, resource-management, handles, vulkan]
date: 2026-04-14
sources: 1
---

# Engine Resources Management: a handle approach（Marco Giordano / A programmer's cave）

[[marco-giordano]] 发表于 2020 年 11 月的文章，系统地介绍他在自研 Vulkan/DX12 引擎里使用的"manager + opaque handle"式资源管理范式。

## 摘要

文章核心主张是：**不要把资源包在对象里**，不要返回指针或智能指针，而是返回一个 32-bit 不透明句柄，所有资源操作都经过对应的 manager（TextureManager、ShaderManager…）。句柄内部分成低 16 位 slot 索引 + 高 16 位 magic number。索引直接作为 manager 自维护 memory pool 的 slot 下标（不是哈希表），magic number 用来处理"slot 被回收再分配"产生的悬垂句柄问题——资源数据里也存一份 magic，每次访问先比对。作者反对用 `std::unordered_map` 做句柄到资源的映射，认为 hash + 碰撞处理在热路径太重，直接 pool 索引是 O(1)。文章给了 Vulkan 纹理 manager 的典型结构：`VkTexture2D` 里用位域塞 width/height/mipLevels/magicNumber，一个 `assertMagicNumber` 辅助函数在 debug 期校验句柄合法性，release 下编译没。作者强调这种写法的好处：所有权问题消失（拷贝句柄免费、不漏）、分配集中（想换 pool 实现一处改全引擎生效）、API 抽象天然（DX12/Vk 两后端共用 handle 类型）、实现成本不高（和 OOP 写法相比代码量相近）。灵感来源是《Game Programming Gems》里的一章，以及 Andre Weissflog 2018 年那篇 "Handles are the better pointers"。

## 关键要点

- 句柄 = 32 位不透明整数，由 index（低 16）+ magic number（高 16）组成，可平凡拷贝
- 索引是 memory pool 的 slot 下标，不走哈希表，访问是 O(1) 直接寻址
- magic number 解决 dangling handle：资源自身也存 magic，读取前 `assertMagicNumber` 比对
- 资源对象是被动数据结构，所有逻辑都在对应 manager 里
- Vulkan 纹理 manager 的 `VkTexture2D` 用位域打包 width/height/mipLevels/magicNumber（16 位计数器）
- debug 下每次访问都做 magic 校验，release 下断言全部编译没
- 所有权问题消失：句柄不 own 数据，拷贝它既不增加引用计数也不漏内存
- DX12/Vulkan 双后端只需要共用 handle 类型，后端结构体 `VkTexture2D` / `D3D12Texture2D` 对调用方完全透明
- 灵感来源：《Game Programming Gems》 + Andre Weissflog "Handles are the better pointers"（2018）
- 作者主张这种模式"和 OOP 方案代码量差不多"，不是更复杂，只是另一种默认

## 链接到的概念

- [[handle-based-resource-manager]]
- [[resource-system-design]] —— Unity 侧对同一问题的 RAII / Addressables 回答
- [[information-hiding]] / [[deep-modules]]
- [[linear-allocator]]
- [[marco-giordano]]

## 原文

- 链接：https://giordi91.github.io/post/resourcesystem/
- 参考：Andre Weissflog, "Handles are the better pointers"（2018）https://floooh.github.io/2018/06/17/handles-vs-pointers.html
- 本地：`raw/articles/giordi91.github.io/2020-11-13_engine-resources-management-a-handle-approach.md`
