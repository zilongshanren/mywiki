---
tags: [source, 编程语言, go, 并发, 网络编程]
date: 2026-04-14
sources: 1
---

# Go 语言初步（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 11 月的博客，记录他用 Go 写了大约两千行代码后的第一手感受，并顺带用 Go 重写了自己 2006 年写过的多连接汇聚服务器。

## 摘要

他喜欢 Go 的理由几乎都指向"语言层面支持了我多年在 C 里手写的规范"：mix-in 风格的 interface 替代继承层次、强类型配合包系统让写法像 Lua 却稳如 C、`defer + panic/recover` 干净地取代了 RAII 与 exception、零初始化贯彻到底、包 init 明确而无 exit、goroutine + `select/chan` 让 CSP 风格并发变成默认写法。他坦言自己花八年锤炼出的 C 编程规范，到头来"只是拙劣地模仿 Go"。实战练手项目是把一个 N 对 1 TCP 汇聚服务器重写成 240 行 Go：外部连接用独立 goroutine 阻塞处理，主循环用 `select` 做事件多路复用；控制指令走 0 号特殊连接，由 in-memory pipe 转成 bufio.Reader 按行解析指令，再经 chan 送回 select 循环；唯一需要手工优化的是给每个包加三字节头时从 16 K array 借 slice 避免 per-packet `make`。最后他强调 Go 的"引用 vs 值"分得比 Java 清楚、Reader/Writer 接口让 socket 与 file 统一，"暗合 Unix 之道"。

## 关键要点

- Go 的 interface 是 mix-in 组合而非继承层次，与他多年用 C 搭对象模型的风格一致
- `defer / panic / recover` 比 C++ 栈对象析构和 exception 干净
- 零初始化 + 内置 `string / slice / gc` 是"现代编程必须"的基础
- 包系统只有 init、没有 exit，正合"模块只能构造不能析构"的哲学
- goroutine + `select/chan` = Erlang 的模型 + C 系血统
- 240 行 Go 重写 2006 年的 N 对 1 连接服务器，几乎不需要性能调优
- Go 区分引用与值比 Java 清晰，却比 C++ 安全

## 链接到的概念

- [[go-goroutine-channels]]
- [[connection-multiplexer-gateway]]
- [[c-interface-oop]]
- [[garbage-collector]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/11/
- 本地：`raw/articles/blog.codingnow.com/2010-11-18_yun-feng-de-blog.md`
