---
tags: [软件设计, C, 面向对象, 接口设计]
date: 2026-04-14
sources: 1
---

# C 语言下的接口式面向对象

云风不喜欢用 C 宏去"模拟"C++ 的对象模型。他认为 C++ 的继承把虚表、字段布局、继承关系全糅在一起，是**过紧的耦合**，也把实现性能上的决策直接硬写进语言层——这跟 C++ 里被滥用的 `inline` 一样破坏了分离原则。真要在 C 里做面向对象，他偏爱一种朴素的"接口表 + 数据指针"组合。

## 出发点：面向对象是"共同操作方式"

他对 OOP 的理解不是"类继承树"，而是"**让一组数据拥有相同的操作方式，可以成组处理**"。这些共同操作方式叫**接口**，在 C 里就是一组函数指针，在 C++ 里就是虚表。同一个数据可以同时符合多个接口，取决于你从哪个切面提取共性。

这也是他长期以来对 UI 框架、3D 场景图这类需要多态调度的场合用 OOP 的动机——用，但用得克制。

## 范式：`foo_object` = 接口表 + data

假设我们想让一组数据都具备某种 `foo` 特性，云风的写法：

```c
/* foo.h */
struct foo_object;
struct i_foo {
    void (*dosomething)(void *data, int arg);
    /* ... */
};
struct foo_object* foo_create(struct i_foo *iface, void *data);
void  foo_release  (struct foo_object *self);
void  foo_dosomething(struct foo_object *self, int arg);
```

```c
/* foo.c */
struct foo_object {
    struct i_foo *iface;   /* 虚表 */
    void         *data;    /* 派生类扩展的数据成员 */
    /* 基类自身的字段也可以放这里 */
};

void foo_dosomething(struct foo_object *self, int arg) {
    self->iface->dosomething(self->data, arg);
}
```

每种"派生类"在自己的 `.c` 里实现一个 `i_foo`（通常是一个 `static` 全局的函数指针结构），并提供一个 `xxx_to_foo()` 方法把自己包装成 `foo_object`。

## 组合而非继承

C++ 用"继承"扩展数据成员，这里用**组合**：`foo_object` 里存一个 `void *data` 指向派生类自己的结构。这多了一层间接，却换来了**更低的耦合**——

- `foo` 的实现文件完全不需要知道任何派生类的内存布局。
- 派生类不受 `foo_object` 基类字段的物理约束，可以自由演化。
- 同一个 `data` 可以同时被包装成 `foo_object` 和 `bar_object`，对应两种接口。

这就是云风所说的"创造积木"的 C 哲学，和 C++ 的 "all-in-one" 继承树形成对照。

## 生命期分离

一个微妙而关键的决定：`foo_object` **不负责 `data` 的生命期**，只负责释放它自己这壳。生命期管理是另一个维度的问题，应当独立出来（交给 Lua GC、或另写一层 C 模块管理）。他说得很重：

> 生命期管理是大多数 C/C++ 软件的复杂度重要来源。

把 object 的"类型语义"和"生命期语义"分层，代码量显著减少，也更不容易写错。这个思路和他用 Lua 做对象生命期载体的做法一脉相承——参见 [[cloudwu]]。

## 零碎但有用的 C 陷阱

同一篇文里他还顺带提醒：

- `void *` 在 C 里可以和任意数据指针互换赋值（C++ 会警告）；
- `void (*foo)()` 是"接受任意参数列表"的函数指针——要想让编译器帮你抓出"多传了参数"的错误，一定要写成 `void foo(void)`；
- 结构初始化在 C89 下很脆弱，C99 的**指定初始化器**（按字段名）可以大幅降低写虚表时的出错概率，值得采用。

## 相关

- [[modular-design]]
- [[c-opaque-struct-modules]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[dependencies]]
- [[cloudwu]]

## Sources

- [[sources/cloudwu-c-serialization-and-c-oop]]
