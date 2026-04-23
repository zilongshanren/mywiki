---
tags: [计算机系统, 内存管理, 调试, C]
date: 2026-04-14
sources: 1
---

# malloc 加壳：狗牌、泄漏检测与源码定位

> 你设计的系统若用出了问题，与其怪别人用错，不如怪自己没设计好。

云风 2010 年 5 月这篇笔记是"接口设计 > 文档说教"的一次具体演绎。他挑了一个**所有 C 程序员都用过**的模块——`malloc/free/realloc`——来说明：即使是最经典、最标准的接口，也远没到"不会被误用"的地步。正确的做法不是写更长的文档，而是给 API **加一层壳**，让常见错误能被运行期尽早捕获。

## 标准 API 的四类常见错误

1. 对同一指针 `free` 两次。
2. 分配了内存但丢失了指针——泄漏。
3. 没初始化就读；或 free 后继续读/写。
4. 越界读写。
5. 忘记检查分配失败。
6. `realloc` 扩容失败后忘记释放**原**指针（返回 NULL 时原块仍有效，这是个经典陷阱，FreeBSD 为此另加了 `reallocf`）。

## 加壳策略一：收紧 API 语义

根据项目的情况**把未定义行为定义掉**：

- 云风的多数项目里，内存总量可以预估，分配永远不该失败——那就在 `my_malloc` 外壳里 `assert(ptr != NULL)`。这么一来调用方不需要写分配失败分支，代码干净很多。（他也强调这不是普适的，某些场景需要允许失败）
- `malloc(0)` 的行为在 C 标准里是**实现定义**。他选择统一返回一个有效地址（让 `malloc(0)` 等价于 `malloc(1)`），和 C++ `operator new` 的行为一致。
- 分配后用 `0xCC` 填充内存（不是 `0`——`0` 会掩盖"忘记初始化"的 bug）。`0xCC` 在 x86 里是 `int3` 断点机器码，错跳到数据区会自动触发调试；同时 `0xCCCCCCCC` 在多数 OS 上是无效地址，解引用会 crash。一个填充字节同时服务三个目的。

## 加壳策略二：狗牌（cookie）

在每次分配的内存块**前后**塞调试元数据：

```c
#define DOGTAG_VALID 0xbadf00d
#define DOGTAG_FREE  0x900dca7e
#define DOGTAG_TAIL  0xd097a90

struct cookie {
    size_t sz;
    int    tag;
};

void* my_malloc(size_t sz) {
    if (sz == 0) sz = 1;
    struct cookie *c = malloc(sizeof(*c) + sz + sizeof(int));
    assert(c != NULL);
    c->sz = sz;
    c->tag = DOGTAG_VALID;
    *(int*)((char*)(c+1) + sz) = DOGTAG_TAIL;  // 尾狗牌
    memset(c+1, 0xCC, sz);
    return c+1;
}

void my_free(void *p) {
    if (p == NULL) return;
    struct cookie *c = (struct cookie *)p - 1;
    assert(c->tag != DOGTAG_FREE);   // 双重释放
    assert(c->tag == DOGTAG_VALID);  // 乱传的指针
    int *tail = (int*)((char*)p + c->sz);
    assert(*tail == DOGTAG_TAIL);    // 尾部越界
    c->tag = DOGTAG_FREE;
    memset(p, 0xCC, c->sz);          // 抹除内容，让悬垂访问也 crash
    free(c);
}
```

**一个不显眼但关键的细节**：头狗牌不要放在 cookie 的第一个字段。高效的 `malloc` 实现（freelist）常常把已释放块的**头 8 字节**拿去当 freelist 的 next 指针——如果你的狗牌就在头 8 字节，会被覆盖，双重释放检测就失灵了。把狗牌放在 cookie 的第二个字段更稳。

## 加壳策略三：源码定位

需要知道是**哪行代码**分配的这块内存？用宏替换：

```c
#define malloc(sz) malloc_proxy(__FILE__, __LINE__)(sz)

typedef void* (*malloc_f)(size_t);

malloc_f malloc_proxy(const char *file, int line) {
    g_filename = file;
    g_line     = line;
    return my_malloc;
}
```

几个妙处：

- `malloc_proxy` 返回一个**函数指针**而不是直接调用，这样 `malloc` 这个宏在**函数指针赋值**上下文（`func_ptr = malloc;`）依然正确——直接 `#define malloc my_malloc` 会在这种写法下出错。
- `__FILE__` / `__LINE__` 通过全局变量旁路传递而非多加参数，保证 `my_malloc` 签名不变。多线程下全局变量会有小竞态，但无伤大雅，也好回避（改成 TLS 即可）。
- `my_malloc` 从全局变量里取出信息写进 cookie，断言时的错误信息就能定位到分配处。

## 加壳策略四：生命期分类 + 泄漏检测

云风把动态分配分成两类：

- **一次性分配**（单件、全局表、常驻资源）：专用一个 API 分配、打特殊 tag，任何对它的 `free` 都 assert 失败。进程退出时由 OS 回收。
- **真正动态的分配**：串成双向链表，程序退出前扫描链表检测泄漏。（MFC 的经典做法）

把这两类分开后，泄漏检测就只需要关注真正的动态部分，信号噪声比高多了。

## 为什么要这么做

这篇文末回到了他的中心主题：**接口设计时就应该预判使用者会怎样用错**。文档和口述都是脆弱的补救。给 API 加壳的成本低、收益高，是务实的 [[information-hiding]]：把"内存安全"这一决策藏在 `my_malloc` 里，上层代码不需要改变用法就自动得到保护。

## 相关
- [[virtual-memory]]
- [[linear-allocator]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[cloudwu]]
- [[custom-allocator-interface]] — Bitsquid 的 proxy/trace allocator 是另一套同目标的加壳思路

## Sources

- [[sources/cloudwu-malloc-wrapper]]
