# Day 5 · Primality Testing — 概率与确定性的哲学

**SICP §1.2.6 | 当「大概率正确」比「绝对正确」更有价值**

---

前四天我们从过程抽象走到递归的两张面孔，再走到增长阶和快速幂。今天，SICP 带来一个思维上的跳跃——

**算法不一定需要给出正确答案。**

这在 1985 年的教材里是一个相当大胆的声明。今天，概率算法已经成为密码学、分布式系统、机器学习的基石，但在 80 年代，主流观念仍然是「算法必须正确，否则就不叫算法」。

SICP 在第一章第六节就打破了这个教条。

---

## 一、判定素数的朴素方法

SICP 先给出了一个朴素但正确的素数判定算法：

```scheme
(define (smallest-divisor n)
  (find-divisor n 2))

(define (find-divisor n test-divisor)
  (cond ((> (square test-divisor) n) n)
        ((divides? test-divisor n) test-divisor)
        (else (find-divisor n (+ test-divisor 1)))))

(define (divides? a b)
  (= (remainder b a) 0))

(define (prime? n)
  (= n (smallest-divisor n)))
```

逻辑很直接：从 2 开始逐个测试，看 n 能被哪个数整除。如果测试到 √n 还没有找到因子，n 就是素数。

为什么只需要测试到 √n？SICP 给了一个脚注解释：

> "The end test for find-divisor is based on the fact that if n is not prime it must have a divisor less than or equal to √n."

如果 n 有一个大于 √n 的因子 d，那么 n/d 一定是一个小于 √n 的因子。所以你一定能先找到那个小的因子。

这个算法的增长阶是 Θ(√n)。

对于小数字没问题。但对于密码学中使用的素数（比如 RSA 中几百位长的素数），√n 本身就是一个天文数字。朴素方法完全不可行。

---

## 二、Fermat 小定理——从数论到算法

接下来 SICP 引入了费马小定理（Fermat's Little Theorem）：

> "If n is a prime number and a is any positive integer less than n, then a raised to the nth power is congruent to a modulo n."

翻译一下：**如果 n 是素数，那么对任意 a（0 < a < n），aⁿ ≡ a (mod n)**。

这个定理的逆否命题是：**如果 aⁿ ≢ a (mod n)，那么 n 一定不是素数。**

这就是 Fermat 素性测试的核心思想。

关键在于：这个定理只给出了**必要条件**，不是**充分条件**。如果 n 通过了测试（aⁿ ≡ a mod n），n **大概率**是素数，但不能 100% 保证。

SICP 对此的描述非常精确：

> "If the result is not equal to a, then n is certainly not prime. If it is a, then chances are good that n is prime. Now pick another random number a and test it with the same method. If it also satisfies the equation, then we can be even more confident that n is prime."

每次测试用一个随机 a。如果失败 → 100% 确定不是素数。如果成功 → 只能增加信心。

---

## 三、expmod——快速幂的模运算版本

Fermat 测试需要计算 aⁿ mod m。直接算 aⁿ 会溢出（aⁿ 增长极快），但利用模运算的性质和快速幂，可以在每一步都取模：

```scheme
(define (expmod base exp m)
  (cond ((= exp 0) 1)
        ((even? exp)
         (remainder
          (square (expmod base (/ exp 2) m))
          m))
        (else
         (remainder
          (* base (expmod base (- exp 1) m))
          m))))
```

这个 `expmod` 和 Day 4 的 `fast-expt` 几乎一模一样，只是每一步都做了 `remainder`。

> "This is very similar to the fast-expt procedure of 1.2.4. It uses successive squaring, so that the number of steps grows logarithmically with the exponent."

增长阶：Θ(log n)。

对比：
- 朴素素性测试：Θ(√n)
- Fermat 测试：Θ(log n)

对于密码学中使用的素数（比如 300 位的数字），√n 大约是 10¹⁵⁰ 量级，而 log n 只有 1000 左右。这是 10¹⁴⁷ 倍的速度差距。**不是快一点，是完全不同维度的可行与不可行。**

---

## 四、概率算法——颠覆性的思维

SICP 用一段非常精彩的文字总结了概率算法的哲学意义：

> "The Fermat test differs in character from most familiar algorithms, in which one computes an answer that is guaranteed to be correct. Here, the answer obtained is only probably correct."

然后，SICP 坦诚地承认了 Fermat 测试的不完美：

> "There do exist numbers that fool the Fermat test: numbers n that are not prime and yet have the property that aⁿ is congruent to a modulo n for all integers a < n. Such numbers are extremely rare, so the Fermat test is quite reliable in practice."

这些「骗子」数字叫做 **Carmichael 数**。最小的 Carmichael 数是 561 = 3 × 11 × 17。它不是素数，但对所有 a，a⁵⁶¹ ≡ a (mod 561) 都成立。Fermat 测试对它完全失效。

但 SICP 马上说：「这些数极其罕见」。在实际应用中，Fermat 测试足够可靠。

更重要的是，SICP 指出存在更好的变体（Exercise 1.28 的 Miller-Rabin 测试）：

> "There are variations of the Fermat test that cannot be fooled. One can prove that, for any n, the condition does not hold for most of the integers a < n unless n is prime."

Miller-Rabin 测试在数学上可以证明：如果 n 不是素数，那么至少 3/4 的 a 会暴露 n 的合数性质。这意味着：
- 测试 1 次：错误概率 < 1/4
- 测试 10 次：错误概率 < (1/4)¹⁰ ≈ 10⁻⁶
- 测试 100 次：错误概率 < (1/4)¹⁰⁰ ≈ 10⁻⁶⁰

这个数字比宇宙中原子数量还要小得多。

---

## 五、概率思维在游戏开发中的应用

这个「大概率正确就够用」的思想，在游戏开发中无处不在，只是你可能没有意识到它和 Fermat 测试是同一类思维。

**物理引擎的碰撞检测**

精确的碰撞检测是 O(n²) 的。在复杂的场景中，n 可能是数万甚至数十万。实时计算不可能完成。

所以游戏引擎用 Broad Phase（AABB、BVH 粗检测）先做一轮筛选，只对「可能碰撞」的物体做精确检测。

Broad Phase 也会犯错——两个 AABB 重叠不代表真的碰撞。但这只是增加了 Narrow Phase 的调用次数，不会导致错误的结果。

**蒙特卡洛全局光照**

游戏中（如 UE5 的 Lumen、Minecraft 的 RTX 光追）使用的光线追踪实际上就是蒙特卡洛积分——随机发射光线，统计平均结果。

每条光线都是一次随机采样。10 条光线的结论不精确，1000 条光线的结果就很接近正确答案了。但你永远不会得到「精确」答案——你只是在增加置信度。

**动画混合的随机化**

当角色在多个动画状态之间切换时，用随机化的过渡时间来避免机械感。这不是精确的数学，而是「感觉对了就行」。

**AI 决策的随机性**

游戏 AI 经常用概率做决策：怪物有 70% 概率追击、30% 概率巡逻。这不是「最优策略」，而是「感觉自然的策略」。

所有这些场景的共同点：**放弃确定性，换取可行性。**

SICP 教你的是：当你遇到一个「理论上可以精确解决但实际上不可行」的问题时，问自己：**「一个大概率正确的答案够用吗？」** 如果够，你就打开了一个全新的解法空间。

---

## 六、确定性 vs 概率性——工程权衡的本质

SICP 今天的课程不只是在教你素数判定，它在教你一种工程思维。

让我们对比两种方法：

| 维度 | 朴素方法 Θ(√n) | Fermat 测试 Θ(log n) |
|------|----------------|---------------------|
| 正确性 | 100% 正确 | 大概率正确 |
| 速度 | 大数字不可行 | 大数字轻松 |
| 实现复杂度 | 简单 | 简单 |
| 数学基础 | 初等数论 | 费马小定理 |

在密码学中，没人用朴素方法生成素数——RSA 密钥的生成需要找到 300 位的素数，朴素方法要算到宇宙热寂。Fermat/Miller-Rabin 测试是唯一实际可行的选择。

这不是「偷懒」，而是**对问题本质的深刻理解**：你不需要 100% 确定 n 是素数，你只需要错误概率小于被随机猜测破解的概率（那本身就是一个极小的数字）。

**品味判断：** 当一个精确算法的复杂度使其在目标规模上不可行时，概率算法不是妥协，而是唯一合理的工程选择。拒绝使用概率算法才是真正的工程失误。

---

## 七、从 Fermat 到现代密码学

Fermat 小定理不仅用于素数检测，它还是 RSA 加密算法的数学基础之一。

RSA 加密的核心：
- 选择两个大素数 p 和 q
- 计算 n = p × q
- 公钥 (n, e)，私钥 (n, d)
- 加密：c = m^e mod n
- 解密：m = c^d mod n

RSA 的安全性依赖于：给定 n，很难分解出 p 和 q。而 Fermat 测试（和 Miller-Rabin 测试）正是用来**快速找到大素数 p 和 q** 的工具。

每当你用 HTTPS 访问一个网站，背后就有一对用概率算法生成的素数在保护你的通信安全。

---

## 八、用 C# 实现今天的算法

把 SICP 的 Scheme 代码翻译成你熟悉的 C#：

```csharp
// 朴素素性测试 — Θ(√n)
public static bool IsPrimeNaive(int n)
{
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)
    {
        if (n % i == 0) return false;
    }
    return true;
}

// 快速幂取模 — Θ(log exp)
public static long ExpMod(long baseVal, long exp, long m)
{
    if (exp == 0) return 1;
    if (exp % 2 == 0)
    {
        long half = ExpMod(baseVal, exp / 2, m);
        return (half * half) % m;
    }
    return (baseVal * ExpMod(baseVal, exp - 1, m)) % m;
}

// Fermat 素性测试 — Θ(log n)
// 返回 true 表示「大概率是素数」，false 表示「确定不是素数」
public static bool FermatTest(long n, Random rng)
{
    if (n < 2) return false;
    // 随机选择 a，其中 1 < a < n-1
    long a = rng.NextInt64(2, n - 1);
    // 检查 a^n ≡ a (mod n)
    return ExpMod(a, n, n) == a % n;
}

// 多次 Fermat 测试 — 每次失败概率 < 1/4
public static bool IsProbablyPrime(long n, int trials = 10)
{
    var rng = new Random();
    for (int i = 0; i < trials; i++)
    {
        if (!FermatTest(n, rng))
            return false; // 确定不是素数
    }
    return true; // 大概率是素数（错误概率 < (1/4)^trials）
}
```

你可以用这段代码做一个有趣的实验：

```csharp
// 测试 Carmichael 数 561 — Fermat 测试的克星
Console.WriteLine(IsProbablyPrime(561));  // 可能返回 true（错误！）
Console.WriteLine(IsPrimeNaive(561));     // 正确返回 false

// 测试一个大素数
Console.WriteLine(IsProbablyPrime(104729));  // 正确返回 true
Console.WriteLine(IsPrimeNaive(104729));     // 也正确，但更慢
```

对 561 这个 Carmichael 数，Fermat 测试会给出错误答案——这就是为什么 SICP 说「有变体不能被欺骗」，暗示应该用 Miller-Rabin。

---

## 九、代码实践：实现 Miller-Rabin 测试

Exercise 1.28 要求实现一个不能被 Carmichael 数欺骗的测试。这就是 Miller-Rabin 测试。C# 实现：

```csharp
// Miller-Rabin 素性测试
// 检查 a^(d * 2^s) mod n 的序列中是否存在「非平凡平方根」
public static bool MillerRabinTest(long n, long a)
{
    // 将 n-1 分解为 d * 2^s
    long d = n - 1;
    int s = 0;
    while (d % 2 == 0)
    {
        d /= 2;
        s++;
    }
    
    // 计算 x = a^d mod n
    long x = ExpMod(a, d, n);
    
    if (x == 1 || x == n - 1) return true; // 可能是素数
    
    // 反复平方 s-1 次
    for (int i = 0; i < s - 1; i++)
    {
        x = (x * x) % n;
        if (x == n - 1) return true; // 可能是素数
        // 如果 x == 1 但前一个 x 不是 ±1，说明找到了非平凡平方根
        if (x == 1) return false; // 确定不是素数
    }
    
    return false; // 确定不是素数
}
```

Miller-Rabin 对 Carmichael 数 561 的测试：

```csharp
// 561 是 Carmichael 数，Fermat 会被骗，Miller-Rabin 不会
Console.WriteLine(MillerRabinTest(561, 2));  // 返回 false ✅
Console.WriteLine(MillerRabinTest(561, 3));  // 返回 false ✅
```

这就是数学的力量——Fermat 测试有一个难以修补的缺陷，但 Miller-Rabin 通过一个简单的额外检查（检查「非平凡平方根」）彻底解决了问题。

---

## 十、品味判断：什么时候用概率算法？

不是所有场景都适合概率算法。给你一个判断框架：

**适合概率算法：**
- 精确解的计算成本远超实际需求（密码学、大数据、物理模拟）
- 错误可以检测和纠正（网络传输、分布式系统）
- 可以通过增加采样次数降低错误概率到可接受范围
- 错误的代价很低（游戏 AI 决策、随机化动画）

**不适合概率算法：**
- 错误的代价极高（医疗诊断、金融交易清算、航天控制）
- 精确解的计算成本可接受（小型系统的确定性逻辑）
- 需要形式化证明正确性（安全关键系统）

在游戏开发中，绝大多数情况适合概率算法。因为游戏的本质不是「精确」，而是「有趣」。一帧的光追结果差了 1% 没人看得出来，但帧率因为过度精确的计算而暴跌，所有人都能感受到。

---

> **今日品味结晶：** SICP 在第一章就用概率算法告诉你：计算机科学的终极目标不是「正确」，而是「在约束条件下做出最好的近似」。确定性是一种奢侈品，概率性是一种工程智慧。真正的专家知道什么时候追求确定性，什么时候拥抱不确定性。

---

## 🎯 今日测验

**Q1（概念）：** Fermat 小定理说的是「如果 n 是素数，则 aⁿ ≡ a (mod n)」。这个定理为什么不能直接反过来用（即「如果 aⁿ ≡ a (mod n)，则 n 是素数」）？Carmichael 数的存在说明了什么？

**Q2（应用）：** 在游戏开发中，你遇到过哪些「放弃确定性换取可行性」的场景？除了 SICP 提到的素数检测和物理模拟，想想你的游戏引擎或游戏项目中，哪些地方用到了类似的概率思维？

**Q3（代码）：** SICP 的 `expmod` 和 Day 4 的 `fast-expt` 几乎一样，只是每步多了 `remainder`。但有一个微妙的区别：`expmod` 先递归再取模，而不是先取模再递归。这个顺序为什么不能反过来？（提示：考虑递归展开时的中间值大小。）

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。

---

*Day 5 / 60 · SICP Coach 模式 · 实时生成*
