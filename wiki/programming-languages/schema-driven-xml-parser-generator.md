---
tags: [programming-languages, code-generation, xml, common-lisp, parser]
date: 2026-04-19
sources: 1
---

# 基于 Schema 描述的 XML 解析器生成器

Patrick Stein 在 2010 年用 Common Lisp 重写了他几年前做过的一个 XML 解析器生成器：工具读入一份「描述 XML 结构如何映射到宿主语言数据结构」的 XML schema，产出两份代码——类型定义文件和 SAX 风格的解析器文件。核心想法是让开发者只声明「字段 name 来自 XML 属性 `@name`、字段 description 来自子节点 `/description/` 文本」，剩下 100 多行的 SAX 事件派发代码由生成器吐出，调用方只需调用 `parse` 拿到填好的对象。

## 声明式 schema 到 CLOS 的映射

Stein 用 `<struct>` 描述每个目标类，`<field>` 指定字段类型与 XML 来源路径（`@attr` 读属性、`/child/.` 读子节点文本），`<array>/<array_element>` 指定嵌套集合。生成器据此产出 `defclass`，并把字段类型（string、integer 等）落到 `:type` 槽声明上，整数类字段在读入时自动 `parse-integer`。这让 Schema 成为真正的 single source of truth：改描述即改类和解析器，无需手写任何 DOM 走访。

## Tagstack + 相对路径的 SAX 风格

内部解析器用的是 Stein 一直在用的 **tagstack** 手法：SAX handler 维护一个「当前进入的标签栈」，每到字段就把「当前 struct 相对路径」作为 key 派发到 `defmethod data progn` 上。这次他把早年版本里「路径一路追溯到根」改成了「相对当前被解析结构」——既减小 key 长度，又让同一子结构 schema 可以在不同父节点下复用。Stein 在文章里吐槽自己几乎每换一个平台都会重写一份 tagstack interface，暗示这是一个在多语言场景下都证明过价值的、比 DOM 更轻的惯用法。

## 元循环与多目标语言

生成器完成度的里程碑是**自举**：它能用自己生成出来的解析器去读取自己描述文件 schema（Stein 原文 "generating its own parser (five times fast)"）。2010-04 的后续发布又补上 Objective-C 后端，因为 Stein 当时在做 iPhone 项目需要同一套 schema 在 Lisp 和 Objective-C 两端复用；Lisp 后端成熟度较 Objective-C 后端高——后者彼时只支持 struct 数组，还不支持 string/integer 数组。对照早年折戟的 Java 版（作者原话：「ugly, ugly, ugly」的代码库几次试图清理成可发布版本都失败），这次用 Lisp 重写后元编程层薄、自举顺利，说明了宿主语言对 code-gen 工具链复杂度的放大作用——在 Java 里难以驯服的 meta-ness 在 Lisp 里几乎只剩结构化模版。

## Sources

- [[sources/nklein-xml-parser-generator]]
