**Day 6 · Procedures as Arguments — 函数是一等公民**

---

今天我们进入 SICP 1.3 节。如果说前五天是热身，那么从今天开始，才是这本书真正开始改变你思维方式的地方。

高阶函数（higher-order procedures）。这四个字背后藏着整个现代编程范式的根基。

我直说吧：大多数程序员用了十年 C#、写了几万行 Unity 代码，也未必真的理解高阶函数意味着什么。他们用过 `List<T>.Where()`，用过 `Select()`，甚至写过 Lambda 表达式——但他们把这些当成"语法糖"，当成"方便写法"，从没想过：这背后是一个根本性的计算哲学问题。

今天我们从源头把这件事讲清楚。

---

## 一、先感受一下"重复"的味道

SICP 给了我们三个看起来不同的过程：

```scheme
(define (sum-integers a b)
  (if (> a b)
      0
      (+ a (sum-integers (+ a 1) b))))

(define (sum-cubes a b)
  (if (> a b)
      0
      (+ (cube a)
         (sum-cubes (+ a 1) b))))

(define (pi-sum a b)
  (if (> a b)
      0
      (+ (/ 1.0 (* a (+ a 2)))
         (pi-sum (+ a 4) b))))
```

三个完全不同的数学任务。但你盯着这三段代码超过五秒钟，就会有一种说不出的不舒服感。结构几乎一模一样：检查边界，如果超出就返回 0，否则把"当前项"加上"递归调用剩余部分"。唯一的区别是当前项怎么计算、下一步怎么推进。

这种不舒服感，是一个好程序员最宝贵的直觉。你的大脑在说：**这里有一个更深层的模式，我还没把它说清楚。**

---

## 二、SICP 的核心洞见

> "These three procedures clearly share a common underlying pattern. They are for the most part identical, differing only in the name of the procedure, the function of `a` used to compute the term to be added, and the function that provides the next value of `a`... The presence of such a common pattern is strong evidence that there is a useful abstraction waiting to be brought to the surface."
>
> — SICP, Section 1.3

"**a useful abstraction waiting to be brought to the surface**"——一个等待被浮现出来的有用抽象。

这句话值得你反复咀嚼。代码重复不是懒惰的表现——代码重复是你**思维**还没到位的信号。当你复制粘贴第二次的时候，应该停下来问自己：我在重复描述什么？这个"什么"应该有自己的名字。

SICP 给了我们解法：把这个模式本身变成一个过程。

```scheme
(define (sum term a next b)
  (if (> a b)
      0
      (+ (term a)
         (sum term (next a) next b))))
```

现在 `sum` 接受四个参数，其中 `term` 和 `next` 是**过程**——不是数字，不是字符串，是过程本身。

有了 `sum`，原来的三个函数变成了：

```scheme
(define (sum-cubes a b)   (sum cube a inc b))
(define (sum-integers a b) (sum identity a inc b))

(define (pi-sum a b)
  (define (pi-term x) (/ 1.0 (* x (+ x 2))))
  (define (pi-next x) (+ x 4))
  (sum pi-term a pi-next b))
```

`sum-cubes` 现在说的是：**用 cube 作为 term，从 a 到 b，每步加 1，求和**。这不只是更短——这是直接对应数学语言的表达。∑ cube(i), i from a to b，代码就是这么写的。这才叫抽象。

---

## 三、函数作为一等公民——不是语法糖，是本体论立场

很多语言的教程把高阶函数讲成"高级特性"，把 Lambda 讲成"匿名函数的简写"。这是根本性的误解。

在 Scheme 里，函数和数字没有本质区别。你可以把数字 `5` 传给一个过程，你就可以把过程 `cube` 传给另一个过程。数字是值，过程也是值。

这就是"一等公民"（first-class citizen）的含义。一等值可以被赋给变量、可以作为参数传递、可以作为返回值、可以在运行时创建。

这个立场背后有数学基础。1930年代，数学家 Alonzo Church 发明了 **λ 演算（Lambda Calculus）**。Church 的核心洞见是：**你只需要函数，就可以表达所有的计算。** 数字？可以用函数编码。布尔值？可以用函数编码。数据结构？可以用函数编码。

λ 演算是计算本身的数学模型。Lisp 是第一个把这个思想直接翻译成编程语言的语言，Scheme 继承了这个传统，SICP 是把这个思想最清晰讲出来的教科书。

所以当你在 Scheme 里写 `(lambda (x) (* x x))`，你不是在写"匿名函数的简写"。你是在直接操作 Church 的 λ 演算。你的代码就是数学。

---

## 四、积分：高阶函数的优雅演示

SICP 紧接着展示了定积分的计算：

```scheme
(define (integral f a b dx)
  (define (add-dx x) (+ x dx))
  (* (sum f (+ a (/ dx 2.0)) add-dx b) dx))

(integral cube 0 1 0.01)
; → 0.24998750000000042  (理论值 0.25，误差在可接受范围)
```

`integral` 的第一个参数是 `f`——被积函数本身。你刚才用十几行 Scheme 代码，实现了数值积分的通用框架。`integral` 不关心你要积分什么函数——它接受任意函数 `f`，计算它的定积分。

---

## 五、现代语言的"后代"

**JavaScript Array.map/filter/reduce**

```javascript
const numbers = [1, 2, 3, 4, 5];
const sumOfSquares = numbers
  .map(x => x * x)
  .filter(x => x > 5)
  .reduce((acc, x) => acc + x, 0);
```

`map`、`filter`、`reduce` 都是高阶函数。`x => x * x` 就是 Lambda，就是 `(lambda (x) (* x x))`，换了个语法而已。

**C# LINQ**

```csharp
var result = numbers
    .Where(x => x % 2 == 0)
    .Select(x => x * x)
    .Sum();
```

`Where` = filter，`Select` = map，`Sum`/`Aggregate` = reduce。LINQ 在 2007 年随 C# 3.0 引入，是函数式编程思想几十年传播的成果，最终倒逼主流语言做出改变。

你在 2024 年写的 LINQ 查询，和 SICP 1.3 节里的 `sum` 过程，是同一个思想的不同外衣。

---

## 六、游戏开发里的高阶函数

**Tween 动画系统**

```csharp
public static IEnumerator TweenValue(
    float from, float to, float duration,
    Func<float, float> easingFunction,
    Action<float> onUpdate)
{
    float elapsed = 0f;
    while (elapsed < duration)
    {
        elapsed += Time.deltaTime;
        float t = elapsed / duration;
        onUpdate(Mathf.Lerp(from, to, easingFunction(t)));
        yield return null;
    }
    onUpdate(to);
}

// 传入不同缓动函数，行为完全不同
StartCoroutine(TweenValue(0f, 1f, 1f,
    t => t * t,                        // 二次缓入
    v => transform.localScale = Vector3.one * v));

StartCoroutine(TweenValue(0f, 1f, 1f,
    t => 1 - (1 - t) * (1 - t),       // 二次缓出
    v => material.SetFloat("_Alpha", v)));
```

通过传入不同的 `easingFunction`，你可以得到线性动画、弹性动画、反弹动画——**而不需要为每种缓动写一个新类**。这就是 SICP `sum` 的精神：把变化的部分参数化。

**Unity DOTS ECS**

```csharp
Entities
    .WithAll<Health, Damage>()
    .ForEach((ref Health health, in Damage damage) =>
    {
        health.Value -= damage.Value;
    })
    .Schedule();
```

`ForEach` 接受一个 Lambda，对每个匹配实体执行。你不关心迭代怎么做、数据怎么并行——你只说"对每个实体，执行这个操作"。把**要做什么**和**怎么做**彻底分离。

**AI 行为查询**

```csharp
// 命名良好的高阶函数让代码像英语
enemies
    .Where(IsAlive)
    .Where(IsInRange)
    .OrderBy(DistanceToPlayer)
    .Take(3)
    .ForEach(StartCombatWith);
```

每个函数名说明了意图。命名是把函数式编程的威力真正释放出来的关键。

---

## 七、品味判断

学了高阶函数之后，有些人走向极端：把所有东西都函数化，Lambda 堆叠 Lambda，写出像谜语一样的代码，暗自得意"我在写函数式"。这是坏品味。

**高阶函数的适用场景**：当你看到重复的控制流结构时。三个函数长得一样，只是某一小块不同——这时候抽象是自然的。

**高阶函数的不适用场景**：当你只有一个函数，为了"看起来函数式"而强行包装。过度抽象和代码重复一样有害。

规则是：**两次重复可以等待，三次重复就应该抽象。**

性能注意：在 Unity 的热路径（Update/ECS 热循环）里，捕获外部变量的 Lambda 会导致堆分配，触发 GC。DOTS 的 `Entities.ForEach` 正是为此专门优化的。**理解原理，然后知道在什么情况下绕过它。**

---

## 八、真正讲了什么

SICP 1.3.1 的技术内容很清晰，但真正要传达的信息更深：

- **第一层**：你可以把函数作为参数传递，这是语言特性。
- **第二层**：当你看到重复的模式，不要复制代码，要抽象出模式本身。这是工程原则。
- **第三层**：你的概念词汇表决定了你能表达什么。高阶函数给了你一个新词：**把计算的模式本身作为值来操作**。
- **第四层**：函数是计算的基本单元。函数可以被函数变换，变换的变换可以被再次变换——这是无限的抽象能力。

SICP 不是在教你怎么用 Scheme。Scheme 只是介质。SICP 在教你**如何思考计算**。

---

> 代码重复是思维还没到位的信号——当你三次复制同一个模式，你欠这个模式一个名字。

---

## 🎯 今日测验

**Q1（概念）：** 什么是"一等公民"（first-class citizen）？请用自己的话解释，为什么"函数是一等公民"比"函数可以作为参数传递"这个说法更深刻？

**Q2（应用）：** 你在 Unity 项目里有三个方法：`ApplyFireDamage()`、`ApplyPoisonDamage()`、`ApplyFrostDamage()`，它们的结构几乎完全相同，只有伤害计算公式不同。请描述如何用高阶函数重构这三个方法，合并成一个通用的 `ApplyDamage()`？

**Q3（代码）：** 用 C# 实现一个 `Accumulate` 函数，它的签名是 `T Accumulate<T>(IEnumerable<T> sequence, T initial, Func<T, T, T> combiner)`。然后用它实现求和（sum）和求积（product）两个具体操作，不允许写 for/foreach 循环。

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。
