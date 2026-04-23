---
tags: [C, 指针, 可移植性, OpenGL]
date: 2026-04-19
sources: 1
---

# 函数指针 vs 数据指针：可移植性

[[ben-supnik|Supnik]] 从一行古怪的 GLX 函数签名开始写起：

```c
void (*glXGetProcAddressARB(const GLubyte *procName))();
```

解密一下其实就是：

```c
typedef void (*GLfunction)();
extern GLfunction glXGetProcAddressARB(const GLubyte *procName);
```

和其他平台（WGL、AGL 一类）把 extension loader 的返回值定义为 `void *` 不同，GLX **返回一个无参数无返回值的函数指针类型**。这让同时支持 Win/Mac/Linux 的代码必须在 GLX 分支上多做一次 cast 到 `void *`，挺烦人。

## C 标准为什么区分 code 指针与 data 指针

评论区给了一个很好的技术答案：**C 标准从不承诺 `void *` 与函数指针等宽**。

`void *` 在语言层面只被保证能承载**数据指针**：任意对象指针可以无损地转到 `void *` 再转回去（C89/C99 明文）。这条承诺**不延伸到函数指针**。原因是历史上的确存在 code 和 data 走不同地址空间、甚至不同位宽的架构：

- 哈佛架构分离 I/D；
- 早期机器可能是 code 32-bit / data 24-bit，或 code 40-bit / data 32-bit，甚至 9-bit byte 的 code 36 / data 27；
- 某些 DSP、微控制器至今仍保留这个设计。

把函数指针塞进一个较窄的 `void *`，会把高位截断，指向另一段无关内存。现代消费级平台（x86、ARM、大多数 POSIX）是 flat model，所以 POSIX 的 `dlsym` 明知违标还是用 `void *` 凑合用——但 OpenGL ARB 要让规范覆盖所有架构，所以严格走函数指针类型。

## 实务上的处理

- 任何两个函数指针之间可以安全 cast（`GLfunction` cast 成 `PFNGLxxxxPROC` 是合法的）；
- 函数指针与数据指针互转是**未定义行为**，但在 flat-memory 平台上工作；
- 跨平台 loader 的干净写法是把 GLX 的返回先转成一个**通用函数指针类型**，再在需要时 reinterpret 到具体签名。

## 相关

- [[ben-supnik]]

## Sources

- [[sources/supnik-glxgetprocaddressarb-syntax]]
