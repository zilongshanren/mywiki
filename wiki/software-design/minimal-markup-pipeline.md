---
tags: [documentation, parser, generator, markup, ruby]
date: 2026-04-19
sources: 1
---

# 极简标记语言管线：parser + generator 两段式

[[niklas-frykholm]] 对文档系统的要求不常见：Doxygen 管内联注释，但「其他一切文档」他偏要自己造一个。原因是现成方案都有硬伤：Word/Pages 不能 diff；HTML/LaTeX 是表现层，不能重排；Wiki 不能跟代码一起打 tag；Markdown/ReST/DocBook 多余太多，又缺 Lua 代码高亮、旁注、数学公式。

他的答案是用不到 200 行 Ruby 手写一套，两个组件足矣：

## parser：每行一对 `(type, text)`

关键决定是**放弃层级 AST，用扁平 line list**。每行打一个 type 标签，像 `(:h1, "Flavors...")`、`(:li, "Strawberry")`、`(:empty, "")`。源文档的语法就是每行开头 `@tag` 决定 type：

```ruby
def parse(line)
  case line
  when /^$/           then @lines << {type: :empty, line: ""}
  when /@(\S+)\s+(.*)$/ then @lines << {type: $1.intern, line: $2}
  else                 @lines << {type: :text, line: line}
  end
end
```

嵌套列表？不做通用层级，直接加一个 `@li_li` 的 type marker 表示「二层列表」。再深就重写文档——作者的原话是「这是可读文档，不是维特根斯坦的逻辑哲学论」。这是用约束换简单性的典型例子，对应 [[strategic-programming]] 里面「为已知用例做到足够好，别扩展到不需要的未知场景」。

## generator：维护当前打开的 tag 栈

生成 HTML 的核心技巧是一个 `context(tags)` 方法，输入**期望当前打开的标签列表**，它自动关掉多余的、打开缺的。这样每行 emit 都不用关心「上一行是不是列表，需不需要补 `</ul>`」：

```ruby
def li(line)
  context(%w(ul li))
  print line
  context(%w(ul))    # 关 li，保留 ul
end
```

`context()` 实现就是双指针对比 `@context` 和目标列表，prefix 匹配后弹栈 close、入栈 open。这样源文档可以单次流式处理，不用像 DOM-based 那样两遍扫。

## 启示

这个架构展示了一个反直觉观点：**文档管线不需要 AST**。line list 覆盖了 95% 的需求，剩下的用「状态化 marker」（`@lua` … `@endlua` 让 parser 进入代码模式）或生成期的附加 pass（TOC、交叉引用）处理。总代码 100 行量级，换来完全可控、易扩展、和代码一起进 repo 的文档工具链。

## 相关

- [[strategic-programming]]
- [[header-as-user-manual]]
- [[tiny-expression-language]]

## Sources
- [[sources/bitsquid-roll-your-own-docs]]
- [[sources/bitsquid-documentation-system-code]] — 2012 年的代码公开版本，补充 @api Lua 模式、bsdoc 文件扩展、HTML context stack 的具体写法
