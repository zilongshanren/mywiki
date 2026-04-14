---
tags: [shader, 代码优化, glsl, shader-art]
date: 2026-04-14
sources: 1
---

# Shader Code Golfing

**Code golf** 是把一段代码压到尽可能少的字符数的比赛游戏；在 shader 圈子里，它直接演化成了一种艺术形式——Twitter 上的 280 字符挑战、Shadertoy 的 tweet-sized shader、190 字节的体素渲染器，都是这种美学的产物。[[xor-shader-artist|Xor]] 认为做 golf 不只是炫技，它对理解语言、发现优化、构建直觉都有实打实的收益。

## 为什么值得试

- **理解语言**：为了缩一个字符，你会被迫去读语言规范的边角——vec 构造函数如何隐式转换、`for` 的三个 slot 能塞多少逻辑、三元运算符能不能返回对。这些知识迁移回"正经"代码里会发现同样有用。
- **优化副作用**：短代码常常更快。因为缩短代码的过程本质上是**找重复计算**、**合并数据通路**的过程——把一个值算一次存起来，比每次重算要短也要快。Xor 写屏幕 shader 时原本以为要两趟做 bokeh，golfing 的过程中意外找到了合一的方法。
- **积累数学替代式**：你会逐渐记住一组等价变换表，看到 `pow(length(x), 2.0)` 条件反射写成 `dot(x, x)`。这种"函数替代"记忆是 shader 优化的核心资产。

## 常用替换技巧

**命名与字面量**：单字母变量名（`p` 位置、`c` 颜色、`O` 输出、`I` 输入）、`1.0 → 1.`、`1000.0 → 1e3`、`vec4(1,1,1,1) → vec4(1)`、`*10. → /.1`。把多个同类型变量用一行声明合并：`float x=0., y=1.;`。

**控制流**：`if/else` 换成三元运算符，节省大量字符。`for(;;)` 比 `while()` 更划算——它在条件前后各有一个"免费 slot" 可以塞初始化和递增语句。避免 `break`，把退出条件直接写进中间 slot。单行循环体可以用逗号运算符省略大括号（但多层嵌套就不能用这招了）。

## 有用的恒等式速查

算术：`floor(x)==x-fract(x)`、`ceil(x)==x+fract(-x)`、`mod(x,y)==x-floor(x/y)*y`、`abs(x)==x*sign(x)`、`step(x,y)==x>y?0.:1.`。若 `x∈[0,1]`，`smoothstep(0.,1.,x)==x*x*(3.-x-x)`。

向量：`dot(v,v)==pow(length(v),2.)`、`length(v)==sqrt(dot(v,v))`、`normalize(v)==v/length(v)`、`reflect(i,n)==i-dot(i,n+n)*n`。参见 [[vector-dot-product]]。

三角：`radians(d)==d/180.*PI`、`cos(x)==sin(x+PI/2.)`。Xor 最爱的两个近似是 `vec2(cos x, sin x)≈cos(x+vec2(0,11))` 和把 2D 旋转矩阵写成 `mat2(cos(x+vec4(0,11,33,0)))`——利用了 `cos` 相位偏移 ≈ 11 弧度时约等于 `sin` 的巧合。

## 相关

- [[vector-dot-product]]
- [[fragment-shader]]
- [[shader-vector-math-primer]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-code-golfing]]
