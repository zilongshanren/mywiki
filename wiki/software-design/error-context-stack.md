---
tags: [error-handling, debugging, scope-guard, thread-local, bitsquid]
date: 2026-04-19
sources: 1
---

# Error Context 栈：用作用域变量给 assert 加上现场

深层工具函数（比如 `parse_json_number`）崩溃时，它并不知道自己是在解析哪份文件、处理哪个 unit——但这正是报错最需要的背景。[[niklas-frykholm]] 在 Bitsquid 给出一个小而好用的模式：**thread-local 的 push/pop 字符串指针栈**，用 RAII 作用域变量管理。

## 接口

```cpp
void init(const char *file)
{
    ErrorContext ec("Parsing JSON:", file);
    JsonDoc *doc = parse_json(file);
}
```

实现极简——两个 `__THREAD` 的 `Array<const char *>`，构造压栈、析构弹栈：

```cpp
class ErrorContext {
public:
    ErrorContext(const char *name, const char *data) {
        _error_context_name->push_back(name);
        _error_context_data->push_back(data);
    }
    ~ErrorContext() { /* pop both */ }
};
```

崩溃时把整个栈打印出来：

```
When spawning level: big_world
When spawning unit: big_bird
When applying material: feathers
Assertion failed: texture != NULL
Texture not loaded: yellow_feathers
```

## 为什么只存指针

每层 context 只推 8 字节（两个指针），不拷贝字符串——前提假设是「字符串生命周期 ≥ ErrorContext 生命周期」，由作用域变量天然保证。这样开销几乎为零，可以在频繁调用的路径上大量使用而不用担心性能。

## 对比异常 decoration 方案

C++ 异常阵营的等价做法是 catch + 加信息 + rethrow，但有两个坏处：一是异常对象必须预先为所有上层可能想加的字段建 member（否则要抛新异常，但位置又错了）；二是这种模式太啰嗦，实际代码里几乎没人坚持得下来。Niklas 的断言：「我没见过一个代码库系统性做 exception decoration 的」。用 context 栈 + 崩溃报告反而更稳定、更一致，而且和 [[crash-on-unexpected-errors]] 的整体哲学咬合。

## 相关

- [[crash-on-unexpected-errors]]
- [[minimize-points-and-types-of-failure]]

## Sources

- [[sources/bitsquid-sensible-error-handling-part-1]]
