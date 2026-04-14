---
tags: [编程语言, C++, 反射, 元编程, 类型系统]
date: 2026-04-14
sources: 1
---

# C++ 运行时反射（via 元编程）

C++ 没有原生的**运行时类型内省（reflection）**。与 Go、Jai、C#、Java 这些把「问一个 type 的成员有几个」作为一等公民的语言不同，C++ 只提供 `typeid` 这种返回 name 字符串的最基本特性。这让「自动序列化」、「自动 UI 编辑器」、「自动网络打包」这些生产力特性只能靠以下三条路走：

1. **手写 macro**：每个要反射的 struct 写一串 `REFLECT_MEMBER(...)`，代码重复、心智负担高。
2. **模板黑魔法**：`boost::hana`、`magic_get`、`refl-cpp` 用 template/SFINAE 提取 tuple-like 结构——功能受限、编译慢。
3. **外部工具生成代码**：用 clang 解析 AST 然后自动写 register 代码。Max Slater 的 Exile 引擎走的就是这条。

## Exile 的方案：libclang + 代码生成

整体架构很简洁：

- 一个**全局 type table**（`type_id → _type_info` 的哈希表），`_type_info` 是一个带标签的 union：`void | int | float | ptr | struct | array | enum | ...`，每个分支装该 type 的元数据（大小、名字、成员列表等）。
- 一个**单独的元程序（meta-program）**——用 `libclang` 解析项目的 C++ 源，遍历 AST，对每个 struct 定义生成 C++ 代码，把该 struct 的 `_type_info` 填充进 type table。构建系统在编译前先跑一次元程序，再 include 它的输出。
- 运行时入口 `TYPEINFO(T)` 是一个宏包装：内部靠 `typeid(T).hash_code()` 得到 key，查表返回 `_type_info*`。对**指针类型**用 SFINAE 做 lazy 插入——`int**` 在第一次被请求时自动创建指向 `int*` 的节点，`int*` 又自动创建指向 `int` 的节点，形成一条递归链。

## 用途展示

有了这套，一个全泛型 `print_struct<T>` 就能把任意类型的成员逐个打印：

```cpp
template<typename T>
void print_struct(T value) {
    uint8_t* addr = (uint8_t*)&value;
    _type_info* info = TYPEINFO(T);
    for (int i = 0; i < info->_struct.member_count; i++) {
        print(info->_struct.member_names[i]);
        uint8_t* m = addr + info->_struct.member_offsets[i];
        print_type(m, TYPEINFO_H(info->_struct.member_types[i]));
    }
}
```

同一个机制直接喂给 ImGui 就得到 `ImGui::EditAny(&any_value)`——用 [[debug-visualization|debug UI]] 修改任何 struct 字段，不需要手写编辑器。

## 局限

- **不处理 OOP**：方法、构造/析构、继承、虚函数都没反射。适合 C 风格的 POD，不适合现代 C++。
- **循环依赖**：原始实现用 AST 顺序输出 type info，相互引用的 type 会有顺序问题——后来才改成先输出空壳再填充。
- **深度嵌套模板**：`std::vector<std::pair<int, std::map<K, V>>>` 这种 libclang 可以解析但 instance 信息展开很脆弱——libtooling 里的 Sema 有更准的类型依赖图，但用起来重。
- **RTTI 的依赖**：虽然 Slater 的实现关闭了 RTTI，但 `typeid` 仍然可用——它对编译时已知类型不需要 RTTI 支持。
- **绝对 name collision 风险**：`hash_code()` 没保证无冲突，健壮实现应用 `std::type_index`。

## 和 Jai 的对比

Jai 这种新语言把反射作为一等公民，`#run` 编译期元编程可以直接看到 AST 并生成代码——没有外部工具这层。Exile 的元程序路线是在 C++ 生态里用尽量少的语言依赖、**把缺失的语言特性补丁进去**的典型案例，思路和 Unreal 的 UHT（Unreal Header Tool）或 Qt 的 moc 一脉相承。

## 相关

- [[higher-order-functions]] — 反射信息本身就是一阶值
- [[abstraction]] — 反射是「把类型作为数据」的一种抽象
- [[max-slater]]

## Sources

- [[sources/slater-exile-reflection]]
