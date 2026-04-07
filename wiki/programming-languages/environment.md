---
tags: [编程语言, sicp]
date: 2026-04-05
sources: 1
---

# 环境（Environment）

**保存「名字 → 值」对的内存结构**，是理解[[closure|闭包]]和作用域的核心。

## 结构

环境是一个**frame chain**：每个 frame 存一组局部绑定，frame 有一个指向外层 frame 的指针。

```
Global Frame: { + : <primitive>, pi : 3.14 }
    ↑
Function Frame: { x : 10, y : 20 }
    ↑
Block Frame: { tmp : 5 }
```

## 名字查找

查找一个变量：从当前 frame 开始，沿着 frame chain 向上找，第一个匹配的就是。

## 作用域规则由链条形状决定

- **词法作用域（静态）**：frame chain 根据代码结构确定。
- **动态作用域**：frame chain 根据调用栈确定。

详见 [[lexical-scoping]]。

## 与闭包的关系

**闭包 = 函数 + 定义时的环境指针**。函数记住它出生时环境链的样子，即使被传到别处调用，依然能访问那个环境里的变量。

## 相关

- [[lexical-scoping]]
- [[closure]]
- [[substitution-model]]（环境模型是代换模型的"状态升级版"）
- [[elements-of-programming]]

## Sources

- [[sources/sicp-day01]]
