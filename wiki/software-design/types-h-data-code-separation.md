---
tags: [cpp, header-organization, compile-time, 数据代码分离, bitsquid]
date: 2026-04-19
sources: 2
---

# types.h：把数据定义集中、把函数按功能分组

这是 [[niklas-frykholm|Niklas Frykholm]] 2012 年在 Bitsquid Blog 提出并后来在 [[bitsquid-foundation-library-concept]] 里落地的 C++ header 组织方式。一句话：**一个 `types.h` 收纳所有 struct/class 的裸数据定义与前向声明；函数按"做什么"而不是"对谁做"分散到独立 `.h/.cpp`**。目标是同时治 C++ 的两个病——include 图传染导致的编译时间膨胀、OOP 方法绑定导致的 class 膨胀。

## 为什么两病同源

标准 C++ "一类一对 header" 让 `array.h` / `vector3.h` 这种基础类型变成"中层 header 的必入客"，一个 #include 传染一片 TU，配合模板和 inline 就走向 [[header-hero-compile-analysis|blowup factor 30+]] 的不归路。回头砍依赖是典型的[[yak-shaving]] 活。

OOP 的"data + method 绑在一个 class"看似内聚，实际把序列化、endian swap、脚本绑定、网络同步这些**横切关注**都塞进 class 里，class 越长越胖；外部函数永远是二等公民。Frykholm 认为这两件事的根都是**"按类型组织代码"**。

## 做法

**`types.h`：只留骨架**

```cpp
struct Vector3 { float x, y, z; };

template <class T>
class Array {
public:
    Array() : _capacity(0), _size(0), _data(nullptr) {}
    ~Array() { free(_data); }
    unsigned _capacity, _size;
    T *_data;
};

class IFileSystem;   // 引用型前向声明
class INetwork;
```

- 按值使用的类型：完整结构体 + C++ 强制的 ctor/dtor/operator，无其它成员函数
- 按引用使用的类型：**仅前向声明**；它们是纯虚接口，由 factory 函数构造（`make_file_system()`）

因为只有类型骨架，`types.h` 本身编译极快；**它是"按值用类型"的唯一入口**，任何 header 只需 include 它就够，不必再级联拉取 `array.h`、`vector3.h`。

**函数按功能组织**

```cpp
// vector3.h
inline Vector3 operator+(const Vector3 &a, const Vector3 &b) { ... }

// array.h
namespace array {
    template<typename T> inline uint32_t size(const Array<T> &a) { return a._size; }
    template<typename T> void push_back(Array<T> &a, const T &item);
}

// serialization.h   ← 所有类型的序列化都在这里
// path.h            ← 所有路径相关的字符串操作
```

真正用到这些操作的 `.cpp` 才 include 相应 header；外部代码可以写 `array_extensions.h` 在 `array` namespace 里追加 `shift` / `binary_search`，与官方函数**地位完全对等**——这一点在传统 OOP 写法里不可能（成员函数永远比 free function 一等）。

## 工程护栏与代价

Frykholm 承认 private 没了：外部可以直接改 `Array::_size`。护栏靠**命名约定**：

- `class Foo { ... };` + 成员带下划线 `_bar` → 视为内部，摸了后果自负
- `struct Foo { int x; };` + 成员不带前缀 → 公开 POD，直接摸是允许的
- 需要真正封装的类型（IFileSystem）走纯虚接口 + factory，根本不暴露数据

还假设一个**零状态即合法**的约定：成员全零是有效空状态。这让 ctor 退化为 `memset`，容器能用 `memmove` 搬数据（[[bitsquid-foundation-library-concept]] 里的集合类正是这么做的）。

代价主要两条：

1. **`types.h` 是重编译热点**：改一次触发全工程重建。Frykholm 的反驳是基础类型改动本身稀少；遇真正大仓可以切成 `math_types.h`、`collection_types.h` 等少数几个 shard，但不要每个类一个 `*_types.h` 文件——那就回到"文件杂耍"。
2. **DRY 有轻微违反**：函数原型要在 `.h` 声明、在 `types.h` 附近的宏/trait 里可能还要再映射一次。对 [[orthodox-cpp]] 的拥趸这是特性不是 bug——相比 inline 函数搬到 `.inl` 文件的"三件套"方案，Frykholm 这一套更彻底地把数据和函数拆开。

## 与其它主张的对照

- **[[c-opaque-struct-modules]]**：C 语言里常见的"把 struct 定义藏到 `.c`、头里只有 `typedef struct Foo Foo; Foo *foo_create();`"是这个模式的**反面**——把数据完全藏起来；Frykholm 的主张是反着来：**把数据完全暴露**，只在命名约定层加护栏。两套都能让 header 瘦；选哪条看你更怕哪件事（外部瞎改 vs. 封装成本）。
- **[[orthodox-cpp]]**：Karadžić 的 C+ 主张是"写得像 C 一样的 C++"，Frykholm 这套 types.h 是它的一个具体 header 层落地样板。
- **传统 `.h + .inl + .cpp` 三段**：保留 `.h` 里的函数声明和 `.inl` 里的 inline 实现——只拆"声明/实现"，不拆"数据/函数"。适合 library 作者想保留 OOP 风格的场景；Frykholm 这套适合引擎内部追求极简与可扩展。

## 落地处

Bitsquid Foundation Library 公开代码里 `collection_types.h` 放 `Array<T>` / `Hash<T>` / `Queue<T>` 骨架，`array.h` / `hash.h` / `queue.h` 放 namespace 内函数。`string_stream` 没有自己的类型，直接操作 `Array<char>`；`hash` 与 `multi_hash` 两套接口共享 `Hash<T>` 数据——这正是"函数按功能组织"的收益：同一块数据可以被多套互不知晓的算法自由扩展。

## 相关

- [[niklas-frykholm]]
- [[bitsquid-foundation-library-concept]]
- [[header-hero-compile-analysis]] —— include 图传染的度量工具
- [[header-as-user-manual]]
- [[c-opaque-struct-modules]] —— 隐藏数据的反面做法
- [[orthodox-cpp]]
- [[custom-allocator-interface]] —— Bitsquid 体系里另一半骨架

## Sources

- [[sources/bitsquid-organizing-header-files]]
- [[sources/bitsquid-foundation-library]]
