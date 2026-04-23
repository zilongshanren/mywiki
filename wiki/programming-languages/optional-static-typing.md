---
tags: [language-design, type-system, gradual-typing]
date: 2026-04-19
sources: 1
---

# 可选静态类型（Optional Static Typing）

同一种语言里，**带类型标注与不带标注的代码可以共存**：标注的地方走静态检查与优化，未标注的地方退回动态分派或类型推断。AS3、haXe 在 2010 年前后就有这套设计；后来 TypeScript、Python 的 type hints、Ruby 3 的 RBS、PHP 的 type declarations 让这套思路进入主流。

## 动机

传统二分法把语言分成「静态 vs 动态」，各有痛点：

- 纯静态（Java、C#）：原型阶段也得把类型写全，写验证代码、写临时脚本都觉得重
- 纯动态（Python、Ruby、早期 JS）：代码一长就没法自信地重构，IDE 补全只能靠启发式

可选类型希望**把类型当作可加的文档+契约**：写 demo 时可省，稳定后再补上，不用重写。

## 运行时语义的两种选择

1. **标注仅做静态检查，运行时擦除**（TypeScript、Python type hints）：性能与动态等价，标错了运行时不爆
2. **标注参与运行时分派/插 cast**（AS3、Dart sound mode）：标注带来性能增益（JIT 可跳过动态查找），标错了会抛类型错误

AS3 属于第二类，Boris 在原文里提到他会「把能标的都标上」来换取性能，唯独在 `Function` 这类被迫动态的地方留白。

## 与类型推断的关系

可选类型 ≠ 类型推断。推断（Haskell、Rust、OCaml）是「类型一定存在，只是你不用写」；可选类型是「类型可以压根不存在，运行时也不生气」。两者可叠：TypeScript 在标注处做检查，未标注处用推断填坑，坑底留 `any`。

## 历史评价

2010 年 Boris 呼吁 JS、Python 加入这套机制，当时几乎没人听。2012 TypeScript 发布、2014 Python 3.5 PEP 484 落地，可选类型的合理性被反复验证。现在新语言基本默认都带上，如 Swift、Kotlin、Dart、Zig 均把「类型标注作为主语法但推断兜底」作为常态。

## Sources

- [[sources/boristhebrave-as3-gems]]
