---
tags: [language-design, oop, closures]
date: 2026-04-19
sources: 1
---

# 方法绑定语义：隐式 vs 显式

从一个对象实例取出方法时，**`this` / `self` 是不是自动跟着走**，是一个看似细枝末节、实则影响大量业务代码（尤其是事件/回调系统）的语言设计选择。

## 两种策略

**隐式绑定**（AS3、JavaScript 的 ES2015+ arrow methods、Python 3 的 bound method）：从实例读方法引用时，返回一个已经绑好 receiver 的可调用值。

```as3
var a:Array = [1,2,3];
var f:Function = a.join;
f(",");  // "1,2,3"，f 记住了 a
```

**显式绑定**（C++98 成员函数指针、早期 JS 裸 `function`、C#「方法组」要显式 new delegate）：取出来的是未绑定方法，调用时必须另外提供 receiver，或用 `.bind(this)` / `std::bind` / lambda 包一层。

## 事件订阅的对称性问题

显式绑定会破坏 add/remove 对称：

```js
// 裸 function 在 JS 里每次 bind 生成新函数，removeListener 无法匹配
button.addEventListener('press', this.onPress.bind(this));
button.removeEventListener('press', this.onPress.bind(this));  // 失效
```

隐式绑定下写起来自然：

```as3
buttonA.addEventListener(Event.PRESS, oojamaflip.flipOut);
// ...后面
buttonA.removeEventListener(Event.PRESS, oojamaflip.flipOut);
```

不需要把 bound 引用存到字段里当 key，add/remove 天然匹配。

## 代价

隐式绑定的代价在于性能与内存：取一次方法就要产生一次 bound object（或至少一次闭包分配）。JIT 可以把热路径优化掉，但冷路径仍多一次分配。C++ 坚持显式绑定，部分原因就是零开销原则——成员函数指针只是一个偏移。

## 现代语言的取舍

- Python 3 bound method、Kotlin 成员引用、Swift 方法值：都走隐式绑定
- Rust 的 `instance.method` 严格讲是 UFCS 糖，需要 `|| instance.method()` 才能拿 closure；属于中间态
- C# 的「method group」在 delegate 转换时隐式绑定，但要求声明 delegate 类型，仍带一些仪式感

Boris 的观点是：**隐式绑定应当作默认**，事件系统、回调、高阶函数全吃这个简洁。

## Sources

- [[sources/boristhebrave-as3-gems]]
