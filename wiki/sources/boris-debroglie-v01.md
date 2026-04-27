---
tags: [source, procedural-generation, wfc, game-development, csharp]
date: 2026-04-27
sources: 1
---

# DeBroglie v0.1（Boris The Brave）

[[boris-the-brave]] 2018 年 10 月发布的开源项目公告，介绍他的 C# WFC 库 DeBroglie 的首个正式版本。

## 摘要

DeBroglie 是一个 C# 库，同时附带 Windows 命令行工具，实现了 Wave Function Collapse 算法，并在此基础上扩展了**非局部约束（non-local constraints）**支持。WFC 本身只做局部约束传播，难以保证生成结果具有某些全局属性（如连通性、特定瓦片出现次数等）；DeBroglie 的设计目标正是填补这一空白，让用户既能获得 WFC 的随机生成能力，又能对大尺度结构施加额外约束，最终用来生成「基于瓦片的酷炫内容」。

## 关键要点

- DeBroglie = C# WFC 实现 + 非局部约束扩展框架
- 同时提供库（可嵌入到游戏或工具）和独立命令行工具
- 非局部约束是对标准 WFC 的核心增强，用于控制全局结构（连通性等）
- v0.1 是初始发布，Boris 此后持续迭代出更多约束类型和功能

## 链接到的概念

- [[wave-function-collapse]]
- [[debroglie-wfc-library]]
- [[game-development/driven-wfc]]

## 原文

- 链接：https://www.boristhebrave.com/2018/10/06/debroglie-v0-1/
- 本地：`raw/articles/boristhebrave.com/2018-10-06_debroglie-v0-1.md`
