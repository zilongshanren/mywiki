---
tags: [source, 软件设计, cpp, 头文件]
date: 2026-04-19
sources: 1
---

# Coding For Two Audiences（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 1 月的文章，给出他「Header Nazi」风格的底层依据：代码同时写给两类读者——编译器和人类——而头文件是给人类读者的书。

## 摘要

Supnik 用一个对比开场：同一份编译结果可以写成 `void * load_model_from_disk(const char *)`（对人类近乎密码），也可以写成 `typedef void * model_3d_ref; model_3d_ref load_model_from_disk(const char * absolute_file_path)`（任何 C 程序员都能一眼看懂语义）。差异对编译器零语义、对人类巨大。由此引出风格准则：头文件要像书一样读。具体操作：物理隔离优先于逻辑封装（能进 .cpp 就不要进 class 的 private 段）、性能必须 inline 时把定义挪到 class 外部、调用约定/生命周期/线程安全等「使用必须知道」的文档全部放头文件。文章同时指出 Joel 那一派「if (0 == x)」型防御式风格只服务第一类读者，对第二类读者没有增益。

## 关键要点

- 头文件是模块的「用户手册」——如果模块真的有用、bug 少、封装到位，未来读头文件的时间远超读实现的时间。
- 物理隔离（.cpp）比逻辑封装（private:）更有效——private 只阻止调用，不阻止阅读。
- inline 为性能而存在时，至少在视觉上别污染 class 声明——挪到 class 外的文件底部。
- 文档写在头文件里才有意义——实现文件里的注释用户永远不会看到。
- C 风格 opaque handle（`typedef void * model_3d_ref`）是服务两类读者的极简手段。

## 链接到的概念

- [[header-as-user-manual]]
- [[information-hiding]]
- [[c-opaque-struct-modules]]
- [[deep-modules]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/01/coding-for-two-audiences.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-01-05_coding-for-two-audiences.md`
