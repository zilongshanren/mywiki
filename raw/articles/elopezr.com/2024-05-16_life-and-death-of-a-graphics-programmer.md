---
title: Life and Death of a Graphics Programmer
url: https://www.elopezr.com/life-and-death-of-a-graphics-programmer/
author: Redorav
published: '2024-05-16'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Recurrent internet discussions show a divide between programmers working in different industries. Topics like code clarity, performance, debuggability, architecture or maintainability are a source of friction. We are, paraphrasing the ![](../../assets/75fd2dc118065942.jpg)


[quote](https://english.stackexchange.com/questions/74737/what-is-the-origin-of-the-phrase-two-nations-divided-by-a-common-language), industries divided by a common language. I am curious about other programmers’ experiences, and I wanted to present a general view of mine as a graphics programmer in games, in the form of anecdotes and examples. It’s not meant to be a rant or exhaustive, rather a description of common problems, pitfalls and personal experience sprinkled in. The target audience is either videogame developers who want to nod throughout or developers writing very different software who are curious about what we do. It focuses on C++ and shader languages because that’s mostly what we use.

**Hard Requirements**

Videogames cram very demanding processing into modest mainstream hardware (consoles, mobile), attempting to run fast and consistently; a combination of I/O, network, audio, physics, pathfinding, low latency input, gameplay, and displaying images on screen in a handful of milliseconds. Similarly, systems like embedded hardware applications (cars, space, low latency trading) are also very constrained but operate in a very specialized domain. On another part of the software spectrum we find UI-centric programs such as word processors, browsers or management software, that are more event-driven and tolerant to a bit more latency.

There are also requirements games don’t have. Most don’t have stringent security concerns like OSs, transportation or banking (except online games or competitive e-sports). Game-breaking bugs aren’t life-threatening. High-frequency trading or automotive image processing applications have very strict correctness requirements, whereas players are mostly tolerant to some glitches as long as they’re having fun. Games don’t distribute their source code or interface with the world’s code so certain API restrictions don’t exist, e.g. we don’t build DLLs or provide SDKs. Some code is specific to a release so there’s a subset that can be hacked together right before shipping.

With that in mind, videogames care about performance in many more areas than others, not just runtime performance but also the tools. Performance becomes part of system correctness. Just as examples, all these situations from different domains are wrong:

- Audio lags behind the image, or image lags behind the audio in a cutscene
- Networking is too slow in an online game and the games pauses frequently
- Streaming is too slow and the game stutters as you traverse
- Inputs lags behind the response and causes lack of control

| I once saw a cutscene system where the audio is not synced to the video/animation but instead the video tracks the audio, to avoid the typical audio drifts and getting more consistent synchronization between them. Humor and fast action is the essence of those cutscenes, and that’s a creative way to make sure the comedy lands correctly |

**Waiting for Mr Compiler**

I spend an inordinate amount of time waiting for the computer to do things I need to work. Sometimes it’s loading, sometimes processing assets, but most of the time it’s compiling, both C++ code and shaders. Every company I worked for always used C++ for the engine and HLSL for shaders. Compile times are not unique to games, but it is the reality in every large codebase I’ve worked on; a frustrating, soulless ritual necessary to get your code from doing A to doing B. It distracts from doing meaningful work and breaks concentration. It is the very opposite of fast iteration. Let’s just state some bullet points from my experience:

- A full rebuild of “the engine” can take anywhere from 10 to 40 minutes. I know of smaller codebases where it’s faster, and there’s definitely worse (e.g. Unreal Engine)
- A full rebuild of “the shaders” can also take a really long time, depending on how your shader setup works
- An incremental build for a single file change can take anywhere from seconds to a full rebuild’s worth of time, depending on whether you touched a header included everywhere or a cpp with no dependencies
- Many shops use Incredibuild to speed up compilation. Even that is often not enough
- Code lives in SSD/NVMe drives now, which means I/O is rarely the issue (compiling through the network does reintroduce the problem)
- Parallel compilation is standard these days, all cores are engaged in this process
- Linking is normally single threaded and can take very long
- Throwing more hardware at the problem mitigates it briefly until your codebase inflates again
- Some codebases use PCHs and others Unity builds. Both are improvements but also manual and difficult to maintain
- We compile for many platforms. A rather extreme example,
[some LEGO games shipped for 7 platforms simultaneously](https://en.wikipedia.org/wiki/Lego_Star_Wars:_The_Force_Awakens) - Every platform’s tooling is different. You might find that compiling for platform X is much slower than for platform Y

A big part of this problem stems from C’s inclusion model, the ancient and for decades refined scribal technique of copy pasting code, I’ll never understand why C++ didn’t evolve something akin to modules decades earlier and spends time developing library addons that bring anecdotal value and further slowdowns. C++ takes pride in the ‘zero-cost abstraction’ model, but that simply does not apply to compile times. Any time you include a header file in a compilation unit, you are paying a non-negligible cost even if you don’t use anything: many standard library headers take hundreds of milliseconds to compile. If you have thousands of cpps instantiating it, this adds up enormously. C++20 modules are making their way into compilers, but large codebases are going to have a hard time migrating.

| There is a constant tension between convenience and compile times. I worked on a codebase where all rendering headers were put inside “render_api.h” and code from other teams included it. It was very simple to set up, but any time I touched a rendering header, it recompiled the entire codebase due to transitive inclusion. Breaking the header apart took a long time whereas putting it in the first place took no effort. Small actions can have large consequences, and the language has not provided a solution for decades |

**A Template to Confusion**

In [The Sorcerer’s Apprentice](https://en.wikipedia.org/wiki/The_Sorcerer%27s_Apprentice), the protagonist is tired of trudging along carrying water when he has the idea to leverage his master’s magic to do it for him. His lack of experience backfires as things spiral out of control because he cannot remember how to undo the spell. In a similar fashion C++ template and macro magic promises to help with many problems but can cause lots of headaches later on. I’ve seen the allure: fighting the compiler hard to get it to do something specific gives a sense of accomplishment. There might also be an element of sunken cost to it. In any case, overusing it is trivial and undoing it not easy.

| One codebase had a powerful shader reflection facility with lots of template and macro metahackery which worked if you left it alone but was incredibly hard to debug, modify and extend. In hindsight, an alternative like code generation could have worked better |

There are valid reasons for its usage but they are often misused and have a lot of downsides:

- Template or macro code beyond the basic is difficult to read and debug
- Error messages are difficult to understand unless you’re experienced
- Template resolution rules are hard to memorize and predict, SFINAE is very complicated
- Templates are slow to compile (see
[rule of Chiel](https://youtu.be/EtU4RDCCsiU?si=67cStT01gJs3vUJl&t=560)) - Template rules are enforced differently in different compilers, adding complexity
- The STL’s usage of templates is essentially infinite, a non-trivial language on top of C++

| I plead guilty to using many templates in my own
|

Unfortunately, there is an assymmetry here: liberal use of templates does a lot of damage to large codebases that you don’t counter by not using them, and adding headers that include template code is easier than it is to remove them.

**Death By a Thousand Shades**

As graphics programmers, shaders are our bread and butter. Here are these relatively small programs that run millions of times in parallel on the GPU to produce pretty images on screen. The shader languages we use to write them are very simple in nature; all the code is inlined, recursion is not allowed, templates are very recent, so you’d think it wouldn’t be much of a pipeline issue. However, reality is always more complicated, because there are so many shaders!

Shader philosophies differ in two axes that I’ll call responsibility and usage. Responsibility refers to who has access to authoring the shaders; it can be just graphics programmers, or technical artists, or general artists and even designers; generally, the more people you have making shaders, the more you’ll have to compile. The usage axis refers to where in the frame these shaders run; for example, shaders that describe material properties typically run during a geometry phase, and lighting or post effect shaders tend to run at the end of the frame in a fullscreen pass. The geometry or material phase is typically where most variation comes from, as you’ll have shaders doing opaque surfaces, cloth, hair, skin, transparency, etc. These variations exist in many places of the frame: for example, depth-only shaders for shadows or depth prepass, transparency shaders, variations for using lightmaps, etc. if I had to guess I’d say that 95% of shaders in a complex game fall into this category. Since the shaders that artists modify is in this second category, we encounter the so-called [combinatorial shader explosion](https://therealmjp.github.io/posts/shader-permutations-part1/).

![Luciano Jacomeli - Compiling Shader 4.24](https://cdna.artstation.com/p/assets/images/images/024/514/180/large/luciano-jacomeli-2.jpg?1582664776)


To put into perspective the extent to which these philosophies vary, consider that Doom 2016 keeps a tight control over shaders where only graphics programmers can modify them, and apparently needs a few hundred shaders, whereas on the other side a typical Unreal Engine project probably ships with 10,000 shaders. Within these extremes, I’ve worked at places where only programmers could create and modify shaders, places where only the technical artists could create the material shaders and places where any artist could create them. The compile times for these range wildly for a full rebuild of shaders.

This of course is only part of the problem, as compilation (at least on PC/mobile) is two-staged: the compilation that happens on the devs’ machines, and the one that happens on the users’ machines. This first step takes the textual shader written either manually by a programmer or through a node graph tool and produces a temporary, optimized common representation of the shader. This needs to be translated to the vendor-specific shader instructions during PSO compilation such as AMD’s RDNA ISA, hence the [#stutterstruggle](https://www.youtube.com/hashtag/stutterstruggle) that has become somewhat of a meme in PC gaming lately.

| One place I worked at had an interesting shader compilation philosophy: when artists saved the material they were authoring, they would compile for all platforms and the binaries would get uploaded to version control. This had the really nice property that nobody else had to compile that shader on their machine, and the disadvantage that making sweeping changes to the shaders became difficult |

**A Heap of Trouble**

Another big problem that makes games difficult is heap allocations. Because games are so dynamic, they tend to spawn and destroy things left and right, be it particles, debris from destruction, short-lived sounds, network packets, etc. In rendering specifically, every frame we prepare and discard thousands of rendering commands, short-lived vertices or per-frame constant buffers. The volatile nature of it is such that if we mainly used heap allocations to do these things, we would encounter:

**Fragmentation:**running out of memory that’s full of holes, small allocations wasting memory divided into larger blocks**Contention/Unpredictability:**threads will block each other for shared resources, hitching at unpredictable times**Cache:**a new allocation is essentially a cache miss

A large part of optimization really boils down to avoiding heap allocations. Instead, games reserve large blocks at boot time, subdivided according to a resource type, create object pools to reuse the memory, arena allocators, or just use the stack, among other techniques. If you e.g. need scratch memory for sorting, allocating on the stack is essentially free and trivial to dispose of. Containers, structures and allocators that encourage this memory pattern are essential. If you’re interested in memory allocation strategies I’d recommend giving [this article](https://www.gingerbill.org/series/memory-allocation-strategies/) a read too.

| Years ago I worked programming Android games in Java. Because the language doesn’t provide value types, even vector math and string processing would keep the heap/garbage collector active and hitching all the time. We resorted to global StringBuffers and Vectors for intermediate calculations, a very cumbersome and error-prone use of the language |

**A Virtual Problem**

[Casey’s performance video](https://www.computerenhance.com/p/clean-code-horrible-performance) sparked a lot of conversation. It compares a vtable model against a switch for polymorphism and measures why virtual functions can be the wrong tool for a set of problems we deal with in games, namely those that process entities at scale. It’s an architectural decision that affects your project’s performance and hard to rework when dealing with deadlines. While I was writing this I saw a great [Youtube talk](https://youtu.be/NAVbI1HIzCE) by Jason Booth who explains this much better, but I’ll give my experience anyway. Consider a real-world case where we have several types of particle emitters, and the simulation happens on the CPU. The virtual function approach looked more or less like this:

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 | class IParticleEmitter { virtual void UpdateParticles() = 0; }; class SparksEmitter : public IParticleEmitter { virtual void UpdateParticles() override; }; class RibbonEmitter : public IParticleEmitter { virtual void UpdateParticles() override; }; vector<IParticleEmitter*> ParticleEmitters; UpdateAllParticleEmitters() { for(IParticleEmitter* particleEmitter : ParticleEmitters) { particleEmitter->Update(); } } |

On the surface it doesn’t look *that* bad. It is relatively easy to understand, and adding a new emitter type is easy. Unfortunately this scales poorly for many particle emitters, and paradoxically has nothing to do with virtual functions in the grand scheme of things; it’s more about where the data lives and how it is processed.

- Update() is called per emitter regardless of the number of particles. Any setup overhead is larger for fewer particles
- Indirection per emitter. Virtual polymorphism requires pointers or references so we can’t put value types in the array
- No guarantee that emitter memory is contiguous. Pointers are but the data itself could come from anywhere
- Typically pointers point to the heap. You could maybe keep a pool of objects in sync with your pointers
- Inlining is prevented as the compiler doesn’t know what code is going to run
- Logically similar data (particles of the same type) is physically disjoint, preventing batch processing or SIMD
- Finally, the virtual dispatch itself, typically a couple of indirections

A second approach could group emitters together based on type and make all the data contiguous.

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 | class SparksEmitter {}; class RibbonEmitter {}; vector<SparksEmitter> SparksEmitters; vector<RibbonEmitter> RibbonEmitters; UpdateAllParticleEmitters() { for(SparksEmitter& emitter : SparksEmitters) { emitter.Update(); } for(RibbonEmitter& emitter : RibbonEmitters) { emitter.Update(); } } |

We’ve given up the ability to add a new particle emitter type without knowing how the update loop works, but now we can have contiguous memory, fewer indirections, no virtual dispatching and greater ability to inline code. We still can’t process particles from different emitters together, so let’s take it further:

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 | class SparksEmitter { vector<SparksParticle> particles; }; class RibbonEmitter { vector<RibbonParticle> particles; }; vector<SparksEmitter> SparksEmitters; vector<RibbonEmitter> RibbonEmitters; UpdateAllParticleEmitters() { // Collect all particles (doesn't have to happen during Update, much better if it's during add/remove) vector<SparksParticle> SparksParticles = CollectAllParticles(SparksEmitters); vector<RibbonParticle> RibbonParticles = CollectAllParticles(RibbonEmitters); for(size_t i = 0; i < SparksParticles.size(); i += 8) { UpdateSparksParticlesBatch(i, i + 8); } for(size_t i = 0; i < RibbonParticles.size(); i += 8) { UpdateRibbonParticlesBatch(i, i + 8); } } |

We are now able to process particles in batches of N (which opens up options e.g. SIMD processing), where all particle data is contiguous for related particles, code can be inlined properly and everything lives happily in the cache. I don’t think we’ve traded off much in terms of readability, and we’ve gained a lot in terms of processing our data in whatever way the machine likes it best. You can probably wrap it up in a ParticleManager and give it the responsibility for all particles. Most problems just need data-driven processing, yet we’re told to make everything object-oriented, loosely coupled, flexible and interface-like.

| The last problem caused by the code above was moving it onto the GPU. Each emitter has two stages: simulation and rendering. Since emitters are processed separately we are forced to interleave simulation and rendering. Toggling compute and graphics is very costly and inefficient; it will cause pipeline stalls and context rolls. In this case the GPU was flatlining during particle rendering and unable to batch the work properly. The solution would have been to collect all related particles, group them into batched compute jobs, then render them all in a few draw calls |

**Code is Not a Painting**

The code I’ve seen in most game codebases is decades old, a sprawling landscape full of ancient landmarks mixed in with new skyscrapers. As people come and go, the ancestral knowledge of what a system does and why is lost, and in its place new code takes over, leaving remnants of the old behind. It’s not a pretty sight. Some programmers spend a lot of time discussing “clean” and “ugly” code. However, code itself is not something you admire for some unspecified visual quality. We have forgotten CPUs run our code. In our world it’s meant to be fast and correct for other departments (art, design, gameplay), and ultimately fast and correct for the player. Some books and advice try to convince programmers that code should be pleasing, elegant or ingenious. I don’t think the wording and approach is conducive to good software, even if I can agree with some ideas.![](../../assets/fe49e6a226007982.jpg)


Trying to make code understandable is a desirable target. We want our colleagues and future selves to navigate code easily to read and make changes, the rationale for code conventions and architecture. However, in the name of clean code we introduce towers of overabstraction, metaprogramming and syntax sugar for programmer convenience and pay a large cost for it in terms of complexity and overhead. There are lots of rules, like “functions should be short”, or “files should contain at most N lines”. Many programmers like to focus a lot on this prescriptive way of programming. One thing many seem to like is to abstract away even the simplest constructs. A simple example, adapted from cppreference:

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 | std::string str = "Hello String"; // Indexed loop (C++) for(size_t i = 0, size = str.size(); i != size; ++i) { str[i] = toupper(str[i]); } // Iterators (C++98) for(auto iter = str.begin(), enditer = str.end(); iter != enditer; ++iter) { *iter = toupper(*iter); } // Ranged-for (C++11) for(char& c : str) { c = toupper(c); } // STL-like (C++17) #include <algorithm> std::transform(str.begin(), str.end(), str.begin(), toupper); |

It is way too simple but can illustrate the point. The snippets above follows the chronological order in which these facilities were introduced into C++. Let’s evaluate each option:

- Standard loop: simple to read, maybe int vs size_t can alter the assembly
- Iterators: not great to look at, abstracts container implementation (whether it’s a good thing is perhaps debatable)
- Ranged for: perhaps clearest in terms of intent, just uses iterators under the hood

The fourth option, while a one liner, has the following problems in my view:

- Opaque/hard to read, need to know what the standard meant by ‘transform’
- Easy to get wrong if you mix up your iterators
- Harder to debug when something doesn’t work
- Pay several hundred ms to include <algorithm> if your cpp wasn’t using it already
- Performance is the same as every other option in an optimized build
- Performance at least 25% slower vs all options (57% vs standard loop) in a debug build. We care about debug builds

| Option | Clang Debug | Clang -O3 |
| Standard Loop | 1.0x | 1.0x |
| Iterators | 1.28x | 1.004x |
| Ranged For | 1.13x | 1.002x |
| std::transform | 1.57x | 1.003x |
| std::for_each | 1.42x | 1.0x |

So what are the tradeoffs and what have we gained? You can modify [the example](https://quick-bench.com/q/e1cII5Zstl4H-5OHMgN_TU-F2PE) and use other similar functions like [accumulate](https://quick-bench.com/q/82vT03aHGCUtFNoKJ9B-VJ58wV4) or remove (which surprisingly [doesn’t remove](https://youtu.be/26aW6aBVpk0?si=hz0786OKC8buwJqz&t=2675)), change compilers or C++ versions and the result is the same. Is it more convenient or readable? I don’t think so, but this is [the way C++ seems to get developed at the moment](https://youtu.be/nqfgOCU_Do4?si=oOAvIKQb6ZFBc1cz&t=980), with features like ranges and views now making their way into C++20 and C++23.

| This obviously doesn’t just apply to C++. I was talking to a friend recently who was complaining about a colleague who liked to write for loops in C# using clean and elegant LINQ (in Unity), and separating queries that could be done in a single loop into multiple lines. Needless to say he had to rewrite all for performance, adding unnecessary work |

I just don’t agree with the philosophy at all. Is it even faster when optimized? Some people claim it is but I’d need to see a proper benchmark; maybe these examples are too simplistic. In any case, if contemporary software was fast, snappy, bug- and error-free using clean code principles and abstractions perhaps there would be some argument. The sad reality is, it isn’t. [Software becomes slower faster than hardware becomes faster](https://en.wikipedia.org/wiki/Wirth%27s_law). We’re only able to mostly get away with it thanks to the incredible advances of hardware. We may be able to continue to be code Picassos, but for how long? We don’t need clean code, we need to relearn that code is a tool and not a painting.

**Write-Once, Read-Multiple**

Code has access patterns just like memory, and in my experience code is written much less frequently than it is read, and is also read more frequently by colleagues than by you. Therefore optimizing for less typing is a very unproductive effort. We have automated code completion, variable renaming and good ol’ copy pasting. We don’t type code like novelists, we type in short bursts and use all sorts of symbols to decorate actual words. We don’t actually write that much new code either, as a lot of the regular work is to modify or improve existing code. Only when writing comments do we actually form a coherent stream, and judging by what I’ve seen we don’t spend a lot of time writing those either (I think we should). Worrying about code beauty or conciseness (fewer lines of code) is a futile exercise if the tradeoff is a non-trivial cognitive load when reading the code and often worse performance. Help your reader. Help your old future self. Don’t be clever with syntax. These types of practical points that don’t introduce penalties I can definitely get on board with. Without meaning to be exhaustive:

- Spend a bit of time trying to name things, especially systems. Naming must be up there with NP problems because it is hard
- Acronyms for symbol names will have your colleagues and new hires wondering what numtl, pxm, nurndr, and clidx mean. Sometimes people even create wiki glossary pages
- Use other teams’ code conventions in their code, even if you don’t like it. Be humble! They’ll read it a lot more than you
- Don’t make complex function stacks and lots of little functions or you’ll end up jumping around the codebase (and the debugger) trying to get a complete picture
- Don’t make complex class hierarchies and architecture to fit some SOLID principle. Abstract when you need to and not earlier
- Try not to reuse variables. If you comment something out in the middle, all the intermediate state is lost
- Document your intention (the action is the code itself) and don’t be noisy.
**//**initialize i or // shift 4 bits only adds noise - Removing braces, spaces or indentation to remove a line of code here and there is not great if someone else spends time wondering whether a bug’s lurking somewhere, or where a scope begins and ends
- Other readability “shortcuts” like writing .5 instead of 0.5 or 1. instead of 1.0 save a tiny amount of time and make your code less readable
- Copy pasting is sometimes fine. Put 3.1415f if the alternative is to drag in math.h just for that. Pythagoras doesn’t care

Anyway, the guiding principle is that you should try to write the code that requires fewer explanations to someone unfamiliar with the code, or clarify strange-looking code with a comment, given that C++ lets you do things in very complex ways. We all have our assumptions and knowledge so it’s bound to be imperfect, but at least it sets an objective.

| One thing I’ve seen in the wild is team-local code conventions. For example, the audio team might use underscores for variables and the rendering team might use camel case. It’s not ideal but the convention itself isn’t that important, what matters is being consistent. It’s still a good idea to set some guidelines early on whenever possible |

**Debug Builds Matter**

This also seems to be a topic we have a hard time agreeing on, for reasons I cannot fathom. I use the Visual Studio debugger every single day. It has been the StandardTM in the games industry for a long time, and is used to debug PC, consoles, mobile, whatever you need. I use breakpoints, watch windows, inspectors, syntax highlighting, natvis visualizers, the whole package, and it helps me immensely. Print-style debugging has its place in specific use cases like logging, threading or hard to reproduce issues. Game studios keep a debug build running at playable framerates (read: 15-25fps) with asserts, bound checks, useful logging, etc. If your debug build is so slow that your programmers won’t use it, you’re doing yourself a disservice. A debug build is not the one you hesitantly reach for when you get a bug, it is the *default* for programmers during development.

A debug build is by definition less optimized than a release build, but that doesn’t mean everything’s fair game because the compiler will optimize it for the end product. Sometimes that means avoiding deep callstacks, using members directly instead of “cleaner” accessors, copy pasting code or using simpler constructs. The program state needs to be simple to inspect, meaning there is value in not creating lots of indirection or multiple interconnected small little functions. This takes us back to the std::transform example, where we inadvertently sacrifice a lot in our debug build to get arguably not much in return.

| Not all debug builds are made equal, sometimes you can mix and match. In one of the places I worked at, gameplay programmers had the issue that their build was too slow to fine tune gameplay, but still wanted to be able to debug their code. The solution was a sort of middle ground where engine code was fully optimized (they didn’t work at that level anyway) but their code was fully debuggable |

**Modern C++ and the STL**

The previous talk brings us to the modern C++ and specifically the STL, always a contentious topic. All game companies I’ve worked for rolled out their own containers and algorithms, with one exception which used parts of the STL. The STL has some good things, but given what we’ve discussed so far, I think I’m not saying anything new by highlighting a few issues that can make game studios consider using alternatives or rolling their own.

- Compile times are high, and also not granular enough. Sometimes you just want a class or a function without transitively bringing in other parts
- There are no STL containers that don’t heap allocate. This is the reason
[EASTL](https://github.com/electronicarts/EASTL)provides**fixed_vector**,**fixed_string**and other fixed containers, and people will happily write code using alloca() and variations. While the STL containers have small-size optimizations, the standard doesn’t mandate the size, so it will vary across compilers, platforms and implementations which is undesirable - There are other missing facilities widely used in gamedev such as intrusive pointers and containers, or alternative hashmaps
- The STL can be
[very slow in debug builds](https://blog.demofox.org/2019/08/10/measuring-debug-stl-container-perf-cost-in-msvc/), and performance can be unpredictable across implementations. Code that is not consistent across platforms and you cannot fix is a liability - The STL is not easy to modify for specific use cases. Because it’s a closed ecosystem provided by the compiler, it’s hard to customize to something else even if 99% of what you want is there
- The code in many STL implementations is fairly esoteric and hard to read, and I don’t think there’s good reasons for it. In an ideal world the STL would be a source of learning, an example of the power of C++
- STL updates are tied to C++ revisions. I think this is a big shortcoming of the STL. Some industries are very slow to adopt. The language should be able to move forward independently and codebases want to update their code much more quickly. If I’m stuck on C++14 for a platform I will have to whip up my own version of span<T> as I cannot use the one from the standard, but C++17 is not an actual requirement
- The STL caters for a very general use case. It supports exceptions, RTTI and other features some industries don’t use
- If you watch Cppcon talks these days, a lot of it focuses on ‘clean’ or ‘elegant’ code provided by the STL, which to me is both incomprehensible for most programmers or just too far removed from the machine to be efficient. Some are solving artificial or syntax sugar problems instead of addressing glaring omissions in the core language
- Picking up on the previous point, many C++ features should belong in the core language. The spaceship operator or initializer_list are defined in terms of headers, which adds compilation overhead. Comparison operators are not that hard to write

Some efforts such as constexpr, module standardization or concepts can be good for the language. Unfortunately, a lot of the improvements to C++ come in late and other efforts such as ranges or linear algebra are more academic than I think people need, fruit of its committee-driven approach to language evolution. There are good libraries out there that do a better job than the STL. I don’t think some of the issues here are necessarily C++-specific though, other languages have long compile times and none of these highly specific fixed containers or facilities. C++ is ultimately a systems programming language that caters to many users, and should be much more dynamic in providing language features that users can then use to build libraries on top of. In this regard I really like [Circle](https://www.circle-lang.org/)‘s approach and highly recommend [this talk](https://youtu.be/x7fxeNqSK2k?si=fFSEZWyaDiHgYsEL).

**The Tools of the Trade**

When we talk about tooling, we talk about two things: the tooling used by programmers and the tooling developed by them for internal use (artists, designers, etc). Both are important for iteration.

For programmers, Visual Studio has been the hallmark of programming environments on Windows since essentially forever. They were basically 20 years ahead of everything else for a very long time. Watch windows, thread debugging, callstacks, data breakpoints, natvis visualizers (to name a few), I can’t see myself working on a million line codebase without all of this (or something similar, I’ve also used 10x, XCode and Eclipse, go for whatever provides the proper tools) Yet somehow, as hardware has become orders of magnitude faster, the Visual Studio experience has become clunkier. I’ve seen codebases where loading the main solution took several minutes. Searching for a string can randomly take minutes or hang, or loading a watch/threads/breakpoints window takes 20 seconds. In one codebase I worked on it would crash every few days. There was one particularly egregious example where installing the Visual Assist plugin would cause it to run out of memory and crash after a minute. Moving the codebase from VS2017 to VS2019 fixed it, but that’s not something a large codebase can do at any time. If you try [older versions](https://youtu.be/GC-0tCy4P1U?t=2166) on contemporary machines you’ll notice things used to be snappy and fast, and the core functionality hasn’t changed too much. Many of the things I used to be able to do I can do today, just slower.

For graphics programmers specifically, we need a particular set of tools to analyze and debug: frame analyzers. These are really important as they show what the GPU is up to in a linear, visual way. A graphics debugger will present the different drawcalls from the point of view of the graphics API the application is using, along with shaders, textures, buffers, etc. These tools were actually pretty cool, the first that I know of on PC was the old version of what is known today as [PIX](https://therealmjp.github.io/posts/d3d-performance-and-debugging-tools-round-up-pix/). There have been [many others](https://www.khronos.org/opengl/wiki/Debugging_Tools) that unfortunately end up dying so the landscape of graphics debugging is in a relatively weird place, where you can end up needing a myriad of programs to analyze the same frame from multiple perspectives or APIs, e.g. Renderdoc, PIX, NSight, Intel GPA, Radeon Profiler, etc. Using these can be involved depending on what you’re doing. Say you have an application and you’re trying to decide which tool to use:

- Renderdoc is my first goto as overlays and resource usage is much faster to track down, but there are no performance counters or support for pixel debugging or raytracing
- PIX does support new features and has performance counters and occupancy graphs, but the overlays and data visualization could do with some work, is slower and only supports D3D12
- NSight is NVIDIA-focused (some features like counters disabled on other cards) and Radeon GPU is AMD only

Graphics APIs are complex and the tools can sometimes fail to replay, crash or just be quite slow due to the amount of data needed. In AAA, replays can be many GBs worth of data. On mobile the landscape is even more fragmented, as each vendor has [its](https://developer.apple.com/documentation/xcode/metal-debugger) [own](https://developer.arm.com/Tools%20and%20Software/Graphics%20Analyzer) [tool](https://developer.qualcomm.com/software/snapdragon-profiler), which is probably good if the tool shows deep insights of the hardware but as a developer it can get complicated fast.

There are othe tools whose performance is critical, necessary for other people to do their job. Texture compression, precomputed lighting generation, mesh optimization, PVS building, LOD generation, navigation meshes, multi-purpose editors, debug menus, there’s so many additional internal tools we write for non-programmers to use. One side of performance is runtime, e.g. how long it takes to execute. It doesn’t seem like a good idea to consciously sacrifice collective hours of waiting for processes to finish so that my code can be ‘maintainable’, ‘cleaner’ or ‘nice’. The other side of tools is how fast I can find and invoke the command I’m looking for, e.g. is my UI well organized, does it have clear labels, identifiable buttons and tooltips. Artists and designers are our clients and they need to be happy and productive using the widgets or whatever else they need to build the world. Even if your main job is not to be a tools programmer you’ll eventually need to pay attention and expose UIs in ways that make sense; as a graphics programmer I’ve had to add countless tickboxes, sliders and buttons for all sorts of editor objects that are lighting-related. It’s way more important to focus on whether the element is in the correct category, the ranges are correct and the tooltips are legible and make sense, than what the code to do all that looks like, and artists absolutely won’t care, ever, whether you used some fancy lambda to achieve the end result.

| I once worked on an engine where we were revamping the editor completely. The previous one hadn’t aged well and was kind of clunky – the kind of editor you’d expect a programmer to make, full of inconsistent menus and ugly icons borrowed from who knows where. A UI designer eventually came on board and she did a wonderful job – iterated over many designs, focused on consistency, readable icons and color schemes which made a world of difference |

**Unearthing History**

Reading a codebase you’ve just arrived at can be a daunting task; sifting through thousands or even millions of lines of code you’ve not written to get at the line you’re looking for takes a combination of patience and experience. If you have knowledgeable colleagues that can point you in the right direction, it can save a ton of time and sanity. Once you become more experienced the search for code can flip on its head: you have a vocabulary of terms and an expectation of how things were done elsewhere, and need to find the way it’s done at your new codebase. That doesn’t mean it’s easy; having worked in 3-4 codebases, my expectations are still subverted in the most creative ways. In any case, good ways to navigate a new codebase are:

- Find places you know already such as D3D API calls or windows functions you’re interested in, and make your way up
- Use the find symbols facilities and fuzzy search to find places that look suspiciously like what you’re looking for. Try a good dictionary of keywords like “render list” or “pipeline” or “lighting” to get an idea of what’s there
- Use bookmarks in your IDE when you find an interesting bit of code you’ve seen for the first time. You might not remember it later

Sometimes you need to put your archaeologist hat on and start digging through the codebase not just as it is, but as it used to be in some remote past. Having the ability to do is is very important to understand the context of some existing code, but can also be useful to know when a bug was introduced, or even recover a piece of code that some colleague told you used to exist and can be beneficial to you now. Sometimes you can even read deleted comments that actually explain better than the code what it was meant to do. Code versioning tools like Perforce or Git have the ability via a [timelapse](https://www.perforce.com/video-tutorials/vcs/using-time-lapse-view) or [blame](https://git-scm.com/docs/git-blame) view to start tracking through specific lines of code until their first appearance, etc. It is an invaluable tool that every codebase should make use of. Unfortunately, I’ve seen practices in some studios that completely disregard this and nuke codebase history by integrating code from another codebase in a copy-paste sort of fashion instead of using the tools’ tracking functionality. This means losing all the rich history of the codebase.

| One place I worked at used to use an old code versioning system called Accurev that had long stopped being supported. When we moved to a new system (Perforce) the history of everything was migrated so we could access it if needed, and proved invaluable moving the codebase forward |

### Use the Source

Although I like to think we tend to be quite open and present many things publicly, gamedev (particularly engine) still keeps many secrets and tightly kept NDA knowledge that can only be transmitted within the confines of the Jedi Temple; whether it’s console knowledge, GPU vendor oddities, specific code patterns or even company secrets, there are certain things you’ll rarely find in Stackoverflow and can only be privy to while you’re employed; even GDC or SIGGRAPH material is often behind a wall that only republic credits can open. It’s one of the reasons I like to work at companies who develop their own engine, you get to learn how to do very similar things in very different ways. A developer that has spent a good amount of time in the codebase knows the ins and outs of all that knowledge and can teach many lessons if you show interest and ask questions. I’ve too often seen people stuck with problems they for some reason can’t bring themselves to ask a question about. Asking is a good exercise:

- Good ones can deepen your insight. Often fellow programmers will point to some paper you’ve never come across that has something similar to what you need
- Not so good ones can either reinforce what you already know with a new perspective, or challenge what you think you knew
- Actual dumb ones can strengthen a friendship, even if you don’t learn that much

A piece of advice that can be useful for more junior devs but also for more experienced people is to find their Jedi Master, a person who is a lot more experienced than you are and can guide you in the ways of the Force. When I first started, navigating through a codebase and using the tools seemed like so many things at once, so much to keep in mind. I’d have to ask the same questions over and over because I just couldn’t remember all the workflows and the idiosincrasies, the tricks, the workarounds, the tribal rituals, the sound of the wooden beams where the infrastructure creaks like an old ship. I was very fortunate to have had essentially two leads at my first graphics job at Tt Games. They were both very different personalities but they spent so much time explaining the rendering pipeline, the render thread, the shader pipeline, why bitfields are cool, how we use the defines in the ubershader, what an intrusive pointer is, when to use placement new, etc. there’s just so much stuff that I got a jumpstart on thanks to them. I can even remember who taught me what in many instances.

For graphics programmers specifically, reading papers and presentations is probably the best way to learn, from SIGGRAPH, GDC or even websites from developers such as the excellent repository by [Guerrilla](https://www.guerrilla-games.com/read). Reading papers is often not straightforward on a first pass when they’re full of integrals and statistics concepts that need a deep grasp of mathematical concepts, so sometimes getting a first read and coming back to it later helps. I find presentations with visual elements and graphs much easier than formulas I have very little intuition for; it’s just a handicap I have to live with. When I first started I built a library around Calibre that has all the papers that I’ve classified over the years and I know other people build libraries like that as well. It’s a good exercise to get an idea for what a paper is roughly about sometimes so you can keep it in your ‘cache’ even if not immediately useful.

**Final Remarks**

Hopefully I’ve been able to give a somewhat informal view of the challenges and day to day we face in games from this graphics perspective, even if ultimately this is just my experience and my opinion on different topics. I really wanted to write an opinion piece like this and I finally got to do it. I hope you enjoyed it. If you’re considering becoming a graphics programmer, don’t let some of the difficulties I’ve outlined here discourage you! Graphics programming for me has been one of the most fulfilling endeavors I have had the pleasure to work on.

An interesting article! One advice I would like to add, especially after you said:

Is to make good notes of everything – about the code you explore (write down which files, which classes, structures, functions do what), what you learned from the materials you’ve read or watched (key points, references to them), about the tasks you need to do. Even if this is not your style, it is worth learning to be well organized with notes.

Hey Adam,

That’s a really good suggestion. I did take notes of pretty much everything but sometimes it’s just so much, or you missed writing down some crucial step with a batch file that somehow activates some other software.

On a related note, one of my Jedi Masters has a civil engineering background and he taught me to draw everything when thinking about problems, for example if I need to reason about shadow maps, just draw a frustum on paper and start drawing lines, angles, texels, etc. This very visual and non-screen method really stuck with me, I have a few notebooks now filled with these kinds of diagrams. He even 3D printed me a sort of multiuse ruler that I still use to this day.

Nicely written. It reminds me of some of the things Casey speaks about regularly, e.g. https://www.youtube.com/watch?v=tD5NrevFtbU (Clean code, horrible performance).

Or as Uncle Bob has said, # programmers double every 5 years, so half the world’s programmers have <5 years of experience. So a lot of code is being written by people who don’t know/appreciate what a computer does. Casey has repeatedly also been bitching about Visual Studio being a horribly slow tool, which it is.

I highly respect Casey and his didactic, pragmatic way of approaching programming for all of us. I’ve heard him say on a few occasions that he didn’t set out to be a teacher but as he saw demand and realized that no one else was saying these things and were being forgotten, he kind of took it upon himself to do that. Visual Studio is at a point where I can barely use it at work for 2-3 days before it crashes, and it’s super slow and clunky. However for many domains there’s just not much else.

Sorry about the video embed – didn’t know it would make such a big and horrible youtube tag – feel free to delete it and just show as text, unfortunately I can’t change it. :/

And yes, I really like Casey. I have watched many of his long programming rant videos, even the ones where he reinvents Windows Terminal are just too perfect! Lucky for me though I can use Jetbrains Rider atm. I will say though, the Visual Studio Installer has been significantly improved the last 3 years or so. It’s still a very clunky experience..

Great and informative article, thanks for writing!

Very nice article, thanks!

But now I wonder: What do you mean with an intrusive vector?

I meant to write intrusive pointer in that paragraph (I’ve corrected it now), but you can also implement an intrusive vector.

An intrusive container is where the container metadata for an object is owned by the object contained. For example, in an intrusive list the previous and next pointers are owned by the object (and therefore you don’t need the list itself to do this management, the object can do it from within the destructor)

An intrusive vector is the same concept, where the index lives inside the object. This means when you have an object you immediately know where inside the vector it lives so for example you can replace it or delete it very quickly if you have the index. The index of course can only be used with that vector

What’s a use case for an “intrusive vector?” If it’s in a vector, then it’s in a contiguous container, so if you have the address of the object and the address of the first object in the container, then you can do pointer math and avoid storing the index in the object and increase the fraction of the vector you can fit in cache at once.

Is the idea that you’re feeding this to something that has the object but not the vector, and you need to track the index independently of the object for later use in that code path?

Hi Ryan,

I’ve only come across one usage of an intrusive vector and that was to replace an intrusive list. The memory for the object doesn’t have to be contiguous in memory so I’m not sure the approach you suggest is generalizable. I can’t remember the specifics right now but I’m thinking about it as some sort of id, where the data is stored in multiple places and the object doesn’t itself contain all the data but can access it via the index, while at the same time all objects can be iterated through via an external object. Deletion of an object is very easy too because an object knows its index so there’s no need to find it in the vector. I’d have to think more about it though, it’s not a very common paradigm and I’m sure we could come up with a better model

Nice article!

Graphics & tools programmer here (among other things). And I’ve gotta say, C++ is overrated. If you really, really need the performance, use C. Otherwise, give C# a chance. It really is OOP done right.

I was skeptic in using C# for a game engine at first. But:

* fast compile time

* rename that actually works

* find-all-refs that actually works

* no corrupt pointer causing bugs to unrelated spots

* not having to manage and free memory (and/or fear leaks)

* no header mess (!!!)

And in reality, you can still pin memory and do your pointer tricks when you

reallyneed to.The only things you need to watch out for is:

* Don’t create (too much) garbage

* Don’t try making “clean code” (cf Casey)

Hey bo,

Thanks for your comment, I’m glad you enjoyed the article. There are some things here I agree and some I disagree with. Let’s start with agrees 🙂

C# is a really nice language. Compared to Java, for example, which I used to have a lot of experience with, I find the extensibility of the language and the ease of its standard library really compelling to get something up and running. It’s pretty easy to create small tools and interfaces and there’s something to be said about a semi-interpreted language that runs almost anywhere. You obviously avoid all the issues with an old language like C or C++ such as headers or compile times, but any contemporary language does that anyway.

As for the renaming, I’ve never found that to be an issue in C++. I use Visual Assist which might be biasing it towards having VS + VA, but I hit rename and I’m confident it’s going to find all the references and rename them properly.

I’d take issue with something like OOP ‘done right’. I don’t think C# diverges much in that sense from C++, it provides interfaces which deep down are just virtual functions and tells you to put everything inside objects. If you have myObject.Draw() in your code you’re already starting wrong.

I cannot agree with the performance side of things either. I use C++ as a better C, other than the standard library which I avoid at all costs these days. I even have my own subset replacement https://github.com/redorav/crstl. I have used game editors made in C#, and while they are functional the UI is laggy and clunky, and soon things stop scaling as well. Mind you, I’ve seen awful editors in C++ too, what I meant is it’s not a guarantee you’ll get a fast, snappy editor. These days I’d probably start using a compiled language with Imgui to get an editor running.

As far as I understand it even things like Windows Explorer have C# UIs and it shows. The kind of programmer who says “you don’t need to manage your memory in X language” is the kind of programmer who’d get it wrong in any language anyway.

I used to program games in Java for Android and the hacks we had to do to avoid the garbage collector were pretty terrible. C# is better in that regard because GCs have improved since then and the language has non-heap facilities like structs, but other than that you’re on your own.

Anyway, I’m glad you enjoyed reading this. Is there something you’re working on you’d like to share? I have a repository where I collect projects people are working on https://github.com/redorav/public_source_engines

I find myself nodding along with a lot of this, but there’s one small point I want to note, because I think it’s important to why some people are enthusiastic about the standard algorithms.

I agree that in the example you posted, std::transform doesn’t add a lot of readability or flexibility over the range-for. But that example is transforming the values in-place, without any other containers being involved. The thing std::transform gets you over range-for is that you can feed it iterators from different containers and it will handle all the iterator arithmetic for you (and even adding things to the destination container, if you use the right iterator type). That means you can have a single line of code that takes things from an input container, transforms them with a function you’ve reused from somewhere else, and puts them in an output container in the same order, with a minimum of syntax involved. You *can* do this without std::transform, of course, but there’s more “ceremony” involved; you track array indices (if you’re even writing to an array) or you call push_back on a vector-like structure or you need an iterator outside the for loop scope that you write the result to and then increment yourself…

It doesn’t feel like a lot of ceremony compared to spinning up a modern graphics API or even just uploading data to a GPU buffer, but most programmers don’t do that kind of thing and any amount of ceremony for something they feel *should* be simple feels onerous for many of them. And they look over at Lisp and Haskell and envy the how short and free of ceremony code in a functional style and a functional programming looks…

Hi Ryan, thanks for the comment

I completely agree with your assessment of why people look for these kinds of functions. Other languages provide a lot of convenient functionality in order to remove the ceremony, as you so well put it, of complicated tasks. Your point about using different containers is an appropriate starting point.

To begin with I would say that I seldom find myself moving data between containers like that, and when I do I immediately start questioning the need of moving the data around in the first place. Any big memory copy or transfer is already relatively suspicious.

The second point I’d argue is that expensive operations need to “feel” expensive in some way, i.e. moving things around cannot be a trivial thing for a program to do and all too many languages do that by default in many ways, such as garbage collection, untyped variable conversions, allocations, etc.

The third point I’d like to make is that I’m not entirely sure I like iterators as a way to abstract containers; they are so different in their implemenation and perfomance characteristics that pretending they are somehow interchangeable in a way that allows you to e.g. transparently swap a vector for a linked list or a hashmap is not helpful in most cases.

My last point is, what happens when you need to do this same operation but with 3 containers? Do you write another version of std::transform? The logic kind of breaks down as soon as you have a few more complex use cases, and you were probably better off writing the logic you needed to begin with.

Ultimately I think that the approach is an effort to forget that computers run code and pretend some sort of mathematical abstract machine does

Typically I wouldn’t expect std::transform to be used to move or duplicate data; you’d use std::transform to take an element and transform it into something completely different. std::transform’s iterator types being templated means the output iterator can be an entirely different type and therefore the output element type can be different, and the iterator abstraction means that the output element need not even be bytes in memory.

You could for example have a function that takes a particle and returns a bool that signifies whether the particle is alive or dead. If you used that with std::transform, your input container might be a vector of particles and your output container could be a bitvector (with a custom iterator that iterates through bits instead of bytes). The function that classifies the particle alive/dead wouldn’t need to know what a bitvector is or how to do bitmasking or even that it needs to do that, because the details of iterating through bits and setting/clearing them is abstracted away by the iterator. The classifier predicate could be reused somewhere else (eg. gameplay logic that needs to monitor a specific particle for some reason) without a container being involved at all.

It is claimed that using algorithms like that to compose existing functionality together instead of writing a lot of bespoke code makes working software faster, easier, and *safer* to write (because there’s less loop machinery to get wrong) and read (because transform is one word with an established meaning and the eye can scan it faster than a loop which could be any length and shape).

Oddly enough, an overload of std::transform that can work with two input and one output containers was added to the standard in C++17. Someone cared enough to get it added, so I assume *somebody* is using it. I also think you totally could write a variadic version of std::transform that took an arbitrary number of input iterator pairs. I’ve also seen people write ECS (and SQL, for that matter) queries that essentially do that, just with tables of components rather than iterator pairs. So, the idea of transform-3 is definitely out there and in use.

It’s a fair point that many programmers probably do want to forget that computers rather than abstract machines run code. And they would tell you that they’re better off in doing so, because they’re really just mathematicians and forcing them to think about how the computer works would just trip them up in the same way that most people will stumble around ungracefully if you ask them to walk while concentrating on what their calves are doing. It also reminds me of that Dijkstra quote about how computer science is about computers in the same way that astronomy is about telescopes – which is to say, very little – and makes me think that many C++ programmers in particular would probably be happier writing Haskell.

I think we are mostly in agreement but you like playing devil’s advocate 🙂 I haven’t written in that many programming languages that I have opinions on everything so take what I say with a pinch of salt. I do have experience programming in languages like Java, C#, Python, Lua or Javascript. After the experience with them I can definitely see why people really struggle with performance and large codebases, and a lot really just boils down to language choices and overabstraction. All of them abstract memory much higher than C/C++ or other system languages. Some of them have very loose typing. Many have syntax sugar that favors looping multiple times cleanly instead of a single ugly one, or include LINQ queries to do basic iteration. For a few of those everything is an object, or everything is on the heap. They are very convenient and it’s very easy to get a basic program up and running but maintenance is difficult in the long run; I have experienced many slow C# UI applications, enough sluggish editors and support apps made with it that I wouldn’t ever start one. Contrast that with systems languages where it’s harder to get things up and running but there are many headaches you can avoid down the line. A lot of C++ is moving towards the convenient abstraction/sugar and I just disagree with the approach