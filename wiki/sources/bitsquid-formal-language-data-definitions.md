---
tags: [source, bitsquid, 数据格式, 序列化]
date: 2026-04-19
sources: 1
---

# A Formal Language for Data Definitions（Bitsquid, 2012-11）

[[niklas-frykholm|Niklas Frykholm]] 发表于 2012 年 11 月的思考型博文：为什么至今没有一种**形式化语言**来描述二进制数据布局？以及如果要造一个，它该长什么样。

## 摘要

Niklas 吐槽文件格式文档一直停留在自然语言 + ASCII 缩进表的水平——"4 bytes header id, 2 bytes header length, 0-20 bytes extra"读起来像侦探破案。他想象一种"带 label 和数组参数化的受限 C"语法，写一份 schema 就能拿来在任意二进制 blob 上双向转 JSON、把调试器的 `autoexp.dat` 黑魔法替掉、生成序列化代码。本质矛盾是**完备性 vs 可读性**：能描述任意格式必须图灵完备，而图灵完备就和手写 C 解包代码没区别了。他的折中是把"声明式"视为某种过程式语言的语法糖——常见情况读起来仍像 struct，刁钻情况再 drop 到过程层。文末讨论了 ASN.1、Protocol Buffers、010 Editor Templates、Synalyze It! 几套先例——评论区基本一致指向 **010 Editor Templates** 是事实标准。

## 关键要点

- 二进制格式文档缺乏"代数记号"级别的形式化描述手段。
- Schema + 双向转换器是最小可用产品（MVP），binary ↔ JSON 是最直接的 reality check。
- 语法选型偏向"受限 C"：直接复用 C struct 语法；扩展数组参数化和区段 label。
- 完备性以"声明式作为过程式的糖"收尾——常用情景保持极简，极端情景可以掉进过程代码。
- 真正棘手的问题是版本化 / 向后兼容、代码生成、避免中间 text 表示——评论区同样指出这一点。
- 评论里有人分享过类似尝试（Sam 提的早期 XML-based block schema），都栽在版本兼容上。

## 链接到的概念

- [[binary-data-definition-language]]
- [[offset-based-resource-blobs]]
- [[c-serialization-metadata]]
- [[schema-driven-xml-parser-generator]]
- [[bitsquid-3-way-json-merge]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2012/11/a-formal-language-for-data-definitions.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2012-11-21_a-formal-language-for-data-definitions.md`
