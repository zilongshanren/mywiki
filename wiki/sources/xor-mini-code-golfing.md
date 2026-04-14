---
tags: [source, shader, 代码优化, shader-art]
date: 2026-04-14
sources: 1
---

# Mini: Code Golfing（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 8 月的一篇 Mini，解释**为什么 shader code golf 值得练**以及一批常用的缩短技巧和数学恒等式。

## 摘要

Code golf 就是把代码压到字符数最少的小游戏，在 shader 圈子里演化成了一种艺术——Twitter 280 字符里塞进 3D 相机带景深 bokeh 的屏幕 shader、190 字节写出体素渲染器。Xor 列出练 golf 的四个理由：**深化语言理解**（会挖到规范的角落）、**意外优化**（短代码常常更快，因为被迫找重复计算）、**积累数学替代式**（如 `dot(x,x)==pow(length(x),2.)`）、**好玩**。然后给出一组可操作技巧：单字母命名 + 约定（`p` 位置、`c` 颜色、`O` 输出）、字面量压缩（`1.0→1.`、`vec4(1,1,1,1)→vec4(1)`）、声明合并、`if/else → ?:`、用 `for(;;)` 的两个"免费 slot" 替代多余语句。最后一大段列常用恒等式备忘：`floor/ceil/fract/mod` 的互换、`length/normalize/reflect/dot` 的替代、三角函数的相位近似 `vec2(cos(x),sin(x)) ≈ cos(x+vec2(0,11))`。

## 关键要点

- Code golf 让你从**"会写能跑"**跨到**"理解语言机制"**。
- **数学替代表**比技巧更值钱：`dot(v,v)` 代替 `length(v)^2`、`1.0/dot(d,d)` 代替 `1.0/length(d)^2` 做平方反比衰减。
- **`for(;;)`** 的三个 slot 比 `while()` 多出两个免费语句位。
- 三元运算符可以塞多变量赋值，能替换 `if/else` 块。
- Xor 号称用这些技巧能把随机 ShaderToy 缩 40%。
- 结尾给读者留了个命题作文：写一个"异或"主题的 tiny shader。

## 链接到的概念

- [[shader-code-golfing]]
- [[vector-dot-product]]
- [[fragment-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/code-golfing
- 本地：`raw/articles/mini.gmshaders.com/2022-08-26_mini-code-golfing.md`
