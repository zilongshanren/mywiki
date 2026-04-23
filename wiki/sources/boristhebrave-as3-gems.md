---
tags: [source, programming-languages, language-design, actionscript]
date: 2026-04-19
sources: 1
---

# X Gems of AS3 Language Design（Boris The Brave / 2010）

[[boris-the-brave]] 2010 年 5 月发表的语言设计杂感，罗列了 ActionScript 3 里他认为值得被更多语言借鉴的几个「小钻石」。尽管 AS3 本身已近乎死去，文章仍是一份早于现代 TypeScript / Kotlin / Swift 的语言设计清单。

## 摘要

作者承认 AS3 慢、泛型弱、标准库薄，但仍喜欢它，原因在于它集齐了几个「少见但该有」的语言特性。第一条是**易于解析的语法**：`var x:Type` 形式比 C/Java 的 `Type x` 对 parser 更友好，泛型使用 `Template.<T>`（带点）避开了 `<T>` 与比较运算符的歧义，Pascal、Ada 早就做对了。第二条是**把常用类型做成语言原语**：regex 字面量、XML 字面量与 E4X 查询（`familyTree..person.(@gender=='M')`）让字符串和半结构化数据处理极度简洁，对比 Lua 这类「常用类型只能走 API」的做法显得特别清爽。第三条是**方法隐式绑定**：`a.join` 直接取出时就绑好了 `this`，省掉 C++98 的成员指针、Python 早期的显式 `self` 绑定、JavaScript 需要 `.bind` 的烦恼，事件订阅/取消写起来自然对称。第四条是**可选静态类型**：变量可带类型也可不带，底层自动插 cast；这让脚本式快写和工程式严格标注可以共存，甩开 Java 的强制显式。AS3 在实践中仍有性能坑，但作为语言设计样本，这几点在 2010 年前后是 underappreciated 的。

## 关键要点

- `var x:Type` 语法对 parser 更友好，也更易读；`Template.<T>` 绕开尖括号歧义
- XML / regex 作为一等语言原语，可配合 E4X 查询直接写类 XPath 表达式
- 从实例取方法时隐式绑定 `this`，让 `addEventListener` / `removeEventListener` 可用同一引用对称调用
- 可选静态类型让原型阶段免类型、成熟后补类型；haXe 也有类似设计
- 作者对 JavaScript、Python 的呼吁最终在 TypeScript、Python 3 type hints、类型推断浪潮中部分兑现

## 链接到的概念

- [[optional-static-typing]]
- [[method-binding-semantics]]
- [[boris-the-brave]]

## 原文

- 链接：https://www.boristhebrave.com/2010/05/04/x-gems-of-as3-language-design/
- 本地：`raw/articles/boristhebrave.com/2010-05-04_x-gems-of-as3-language-design.md`
