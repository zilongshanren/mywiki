---
title: Nested Coroutines in Unity - Alan Zucconi
url: https://www.alanzucconi.com/2017/02/15/nested-coroutines-in-unity/
author: Alan Zucconi
published: '2017-02-15'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial shows how to make the most out of coroutines in Unity.

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Synchronous Waits](https://www.alanzucconi.com#part1) - Part 2.
[Asynchronous Coroutines](https://www.alanzucconi.com#part2) - Part 3.
[Synchronous Coroutines](https://www.alanzucconi.com#part3) - Part 4.
[Parallel Coroutines](https://www.alanzucconi.com#part4) [Conclusion](https://www.alanzucconi.com#conclusion)

#### Introduction

Each Unity script comes with two important functions: `Start`

and `Update`

. While the former is invoked when an object is enabled after being created, the latter is called during each frame. By design, the next frame cannot start until `Update`

has terminated its job. This introduces a strong design limitation: `Update`

cannot easily model events that last for more than one frame.

To be completely honest, every custom behaviour you can imagine can be implemented using `Start`

and `Update`

. However, events that happens over multiple frames (such as animations, dialogues, waits, …) are harder to code. This is because their logic cannot be written in a consistent flow. It has to be fragmented, spread over multiple frames. This often leads to code that is not just harder to write, but also harder to maintain.

What would be perfect is to have something that can be executed in parallel, unconstrained from the short life of a single frame. If you are a programmer, this will probably resonate with the concept of **thread**. Threads are pieces of code that are executed in parallel. Working with threads, however, is very tricky. This is because when multiple threads are working on a shared variable without any limitation , there can be issues. By design, Unity strongly discourages the use a threads. However, it offers a good compromise: **coroutines**. Coroutines are functions which can lasts more than one frame. Moreover, they come with expressive constructs to interrupt and resume their executions due to arbitrary conditions.

Coroutines are normal C# functions which return `IEnumerator`

. To execute such a function like a coroutine (and not like a *traditional* function), one has to use the `StartCoroutine`

method ([UnityDoc](https://docs.unity3d.com/ScriptReference/MonoBehaviour.StartCoroutine.html)). For instance:

void Start () { // Execute A as a coroutine StartCoroutine( A() ); } IEnumerator A () { ... }

executes `A`

as a coroutine. The method `StartCoroutine`

terminates immediately, but spawns a new coroutine that is executed in parallel.

#### Synchronous Waits

If you have used coroutines before, it is likely that you have already encountered the class `WaitForSeconds`

([UnityDoc](https://docs.unity3d.com/ScriptReference/WaitForSeconds.html)). Like all the other classes that extend `YieldInstruction`

, it allows to temporarily suspend the execution of a coroutine. When coupled with `yield return`

, `WaitForSeconds`

provides an expressive way to delay the execution of the remaining code.

The following piece of code shows how it can be used within a coroutine:

IEnumerator A() { ... yield return new WaitForSeconds(10f); ... }

![](../../assets/72d0ba2594fa791a.png)

The diagram above, *loosely* inspired by the **sequence diagrams in UML** ([Wikipedia](https://en.wikipedia.org/wiki/Sequence_diagram)), illustrates the effect of `WaitForSeconds`

. When invoked in a coroutine (called `A`

) it suspends its execution until a certain amount of time has passed. This type of wait is called **synchronous**, because the coroutine waits for for another operation to complete.

#### Asynchronous Coroutines

Unity also allowed to start new coroutines within an existing coroutine. The most simple way in which this can be achieved, is by using `StartCoroutine`

. When invoked like this, the spawned coroutine co-exist in parallel with the original one. They do not interact directly, and most importantly they do not wait for each other. In comparison with the synchronous wait presented in the previous paragraph, this situation is **asynchronous**, at the two coroutines do not attempt to remain in synch.

IEnumerator A() { ... // Starts B as a coroutine, and continue the execution StartCoroutine( B() ); ... }

![](../../assets/f87c0aa0083c6910.png)

It is important to notice that, in this example, `B`

is a totally independent coroutine. Terminating `A`

does not affect `B`

, and vice versa.

#### Synchronous Coroutines

It is also possible to execute a nested coroutine and to wait for its execution to be completed. The simplest way to do this, is by using `yield return`

.

IEnumerator A() { ... // Waits for B to terminate yield return StartCoroutine( B() ); ... }

![](../../assets/2dc2c24e4af90d2c.png)

It’s worth noticing that, since the execution of `A`

is suspended during the execution of `B`

, this particular case does not need to start another coroutine. One might be tempted to optimise the coroutine by writing something like this:

IEnumerator A() { ... // Executes B as part of A B(); ... }

Executing `B`

as a traditional function has almost the same effect. The only difference, however, is that B will be executed in a single frame. By using `StartCoroutine`

, instead, `A`

is suspended and the next frame can occur.

The reason why this example is shown, however, is to introduce more complex cases of **coroutine synchronisation**.

#### Parallel Coroutines

When a coroutine is started using `StartCoroutine`

, a special object is returned. This can be used to query the state of the coroutine and, optionally, to wait for its termination.

In the example below the coroutine `B`

is executed asynchronously. Its father `A`

can continue its execution for as long as it needs. Then, if necessary, it can yield to the reference to `B`

for a synchronous wait.

IEnumerator A() { ... // Starts B as a coroutine and continues the execution Coroutine b = StartCoroutine( B() ); ... // Waits for B to terminate yield return b; ... }

![](../../assets/a3e4d031a99e698a.png)

This is particularly helpful if you want to start several parallel coroutines, all at the same time:

IEnumerator A() { ... // Starts B, C, and D as coroutines and continues the execution Coroutine b = StartCoroutine( B() ); Coroutine c = StartCoroutine( C() ); Coroutine d = StartCoroutine( D() ); ... // Waits for B, C and D to terminate yield return b; yield return c; yield return d; ... }

![](../../assets/97420814318a415b.png)

This new paradigm allows to start an arbitrary numbers of parallel computations, and to resume the execution when all of them have terminated.

#### Conclusion

This post shows several different patterns that can be implemented in your game to use coroutines effectively. The next posts of this series will focus on how to extends coroutines to support custom waits and events.

- Part 1.
[Iterators in C#: yields, IEnumerable and IEnumerator](https://www.alanzucconi.com/2017/01/22/iterators-c-yield-ienumerable-ienumerator/) - Part 2.
**Nested Coroutines** - Part 3. Extending Coroutines

## Leave a Reply Cancel reply