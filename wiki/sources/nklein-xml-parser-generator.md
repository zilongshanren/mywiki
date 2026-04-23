---
tags: [source, programming-languages, common-lisp, code-generation, xml]
date: 2026-04-19
sources: 1
---

# XML Parser Generator / Parser Generator released（Patrick Stein, nklein software）

[[patrick-stein]] 在 2010 年 3 月和 4 月先后发布的两篇博文，合并成一份摘要。前文介绍他用 Common Lisp 重写多年前在 Java 上没能收尾的 XML 解析器生成器思路与用法；后文是两行版本说明，补报已支持 Objective-C 后端。

## 摘要

Stein 需要在 Objective-C 下解析各种 XML，但早年 Java 版代码库「ugly, ugly, ugly」且源码也丢了，于是用 Common Lisp 重写。工具接受一份 XML schema 描述（用 `<struct>`/`<field>`/`<array>` 声明目标数据结构与 XML 字段路径），生成两份 Lisp 文件：`types.lisp` 里的 `defclass` 定义和 `reader.lisp` 里的 SAX handler。handler 沿用他习惯的 **tagstack** 手法，把 `@attr`、`/child/.` 这类路径作为 key 派发到 `defmethod data progn` 上；整数字段自动 `parse-integer`。3 月版本已经能自举——用自己生成的解析器读 schema 描述文件；4 月版本加上 Objective-C 后端，但 Objective-C 后端暂时只支持 struct 数组，string/integer 数组仍然只有 Lisp 后端能生成。相对于早期 Java 版，Stein 这次改进了 tagstack：路径从「到根的绝对路径」变成「相对当前结构」，提高了子结构复用性。

## 关键要点

- Schema 用 XML 写，字段来源用 `@attr`、`/child/.` 表达——文本内容与属性统一到一个派发通道
- 生成目标：`defclass` 类型文件 + 134 行级别的 SAX reader，调用方只见 `parse` 入口
- **自举**：生成器能生成自己读入 schema 所用的解析器
- Tagstack 用相对路径而非绝对路径，鼓励子结构 schema 复用
- 多后端思路：Common Lisp + Objective-C，计划扩展到其它语言
- 反思：Java 版本因元编程层笨重几次清理都失败；Lisp 重写直接完成自举——这是宿主语言对 code-gen 元循环成本的放大案例
- 4 月 release 公告只有两行正文，附主页链接；合并到同一篇摘要

## 链接到的概念

- [[schema-driven-xml-parser-generator]]
- [[patrick-stein]]

## 原文

- 链接 1：<http://nklein.com/2010/03/xml-parser-generator/>
- 链接 2：<http://nklein.com/2010/04/parser-generator-released/>
- 本地：`raw/articles/nklein.com/2010-03-16_xml-parser-generator-nklein-software.md`
- 本地：`raw/articles/nklein.com/2010-04-09_parser-generator-released-nklein-software.md`
