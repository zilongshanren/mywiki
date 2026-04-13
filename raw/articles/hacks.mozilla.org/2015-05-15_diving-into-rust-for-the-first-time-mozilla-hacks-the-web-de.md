---
title: Diving into Rust for the first time – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/05/diving-into-rust-for-the-first-time/
author: Szmozsánszky István
published: '2015-05-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![Rust programming language](../../assets/8b305666f41cb258.jpg)

[Rust](http://rust-lang.org) is a new programming language which focuses on performance, parallelization, and memory safety. By building a language from scratch and incorporating elements from modern programming language design, the creators of Rust avoid a lot of “baggage” (backward-compatibility requirements) that traditional languages have to deal with. Instead, Rust is able to fuse the expressive syntax and flexibility of high-level languages with the unprecedented control and performance of a low-level language.

Choosing a programming language usually involves tradeoffs. While most modern high-level languages provide tools for safe concurrency and memory safety, they do this with added overhead (e.g. by using a [GC](http://en.wikipedia.org/wiki/Garbage_collection_%28computer_science%29)), and tend to lack performance and fine-grained control.

To deal with these limitations, one has to resort to low-level languages. Without the safety nets of most high-level languages this can be fragile and error-prone. One suddenly has to deal with manual memory management, resource allocation, [dangling pointers](http://en.wikipedia.org/wiki/Dangling_pointer), etc. Creating software that can leverage the growing number of cores present in today’s devices is difficult — making sure said code works *correctly* is even harder.

So how does Rust incorporate the best of both worlds in one language? That’s what we’ll show you in this article. [Rust 1.0.0 stable](http://blog.rust-lang.org/2015/05/15/Rust-1.0.html) has just been released. The language already has a [vibrant community](http://users.rust-lang.org/t/rust-1-0-launch-event-details-action-required-for-event-organizers/1025), a growing [ecosystem of crates](http://crates.io) (libraries) in its package manager, and developers harnessing its capabilities in a variety of projects. Even if you’ve never touched a lower-level language, it’s a perfect time for you to dive in!

## Use cases for Rust today

So for systems hackers, Rust seems like a great choice, but how about those who are not familiar with low-level languages? Maybe the last time you heard the words “C” and “stack/heap allocation” was 10 years ago in CompSci 101 (or maybe never). Rust provides the performance typically seen only in low-level systems languages — but most of the time it certainly *feels* like a high-level language! Here are a few examples of how you can leverage Rust now in practical applications:

*I want to hack on hardware/write Internet-of-Things applications*

The [IoT](http://en.wikipedia.org/wiki/Internet_of_Things) era and the expansion of the maker movement enables a real democratization of hardware projects. Whether it is the Raspberry Pi, Arduino, or one of the young titans like the BeagleBone or Tessel, you can choose from a slew of languages to code your hardware projects, including Python or JavaScript.

There are times, however, when the performance these languages offer is simply not adequate. At other times, the microcontroller hardware you are aiming for is not suited to the runtimes these languages require: slow chips with tiny memory reserves and ultra-low-power applications still require a close-to-the-metal language. Traditionally that language has been C — but as you might have guessed, Rust is the new kid on the block.

Rust supports a wide variety of exotic platforms. While some of this is still experimental, support includes [generic ARM](https://zinc.rs/) hardware, the Texas Instruments [TIVA dev board](http://antoinealb.net/programming/2015/05/01/rust-on-arm-microcontroller.html), and even the [Raspberry Pi](https://github.com/Ogeon/rust-on-raspberry-pi). Some of the newest IoT boards like the [Tessel 2](https://tessel.io/) even come with official, out-of-the-box Rust support!

*I’m operating high-performance computing applications that scale to multiple cores*

Studies suggest [Rust is already great for HPC (high-performance computing)](http://octarineparrot.com/assets/mrfloya-thesis-ba.pdf). You don’t even have to rewrite your whole application in Rust: its flexible [Foreign Function Interface (FFI)](http://doc.rust-lang.org/book/ffi.html) provides efficient C bindings that let you expose and call Rust code without any noticable overhead. This allows you to rewrite your app module by module, slowly transitioning towards a better developer experience that will result in performance on par with the old code or better. You also get a more maintainable codebase with fewer errors, which scales better on a high number of cores.

*I simply need something fast!*

Rust is great for rewriting performance-sensitive parts of your application. It interfaces well with other languages via FFI and has a tiny runtime that competes with C and C++ in most cases, even when resources are limited.

Despite the work-in-progress nature of the language, there are already business-critical, live production applications that have been making good use of Rust for some time: Yehuda Katz’s startup, Skylight uses high-performance [Rust code embedded in a ruby gem](http://blog.skylight.io/bending-the-curve-writing-safe-fast-native-gems-with-rust/) for data-crunching. The 1.0.0 stable release is also an important milestone in that no breaking changes should happen from now on. That makes it safe to recommend Rust for even the most demanding and robust applications!

Watch Yehuda Katz and Tom Dale talk about the [basics of Rust programming](https://www.youtube.com/watch?v=LazvK39Oc4U) and how they used Rust with Ruby in their app.

## Getting started with Rust

There are many tutorials covering Rust in general, as well as specific aspects of the language. For example, the [Rust blog](https://blog.rust-lang.org) has great articles on various facets of developing Rust applications. There are also excellent introductory talks such as Aaron Turon’s talk at Stanford University. He explains the main concepts and motivations behind Rust nicely, and the talk serves as the perfect appetizer, starting you on your journey:

Talks and tutorials are no substitute for *writing code*, right? Rust’s got you covered in that regard, too! The [Rust Book](http://doc.rust-lang.org/book/) was conceived to help you get started — from installation to that first *Hello World* to providing an in-depth reference for all the core language features.

Another resource worth mentioning is [Rust by Example](http://rustbyexample.com/), which guides you through Rust’s key features, from the basics to the arcane powers of traits, macros, and the FFI. Rust By Example offers invaluable live-editable, in-browser examples with all of the articles. You don’t even have to download and compile Rust, as you can try (and edit) all of these examples from the comfort of your living room couch, just as they are. There is also a [Rust Playpen](http://play.rust-lang.org/) for the exact same purpose.

Not that downloading and installing Rust is much trouble, anyway. Head to the [Rust homepage](http://rust-lang.org) and download the appropriate binary/installer there. The downloads contain all the tools you need to get started (like `rustc`

, the compiler, or `cargo`

the package manager), and are available pre-built for all platforms (Windows, Linux, and OSX).

What is it then, that makes Rust so unique, so *different?*

## The Rust Way

Arguably it’s Rust’s unique [ownership model](https://doc.rust-lang.org/book/ownership.html) that allows it to [really shine](http://manishearth.github.io/blog/2015/05/03/where-rust-really-shines/) — eliminating whole classes of errors related to threading and memory management, while easing development and debugging. It is also invaluable in keeping the language runtime minimal and the compiler output lean and performant.

### The ownership model

The basic principle of Rust’s ownership model is that every resource can belong to one and only one “owner.” A “resource” can be anything — from a piece of memory to an open network socket to something more abstract like a [mutex lock](http://blog.rust-lang.org/2015/04/10/Fearless-Concurrency.html). The owner of said resource is responsible for using, possibly lending out the resource (to other users), and finally cleaning it up.

All this happens automatically, with the help of scopes and bindings: bindings either own or borrow values, and last till the end of their scope. As bindings go out of scope, they either give their borrowed resource back, or in case they were the owner, dispose of the resource.

What’s even better is that the checks required for the ownership model to work are executed and enforced by the Rust compiler and “borrow checker” *during compilation*, which in turn results in various benefits.

### Zero-cost abstractions

Since the correct operation of a program is asserted at compilation time, code that compiles can generally be considered safe with regard to most common types of memory and concurrency errors (such as [use-after-free bugs](https://www.owasp.org/index.php/Using_freed_memory) or [data races](http://doc.rust-lang.org/book/concurrency.html#safe-shared-mutable-state)). This is possible because Rust complains at compilation time if the programmer attempts to do something that violates the principles above, which in turn helps [keep the language runtime minimal](https://news.ycombinator.com/item?id=9477513).

By deferring these checks till compilation time, there’s no need to perform them during runtime (code is already “safe”), and no runtime overhead. In the case of memory allocations, there is no need for runtime garbage collection, either. This — advanced language constructs with little to no runtime overhead — is the basic idea of “zero-cost abstractions.”

Though a thorough explanation of the ownership model is outside the scope of this article, the Rust Book (linked above) and various talks and articles excel in explaining its principles. The principles of ownership and the borrow checker are essential for understanding Rust, and are key to other powerful aspects of the language, like its handling of concurrency and parallelism.

### Two birds, one language construct

Shared mutable state is the root of all evil. Most languages attempt to deal with this problem through the

mutablepart, but Rust deals with it by solving thesharedpart.

—[The Rust Book]

Aside from memory safety, paralellism and concurrency are the second most important focus in Rust’s philosophy. It might seem surprising, but the ownership system (coupled with a few handy traits) also provides powerful tools for threading, synchronization, and concurrent data access.

When you try some of the built-in concurrency primitives and start digging deeper into the language, it may come as a surprise that those primitives are provided by the *standard library*, rather than being part of the language core itself. Thus, coming up with new ways to do concurrent programming is in the hands of library authors — rather than being hard-wired into Rust, restricted by the language creators’ future plans.

### Performance or expressiveness? Choose both!

Thanks to its static type system, carefully selected features, and having no garbage collector, Rust compiles into performant and predictable code that’s on par with code written in traditional, low-level languages (such as C/C++).

By moving the various checks out of the runtime and getting rid of garbage collection, the resulting code mimics the performance characteristics of other low-level languages, while the language itself remains much more expressive. The (seemingly) high level constructs (strings, collections, higher order functions, etc.) mostly avoid the runtime performance hit commonly associated with them. Since the Rust compiler’s output is in the [LLVM intermediate representation](http://en.wikipedia.org/wiki/LLVM#LLVM_Intermediate_Representation), the final machine code makes good use of the LLVM compiler’s cross-platform benefits and all additional (current and future) optimizations automatically.

We could go on for hours about how with Rust you never have to [worry about closing sockets or freeing memory](http://blog.skylight.io/rust-means-never-having-to-close-a-socket/), how traits and macros give you incredible flexibility for [overloading operators](http://rustbyexample.com/trait/ops.html), or even working with Rust’s functional aspect, juggling iterators, closures and [higher order functions](http://rustbyexample.com/fn/hof.html). But we wouldn’t want to overwhelm you early on! Sooner or later you will come across these anyway — and it’s more fun to discover for yourself exactly how deep the rabbit hole is.

So now instead, let’s finally look at some code.

### Say hello to Rust

Without further ado — your very first Rust code:

```
fn main() {
println!("Hello, Rust!");
}
```


Wait, is that it? This may seem a bit anti-climactic, but there are only so many ways to write a Hello World in Rust. Bear with us while we share a slightly more complex example — and another timeless classic.

### What’s all this Fizzbuzz about

We are going old-school with the FizzBuzz program! Fizzbuzz is an algorithm in which we count upwards for all eternity, replacing some of the numbers with *fizz* (for numbers evenly divisible by 3), *buzz* (for numbers divisible by 5), or *fizzbuzz* (divisible by both 3 **and** 5).

Also to show our point (and to help familiarize you with Rust’s semantics), we have included the C and Python versions of the same algorithm:

**Imperative fizzbuzz – C version**

```
#include
int main(void)
{
int num;
for(num=1; num<101; ++num)
{
if( num%3 == 0 && num%5 == 0 ) {
printf("fizzbuzz\n");
} else if( num%3 == 0) {
printf("fizz\n");
} else if( num%5 == 0) {
printf("buzz\n");
} else {
printf("%d\n",num);
}
}
return 0;
}
```


**Imperative fizzbuzz – Python version**

```
for num in xrange(1,101):
if num%3 == 0 and num%5 == 0:
print "fizzbuzz"
elif num%3 == 0:
print "fizz"
elif num%5 == 0:
print "buzz"
else:
print num
```


**Imperative fizzbuzz – Rust version**

```
fn main() {
for num in 1..101 { // Range notation!
match (num%3, num%5) { // Pattern Matching FTW!
(0, 0) => println!("fizzbuzz"),
(0, _) => println!("fizz"),
(_, 0) => println!("buzz"),
_ => println!("{}", num)
}
}
}
```


Even on such a small snippet, some of Rust’s power starts to show. The most obvious difference might be that we are using [pattern matching](http://rustbyexample.com/flow_control/match.html), instead of traditional `if`

statements. We *could* use those, however `match`

is a very useful addition to a [Rustacean](http://www.rustaceans.org/)‘s arsenal.

The other thing to note is the range notation in the `for`

-loop’s declaration (similar to its Python counterpart). It interesting, though, that in this case we *could not* have used a “traditional” C-like for loop instead — as [it is by design unsupported in Rust](http://doc.rust-lang.org/book/loops.html#for). Traditional

`for`

loops are considered error-prone and are replaced with the safer and more flexible [iterable concept](https://doc.rust-lang.org/book/iterators.html).

Here’s a more elaborate look at what happens in the pattern-matching phase of our fizzbuzz example:

```
...
// For pattern matching, we build a tuple, containing
// the remainders for integer division of num by 3 and 5
match (num%3, num%5) {
// When "num" is divisible by 3 AND 5 both
// (both remainders are 0)
// -> print the string "fizzbuzz"
(0, 0) => println!("fizzbuzz"),
// When "num" is divisible by 3 (the remainder is 0)
// Is "num" divisible by 5? -> we don't care
// -> print the string "fizz"
(0, _) => println!("fizz"),
// When "num" is divisible by 5 (the remainder is 0)
// Is "num" divisible by 3? -> we don't care
// -> print the string "buzz"
(_, 0) => println!("buzz"),
// In any other cases, just print num's value
// Note, that matching must be exhaustive (that is,
// cover all possible outcomes) - this is enforced
// by the compiler!
_ => pintln!("{}", num)
}
...
```


This is not the place to go deep on how pattern matching or destructuring work, or what tuples are. You’ll find excellent articles on these topics in the [Rust Book](http://doc.rust-lang.org/book/primitive-types.html#tuples), the [Rust Blog](http://blog.rust-lang.org/2015/04/17/Enums-match-mutation-and-moves.html), or over at [Rust By Example](http://rustbyexample.com/flow_control/match.html), but we think it’s a great way to demonstrate the features and nuances that make Rust both powerful and effective.

### How about some functional Fizzbuzz

To expand on the last example and demonstrate Rust’s true flexibility, in our second example we’ll crank our fizzbuzz up a notch! Rust calls itself multi-paradigm. We can put that to the test by rewriting our fizzbuzz example in functional style. To help put the code in perspective, we will also show the implementations in JavaScript (the ECMAScript 6 flavor), too:

**Functional fizzbuzz – JavaScript (ES6) version**

```
Array.from(Array(100).keys()).slice(1)
.map((num) => {
if (num%3 === 0 && num%5 === 0) {
return "fizzbuzz";
} else if (num%3 === 0) {
return "fizz";
} else if (num%5 === 0) {
return "buzz";
} else {
return num;
}
})
.map(output => console.log(output));
```


**Functional fizzbuzz – Rust version**

```
fn main() {
(1..101)
.map(|num| {
match (num%3, num%5) { // Pattern Matching FTW!
(0, 0) => "fizzbuzz".to_string(),
(0, _) => "fizz".to_string(),
(_, 0) => "buzz".to_string(),
_ => format!("{}", num)
}
})
.map(|output| { println!("{}", output); output })
.collect::<Vec<_>>();
}
```


Not only can we mimic JavaScript’s functional style with [closures](http://doc.rust-lang.org/book/closures.html) and functional method calls, but thanks to Rust’s powerful [pattern matching](http://tmpvar.com/blog.rust-lang.org/2015/04/17/Enums-match-mutation-and-moves.html), we can even trump JavaScript’s expressiveness a bit.

Note: Rust’s iterators are lazy, so we actually need the `.collect()`

call (which is called a *consumer*) for this to work — if you leave that out, none of the above code will execute. Check out the [consumers](http://doc.rust-lang.org/book/iterators.html#consumers) section of the Rust Book to learn more.

### Picking a project

You’re eager to dive into Rust and ready to start something cool. But what to build? You could start small—write a small app or a tiny library, and upload it to [crates.io](http://crates.io). People have created many exciting projects in Rust already — from pet *nix-like kernels to embedded hardware projects, from games to web server frameworks, proving that the only limit is your imagination.

If you want to start small, but contribute something useful while learning the intricacies of Rust programming, consider contributing to some of the projects already thriving on GitHub (or even the Rust compiler itself — which is also written in Rust).

Or, you could start by rewriting small parts of your production app, and experimenting with the results. Rust’s [Foreign Function Interface (FFI)](http://doc.rust-lang.org/book/ffi.html) is intended as a drop-in replacement for C code. With minimal effort you could replace small parts of your application with Rust implementations of the same code. But interoperability doesn’t stop there — these C bindings work both ways. This means you can use all standard C libraries in your Rust apps — or (since many programming languages come with standard C interface libraries) make calls back-and-forth between Rust and Python, Ruby, [node.js](http://calculist.org/blog/2015/12/23/neon-node-rust/) or even [Go](https://github.com/medimatrix/rust-plus-golang)!

Watch Dan Callahan’s talk [“My Python’s a little Rust-y](https://www.youtube.com/watch?v=3CwJ0MH-4MA) on how to hook up Rust with Python.

There are virtually no languages that don’t work with Rust: want to [compile Rust to JavaScript](http://www.reddit.com/r/rust/comments/20nnkk/rust_and_emscripten_a_small_success/) or [use inline assembly in your code](https://doc.rust-lang.org/book/inline-assembly.html)? Yes, you can!

**Now get out there and build something awesome.**

Please don’t forget — Rust is not simply a programming language — it’s also a *community*. Should you ever feel stuck, don’t be shy to ask for help, either on the [Forums](https://users.rust-lang.org/) or [IRC](https://chat.mibbit.com/?server=irc.mozilla.org&channel=%23rust). You could also share your thoughts and creations on the [Rust Reddit](http://www.reddit.com/r/rust/).

Rust is already great — it’s people like **you** who are going to make it ever more *awesome*!

## About Szmozsánszky István

Known by most as "Flaki", JavaScript-fiddler, Firefox OS enthusiast and IoT hacker. A Service Workers advocate fighting for open webapps' parity with native — meanwhile being utterly fascinated by microcontrollers, NFC and hardware hacking as a sideshow.

## 6 comments

IvanMay 15th, 2015 at 18:34inconMay 15th, 2015 at 19:53RedgeMay 16th, 2015 at 04:11Havi Hoffman [Editor]May 18th, 2015 at 10:07gialloporporaMay 30th, 2015 at 13:41gialloporporaJune 1st, 2015 at 03:48