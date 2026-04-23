---
tags: [异步, API, 回调, future, promise, 设计, bitsquid]
date: 2026-04-19
sources: 1
---

# 异步 API 的极简设计：ID token 与 implicit API

[[niklas-frykholm|Niklas Frykholm]] 2012 年讨论异步 API（leaderboard、web fetch 这类有延时返回的调用）的设计选择，给出一条非常 Bitsquid 味的主张：**对象越少越好，有时候最好的 async API 看起来根本不像 async**。

## 四种选择，从差到好

### 1. 回调——不好

```cpp
leaderboard->set_score(100, set_score_cb, my_user_data);
```

Niklas 点名四类毛病，延续了他在 [[polling-callbacks-events]] 里的立场：

- **调用时机失控**——回调可能在你 `update_leaderboard()` 之外触发，打乱你精心设计的每帧秩序。
- **回调里能做什么不明**——callback 里删一下正在被遍历的 `_leaderboard_operations` vector，立刻崩；这类 bug 他被咬过无数次。"每次我看见一个 callback，脑子里警钟响起：danger——any thing can happen."
- **context 总是错的**——回调在 global / top-level context 发生，然后必须 cast `user_data` 再钻到真正知道该干什么的代码——**代码流难读**。
- 总结：难读、难追踪、埋暗 bug、引 cache miss。

### 2. Request 对象 / C++11 futures——还是过度

```cpp
SetScoreRequest *request = _leaderboard->set_score(100);
if (request->is_done()) { ... delete request; }
```

比回调好，但"多一个对象就好"的 OO 教条。Niklas 的反对集中在：

- 这些对象**什么实事也不干**——只是一个在你代码和 `_leaderboard` 之间来回传话的中间人。
- 调用者要存放它们、记得释放——错过就是 leak。
- 要把 API 暴露给脚本层（Lua）？每个 request 对象都要额外 bind，噪音。

### 3. ID token——他推荐的基线

```cpp
unsigned set_score(int value);
enum SetScoreResult {SSR_IN_PROGRESS, SSR_SUCCESS, SSR_FAILURE, SSR_NO_INFORMATION};
SetScoreResult set_score_result(unsigned id);
```

- 没有需要 user 持有的对象；ID 自然可被 Lua 这类脚本语言使用。
- **不设 release 接口**——release API 既是负担也易错。
- 存储用定长 **round-robin buffer**：只记最近 64 次的结果。超过 64 次之前的请求？直接返回 `SSR_NO_INFORMATION`。

```cpp
static const int MAX_IN_FLIGHT = 64;
char results[MAX_IN_FLIGHT];
unsigned num_requests;

SetScoreResult set_score_result(unsigned id) {
    if (num_requests - id > MAX_IN_FLIGHT)
        return SSR_NO_INFORMATION;
    return results[id % MAX_IN_FLIGHT];
}
```

64 字节换掉所有显式的"所有权管理"——Niklas 认为这个 trade 非常划算。这个手法与 [[id-based-lifetime-with-kill-flag]] 是同一家族的思路：**用固定容量的环形容器替代精细的生命期追踪**。

### 4. Implicit API——最优解

最彻底的一步是**让用户根本不需要知道这是 async 操作**：

```cpp
/// Sets the score. This is async internally.
void set_score(int score);
/// Returns the last score acknowledged by the server.
int acknowledged_score();
```

用户只关心"我设过的分" vs "服务器确认的分"，而不关心 request 的生命周期。再极端一点——一个异步 web fetcher 的 API 可以是：

```cpp
const char *fetch(const char *url);
```

还没拿到就返回 NULL；拿到后下一次调用返回数据；再下一次自动 free。一个函数。

## 可迁移的设计准则

- **把异步性当实现细节而非 API 语义**——能抽掉就抽掉。
- **ID 优于对象**——尤其当对象没行为、只是个通知载体时。
- **固定容量优于 unbounded**——既解决了 "谁来释放" 也自动给出 back-pressure 行为（超限直接 `NO_INFORMATION`）。
- **牺牲通用性换简洁**：64 条的上限、只看"最后一次确认的状态"——都放弃了某些使用场景，但换来 API 的根本简化。

评论区有人提到用 signal / slot + copy-on-write vector 应对"在回调中删自己"的问题——Niklas 并不反对在局部场景这么做，但仍强调："你能抽掉异步语义就去抽"。

## 相关

- [[niklas-frykholm]]
- [[polling-callbacks-events]] — 同一作者更早的 callback vs poll 立场
- [[system-decoupling-patterns]] — ID 引用作为解耦第四原则
- [[id-based-lifetime-with-kill-flag]] — ID 替代 pointer 的生命期管理
- [[api-fast-path-design]] — 另一种"把实现细节藏在接口背后"的例证

## Sources

- [[sources/bitsquid-simpler-async-api]]
