---
title: 'Fearless Security: Memory Safety – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/01/fearless-security-memory-safety/
author: Diane Hosfelt
published: '2019-01-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Fearless Security

Last year, Mozilla shipped [Quantum CSS](https://hacks.mozilla.org/2017/08/inside-a-super-fast-css-engine-quantum-css-aka-stylo/) in Firefox, which was the culmination of 8 years of investment in Rust, a memory-safe systems programming language, and over a year of rewriting a major browser component in Rust. Until now, all major browser engines have been written in C++, mostly for performance reasons. However, with great performance comes great (memory) responsibility: C++ programmers have to manually manage memory, which opens a Pandora’s box of vulnerabilities. Rust not only prevents these kinds of errors, but the techniques it uses to do so also prevent [data races](https://blog.regehr.org/archives/490), allowing programmers to reason more effectively about parallel code.

In the coming weeks, this three-part series will examine memory safety and thread safety, and close with a case study of the potential security benefits gained from rewriting Firefox’s CSS engine in Rust.

## What Is Memory Safety

When we talk about building secure applications, we often focus on memory safety. Informally, this means that in all possible executions of a program, there is no access to invalid memory. Violations include:

- use after free
- null pointer dereference
- using uninitialized memory
- double free
- buffer overflow

For a more formal definition, see Michael Hicks’ [ What is memory safety post](http://www.pl-enthusiast.net/2014/07/21/memory-safety/) and

[, a paper that formalizes memory safety.](https://arxiv.org/pdf/1705.07354.pdf)

*The Meaning of Memory Safety*Memory violations like these can cause programs to crash unexpectedly and can be exploited to alter intended behavior. Potential consequences of a memory-related bug include information leakage, arbitrary code execution, and remote code execution.

## Managing Memory

Memory management is crucial to both the performance and the security of applications. This section will discuss the basic memory model. One key concept is *pointers*. A pointer is a variable that stores a memory address. If we visit that memory address, there will be some data there, so we say that the pointer is a reference to (or points to) that data. Just like a home address shows people where to find you, a memory address shows a program where to find data.

Everything in a program is located at a particular memory address, including code instructions. Pointer misuse can cause serious security vulnerabilities, including information leakage and arbitrary code execution.

### Allocation/free

When we create a variable, the program needs to allocate enough space in memory to store the data for that variable. Since the memory owned by each process is finite, we also need some way of reclaiming resources (or *freeing* them). When memory is freed, it becomes available to store new data, but the old data can still exist until it is overwritten.

### Buffers

A *buffer* is a contiguous area of memory that stores multiple instances of the same data type. For example, the phrase “My cat is Batman” would be stored in a 16-byte buffer. Buffers are defined by a starting memory address and a length; because the data stored in memory next to a buffer could be unrelated, it’s important to ensure we don’t read or write past the buffer boundaries.

### Control Flow

Programs are composed of subroutines, which are executed in a particular order. At the end of a subroutine, the computer jumps to a stored pointer (called the *return address*) to the next part of code that should be executed. When we jump to the return address, one of three things happens:

- The process continues as expected (the return address was not corrupted).
- The process crashes (the return address was altered to point at non-executable memory).
- The process continues, but not as expected (the return address was altered and control flow changed).

## How languages achieve memory safety

We often think of programming languages on a [spectrum](https://www.memorymanagement.org/mmref/lang.html). On one end, languages like C/C++ are efficient, but require manual memory management; on the other, interpreted languages use automatic memory management (like reference counting or garbage collection [GC]), but pay the price in performance. Even languages with highly optimized garbage collectors can’t match the [performance](http://greenlab.di.uminho.pt/wp-content/uploads/2017/09/paperSLE.pdf) of non-GC’d languages.

### Manually

Some languages (like C) require programmers to manually manage memory by specifying when to allocate resources, how much to allocate, and when to free the resources. This gives the programmer very fine-grained control over how their implementation uses resources, enabling fast and efficient code. However, this approach is prone to mistakes, particularly in complex codebases.

Mistakes that are easy to make include:

- forgetting that resources have been freed and trying to use them
- not allocating enough space to store data
- reading past the boundary of a buffer

![Shake hands with danger!](../../assets/8b065106026230f0.jpeg)


*A safety video candidate for manual memory management*

### Smart pointers

A [smart pointer](http://ootips.org/yonat/4dev/smart-pointers.html) is a pointer with additional information to help prevent memory mismanagement. These can be used for automated memory management and bounds checking. Unlike raw pointers, a smart pointer is able to self-destruct, instead of waiting for the programmer to manually destroy it.

There’s no single smart pointer type—a smart pointer is any type that wraps a raw pointer in some practical abstraction. Some smart pointers use *reference counting* to count how many variables are using the data owned by a variable, while others implement a scoping policy to constrain a pointer lifetime to a particular scope.

In reference counting, the object’s resources are reclaimed when the last reference to the object is destroyed. Basic reference counting implementations can suffer from performance and space overhead, and can be difficult to use in multi-threaded environments. Situations where objects refer to each other (cyclical references) can prohibit either object’s reference count from ever reaching zero, which requires more sophisticated methods.

## Garbage Collection

Some languages (like Java, Go, Python) are [ garbage collected](https://en.wikipedia.org/wiki/Tracing_garbage_collection). A part of the runtime environment, named the garbage collector (GC), traces variables to determine what resources are reachable in a graph that represents references between objects. Once an object is no longer reachable, its resources are not needed and the GC reclaims the underlying memory to reuse in the future. All allocations and deallocations occur without explicit programmer instruction.

While a GC ensures that memory is always used validly, it doesn’t reclaim memory in the most efficient way. The last time an object is used could occur much earlier than when it is freed by the GC. Garbage collection has a performance overhead that can be prohibitive for performance critical applications; it requires up to [5x as much memory](https://people.cs.umass.edu/~emery/pubs/gcvsmalloc.pdf) to avoid a runtime performance penalty.

### Ownership

To achieve both performance and memory safety, Rust uses a concept called ownership. More formally, the ownership model is an example of an [affine type system](https://gankro.github.io/blah/linear-rust/). All Rust code follows certain ownership rules that allow the compiler to manage memory without incurring runtime costs:

- Each value has a variable, called the owner.
- There can only be one owner at a time.
- When the owner goes out of scope, the value will be dropped.

Values can be [moved](https://doc.rust-lang.org/beta/rust-by-example/scope/move.html) or [borrowed](https://doc.rust-lang.org/beta/rust-by-example/scope/borrow.html) between variables. These rules are enforced by a part of the compiler called the borrow checker.

When a variable goes out of scope, Rust frees that memory. In the following example, when `s1`

and `s2`

go out of scope, they would both try to free the same memory, resulting in a double free error. To prevent this, when a value is moved out of a variable, the previous owner becomes invalid. If the programmer then attempts to use the invalid variable, the compiler will reject the code. This can be avoided by creating a deep copy of the data or by using references.

[Example 1](https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&gist=758b475abc30e7a4f28398545791b4c7): Moving ownership

```
let s1 = String::from("hello");
let s2 = s1;
//won't compile because s1 is now invalid
println!("{}, world!", s1);
```


Another set of rules verified by the borrow checker pertains to variable lifetimes. Rust prohibits the use of uninitialized variables and dangling pointers, which can cause a program to reference unintended data. If the code in the example below compiled, `r`

would reference memory that is deallocated when `x`

goes out of scope—a dangling pointer. The compiler tracks scopes to ensure that all borrows are valid, occasionally requiring the programmer to explicitly annotate variable lifetimes.

[Example 2](https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&gist=174cf01d8372d0edb9405ada891e8316): A dangling pointer

```
let r;
{
let x = 5;
r = &x;
}
println!("r: {}", r);
```


The ownership model provides a strong foundation for ensuring that memory is accessed appropriately, preventing undefined behavior.

## Memory Vulnerabilities

The main consequences of memory vulnerabilities include:

**Crash:**accessing invalid memory can make applications terminate unexpectedly**Information leakage:**inadvertently exposing non-public data, including sensitive information like passwords**Arbitrary code execution (ACE):**allows an attacker to execute arbitrary commands on a target machine; when this is possible over a network, we call it a remote code execution (RCE)

Another type of problem that can appear is [memory leakage](https://en.wikipedia.org/wiki/Memory_leak), which occurs when memory is allocated, but not released after the program is finished using it. It’s possible to use up all available memory this way. Without any remaining memory, legitimate resource requests will be blocked, causing a denial of service. This is a memory-related problem, but one that can’t be addressed by programming languages.

The best case scenario with most memory errors is that an application will crash harmlessly—this isn’t a good best case. However, the worst case scenario is that an attacker can gain control of the program through the vulnerability (which could lead to further attacks).

### Misusing Free (use-after-free, double free)

This subclass of vulnerabilities occurs when some resource has been *freed*, but its memory position is still referenced. It’s a [powerful exploitation method](https://sensepost.com/blog/2017/linux-heap-exploitation-intro-series-used-and-abused-use-after-free/) that can lead to out of bounds access, information leakage, code execution and [more](https://scarybeastsecurity.blogspot.com/2017/05/ode-to-use-after-free-one-vulnerable.html).

Garbage-collected and reference-counted languages prevent the use of invalid pointers by only destroying unreachable objects (which can have a performance penalty), while manually managed languages are particularly susceptible to invalid pointer use (particularly in complex codebases). Rust’s borrow checker doesn’t allow object destruction as long as references to the object exist, which means bugs like these are prevented at compile time.

### Uninitialized variables

If a variable is used prior to initialization, the data it contains could be anything—including random garbage or previously discarded data, resulting in information leakage (these are sometimes called *wild pointers*). Often, memory managed languages use a default initialization routine that is run after allocation to prevent these problems.

Like C, most variables in Rust are uninitialized until assignment—unlike C, you can’t read them prior to initialization. The following code will fail to compile:

[Example 3](https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&gist=616d9186c8eb4c6ae1ddb24aae54a88f): Using an uninitialized variable

```
fn main() {
let x: i32;
println!("{}", x);
}
```


### Null pointers

When an application dereferences a pointer that turns out to be null, usually this means that it simply accesses garbage that will cause a crash. In some cases, these vulnerabilities can lead to arbitrary code execution [1](https://lwn.net/Articles/342330/) [2](http://www.fuzzysecurity.com/tutorials/expDev/16.html) [3](https://hackernoon.com/fixing-the-billion-dollar-mistake-in-go-by-borrowing-from-rust-66fab3ea715e). Rust has two types of pointers, [references](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html) and [raw pointers](https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html#dereferencing-a-raw-pointer). References are safe to access, while raw pointers could be problematic.

Rust prevents null pointer dereferencing two ways:

- Avoiding nullable pointers
- Avoiding raw pointer dereferencing

Rust avoids nullable pointers by replacing them with a special [ Option type](https://doc.rust-lang.org/rust-by-example/std/option.html). In order to manipulate the possibly-null value inside of an

`Option`

, the language requires the programmer to explicitly handle the null case or the program will not compile.When we can’t avoid nullable pointers (for example, when interacting with non-Rust code), what can we do? Try to isolate the damage. Any dereferencing raw pointers must occur in an unsafe block. This keyword [relaxes Rust’s guarantees](https://doc.rust-lang.org/nomicon/meet-safe-and-unsafe.html) to allow some operations that could cause undefined behavior (like dereferencing a raw pointer).

### Buffer overflow

While the other vulnerabilities discussed here are prevented by methods that restrict access to undefined memory, a buffer overflow may access legally allocated memory. The problem is that a buffer overflow inappropriately accesses legally allocated memory. Like a use-after-free bug, out-of-bounds access can also be problematic because it accesses freed memory that hasn’t been reallocated yet, and hence still contains sensitive information that’s supposed to not exist anymore.

A buffer overflow simply means an out-of-bounds access. Due to how buffers are stored in memory, they often lead to information leakage, which could include sensitive data such as passwords. More severe instances can allow ACE/RCE vulnerabilities by overwriting the instruction pointer.

Example 4: Buffer overflow (C code)

```
int main() {
int buf[] = {0, 1, 2, 3, 4};
// print out of bounds
printf("Out of bounds: %d\n", buf[10]);
// write out of bounds
buf[10] = 10;
printf("Out of bounds: %d\n", buf[10]);
return 0;
}
```


The simplest defense against a buffer overflow is to always require a bounds check when accessing elements, but this adds a [runtime performance penalty](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4487316/).

How does Rust handle this? The built-in buffer types in Rust’s standard library require a bounds check for any random access, but also provide iterator APIs that can reduce the impact of these bounds checks over multiple sequential accesses. These choices ensure that out-of-bounds reads and writes are impossible for these types. Rust promotes patterns that lead to bounds checks only occurring in those places where a programmer would almost certainly have to manually place them in C/C++.

## Memory safety is only half the battle

Memory safety violations open programs to security vulnerabilities like unintentional data leakage and remote code execution. There are various ways to ensure memory safety, including smart pointers and garbage collection. You can even [formally prove memory safety](https://eprint.iacr.org/2017/536.pdf). While some languages have accepted slower performance as a tradeoff for memory safety, Rust’s ownership system achieves both memory safety and minimizes the performance costs.

Unfortunately, memory errors are only part of the story when we talk about writing secure code. The next post in this series will discuss concurrency attacks and thread safety.

## Exploiting Memory: In-depth resources

[Heap memory and exploitation](https://heap-exploitation.dhavalkapil.com/)

[Smashing the stack for fun and profit](http://www-inst.eecs.berkeley.edu/~cs161/fa08/papers/stack_smashing.pdf)

[Analogies of Information Security](https://brage.bibsys.no/xmlui/bitstream/handle/11250/2403236/15860_FULLTEXT.pdf?sequence=1)

[Intro to use after free vulnerabilities](https://www.purehacking.com/blog/lloyd-simon/an-introduction-to-use-after-free-vulnerabilities)

## 6 comments

TonyJanuary 23rd, 2019 at 17:33Diane HosfeltJanuary 23rd, 2019 at 17:40jasJanuary 24th, 2019 at 02:55Diane HosfeltJanuary 24th, 2019 at 14:43MarkJanuary 24th, 2019 at 10:18DanDJanuary 30th, 2019 at 05:40