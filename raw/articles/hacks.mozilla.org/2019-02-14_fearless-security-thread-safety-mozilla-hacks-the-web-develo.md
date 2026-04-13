---
title: 'Fearless Security: Thread Safety – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/02/fearless-security-thread-safety/
author: Diane Hosfelt
published: '2019-02-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In Part 2 of my three-part Fearless Security series, I’ll explore thread safety. *

Today’s applications are multi-threaded—instead of sequentially completing tasks, a program uses threads to perform multiple tasks simultaneously. We all use *concurrency* and *parallelism* every day:

- Web sites serve multiple simultaneous users.
- User interfaces perform background work that doesn’t interrupt the user. (Imagine if your application froze each time you typed a character because it was spell-checking).
- Multiple applications can run at the same time on a computer.

While this allows programs to do more faster, it comes with a set of synchronization problems, namely deadlocks and data races. From a security standpoint, why do we care about thread safety? Memory safety bugs and thread safety bugs have the same core problem: invalid resource use. Concurrency attacks can lead to similar consequences as memory attacks, including privilege escalation, arbitrary code execution (ACE), and bypassing security checks.

Concurrency bugs, like implementation bugs, are closely related to program correctness. While memory vulnerabilities are nearly always dangerous, implementation/logic bugs don’t always indicate a security concern, unless they occur in the part of the code that deals with ensuring security contracts are upheld (e.g. allowing a security check bypass). However, while security problems stemming from logic errors often occur near the error in sequential code, concurrency bugs often happen in [different functions from their corresponding vulnerability](http://www.cs.columbia.edu/~junfeng/papers/owl-dsn18.pdf), making them difficult to trace and resolve. Another complication is the overlap between mishandling memory and concurrency flaws, which we see in data races.

Programming languages have evolved different concurrency strategies to help developers manage both the performance and security challenges of multi-threaded applications.

## Problems with concurrency

It’s a common axiom that parallel programming is hard—our brains are better at sequential reasoning. Concurrent code can have unexpected and unwanted interactions between threads, including deadlocks, race conditions, and data races.

A *deadlock* occurs when multiple threads are each waiting on the other to take some action in order to proceed, leading to the threads becoming permanently blocked. While this is undesirable behavior and could cause a denial of service attack, it wouldn’t cause vulnerabilities like ACE.

A *race condition* is a situation in which the timing or ordering of tasks can affect the correctness of a program, while a *data race* happens when multiple threads attempt to concurrently access the same location in memory and at least one of those accesses is a write. There’s a lot of overlap between data races and race conditions, but they can also [occur independently](https://blog.regehr.org/archives/490). [There are no benign data races](https://software.intel.com/en-us/blogs/2013/01/06/benign-data-races-what-could-possibly-go-wrong).

### Potential consequences of concurrency bugs:

- Deadlock
- Information loss: another thread overwrites information
- Integrity loss: information from multiple threads is interlaced
- Loss of liveness: performance problems resulting from uneven access to shared resources

The best-known type of concurrency attack is called a [TOCTOU](https://en.wikipedia.org/wiki/Time_of_check_to_time_of_use) (time of check to time of use) attack, which is a race condition between checking a condition (like a security credential) and using the results. TOCTOU attacks are examples of integrity loss.

Deadlocks and loss of *liveness* are considered performance problems, not security issues, while information and integrity loss are both more likely to be security-related. This [paper from Red Balloon Security](https://www.redballoonsecurity.com/publications/papers/Concurrency_Attacks.pdf) examines some exploitable concurrency errors. One example is a pointer corruption that allows privilege escalation or remote execution—a function that loads a shared ELF (Executable and Linkable Format) library holds a semaphore correctly the first time it’s called, but the second time it doesn’t, enabling kernel memory corruption. This attack is an example of information loss.

The trickiest part of concurrent programming is testing and debugging—concurrency bugs have poor reproducibility. Event timings, operating system decisions, network traffic, etc. can all cause different behavior each time you run a program that has a concurrency bug.


Not only can behavior change each time we run a concurrent program, but inserting print or debugging statements can also modify the behavior, causing *heisenbugs* (nondeterministic, hard to reproduce bugs that are common in concurrent programming) to mysteriously disappear. These operations are slow compared to others and change message interleaving and event timing accordingly.

Concurrent programming is hard. Predicting how concurrent code interacts with other concurrent code is difficult to do. When bugs appear, they’re difficult to find and fix. Instead of relying on programmers to worry about this, let’s look at ways to design programs and use languages to make it easier to write concurrent code.

First, we need to define what “threadsafe” means:

“A data type or static method is threadsafe if it behaves correctly when used from multiple threads, regardless of how those threads are executed, and without demanding additional coordination from the calling code.”

MIT

## How programming languages manage concurrency

In languages that don’t statically enforce thread safety, programmers must remain constantly vigilant when interacting with memory that can be shared with another thread and could change at any time. In sequential programming, we’re taught to avoid global variables in case another part of code has silently modified them. Like manual memory management, requiring programmers to safely mutate shared data is problematic.

Generally, programming languages are limited to two approaches for managing safe concurrency:

- Confining mutability or limiting sharing
- Manual thread safety (e.g. locks, semaphores)

Languages that limit threading either confine mutable variables to a single thread or require that all shared variables be immutable. Both approaches eliminate the core problem of data races—improperly mutating shared data—but this can be too limiting. To solve this, languages have introduced low-level synchronization primitives like *mutexes*. These can be used to build threadsafe data structures.

### Python and the global interpreter lock

The reference implementation of Python, CPython, has a mutex called the Global Interpreter Lock (GIL), which only allows a single thread to access a Python object. Multi-threaded Python is notorious for being [inefficient](https://hackernoon.com/concurrent-programming-in-python-is-not-what-you-think-it-is-b6439c3f3e6a) because of the time spent waiting to acquire the GIL. Instead, most parallel Python programs use multiprocessing, meaning each process has its own GIL.

### Java and runtime exceptions

[Java](https://en.wikipedia.org/wiki/Java_concurrency) is designed to support concurrent programming via a shared-memory model. Each thread has its own execution path, but is able to access any object in the program—it’s up to the programmer to synchronize accesses between threads using Java built-in primitives.

While Java has the building blocks for creating thread-safe programs, [thread safety](https://www.journaldev.com/1061/thread-safety-in-java) is **not** guaranteed by the compiler (unlike memory safety). If an unsynchronized memory access occurs (aka a data race), then Java will raise a runtime exception—however, this still relies on programmers appropriately using concurrency primitives.

### C++ and the programmer’s brain

While Python avoids data races by synchronizing everything with the GIL, and Java raises runtime exceptions if it detects a data race, C++ relies on programmers to manually synchronize memory accesses. Prior to C++11, the standard library [did not include concurrency primitives](http://www.modernescpp.com/index.php/c-core-guidelines-rules-for-concurrency-and-parallelism).

Most programming languages provide programmers with the tools to write thread-safe code, and post hoc methods exist for detecting data races and race conditions; however, this does not result in any guarantees of thread safety or data race freedom.

## How does Rust manage concurrency?

Rust takes a multi-pronged approach to eliminating data races, using ownership rules and type safety to guarantee data race freedom at compile time.

The [first post](https://hacks.mozilla.org/2019/01/fearless-security-memory-safety/) of this series introduced ownership—one of the core concepts of Rust. Each variable has a unique owner and can either be moved or borrowed. If a different thread needs to modify a resource, then we can transfer ownership by moving the variable to the new thread.

Moving enforces exclusion, allowing multiple threads to write to the same memory, but never at the same time. Since an owner is confined to a single thread, what happens if another thread borrows a variable?

In Rust, you can have either one mutable borrow or as many immutable borrows as you want. You can never simultaneously have a mutable borrow and an immutable borrow (or multiple mutable borrows). When we talk about memory safety, this ensures that resources are freed properly, but when we talk about thread safety, it means that only one thread can ever modify a variable at a time. Furthermore, we know that no other threads will try to reference an out of date borrow—borrowing enforces either sharing or writing, but never both.

Ownership was designed to mitigate memory vulnerabilities. It turns out that it also prevents data races.

While many programming languages have methods to enforce memory safety (like reference counting and garbage collection), they usually rely on manual synchronization or prohibitions on concurrent sharing to prevent data races. Rust’s approach addresses both kinds of safety by attempting to solve the core problem of identifying valid resource use and enforcing that validity during compilation.

### But wait! There’s more!

The ownership rules prevent multiple threads from writing to the same memory and disallow simultaneous sharing between threads and mutability, but this doesn’t necessarily provide thread-safe data structures. Every data structure in Rust is either thread-safe or it’s not. This is communicated to the compiler using the type system.

A well-typed program can’t go wrong.

Robin Milner, 1978

In programming languages, type systems describe valid behaviors. In other words, a well-typed program is well-defined. As long as our types are expressive enough to capture our intended meaning, then a well-typed program will behave as intended.

Rust is a type safe language—the compiler verifies that all types are consistent. For example, the following code would not compile:

```
let mut x = "I am a string";
x = 6;
```


```
error[E0308]: mismatched types
--> src/main.rs:6:5
|
6 | x = 6; //
| ^ expected &str, found integral variable
|
= note: expected type `&str`
found type `{integer}`
```


All variables in Rust have a type—often, they’re implicit. We can also define new types and describe what capabilities a type has using the [trait system](https://blog.rust-lang.org/2015/05/11/traits.html). Traits provide an interface abstraction in Rust. Two important built-in traits are `Send`

and `Sync`

, which are exposed by default by the Rust compiler for every type in a Rust program:

`Send`

indicates that a struct may safely be sent between threads (required for an ownership move)`Sync`

indicates that a struct may safely be shared between threads

This example is a simplified version of the [standard library code](https://github.com/rust-lang/rust/blob/c84e7976423bb910bb5eb5eecffc7e33a897a97f/src/libstd/thread/mod.rs#L379-L383) that spawns threads:

```
fn spawn<Closure: Fn() + Send>(closure: Closure){ ... }
let x = std::rc::Rc::new(6);
spawn(|| { x; });
```


The `spawn`

function takes a single argument, `closure`

, and requires that `closure`

has a type that implements the `Send`

and `Fn`

traits. When we try to spawn a thread and pass a closure value that makes use of the variable `x`

, the compiler rejects the program for not fulfilling these requirements with the following error:

```
error[E0277]: `std::rc::Rc<i32>` cannot be sent between threads safely
--> src/main.rs:8:1
|
8 | spawn(move || { x; });
| ^^^^^ `std::rc::Rc<i32>` cannot be sent between threads safely
|
= help: within `[closure@src/main.rs:8:7: 8:21 x:std::rc::Rc<i32>]`, the trait `std::marker::Send` is not implemented for `std::rc::Rc<i32>`
= note: required because it appears within the type `[closure@src/main.rs:8:7: 8:21 x:std::rc::Rc<i32>]`
note: required by `spawn`
```


The `Send`

and `Sync`

[traits](https://doc.rust-lang.org/nomicon/send-and-sync.html) allow the Rust type system to reason about what data may be shared. By including this information in the type system, thread safety becomes type safety. Instead of relying on documentation, [thread safety is part of the compiler’s law](https://blog.rust-lang.org/2015/04/10/Fearless-Concurrency.html).

This allows programmers to be opinionated about what can be shared between threads, and the compiler will enforce those opinions.

While many programming languages provide tools for concurrent programming, preventing data races is a difficult problem. Requiring programmers to reason about complex instruction interleaving and interaction between threads leads to error prone code. While thread safety and memory safety violations share similar consequences, traditional memory safety mitigations like reference counting and garbage collection don’t prevent data races. In addition to statically guaranteeing memory safety, Rust’s ownership model prevents unsafe data modification and sharing across threads, while the type system propagates and enforces thread safety at compile time.

![Pikachu finally discovers fearless concurrency with Rust](../../assets/bf3b2067fb6f8155.jpg)


## One comment

DavidMarch 7th, 2019 at 15:30