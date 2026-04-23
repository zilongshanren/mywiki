---
tags: [source, bitsquid, documentation, markup, ruby]
date: 2026-04-19
sources: 1
---

# Caring by Sharing: The Bitsquid Documentation System（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2012 年 3 月的文章，是 2011 年《Simple Roll-Your-Own Documentation》的后续——这次把代码公开出来并讲清系统设计。

## 摘要

系统读 `.bsdoc` 源文件（自定义 markup），输出 HTML，再用 HTML Help Compiler 编成 `.chm`。为什么不用 Markdown/Textile/RDoc/Doxygen 等：没有现成系统能完全贴合 Bitsquid 的需求。例如 Lua API 的文档用 `@api` 模式——每个未缩进行描述一个 Lua 函数，缩进的行是其文档，系统会自动识别签名、生成索引、跨类函数交叉引用。关键的设计准则是**保留语义信息**（不仅是"斜体"，而是"这是 Lua 函数签名"、"这是 C++ 代码"）和**减少杂乱**。代码公开后强调其实 generic 部分（`paragraph_parser.rb` / `span_parser.rb` / `generator.rb` / `toc.rb`）才是可复用的，具体 markup 规则集中在 `bsdoc.rb`。三个值得借鉴的设计点：**line-by-line 解析**（O(N)、易推理）；**无中间表示**（bsdoc 直接转 HTML，不建 AST）；**HTML "context"**——rule 发射时给 generator 一个 tag 列表 `%w(ul li p)` 加文本，generator 自动对比相邻行的 context 来开关最少必要的 tag，输出结构良好的 HTML；嵌套通过 indent 驱动递归 + prepend 前缀 context 来处理，不写任何特殊嵌套规则。Doxygen 被保留用于 inline C++ 注释——因为那确实解决了"解析 C++"这个真正困难的问题；而"文本 → HTML"本身不是难题，自建完全值得。

## 关键要点

- `.bsdoc` 自定义 markup + Ruby 工具链 + HTML Help Compiler → .chm。
- `@api` 是专门为 Lua 接口文档加的模式，识别函数签名并建索引。
- Generic 部分可复用，markup 规则独立在 `bsdoc.rb`。
- 三个设计决策：line-by-line、无 AST、HTML context stack。
- "没有 intermediate representation" 是简化的关键——直接生成。
- Doxygen 值得用是因为它解决了真正难的 C++ 解析；text→html 不难，自己写。
- 本文与 2011 年《Simple Roll-Your-Own Documentation》互补——后者讲哲学，此文给代码与具体实现细节。

## 链接到的概念

- [[minimal-markup-pipeline]]
- [[strategic-programming]]
- [[header-as-user-manual]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/03/caring-by-sharing-bitsquid.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-03-04_caring-by-sharing-the-bitsquid-documentation-system.md`
