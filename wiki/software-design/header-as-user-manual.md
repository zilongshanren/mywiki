---
tags: [软件设计, cpp, 接口设计, 可读性]
date: 2026-04-19
sources: 1
---

# 头文件即用户手册

[[ben-supnik]] 的 C/C++ 风格原则：**所有代码都写给两类读者**——编译器和人类。编译器只关心语法正确，人类要从声明里推断语义。因此**头文件应该像书一样可读**，因为它是这个模块对人类读者的说明书。

## 两类读者

同样一份翻译单元在编译器眼里是等价的：

```c
void * load_model_from_disk(const char *);
void draw_model(void *, float, float, float);
void deallocate_model(void *);
```

但写成这样，人类能立刻猜出这是一个 3D 模型加载/绘制 API：

```c
typedef void * model_3d_ref;
model_3d_ref load_model_from_disk(const char * absolute_file_path);
void draw_model(model_3d_ref the_model, float where_x, float where_y, float where_z);
void deallocate_model(model_3d_ref kill_this);
```

差异全在参数命名和 typedef 上——对编译器零语义，对读者几乎就是文档。Supnik 把这条推成风格准则：写代码要同时服务两类读者，而**服务人类读者的成本低、回报高**。

## Header Nazi 的操作原则

如果一个模块是「有用、bug 少、封装合理」的，那么未来看头文件的时间会远远超过看实现的时间（理想情况甚至不需要看实现）。因此：

- **物理隔离优先于逻辑封装**：能放到 `.cpp` 里就放到 `.cpp` 里，而不是塞进 `class` 的 `private:` 区。后者仍会污染头文件，分散读者注意力，还容易让新手把实现当接口。C 风格的 [[c-opaque-struct-modules|opaque struct]] 把这个原则推到极限。
- **inline 写到 class 外部**：为性能必须 inline 时，把定义挪到头文件底部，声明和定义分开，保持类定义区干净。
- **说明性注释全部放头文件**：调用约定、生命周期、线程安全性——所有「要用这个 API 必须知道的事」都放头文件。实现文件里只写「为什么这么实现」这类对用户透明的内容。

这和 Ousterhout 的 [[information-hiding]] 同构：接口暴露面越小越好，实现细节越藏得深越好。物理隔离 > 逻辑封装是比 [[deep-modules|深模块]] 更强的戒律——逻辑封装只阻止调用，不阻止阅读。

## 和 [[cpp-multi-paradigm-discipline]] 的关系

Supnik 自己后来在 2019-2021 年一系列 C++ 文章里（见 [[cpp-multi-paradigm-discipline]]）依然贯彻这条：C++ 模板/继承/friend 都容易把实现泄露到头文件里，他因此偏好 `pimpl` + C ABI 接口，即使损失零售性能也要换取头文件纯净。本文是他这条长期偏好的最早源头之一。

## 相关
- [[information-hiding]]
- [[c-opaque-struct-modules]]
- [[deep-modules]]
- [[cpp-multi-paradigm-discipline]]
- [[header-file-vs-pub-export]]
- [[types-h-data-code-separation]] —— 另一种 header 组织哲学：数据集中 / 函数按功能分散

## Sources

- [[sources/supnik-coding-for-two-audiences]]
