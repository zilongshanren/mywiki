---
tags: [source, ue, unreal, 蓝图, 资产验证, 2025]
date: 2026-04-19
sources: 1
---

# Validating Blueprints' Content in Unreal（Thomas Poulet / 2025）

[[thomas-poulet]] 2025 年 12 月一篇短文。来自客户提问：贴图大小和三角形数能自动验，**蓝图的 component 设置**（比如一个派生蓝图里的某 component 必须打特定 tag）要怎么自动验？

## 摘要

Unreal 的 **Asset Validator** 是项目里强制内容约定的好工具，能直接在蓝图里写规则。但要验蓝图本身的**内部组件**会踩两个坑：(1) `CanValidateAsset` 拿到的是 `Blueprint` 类型的对象而**不是**派生类的实例，`Cast<T>` 恒失败——得用 `Blueprint.GeneratedClass` 对比 class；(2) 蓝图不是「已实例化的 actor」而是**生成配方**，要用 **Subobject Data Subsystem** 遍历配方 subobject，逐个 cast 到目标 component 类型。有一个已知 quirk：**遍历会重复经过同一个 component**，有副作用的检查要自己去重。文章最后建议：**报错信息一定要写明白**，让内容团队拿到就能改。

## 关键要点

- **Asset Validator 是 UE 编辑器自带的 data validation 框架**，C++ 或蓝图都能写。
- **蓝图 ≠ 蓝图类的实例**：输入是 `Blueprint` asset，validator 要去比它的 `GeneratedClass`。
- **Subobject Data Subsystem** 才能遍历蓝图的组件配方。
- **去重**：loop 可能重复访问同一个 subobject。
- **错误文案**：越具体越好。

## 链接到的概念

- [[thomas-poulet]]
- [[ue-asset-validator-blueprint]]

## 原文

- 链接：<https://blog.thomaspoulet.fr/posts/validating-blueprints-content-in-unreal/>
- 本地：`raw/articles/blog.thomaspoulet.fr/2025-12-02_validating-blueprints-content-in-unreal-thomas-poulet.md`
