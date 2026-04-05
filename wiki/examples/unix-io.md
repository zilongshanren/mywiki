---
tags: [经典案例, 深模块, 接口设计, aposd]
date: 2026-04-05
sources: 2
---

# Unix I/O —— 深模块的标杆

Unix I/O 是 Ousterhout 举的**最经典的 [[deep-modules|深模块]] 例子**。

五个系统调用：

```c
int open(const char* path, int flags, mode_t permissions);
ssize_t read(int fd, void* buffer, size_t count);
ssize_t write(int fd, const void* buffer, size_t count);
off_t lseek(int fd, off_t offset, int referencePosition);
int close(int fd);
```

就这五个。

## 隐藏在背后的

> "A modern implementation of the Unix I/O interface requires hundreds of thousands of lines of code, which address complex issues such as:
> - How are files represented on disk in order to allow efficient access?
> - How are directories stored, and how are hierarchical path names processed?
> - How are permissions enforced?
> - How is functionality divided between interrupt handlers and background code?
> - What scheduling policies are used when there are concurrent accesses?
> - How can recently accessed file data be cached in memory?
> - How can a variety of different secondary storage devices be incorporated into a single file system?"

几十万行代码处理磁盘布局、目录结构、权限、中断、并发、缓存、设备抽象——全部隐藏在这五个函数后面。

## 调用者的视角

你只需要知道：
- `open` 打开文件，返回文件描述符
- `read` 从文件读数据
- `write` 向文件写数据
- `lseek` 调整读写位置
- `close` 关闭文件

你不需要知道文件系统实现、缓存策略、并发访问处理。这些复杂性全部被接口的简洁性「吃掉了」。

## 接口的稳定性

> "Implementations of the Unix I/O interface have evolved radically over the years, but the five basic kernel calls have not changed."

接口几十年不变，实现可以大幅改进——这是深模块的另一重好处：**实现的变化不会影响调用者**。

## 常见情况优先

> "In contrast, the designers of the Unix system calls made the common case simple. For example, they recognized that sequential I/O is most common, so they made that the default behavior. Random access is still relatively easy to do, using the lseek system call, but a developer doing only sequential access need not be aware of that mechanism."

**把常见情况做简单，把不常见情况做可能**。这是接口设计的黄金法则。缓冲作为内核默认，不需要调用者显式请求——对比 [[java-io]] 的显式 `BufferedInputStream`，这是完全不同的设计哲学。

## 相关

- 体现的原则：[[deep-modules]]、[[information-hiding]]、[[interface-vs-implementation]]
- 反面案例：[[java-io]]
- 更深的同类：[[garbage-collector]]

## Sources

- [[sources/aposd-day04]]
- [[sources/aposd-day05]]
