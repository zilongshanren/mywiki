---
tags: [c++20, 协程, promise_type, 异步, 工厂模式]
date: 2026-04-27
sources: 3
---

# C++20 协程：promise_type、工厂语义与 co_await 即 .then

Ben Supnik 的五篇系列文章（前三篇）把 C++20 协程机制拆成三个直觉：**命名槽**、**工厂函数**、**链式延续**。

## promise_type 是控制块，不是承诺

C++ 标准把协程的"控制结构体"命名为 `promise_type`，Supnik 认为这是一个误导性名称——它与 `std::promise` / `std::future` 模型几乎没有关系。更准确的称呼是"traits"或"control block"，因为它实际承担三件事：

1. **生命周期策略**：`initial_suspend` 决定协程创建后是否立即运行；`final_suspend` 决定结束后是否自我销毁。
2. **CPU 控制流**：由于挂起点本身是 awaitable，可以在起点和终点"跳转"到任意其他协程。
3. **Handle 类型**：决定调用方拿到什么句柄。

最小可用的 `promise_type`（"fire and forget"）：`initial_suspend` → `suspend_never`，`final_suspend` → `suspend_never`，`return_void` 留空，`unhandled_exception` 留空。

## 协程看起来像函数，用起来像工厂

这是理解 C++20 协程语义的关键转变：你**写**的是函数体，调用方**得到**的是一个指向新建协程状态机的 handle。调用一次 `fetch_file(url, path)` 并不是"运行 fetch_file"，而是"创建一个 fetch_file 协程实例，让它跑到第一个 `co_await` 就返回"。

fire-and-forget 模式下，调用方拿到的 handle 几乎无用——协程自己跑完自己死。这和 callback 式的"发出请求，结果在回调里处理"完全等价，适合把旧 callback API 包装成更可读的顺序代码。

```cpp
async fetch_file(string url, string path) {
    string data = co_await http::download_url(url);
    co_await disk::write_file_to_path(path, data);
}
// 调用方：for (auto spec : list) fetch_file(spec.url, spec.path);
// 每次调用立即返回，所有 IO 并发进行
```

## co_await 是协程的 .then

在基于 continuation / future 的异步系统里，`.then(lambda)` 表达的是"**此后**发生的事"——不关心何时运行，只关心在前置操作完成**之后**运行。`co_await` 提供完全相同的语义，但把 continuation 写成直线代码而不是嵌套 lambda。

```cpp
// callback 版
future<string> data = file.async_load("~/stuff.txt");
data.then([data]{ printf("%s\n", data.get().c_str()); });

// co_await 版（等价语义）
string data = co_await file.async_load("~/stuff.txt");
printf("%s\n", data.c_str());
```

凡是有"完成后回调"接口的对象都可以包装成 awaitable：线程池调度、非阻塞 I/O、按需加载对象、串行队列（非阻塞 mutex 等价物）。`await_suspend` 会把当前协程的 `coroutine_handle` 传给 awaitable，awaitable 可以将其存入 FIFO 或任意数据结构，在正确时机调用 `resume()`。

## 与已有概念的关系

- [[coroutine-awaitable-pattern]] — 更深入地拆解 awaitable 与协程的接口协议
- [[stackless-vs-stackful-coroutines]] — C++20 选择 stackless 的原因及限制
- [[closure]] — co_await 之后的代码本质上是被编译器生成的闭包

## Sources

- [[sources/supnik-coroutines-1-names]]
- [[sources/supnik-coroutines-2-factories]]
- [[sources/supnik-coroutines-3-coawait]]
