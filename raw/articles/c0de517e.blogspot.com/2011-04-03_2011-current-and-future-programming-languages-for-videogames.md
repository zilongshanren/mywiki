---
title: 2011 Current and Future programming languages for Videogames
url: http://c0de517e.blogspot.com/2011/04/2011-current-and-future-programming.html
published: '2011-04-03'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

There are so many interesting langauges that are gaining popularity these days, I thought it could be interesting to write about them and how they apply to videogames. I plan to do this every year, and probably to create a poll as well.


If I missed your favorite language,

If I missed your favorite language,

**comment on this article**, so at least I can include that in the poll!Now, before we start, we have to define what "videogames" we are talking about. Game programming has always been an interdisciplinary art: AI, graphics, systems, geometry, tools, physics, database, telemetry, networking, parallel computing and more.

This is even more true nowadays that we everything turned into a gaming platforms: browsers, mobile devices, websites and so on. So truly, if we talk about videogames at large there are very few programming languages that are intresting but not relevant to our business.

So I'll be narrowing this down to languages that could or should be considered by an AAA game studio, working on consoles (Xbox 360 and PS3) as its primary focus, while maybe still keeping an eye on PC and Wii. Why? Well mostly because that's the world I know best. Let's go.


*Scripting Languages***Where and why we need them:**Code as Data, trivial to hotswap and live-edit, easier for non-programmers. Usually found in loading/initialization systems, AI and gameplay conditions or to define the order of operation of complex sub-systems (i.e. what gets rendered in a frame when). Scripting languages are usually interpreted (some come with optional JITs) so porting to a new platform is usually not a big deal. In many fields scripting is used to glue together different libraries, so you want a language with a lot of bindings (Perl, Python). For games though, we are more interested in embedding the language and extending it, so small, easy to modify interpreters are a good thing.

**Current champion and its strenghts:**

[Lua](http://www.lua.org/)(a collection of nice presentations about it can be found on the

[Havok website](http://www.havok.com/index.php?page=gdc-lua-tutorial&hl=en_US)). It's the

[de-facto standard](http://en.wikipedia.org/wiki/Category:Lua-scripted_video_games). Born as a data definition language it can very well replace XML (bleargh) as an easier-to-parse, more powerful way of initializing systems.

It's also blessed with one of the fastest interpreters out there (even if it's not so cool on the simpler in-order cores that power current consoles and low-power devices) and with a decent incremental garbage collector. Easy to integrate, easy to customize, and most people are already familiar with its syntax (not only because it's so popular, but also because it's very similar to other popular scripting languages inspired by ECMAScript). Havok sells an optimized VM (

[Havok Script](http://www.havok.com/index.php?page=havok-script&hl=en_US), previously called Kore).**Why we should seek an alternative:**

Lua is nice but it's not born for videogames, and sometimes it shows. It's fast but not fast enough for many tasks, especially on consoles (even if some projects , like

[Lua-LLVM](http://code.google.com/p/llvm-lua/),

[lua2c](https://github.com/davidm/lua2c#readme)and

[MetaLua](http://metalua.luaforge.net/)could make the situation better). It has a decent garbage collector but still it generates too much garbage (it allocates for pretty much everything, it's possible to use it in a way that minimizes the dynamic allocations but then you'll end up throwing away much of the language) and the incremental collector pauses can still be painful. It's extensible but you can only easily hook up C functions to it (and the calling mechanism is not too fast) while you need to patch its internals if you want to add a new type. Types can be defined in Lua itself, but that's seldom useful to games. There is a very cool

[JIT](http://luajit.org/)for it, but it runs on very few platforms.

Personally I'd trade many language features (OOP, Coroutines, Lambdas,

[Metamethods](http://lua-users.org/wiki/MetamethodsTutorial), probably even script-defined structures or types) for more performance on consoles and easier extensibility with custom types, native function calls (invoking function pointers directly from the script without the need of wrappers) etc...

**Present and future alternatives:**

[IO](http://www.iolanguage.com/). It's a very nice language, in some way similar to Lua (it has a small VM, an incremental collector, coroutines, it's easy to embed...) but with a different (more minimal) syntax. Can do some cool things like binding C++ types to the language, it supports Actors and Futures, it has Exceptions and native Vector (SIMD) support.

[Stackless Python](http://www.stackless.com/). Python, with coroutines (fibers, microthreads, call them as you wish) and task serialization. It's Python. Many people

[love python](http://wiki.python.org/moin/PythonGames), it's a well known language (also used in many tools and commercial applications, either via

[CPython](http://en.wikipedia.org/wiki/CPython)or

[IronPython](http://ironpython.net/)) and it's not one of the slowest scripting languages around (let's say, it's faster than Ruby, but slower than Lua). It's a bigger language, more complex to embed and extend. But if you really need to run many scripted tasks (see

[Grim Fandango](http://www.lua.org/wshop05/Mogul.pdf)and

[Eve Online](http://www.slideshare.net/Arbow/stackless-python-in-eve)presentations for examples of games using coroutines), it might be a good idea.

[JavaScript](http://en.wikipedia.org/wiki/JavaScript).

[ActionScript](http://www.adobe.com/devnet/actionscript.html), another ECMAScript implementation, is already very commonly found in games due to the reliance on Flash for menus. HTML5 looks like a possible contender, and modern browsers are always pushing to have faster and faster JavaScript JIT engines. Some JITs are only available for IA-32 platforms (like Google

[V8](http://code.google.com/p/v8/)) but some others (like Mozilla TraceMonkey/JaegerMonkey) support PPC as well. The language itself is not really neat and it's full of pitfalls (Lua is much cleaner) but it's usable (also, there are languages that compile to JavaScript and that "clean it up" like

[coffeeScript](http://jashkenas.github.com/coffee-script/)and

[haXe](http://haxe.org/)). VMs tend to be big and not easy to understand or extend.

[Scheme](http://en.wikipedia.org/wiki/Scheme_%28programming_language%29). Scheme is one the the two major lisp dialects (the other one being Common Lisp). It's very small and "clean". Easy to parse, not to hard to write an interpreter, and easy to extend. It's Lisp, so some people will love it, some will totally hate it. There are quite a few intepreters (

[Chicken](http://www.call-cc.org/),

[Bigloo](http://www-sop.inria.fr/indes/fp/Bigloo/),

[Gambit](http://dynamo.iro.umontreal.ca/~gambit/wiki/index.php/Main_Page)) that also come with a scheme-to-C compiler and some (like

[YScheme](http://code.google.com/p/ypsilon/)) that have short-pause GC for realtime applications, and that's quite lovely when you have to support many different platforms.

[Guile](http://en.wikipedia.org/wiki/GNU_Guile)is a scheme interpreter explicitly written to be embedded.

[TCL](http://www.tcl.tk/about/). Probably a bit "underpowered" compared to the other languages, it's born to be embeddable and extensible, almost to the point that it can more be seen as a platform for writing DSL than as a language. Similar to Forth, but without the annoying RPN syntax. Not very fast, but very easy.

*Gaming-specific scripting languages*. There are quite a few languages that were made specifically for videogames, most of them in reaction to Lua, most of them similar to Lua (even if they mostly go for a more C-like syntax). None of them is as popular as Lua, and I'd say, none of them emerges as a clear winner over Lua in terms of features, extensibility or speed. But many are worth considering:

[Squirrel](http://squirrel-lang.org/),

[AngelScript](http://www.angelcode.com/angelscript/),

[GameMonkey](http://www.somedude.net/gamemonkey/),

[ChaiScript](http://www.chaiscript.com/),

[MiniD](http://www.dsource.org/projects/minid).

*Other honorable mentions*.

[Pawn](http://www.compuphase.com/pawn/pawn.htm)is probably the closer to what I'd like to have, super small (it has no types, variables are a 32bit "cell" that can hold an integer or can be cast to a float, a character or a boolean) and probably the fastest of the bunch, but it seems to be discontinued as its last release is from 2009.

[Falcon](http://www.falconpl.org/index.ftd?page_id=facts)is pretty cool too, but it seems to be geared more towards being a "ruby" than a "lua" (that's to say, a complete, powerful multi-paradigm language to join libraries instead of an extension, embedded language) even if they claim to be fast and to be easy to embed. Last, I didn't investigate it much, but knowing

[Wouter](http://strlen.com/)'s experience in crafting scripting languages, I won't be surprised if

[CubeScript](http://cube.wikispaces.com/Scripting+Guide)was a hidden gem.

*Roll your own*. Yes, really, I'm serious. It's not that hard, especially using a parser-generator tool.

[AntLR](http://www.antlr.org/)is one of the best and easiest (see this

[video tutorial](http://vimeo.com/8137747)). Interpreters are "easy" and

[LLVM](http://llvm.org/)can be used to write a native compiler that targets consoles (Wii, Ps3, 360 can all be targeted with it) for optimized builds.


**High-level languages****Where and why we need them:**For "high level" here we mean languages that "higher than C". We seek for features like type-safety, serialization, reflection, annotations and introspection, runtime code generation, dynamic loading, native threads, better tools integration (refactoring, automated coverage and testing), object lifetime management and so on and on. Usually, they are based on a VM and a JIT, and approach (in theory could even surpass, due to runtime optimizations) the speed of native-compiled systems.

Such languages can be used for most of the game code, even without loss of speed as anyways most games end up implementing such features in their own, often slow, cumbersome, error-prone ways (i.e. reference counting for lifetime management, macros and templates for reflection and so on).

**Current champion and its strenghts:**

[CLI](http://en.wikipedia.org/wiki/Common_Language_Infrastructure)(plus CLS) and

[C#](http://msdn.microsoft.com/en-us/vcsharp/aa336809.aspx). For a while there was some fascination with Java, and some PC titles shipped using it, but today C# wins hands down. It's the de-facto standard for tools, and it's getting into the shipped titles as well.

[Unity](http://unity3d.com/)is one of the most used game engines out there, and it's based on C#. Microsoft

[XNA](http://blogs.msdn.com/b/xna/)puts C# on the 360. Some games on consoles already shipped using C# in their runtime.

Mono is a strong opensource implementation, it has a JIT, an ahead-of-time compiler and an interpreter. It can even use

[LLVM](http://www.mono-project.com/Mono_LLVM)as a backend (LLVM targets . Also, CLI supports

[many many](http://en.wikipedia.org/wiki/List_of_CLI_languages)other languages (notably,

[F#](http://msdn.microsoft.com/en-us/fsharp/default.aspx)), including dynamic ones via the

[DLR](http://en.wikipedia.org/wiki/Dynamic_Language_Runtime), so it can serve for scripting as well (see

[IronPython](http://ironpython.net/), IronRuby, IronScheme,

[Boo](http://boo.codehaus.org/)and so on...)

**Why we should seek an alternative:**

We shouldn't. Maybe one day we will, but right now it would be lovely to try to have more and more game code written in a higher level language, instead we still rely mostly on the systems language plus some limited scripting. CLI is our best bet so far.

**Present and future alternatives:**

[JVM](http://en.wikipedia.org/wiki/Java_Virtual_Machine)languages. The Java Virtual Machine was cool, and nowadays still hosts many interesting languages (notably,

[Clojure](http://clojure.org/)and

[Scala](http://www.scala-lang.org/)). But the truth is, most of them are also available for the CLI, the JVM does not have any technological advantage over the former (actually it can be a bit harder to compile) and we don't have an equivalent of the excellent Mono project for it. Surely there are some awesome JIT

[compilers](http://openjdk.java.net/groups/hotspot/), LLVM support via the

[VMKit Project](http://vmkit.llvm.org/), even code

[hotswapping](http://www.zeroturnaround.com/jrebel/)frameworks, but it seems that it's loosing momentum quickly for gaming and it's being pushed more and more into the server realm.

[Erlang](http://en.wikipedia.org/wiki/Erlang_%28programming_language%29)is another language based on a VM that is having quite some buzz. It was meant for servers and it shows, but more and more games are looking into coroutines and actors for parallelism (Mono added coroutines mostly for games), and Erlang was made specifically for that. It's a functional language that revolves around actors for concurrency. It supports code hot swapping natively and that alone is enough to put it in this list.

[Mono](http://www.mono-project.com/Main_Page)is a CLI/CLS implementation, but it's worth noticing that it added enough extensions to be considered a platform on its own. Some are compiler extensions that do not change the language (i.e. programs using

[Mono.Simd](http://mono.simd/)will run on any CLI, even if they won't probably use Simd instructions to speed up the computations), but some are not, notably

[Continuations](http://www.mono-project.com/Continuations)support (and for example

[Unity](http://unity3d.com/support/documentation/ScriptReference/index.Coroutines_26_Yield.html)heavily relies on that) and the uber-cool

[assembly injection](http://tirania.org/blog/archive/2008/Sep-29.html)support.

[OCaml](http://caml.inria.fr/).

[ML-family](http://en.wikipedia.org/wiki/ML_%28programming_language%29)languages in a perfect world would rule Algol-like ones. ML is

[neat](http://www.ps.uni-saarland.de/alice/), strongly statically typed but with powerful type inferencing, functional but impure and strict. All with a syntax that really makes sense, not so minimal as the Lisp family is and way easier (and way less

[research-oriented](http://haskell.org/onlinereport/preface-jfp.html)) than Haskell. OCaml is one of the leading ML dialects, probably the most used one (together with the already mentioned F#). It has a good optimizing compiler that works on a number of platforms. Realistically? It won't happen yet.

ML is a great language to know and use but it's too far removed from Algol (see

[LangPop](http://www.langpop.com/#)and

[Tiobe](http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html), for which programming langauges are well known...) to be successful in my opinion (maybe F# could change that...), also there are many nice dialects but no big standards with multiple compiler implementations, that is what you really need to be "safe" when choosing a systems language.

[Haskell](http://haskell.org/haskellwiki/Haskell). It's perhaps surprising that this one made into the list. At least, it surprises me, I was "forced" to add it due to the demands that I had here and on the survey. I guess a lot of its "popularity" among video game programmers is due to

[this paper](http://www.cs.princeton.edu/~dpw/popl/06/Tim-POPL.ppt)by Tim Sweeney, where he uses Haskell to demonstrate how types can help our job.

Haskell was born as a research tool, a "definitive" functional language capable of supporting many different

[models of computation](http://www.willamette.edu/~fruehr/haskell/evolution.html). It's a purely functional, strongly typed language, so you can "reason" about it formally. It's lazy by default. Now while being lazy, functional and strongly typed is

[undoubtedly nice](http://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf), I don't being pure or lazy by default is.

Surely, in theory having no side-effects makes automatic parallelization possible, and Parallel Haskell does that neatly but in practice the results are not great. And it's true that monads are not that hard (

[this tutorial is neat](http://blog.sigfpe.com/2006/08/you-could-have-invented-monads-and.html)) and there are plenty of

[nice resources](http://haskell.org/haskellwiki/Learning_Haskell)on the language, but I still don't think

[purely functional data structures](http://www.cs.cmu.edu/~rwh/theses/okasaki.pdf)are something that most people will easily understand or be able to write (in fact most basic data structures that we take for grated in the mutable programming world, are still considered great

[research topics](http://nix-tips.blogspot.com/2011/03/how-to-choose-haskell-array-library.html)when turned into persistent versions).

Reasoning about space and time performance of an Haskell program is also very hard, and while I do think that a good language should decouple the logical representation of data to their physical layout, I also think we need still to be able to strictly control both. In some domains, more declarative languages are surely welcome.

I do think that Haskell is a language that needs to be learned, and it's great to experiment with. But I personally don't see it as something we will use in the foreseeable future.


**System programming****Where and why we need them:**High performance, core code. Languages in this tier need to be able to directly manipulate memory, need to support all platforms functionality, even better, support inline assembly. Statically compiled, strict languages. Used for computational kernels, core data structures and direct interface with the hardware.

**Current champion and its strengths:**

Native platform libraries interface with them and only them out of the box. In other words, right now for any practical purpose, that means that ANY other language in this category has to have an easy, fast interface with C/C++ or compile to (generate) C/C++.

All the programmers in your company know at least some C and C++.

**Why we should seek an alternative:**

C is too low-level for the needs of huge projects as modern games are, it tends to become cumbersome if used for large parts of your source.

C++ is made

[of evil](http://yosefk.com/c++fqa/). Probably not many in your company really know all of C, surely no one fully understands C++.

Also, both C and C++ are showing their age in some respect. Important concepts like SIMD operations are supported only through compiler extensions. Other language features made sense ten years ago but not too much now (for example, short-circuiting boolean operations generates branches that often cost more than what they save).

**Present and future alternatives:**

[D](http://www.digitalmars.com/d/). D is C++ done right. There is a proprietary compiler from Digital Mars and frontends for GCC and LLVM. It's an interesting, well made language, supported even by

[Alexandrescu](http://www.amazon.com/exec/obidos/ASIN/0321635361/modecdesi-20), an hardcore C++ guru.

It looks like C++ but it's much simpler (it drops all C compatibility, the preprocessor, multiple inheritance, forward declarations and include files, non-virtual member functions and so on) and much more powerful (sane memory management, sane templates, first-class functions and closures, immutable structures, modules, threads, contracts, dynamically compiled code). It still misses some needed features (like runtime reflection, even if I hear it's not hard to add as it supports compile-time reflection), but most of it is there.

It's major obstacle to success is the fact that is similar to C++. So similar that is questionable if it's superior design is worth the trouble of migrating to a language that still does not guarantee support on each platform out of the box.



[Objective-C](http://en.wikipedia.org/wiki/Objective-C). I don't have enough experience to write about this, but I had a few comments by programmers advocating it, so I'll have to include it here. It's already used in games as it's the language of choice for Apple devices, but I don't know if it could be suitable for AAA games.[Go](http://golang.org/). Go is a very recent language created by Griesemer, Pike and Thompson at Google. That's enough to be worth considering. Currently there are a few compilers, notably one in the GCC stack. It's much simpler than C++, it only supports interfaces but it does not need to declare inheritance, it's garbage collected, it does not permit pointer arithmetic and it supports threads and tasks (via "goroutines"). One of its goals was to m

[ake software development faster, and dependency management easier](http://golang.org/doc/go_faq.html). That's exactly what we need. Go is still too young, but it surely needs to be followed.

[Rust](https://github.com/graydon/rust/wiki/Language-FAQ)is an experimental language by Mozilla Labs. It's still in development and its syntax is not finalized yet but it looks incredibly promising. It currently has a compiler that uses LLVM as its backend. It's memory safe, immutable by default, concurrent (with coroutine and actor support), it has first class functions and a neat way of expressing and enforcing invariants at runtime and compile-time. It also supports "localized rule-breaking" meaning that safety rules can be broken "if explicit about where and how".

*C*. If we manage to port more and more code to a language in the previous category (higher level) then we might not need any neat feature in our systems programming language, just sheer speed and compatibility with the hardware.

C would be a great choice, and it often manages to implement features that are important for performance

[before](http://en.wikipedia.org/wiki/C1X)C++. It's also way easier to parse and reason about than C++ so it's better for tools, it's easier for[compilers](http://clang.llvm.org/)to work with it (good luck finding a 100% compliant C++ one) and so on.Many people in the industry are looking back at C or going for a more C-like programming style, I even heard talks of projects to extend C with novel object models (via code generation) to avoid C++.

[OpenCL](http://www.khronos.org/opencl/). Yes, it's a language for GPUs. That's to say very powerful processors made of many low-power, in-order, shared-cache parallel processing units. In other words, the future. We need a language for data-parallel computations, and OpenCL seems to be a reasonable choice. I would personally prefer something even more restrictive and stream-oriented, with well-defined inputs and outputs (easy to check for correctness!) and means of connection and buffering between the kernels, but OpenCL is the standard and it's supported by every GPU vendor. Moreover, we already have several CPU implementations, like

[FOXC](http://www.fixstars.com/en/foxc/)that spits out C code from OpenCL, Intel

[OpenCL SDK](http://software.intel.com/en-us/articles/intel-opencl-sdk/)for x86 CPUs, IBM

[OpenCL for Cell](http://www.alphaworks.ibm.com/tech/opencl). There are also similar initiatives targeting NVidia's proprietary Cuda language, like

[GPUOcelot](http://code.google.com/p/gpuocelot/wiki/Roadmap). Of course

[LLVM](http://llvm.org/devmtg/2009-10/OpenCLWithLLVM.pdf)plays a major role again, even

[AMD's](http://llvm.org/devmtg/2010-11/Villmow-OpenCL.pdf)GPU compiler seems to be based on it, and there are both backends and frontends in the works for it.

*Your own C/C++*. To a degree, everyone is already using their own version of C++ incompatible with everyone else's. That's because to use C++ in production you have to both restrict and extend it. That's usually done with coding guidelines and reviews plus custom libraries with a sprinkle of preprocessor macros (and setting your compilers to the maximum warning level plus enabling warnings as errors). In other words, horribly.

It is possible, with tools, to do better. Parsers and rules can be used to restrict the language in a well-enforced way. There are a few of such tools and they are mostly commercial (

[cppcheck](http://en.wikipedia.org/wiki/Cppcheck)is a notable exception, parsing and understanding C++ is a nightmare) like[PC-Lint](http://www.gimpel.com/),[Coverity](http://coverity.com/products/static-analysis.html),[Lattix](http://www.lattix.com/)(for dependency analysis and design rules enforcement),[PVS-Studio](http://www.codeproject.com/Catalogs/3179/PVS-Studio.aspx)and so on.Parsers can also be used to enhance the language, by gathering and exposing information, either to be directly used (i.e.

[reflection](http://www.garret.ru/cppreflection/docs/reflect.html)) or to be fed into code-generation tools (to generate bindings or for serialization etc). It's a very interesting possibility, and we have a number of different ways to extract information.Compilers can help, it's possible to parse their parse symbol and debugging files, some can even directly output useful data (most notably,


Last but not least, code generation: after parsing either vanilla C++ or an annotated version with custom extensions, for most practical uses we'll need to emit some code.

[GCC](http://www.gccxml.org/HTML/Index.html)and[CLang](http://clang.llvm.org/doxygen/group__CINDEX__CPP.html)with[libCLang](http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang/#), even Visual C++[considered](http://blogs.msdn.com/b/vcblog/archive/2006/08/16/702823.aspx)this but I don't see it[happening](https://connect.microsoft.com/Phoenix)yet).[Doxygen](http://www.stack.nl/~dimitri/doxygen/index.html)also has a good parser that can extract quite some interesting information,[SWIG](http://www.swig.org/)can parse headers and there are also a few parsers dedicated to language extension and analysis, like[PyCParser](http://code.google.com/p/pycparser/),[CTool](http://ctool.sourceforge.net/)and[CIL](http://hal.cs.berkeley.edu/cil/)for C,[Transformers](http://www.lrde.epita.fr/cgi-bin/twiki/view/Transformers/),[OpenC++](http://opencxx.sourceforge.net/)and[VivaCore](http://www.viva64.com/en/vivacore-library/)(that is used by the PVS-Studio linter),[ELSA](http://www.scottmcpeak.com/elkhound/sources/elsa/),[Harmonia](http://harmonia.cs.berkeley.edu/harmonia/index.html), that tries to build an incremental tool for refactoring and program transformation, and commercial ones like[Understand](http://www.scitools.com/).Last but not least, code generation: after parsing either vanilla C++ or an annotated version with custom extensions, for most practical uses we'll need to emit some code.

This is for example, the approach followed by QT's

[MOC compiler](http://doc.qt.nokia.com/4.7/moc.html#moc)to implement their object model. Some tools support full source-to-source translation (parsing and emitting code), like the[DMS toolkit](http://www.semanticdesigns.com/Products/DMS/DMSToolkit.html),[Stratego/XT](http://strategoxt.org/)or the[ROSE](http://www.rosecompiler.org/)compiler.But code generation is not only useful for source-to-source transforms and language enhancement, it's also vital to bridge data and DSLs to C++ and in general to create interfaces between different systems. That's the approach used by object models like

[COM](http://en.wikipedia.org/wiki/Component_Object_Model), or data formats like Google[protobufs](http://en.wikipedia.org/wiki/Protocol_Buffers)and many other domains. Many frameworks approach this as a text generation problem (like[Cog](http://nedbatchelder.com/code/cog/)and[Cheetah](http://www.cheetahtemplate.org/)) similar to what JSP does for web pages, but there are also generators capable of working directly from a[syntax tree](http://www.rosecompiler.org/ROSE_HTML_Reference/group__ROSE__BackEndGroup.html)or something in the middle between the two, like[cppgenmodel](http://code.google.com/a/eclipselabs.org/p/cppgenmodel/)and[rGen](http://ruby-gen.org/).**Conclusions**

Ok so, let's say I have a few months and I have to write a new game engine. What would be my best bet? Well I'd have to toss a coin between CLI+C and Lua+My own C++.

The CLI is a very good platform, and it's surprisingly well supported in gaming. For current-gen it would be a no brainer, Mono already supports all that you need and even rolling your own CLI compiler with LLVM is not an impossible task at all (and you can generate symbols to be able to use existing debuggers/profilers and so on). Microsoft will surely continue to push it even on future platforms, and other vendors and many studios are interested in the technology as well. The only problem I can see is that you won't get a 100% guarantee that you can support any future platform day-zero, as we are not seeing vendors shipping their own CLI for general game development yet.

The other option is to invest in a good, proprietary data/object/module/service/task model for C++, banishing its own OO system, restricting object usage mostly to services to be contained in dynamic linkable, hotswappable modules and to data structures. A generic data model with reflection and serialization support could be used for communication between modules, RPC, persistence and data parallel computations. All this wrapped in some DSLs to code-generate all the fluff. It won't be any easier (personally I think it would be harder, for me) than writing a CLI compiler with LLVM from scratch, and it will be much messier, but 100% future proof.

**Addendum**


*AI-specific languages*. I believe in a world where no game will need to implement a state machine. There are quite a few "AI" languages, from the obvious[Prolog](http://en.wikipedia.org/wiki/Prolog)family to constrain programming languages to more general frameworks like[Soar](http://sitemaker.umich.edu/soar/home). I'm not an AI expert, and I don't believe that we'll ever see one of these in a game, but they are great inspirations for[DSLs](http://en.wikipedia.org/wiki/Domain-specific_language), often embedded into other languages (internal DSLs).


*Languages for number crunching*. As I wrote for the scripting and AI-specific language, there is a lot of inspiration to be found looking at "obscure" task specific languages. Parallelism, concurrency and memory bandwidth are not only problems nowadays, they were problems even for the early supercomputers. Most of these languages are not going to be ever seen in a game (and many of them are hard to be seen in applications anywhere!) but understanding them is great, especially if you're going to design a DSL.

Nowadays "

## 44 comments:

Great overview.





The biggest problem about using higher level languages is binding existing C++ code to them.

We still don't have a solution that works seamlessly, so you either have to drop back to C or use tools to generate C wrappers automatically (SWIG comes to mind).

I've recently been refactoring all my core C++ code to C, and binding it becomes so much easier, so my current approach is: C interfaces, C++ implementation, and C# to glue it all via Mono.

It's the least painful way I've found to integrate it all.

What about objective c? Well supported by gcc no?

A lot of C++ blind spots have been fixed or amended in C++11, especially when it comes to noobs mistakes.

I'm definitely not as good as you but I would like to suggest considering objective c. Many ppl din realize that this language is being developed for longer than java and c#. It's like c++, but with very powerful metaprogramming. You almost feel like you are writing in a scripting language. It doesn't compile to byte code if I am not wrong. It's all c calls and a runtime. True that it's the combination of the apple API (core and cocoa) that make this language so powerful. my favorite concept is their autorelease and notification center. In Mac OS x it spot a garbage collector too. This language is a joy to write for me. you are free to write c codes or c++ codes in objective c. it's like writing asm in c or c++. I highly recommend.

Nova77: yes sure, adding hundreds of pages to an already bloated standard and not deprecating or dropping compatibility towards a single thing surely helps a lot with that...

Lxcid: I should look more into that, I don't know enough about ObjectiveC to write about it right now. I'll maybe add it later.

triton: the real hard problem with binding is that our codebases most of the times are not modular enough. If there were well defined modules with minimal interfaces, then binding would be a very small problem. :/

V8 also targets ARM6 and ARM7, but can't run on iOS due to not being able to set a page to executable.



I think it would be worthwhile for your summary to also mention memory usage characteristics. For example, last time I checked, many operations in Erlang causes a new alloc without a corresponding free; this pretty much rules it out as an embedded game language.

http://www.google.com/search?sourceid=chrome&ie=UTF-8&q=erlang+memory+usage

PS, overall I found your article a good read, thought I should mention that ;)

CubeScript initially was designed to just be stupidly simplistic while still being powerful: all code & data are strings, but that embodies very powerful closures, macros, dynamic scope and such (it is so expressive, it will make Scheme cry ;). All that in a fraction of the code of Lua, and easy to extend with new builtins.


It is SLOW however (see strings, above). The most recent version in the sauerbraten SVN has gained a bytecode interpreter, speeding it up an order of magnitude, at the cost of that whole simplicity thing.

In summary, I would NOT recommend anyone to use it, unless what you do can be described as "very expressive configuration" :)

Wouter: cool, yes I understand when you are manipulating strings, it's easier to be "powerful", I wrote a string-rewriting based language for a build tools years ago and it was stupid, slow but fairly expressive.



Thanks for sharing here!

I also love your time tracking app, I've tried a commercial one a while ago, the idea is neat, super useful! I'll try the treesheets one tomorrow at work!

Just a note: at Unity we use CLI (Mono) as a game scripting language. All the underlying engine / runtime part is C/C++. Some editor tools are C#, some C++. So at least in some cases, CLI/C#/Mono could be moved up to the "scripting languages" category.

Nick: I think in the new iOS you can enable the execute bit for pages, and thus execute JITed code. They also use a JIT now in the WebKit JavaScript engine.


NeARAZ: I'm curious, how do you bind the code at Unity? Do you use p/Invoke or register internal Mono functions? And do you auto-generate the wrappers with SWIG / custom tool?

@DEADC0DE: I am not sure to understand the sarcasm. There's many good reasons to keep compatibility and a lot of the introduced features (auto, foreach, lambda, etc..) will make the code cleaner and easier to understand for noobs.


Regarding 'adding new features', one of the big issues of C++ is the flurry of implementations to do basic things that were not covered by the standard. How many threads libraries do you know? I am all for putting such things under the same umbrella.

This is a great overview! Thanks for sharing your insight and for useful links.



I'm working with Objective-C mostly and to me it's "C++ done right". Now that you mentioned D, I'm going to take a closer look at it too.

I think we would all agree that the next big systems programming language has to have integrated support for parallelism and concurrency of some kind. The trend is growing really fast now.

It is interesting to note that although we're moving fast to the future of high performance hardware, a good programming language is still largely defined by its implementation, not only its programming model. In other words, it's not likely that one will choose a language over Lua which is even better than Lua, but slower than Ruby.

Writing a game-engine by writing your very own programming language first, is almost always the Wrong Thing. imho

Great article. C++ I think is a horrible language that will eventually collapse on itself. Since C++ is trying to be both a system level language and a higher level language at the same time it often fails. I think it is interesting because as C++ programs get older we will realize the cost of maintaining C++ is very high. Targeting C as the system level language is the correct move because of easy integration with existing code.

NeARAZ: yes, I guess it was not clear the way I wrote it in the article. I guess you can call it game scripting, to me it's a bit borderline. If we roughly say that the scripting is what is usually left in the hands of a designer (I know, that's not right as we use scripting in rendering or loading and other things) and the coding is what is done by a game engineer, I'd say the use of C# in Unity falls more towards the second.

nova77: This can evolve in a huge discussion if we delve in the details, but let's say that for me the three capital sins of C++ can be grouped in:





1) Too complex.

No one really understands all of C++. I've worked with many people that were very skilled at it, and still they didn't claim to fully understand it. The average programmer gets it mostly wrong.

Even computers don't get it (very hard to write tools)

2) Too wrong.

Bad defaults, wrong keywords (typical example: having to declare constructors explicit), bad decisions that make tricky to write complex code and require books on coding guidelines, static checkers and so on.

3) Underpowered.

No/stupid (RC) object lifetime management, no SIMD, no threads, no closures/continuations/coroutines,no sane macro system, no real generics, no reflection etc etc etc.

Now the new standard addresses only point 3 a tiny tiny little bit. That's it. It totally ignores 1 and 2 that are the hard ones (no actually, it makes them _worse_). The only thing that could have helped a bit for complexity was removed (contracts). It adds to the standard what? Threads, yeah thanks, a standard would have been helpful 10 years ago, now everyone has their own stuff anyways. Lambdas and auto are a nice syntactic sugar, I admit, but it's really cosmetic there...

Anon: "Writing a game-engine by writing your very own programming language first, is almost always the Wrong Thing. imho" -



We do already! Writing a game engine is already, right now, the art of removing crap from C++ and adding features back. We all have our own object model that is not the C++ one. Most of the times is not a great one (we should spend more energy) and it's only informally enforced (code reviews, everyone has to write the code a given way).

I'm just saying that if we want to keep doing that, it's possible, but at least let's be honest and use tools to statically check that people are using the company-wide C++ dialect and not their own personal version.

C# is also used for server development. Bungie.net runs completely on C#, from game servers to web site (and all web services in-between). I believe Blizzard's Titan project also is being designed from the ground up to use C# for the server side.


On the client side, while you mention that C# can be used with XNA I believe that Mono (open-source CLR for Linux/Mac) is being ported to PS3 as well by Sony.

Kerr: I won't say anything about Sony... About the servers, I didn't include them in the survey, otherwise as I wrote in the introduction, we should really consider any langauge out there.

@DEADC0DE: I respectfully disagree but I don't want this to become an endless thread. If you happen to be in London we can have a chat over a beer. :)

nova77: same if U come to Vancouver

Another systems level language worth looking into is Clay - http://tachyon.in/clay/

I actually think Haskell is quite a bit "easier" than the ML languages, especially OCaml. I also do not really see why it should be considered research oriented anymore, Haskell as it is today is not what it was when it was first envisioned as a standardized lazy functional language.







The syntax is much lighter weight and more consistent, and the typeclasses make things like "*." from OCaml unnecessary and in general make it so that the type system gets in the way a bit less. It still might be an adaption having to do all those explicit casts.

One note is OCaml's implicit functionality that does the equivalent of Haskell's "deriving Eq".

Syntax wise though, Haskell could almosst be thought of a prettier, simpler OCaml.

Learning is another problem. Haskell has excellent tutorials online much like Python does, when I tried learning OCaml and Scheme I did not find those same sorts resources to be available.

Really, Haskell is just less surprising, cleaner looking, and easier to learn than OCaml is.

In the context of videogames though, I suppose haskell performance might be harder to reason about because the way the code is evaluated is so strange and has perhaps more in common with languages like Prolog in some cases than it does with OCaml. I do not really care about those semantics though, but I understand that OCaml might be easier if you do.

Anonym: You may be right about the availability of teaching material, Haskell is indeed fairly strong. And I'm not so experienced with the language, I personally prefer the ML family so I might be biased...





But I would be really surprised if any game programmer found it easier or more natural than OcaML.

And it's not a matter of syntax (syntax rarely matters), it's a matter of semantics.

Do you think that a C programmer will find it easy to implement any but the simplest list data structure in Haskell? Will you volounteer to explain monads to every guy on a team?

Not to mention that being purely functional is handy if you are doing language research but imho it does not add anything to a language that has to be used in production.

It might be worth noting that D comes in two versions. D 1.0 was indeed simpler than C++, but it's currently dead. D 2.0 comes with its own set of insanity which in many areas looks more involved than C++ (the const system, for instance, which isn't even used by the standard library, because they don't know how to use it).

Thanks for your reply.












I had written that comment in reply to c0de517e's blog post, where he seemed to imply that Haskell was mostly of research interest and more difficult to learn than OCaml. As you would have realized from my comment, I do not believe either of these perceptions to be correct. Haskell does, of course, attract the attention of researchers working on novel or improved compilers or interesting language extensions but this is true even of things like Python, JavaScript, and C. Being a good language for researchers to play with is just a good thing if you want your language to improve with time, as Haskell did. OCaml isn't "much easier" than Haskell and really is perhaps "slightly harder" instead. However, now I want to reply to your post.

First, I will say that (barring big mistakes with semantics-related choices) syntax is probably the most important thing for a language to get right. Syntax is pervasive and undesirable to have to escape from as those exceptions make things inconsistent and require more complexity to be memorized by the programmer.

On data structures, the way Haskell notates them is the same way they are done in OCaml. Thus, if a C programmer can do it in OCaml they should have no trouble with the equivalent Haskell data structure.

On monads, this is what it means to be a monad:

[[1,3],[3,5]] -> [1,3,3,5]

See how the nested list was collapsed? That collapsibility makes it a monad.

The motivation is a bit harder to explain, but you do not need to know about Monads to program Haskell any more than you need to know about operator overloading to program C++. And really, the thing that you'd have to explain would be typeclasses rather than Monads specifically, which are a cool language feature, but like operator overloading you can hold off teaching about it for quite some time and students will still be able to write substantial programs.

Typeclasses like Monad also make learning a bit easier by obviating the need for things like "*.", which I mentioned earlier. You do not have to know how they work to benefit from them.

I do not think it is either fair nor accurate to say that "purely functional" is mainly of research interest, or object-oriented programming (a different concept that has the same motivations and benefits of pure functional programming) would never have become the mainstream ideology it is today. Just like good object oriented design, pure functional programming makes code easier to test and maintain later down the line, and makes it easier to think about the individual components acting independently. OCaml pushes both those approaches.

Haskell does do one thing differently to OCaml with regards to this, it actually allows you to express purity at the type level by having you use a special data structure for IO operations. This does lead to some extra learning curve as to understanding why "IO String" is different from "String". I like to explain it in terms of "IO String" being like "PWD" or "WHOAMI" on a DOS prompt, and that >>= is analogous to the DOS pipe character ('|'). PWD and WHOAMI are programs, not strings, they only output strings when you run them.

I had to cut this down drastically to get it accepted as a comment, but I hope it addresses everything you mentioned. Cheers, Barend.

Barend: I don't think our views of the language are too far apart, but as it often happen online we're arguing on the context.






"Simpler" for example depends really on the audience. Scheme is way "simpler" than C but it would probably be "harder" in a game development scenario than lua or tcl.

Also when I said that the syntax does not matter much, I didn't mean that it does not matter for a language, but programmers can usually adjust to a different syntax way faster than they do to a different programming paradigm.

With that in mind, I think that most game devs will feel more at ease with a ML derivative than with Haskell.

If we were to talk about languages to teach to undergrads, then I probably would have made a different list...

I do still think though that being purely functional is a pain :) Many data structures are harder to implement/to reason about in a purely functional fashion, and I'd yet to see any practical advantage of a purely functional language over an impure one.

I don't agree that functional programming doesn't help with concurrency. Your example is

fine-grained parallelism, not concurrency.Anon: I didn't say "functional" I said "pure functional" does not help. And you're free to not agree, if you want to discuss though you should argument a bit more than that.

You discussed a lot of Lua VMs, but you missed the fastest one: LuaJIT, which gets speed comparable to Java in many benchmarks.

Scaevolus: "There is a very cool JIT for it, but it runs on very few platforms." And there is a link to it...

Tim Sweeney from Epic Games talked about this in this set of slides:



http://www.scribd.com/doc/5687/The-Next-Mainstream-Programming-Language-A-Game-Developers-Perspective-by-Tim-Sweeney

Haskell seems to tick most of his boxes...

Mark: he made examples in haskell, but i don't think he would advocate it for games.

Nice overview!





Wouter: I was thinking, an extremely minimal scripting language suited for games wouldn't need heavy string manipulation (if at all). String manipulation is slow and less predictable as it deals with dynamic data structures.

Instead of strings, it'd be efficient to use symbols which can be regarded as numeric IDs in production, where possible.

You generally want to internationalize any strings the user sees, so these can be stored in some database instead of directly in your script.

I'm not sure if such a language exists.

I'm not sure Io will ever seriously be in the running as a game scripting language.



Io's a neat idea, but the way Steve has chosen to implement it and define its semantics leaves it almost completely insoluble to modern optimization techniques. One of the reasons Lua is so popular is that it strikes an excellent compromise between what's pleasant to use and what is amenable to aggressive optimization in a bytecode-compiling interpreter.

Which is too bad, because there is a certain beauty to the way Io's syntax is spun into its runtime state. It's far more likely that another inheritor of Self will have to emerge before we see that language family in the gaming domain.

@deadcode: I believe he did just that. Granted, he noted a few things that he'd change, like going from lazy to lenient evaluation, and being more explicit about types rather than aiming to infer them, but the whole point of the slides was that Haskell is far more appropriate for future game dev than C++.

Mark: Next time I see him I'll ask... Meanwhile, I'll add Haskell to the list in the article, as many people are mentioning it

I remember Sweeney discussing about it on LtU. He said that the next "gaming programming language" is not going to be Haskell but it certainly will be closer to Haskell than to C++.


Anyway, somebody should look that discussion on LtU. I can't find it.

Post a Comment