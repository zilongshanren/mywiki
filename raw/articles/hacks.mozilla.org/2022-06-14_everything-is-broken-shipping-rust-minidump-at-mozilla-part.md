---
title: 'Everything Is Broken: Shipping rust-minidump at Mozilla – Part 1 – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2022/06/everything-is-broken-shipping-rust-minidump-at-mozilla/
author: Aria Beingessner
published: '2022-06-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Everything Is Broken: Shipping rust-minidump at Mozilla**

For the last year I’ve been leading the development of [rust-minidump](https://github.com/luser/rust-minidump/), a pure-Rust replacement for the minidump-processing half of [google-breakpad](https://chromium.googlesource.com/breakpad/breakpad/).

Well actually in some sense I *finished* that work, because Mozilla already [deployed it](https://github.com/luser/rust-minidump/tree/master/minidump-stackwalk) as [the crash processing backend for Firefox](https://crash-stats.mozilla.org/) 6 months ago, it runs in half the time, and seems to be more reliable. (And you know, *isn’t* a terrifying ball of C++ that parses and evaluates arbitrary input from the internet. We did our best to isolate Breakpad, but still… *yikes*.)

This is a pretty fantastic result, but there’s always more work to do because *Minidumps are an inky abyss that grows deeper the further you delve…* wait no I’m getting ahead of myself. First the light, then the abyss. Yes. Light first.

What I *can* say is that we have a very solid implementation of the core functionality of minidump parsing+analysis for the biggest platforms (x86, x64, ARM, ARM64; Windows, MacOS, Linux, Android). But if you want to read minidumps generated on a *PlayStation 3* or process a *Full Memory* dump, you won’t be served quite as well.

We’ve put a lot of effort into documenting and testing this thing, so I’m pretty confident in it!

**Unfortunately! Confidence! Is! Worth! Nothing!**

Which is why this is the story of how we did our best to make this nightmare as robust as we could and still got 360 dunked on from space by the sudden and *incredible* fuzzing efforts of [@5225225](https://github.com/5225225).

This article is broken into two parts:

- what minidumps are, and how we made rust-minidump
- how we got absolutely owned by simple fuzzing

You are reading part 1, wherein we build up our hubris.

**Background: What’s A Minidump, and Why Write rust-minidump?**

Your program crashes. You want to know why your program crashed, but it happened on a user’s machine on the other side of the world. A full coredump (all memory allocated by the program) is enormous — we can’t have users sending us 4GB files! Ok let’s just collect up the most important regions of memory like the stacks and where the program crashed. Oh and I guess if we’re taking the time, let’s stuff some metadata about the system and process in there too.

Congratulations you have invented [Minidumps](https://docs.microsoft.com/en-us/windows/win32/debug/minidump-files). Now you can turn a 100-thread coredump that would otherwise be 4GB into a nice little 2MB file that you can send over the internet and do postmortem analysis on.

Or more specifically, Microsoft did. So long ago that their docs don’t even discuss platform support. MiniDumpWriteDump’s supported versions are simply “Windows”. Microsoft Research has presumably developed a time machine to guarantee this.

Then Google came along (circa 2006-2007) and said “wouldn’t it be nice if we could make minidumps on *any* platform”? Thankfully Microsoft had actually built the format pretty extensibly, so it wasn’t too bad to extend the format for Linux, MacOS, BSD, Solaris, and so on. Those extensions became [google-breakpad](https://chromium.googlesource.com/breakpad/breakpad/) (or just Breakpad) which included a ton of different tools for generating, parsing, and analyzing their extended minidump format (and native Microsoft ones).

Mozilla helped out with this a lot because apparently, our crash reporting infrastructure (“Talkback”) was *miserable* circa 2007, and this seemed like a nice improvement. Needless to say, we’re pretty invested in breakpad’s minidumps at this point.

Fast forward to the present day and in a hilarious twist of fate, products like VSCode mean that Microsoft now supports applications that run on Linux and MacOS so it runs breakpad in production and has to handle non-Microsoft minidumps somewhere in its crash reporting infra, so someone else’s extension of their own format is somehow their problem now!

Meanwhile, Google has kind-of moved on to [Crashpad](https://chromium.googlesource.com/crashpad/crashpad). I say kind-of because there’s still a lot of Breakpad in there, but they’re more interested in building out tooling on top of it than improving Breakpad itself. Having made a few changes to Breakpad: **honestly fair**, I don’t want to work on it either. Still, this was a bit of a problem for us, because it meant the project became increasingly under-staffed.

By the time I started working on crash reporting, Mozilla had basically given up on upstreaming fixes/improvements to Breakpad, and was just using its own patched fork. But even *without* the need for upstreaming patches, every change to Breakpad filled us with dread: many proposed improvements to our crash reporting infrastructure stalled out at “time to implement this in Breakpad”.

Why is working on Breakpad so miserable, you ask?

Parsing and analyzing minidumps is basically an exercise in writing a fractal parser of platform-specific formats nested in formats nested in formats. For many operating systems. For many hardware architectures. And all the inputs you’re parsing and analyzing are terrible and buggy so you *have* to write a really permissive parser and crawl forward however you can.

Some specific MSVC toolchain that was part of Windows XP had a bug in its debuginfo format? **Too bad, symbolicate that stack frame anyway!**

The program crashed because it horribly corrupted its own stack? **Too bad, produce a backtrace anyway!**

The minidump writer itself completely freaked out and wrote a bunch of garbage to one stream? **Too bad, produce whatever output you can anyway!**

Hey, you know who has a lot of experience dealing with really complicated permissive parsers written in C++? Mozilla! That’s like *the core functionality* of a web browser.

Do you know Mozilla’s secret solution to writing really complicated permissive parsers in C++?

**We stopped doing it.**

We developed Rust and ported our nastiest parsers to it.

We’ve done it a lot, and [when we do](https://hacks.mozilla.org/2017/08/inside-a-super-fast-css-engine-quantum-css-aka-stylo/) we’re always like [“wow this is so much more reliable and easy to maintain and it’s even faster now”](https://www.joshmatthews.net/rbr17/). Rust is a really good language for writing parsers. C++ really isn’t.

So we Rewrote It In Rust (or as the kids call it, “Oxidized It”). Breakpad is big, so we haven’t actually covered all of its features. We’ve specifically written and deployed:

[dump_syms](https://github.com/mozilla/dump_syms)which processes native build artifacts into symbol files.[rust-minidump](https://github.com/luser/rust-minidump/)which is a collection of crates that parse and analyze minidumps. Or more specifically, we deployed[minidump-stackwalk](https://github.com/luser/rust-minidump/tree/master/minidump-stackwalk), which is the high-level cli interface to all of rust-minidump.

Notably missing from this picture is *minidump writing*, or what google-breakpad calls a *client* (because it runs on the client’s machine). We *are *working [on a rust-based minidump writer](https://github.com/rust-minidump/minidump-writer), but it’s not something we can recommend using quite yet (although it has sped up a lot thanks to help from [Embark Studios](https://embark.dev/)).

This is arguably the messiest and hardest work because it has a horrible job: use a bunch of native system APIs to gather up a bunch of OS-specific and Hardware-specific information about the crash AND do it for a program that just crashed, on a machine that *caused *the program to crash.

We have a long road ahead but every time we get to the other side of one of these projects it’s *wonderful*.


**Background: Stackwalking and Calling Conventions**

One of rust-minidump’s ([minidump-stackwalk’s](https://github.com/luser/rust-minidump/tree/master/minidump-stackwalk)) most important jobs is to take the state for a thread (general purpose registers and stack memory) and create a backtrace for that thread (unwind/stackwalk). This is a surprisingly complicated and messy job, made only more complicated by the fact that *we are trying to analyze the memory of a process that got messed up enough to crash*.

This means our stackwalkers are inherently working with dubious data, and all of our stackwalking techniques are based on heuristics that can go wrong and we can very easily find ourselves in situations where the stackwalk goes backwards or sideways or infinite and we just have to try to deal with it!

It’s also pretty common to see a stackwalker start *hallucinating*, which is my term for “the stackwalker found something that looked plausible enough and went on a wacky adventure through the stack and made up a whole pile of useless garbage frames”. Hallucination is most common near the bottom of the stack where it’s also least offensive. This is because each frame you walk is another chance for something to go wrong, but also increasingly uninteresting because you’re rarely interested in confirming that a thread started in The Same Function All Threads Start In.

All of these problems would basically go away if everyone agreed to properly preserve their cpu’s [PERFECTLY GOOD DEDICATED FRAME POINTER REGISTER](https://gankra.github.io/blah/compact-unwinding/#frame-pointer-unwinding-standard-prologues). Just kidding, turning on frame pointers doesn’t really work either because Microsoft [invented chaos frame pointers](https://github.com/rust-lang/rust/issues/82333) that can’t be used for unwinding! I assume this happened because they accidentally stepped on the wrong butterfly while they were traveling back in time to invent minidumps. (I’m sure it was a decision that made more sense 20 years ago, but it has not aged well.)

If you would like to learn more about the different techniques for unwinding, [I wrote about them over here](https://gankra.github.io/blah/compact-unwinding/#background-unwinding-and-debug-info) in my [article on Apple’s Compact Unwind Info](https://gankra.github.io/blah/compact-unwinding). I’ve also attempted to [document breakpad’s STACK WIN and STACK CFI unwind info formats here](https://docs.rs/breakpad-symbols/latest/breakpad_symbols/walker/index.html), which are more similar to the DWARF and PE32 unwind tables (which are basically tiny programming languages).

If you would like to learn more about ABIs in general, [I wrote an entire article about them here](https://gankra.github.io/blah/rust-layouts-and-abis/#calling-conventions). The end of that article also includes an [introduction to how calling conventions work](https://gankra.github.io/blah/rust-layouts-and-abis/#calling-conventions). Understanding calling conventions is key to implementing unwinders.


**How Hard Did You Really Test Things?**

Hopefully you now have a bit of a glimpse into why analyzing minidumps is an enormous headache. And of course you know how the story ends: that fuzzer kicks our butts! But of course to really savor our defeat, you have to see how hard we tried to do a good job! It’s time to build up our hubris and pat ourselves on the back.

So how much work *actually* went into making rust-minidump robust before the fuzzer went to work on it?

Quite a bit!

I’ll never argue all the work we did was *perfect* but we definitely did some good work here, both for synthetic inputs and real world ones. Probably the biggest “flaw” in our methodology was the fact that we were only focused on getting Firefox’s usecase to work. Firefox runs on a lot of platforms and sees a lot of messed up stuff, but it’s still a fairly coherent product that only uses so many features of minidumps.

This is one of the nice benefits of our recent work with [Sentry](https://sentry.io/), which is basically a Crash Reporting As A Service company. They are *way* more liable to stress test all kinds of weird corners of the format that Firefox doesn’t, and they have definitely found (and fixed!) some places where something is wrong or missing! (And they recently deployed it into production too! 🎉)

But hey don’t take my word for it, check out all the different testing we did:

**Synthetic Minidumps for Unit Tests**

rust-minidump includes a [synthetic minidump generator](https://github.com/rust-minidump/rust-minidump/tree/553735e2624dcc6af82167f502cf92ae9a9fdc87/minidump-synth) which lets you come up with a high-level description of the contents of a minidump, and then produces an actual minidump binary that we can feed it into the full parser:

// Let’s make a synth minidump with this particular Crashpad Info…

let module = ModuleCrashpadInfo::new(42, Endian::Little) .add_list_annotation("annotation") .add_simple_annotation("simple", "module") .add_annotation_object("string", AnnotationValue::String("value".to_owned())) .add_annotation_object("invalid", AnnotationValue::Invalid) .add_annotation_object("custom", AnnotationValue::Custom(0x8001, vec![42])); let crashpad_info = CrashpadInfo::new(Endian::Little) .add_module(module) .add_simple_annotation("simple", "info"); let dump = SynthMinidump::with_endian(Endian::Little).add_crashpad_info(crashpad_info); // convert the synth minidump to binary and read it like a normal minidump let dump = read_synth_dump(dump).unwrap();

// Now check that the minidump reports the values we expect…

minidump-synth intentionally avoids sharing layout code with the actual implementation so that incorrect changes to layouts won’t “accidentally” pass tests.

*A brief aside for some history*: this testing framework was started by the original lead on this project, [Ted Mielczarek](https://twitter.com/TedMielczarek). He started rust-minidump as a side project to learn Rust when 1.0 was released and just never had the time to finish it. Back then he was working at Mozilla and also a major contributor to Breakpad, which is why rust-minidump has a lot of similar design choices and terminology.

This case is no exception: our minidump-synth is a shameless copy of the [synth-minidump utility in breakpad’s code](https://chromium.googlesource.com/breakpad/breakpad/+/refs/heads/main/src/processor/synth_minidump.cc), which was originally written by our *other* coworker [Jim Blandy](https://www.red-bean.com/~jimb/). Jim is one of the only people in the world that I will actually admit writes really good tests and docs, so I am totally happy to blatantly copy his work here.

Since this was all a learning experiment, Ted was understandably less rigorous about testing than usual. This meant a lot of minidump-synth was unimplemented when I came along, which also meant lots of minidump features were completely untested. (He built an absolutely great skeleton, just hadn’t had the time to fill it all in!)

We spent *a lot* of time filling in more of minidump-synth’s implementation so we could write more tests and catch more issues, but this is *definitely* the weakest part of our tests. Some stuff was implemented before I got here, so I don’t even *know* what tests are missing!

This is a good argument for some code coverage checks, but it would probably come back with “wow you should write a lot more tests” and we would all look at it and go “wow we sure should” and then we would probably never get around to it, because there are *many* things we *should* do.

On the other hand, Sentry has been very useful in this regard because they already *have* a mature suite of tests full of weird corner cases they’ve built up over time, so they can easily identify things that really matter, know what the fix should roughly be, and can contribute pre-existing test cases!

**Integration and Snapshot Tests**

We tried our best to shore up coverage issues in our unit tests by adding more holistic tests. There’s a few checked in Real Minidumps that we have [some integration tests for](https://github.com/luser/rust-minidump/blob/40c3390f5705890f932f78b7db4fc02866e012b8/minidump-processor/tests/test_processor.rs) to make sure we handle Real Inputs properly.

We even wrote a bunch of [integration tests for the CLI application that snapshot its output](https://github.com/luser/rust-minidump/blob/40c3390f5705890f932f78b7db4fc02866e012b8/minidump-stackwalk/tests/test-minidump-stackwalk.rs) to confirm that we never *accidentally* change the results.

Part of the motivation for this is to ensure we don’t break the JSON output, which we also wrote a [very detailed schema document for](https://github.com/luser/rust-minidump/blob/40c3390f5705890f932f78b7db4fc02866e012b8/minidump-processor/json-schema.md) and are trying to keep stable so people can actually rely on it while the actual implementation details are still in flux.

Yes, [minidump-stackwalk](https://github.com/luser/rust-minidump/tree/master/minidump-stackwalk) is supposed to be stable and reasonable to use in production!

For our snapshot tests we use [insta](https://github.com/mitsuhiko/insta), which I think is fantastic and more people should use. All you need to do is assert_snapshot! any output you want to keep track of and it will magically take care of the storing, loading, and diffing.

Here’s one of the snapshot tests where we invoke the CLI interface and snapshot stdout:

#[test] fn test_evil_json() { // For a while this didn't parse right let bin = env!("CARGO_BIN_EXE_minidump-stackwalk"); let output = Command::new(bin) .arg("--json") .arg("--pretty") .arg("--raw-json") .arg("../testdata/evil.json") .arg("../testdata/test.dmp") .arg("../testdata/symbols/") .stdout(Stdio::piped()) .stderr(Stdio::piped()) .output() .unwrap(); let stdout = String::from_utf8(output.stdout).unwrap(); let stderr = String::from_utf8(output.stderr).unwrap(); assert!(output.status.success()); insta::assert_snapshot!("json-pretty-evil-symbols", stdout); assert_eq!(stderr, ""); }

**Stackwalker Unit Testing**

The stackwalker is easily the most complicated and subtle part of the new implementation, because every platform can have *slight* quirks and you need to implement several different unwinding strategies and carefully tune everything to work well *in practice*.

The scariest part of this was the call frame information (CFI) unwinders, because they are basically little virtual machines we need to parse and execute at runtime. Thankfully breakpad had long ago smoothed over this issue by defining a simplified and unified CFI format, STACK CFI (well, nearly unified, x86 Windows was still a special case as STACK WIN). So even if DWARF CFI has a ton of complex features, we mostly need to implement a [Reverse Polish Notation Calculator](https://en.wikipedia.org/wiki/Reverse_Polish_notation) except it can read registers and load memory from addresses it computes (and for STACK WIN it has access to named variables it can declare and mutate).

Unfortunately, [Breakpad’s description for this format is pretty underspecified](https://chromium.googlesource.com/breakpad/breakpad/+/master/docs/symbol_files.md) so I had to basically pick some semantics I thought made sense and go with that. This made me *extremely* paranoid about the implementation. (And yes I will be more first-person for this part, because this part was genuinely where I personally spent most of my time and did a lot of stuff from scratch. All the blame belongs to me here!)

The[ STACK WIN / STACK CFI parser+evaluator](https://docs.rs/breakpad-symbols/latest/breakpad_symbols/walker/index.html) is 1700 lines. 500 of those lines are a detailed documentation and discussion of the format, and 700 of those lines are an enormous pile of ~80 test cases where I tried to come up with every corner case I could think of.

I even checked in two tests I *knew* were failing just to be honest that there were a couple cases to fix! One of them is a corner case involving dividing by a negative number that almost certainly just doesn’t matter. The other is a buggy input that old x86 Microsoft toolchains actually produce and parsers need to deal with. The latter was fixed before the fuzzing started.

And 5225225 *still* found an integer overflow in the STACK WIN preprocessing step! (Not actually that surprising, it’s a hacky mess that tries to cover up for how messed up x86 Windows unwinding tables were.)

(The code isn’t terribly interesting here, it’s just a ton of assertions that a given input string produces a given output/error.)

Of course, I wasn’t satisfied with just coming up with my own semantics and testing them: I also [ported most of breakpad’s own stackwalker tests to rust-minidump](https://github.com/luser/rust-minidump/blob/master/minidump-processor/src/stackwalker/x86_unittest.rs)! This definitely found a bunch of bugs I had, but also taught me some weird quirks in Breakpad’s stackwalkers that I’m not sure I *actually* agree with. But in this case I was flying so blind that even being bug-compatible with Breakpad was some kind of relief.

Those tests also included several tests for the non-CFI paths, which were similarly wobbly and quirky. I still really hate a lot of the weird platform-specific rules they have for stack scanning, but I’m forced to work on the assumption that they might be load-bearing. (I definitely had several cases where I disabled a breakpad test because it was “obviously nonsense” and then hit it in the wild while testing. I quickly learned to accept that **Nonsense Happens And Cannot Be Ignored**.)

One major thing I *didn’t* replicate was some of the really hairy hacks for STACK WIN. Like there are several places where they introduce extra stack-scanning to try to deal with the fact that stack frames can have mysterious extra alignment that the windows unwinding tables just don’t tell you about? I guess?

There’s almost certainly some exotic situations that rust-minidump does worse on because of this, but it probably also means we do better in some random other situations too. I never got the two to perfectly agree, but at some point the divergences were all in weird enough situations, and as far as I was concerned both stackwalkers were producing equally bad results in a bad situation. Absent any reason to prefer one over the other, divergence seemed acceptable to keep the implementation cleaner.

Here’s a simplified version of one of the ported breakpad tests, if you’re curious (thankfully minidump-synth is based off of the same binary data mocking framework these tests use):

#[test] fn test_x86_frame_pointer() { let mut f = TestFixture::new(); let frame0_ebp = Label::new(); let frame1_ebp = Label::new(); let mut stack = Section::new(); // Setup the stack and registers so frame pointers will work stack.start().set_const(0x80000000); stack = stack .append_repeated(12, 0) // frame 0: space .mark(&frame0_ebp) // frame 0 %ebp points here .D32(&frame1_ebp) // frame 0: saved %ebp .D32(0x40008679) // frame 0: return address .append_repeated(8, 0) // frame 1: space .mark(&frame1_ebp) // frame 1 %ebp points here .D32(0) // frame 1: saved %ebp (stack end) .D32(0); // frame 1: return address (stack end) f.raw.eip = 0x4000c7a5; f.raw.esp = stack.start().value().unwrap() as u32; f.raw.ebp = frame0_ebp.value().unwrap() as u32; // Check the stackwalker's output: let s = f.walk_stack(stack).await; assert_eq!(s.frames.len(), 2); { let f0 = &s.frames[0]; assert_eq!(f0.trust, FrameTrust::Context); assert_eq!(f0.context.valid, MinidumpContextValidity::All); assert_eq!(f0.instruction, 0x4000c7a5); } { let f1 = &s.frames[1]; assert_eq!(f1.trust, FrameTrust::FramePointer); assert_eq!(f1.instruction, 0x40008678); } }

## A Dedicated Production Diffing, Simulating, and Debugging Tool

Because minidumps are so horribly fractal and corner-casey, I spent *a lot* of time terrified of subtle issues that would become huge disasters if we ever actually tried to deploy to production. So I also spent a bunch of time building [socc-pair](https://github.com/Gankra/socc-pair/), which takes the id of a crash report from Mozilla’s [crash reporting system](https://crash-stats.mozilla.org/) and pulls down the minidump, the old breakpad-based implementation’s output, and extra metadata.

It then runs a local rust-minidump (minidump-stackwalk) implementation on the minidump and does a domain-specific diff over the two inputs. The most substantial part of this is a fuzzy diff on the stackwalks that tries to better handle situations like when one implementation adds an extra frame but the two otherwise agree. It also uses the reported techniques each implementation used to try to identify whose output is more trustworthy when they totally diverge.

I also ended up adding a bunch of mocking and benchmarking functionality to it as well, as I found more and more places where I just wanted to simulate a production environment.

Oh also I added [really detailed trace-logging for the stackwalker](https://github.com/luser/rust-minidump/tree/master/minidump-stackwalk#debugging-stackwalking) so that I could easily post-mortem debug why it made the decisions it made.

This tool found so many issues and more importantly has helped me quickly isolate their causes. I am so happy I made it. Because of it, we know we actually *fixed* several issues that happened with the old breakpad implementation, which is great!

Here’s a trimmed down version of the kind of report socc-pair would produce (yeah I abused diff syntax to get error highlighting. It’s a great hack, and I love it like a child):

comparing json... : { crash_info: { address: 0x7fff1760aca0 crashing_thread: 8 type: EXCEPTION_BREAKPOINT } crashing_thread: { frames: [ 0: { file: wrappers.cpp:1750da2d7f9db490b9d15b3ee696e89e6aa68cb7 frame: 0 function: RustMozCrash(char const*, int, char const*) function_offset: 0x00000010 - did not match + line: 17 - line: 20 module: xul.dll ..... unloaded_modules: [ 0: { base_addr: 0x7fff48290000 - local val was null instead of: code_id: 68798D2F9000 end_addr: 0x7fff48299000 filename: KBDUS.DLL } 1: { base_addr: 0x7fff56020000 code_id: DFD6E84B14000 end_addr: 0x7fff56034000 filename: resourcepolicyclient.dll } ] ~ ignoring field write_combine_size: "0" } - Total errors: 288, warnings: 39 benchmark results (ms): 2388, 1986, 2268, 1989, 2353, average runtime: 00m:02s:196ms (2196ms) median runtime: 00m:02s:268ms (2268ms) min runtime: 00m:01s:986ms (1986ms) max runtime: 00m:02s:388ms (2388ms) max memory (rss) results (bytes): 267755520, 261152768, 272441344, 276131840, 279134208, average max-memory: 258MB (271323136 bytes) median max-memory: 259MB (272441344 bytes) min max-memory: 249MB (261152768 bytes) max max-memory: 266MB (279134208 bytes) Output Files: * (download) Minidump: b4f58e9f-49be-4ba5-a203-8ef160211027.dmp * (download) Socorro Processed Crash: b4f58e9f-49be-4ba5-a203-8ef160211027.json * (download) Raw JSON: b4f58e9f-49be-4ba5-a203-8ef160211027.raw.json * Local minidump-stackwalk Output: b4f58e9f-49be-4ba5-a203-8ef160211027.local.json * Local minidump-stackwalk Logs: b4f58e9f-49be-4ba5-a203-8ef160211027.log.txt

**Staging and Deploying to Production**

Once we were confident enough in the implementation, a lot of the remaining testing was taken over by Will Kahn-Greene, who’s responsible for a lot of the server-side details of our crash-reporting infrastructure.

Will spent a bunch of time getting a bunch of machinery setup to manage the deployment and monitoring of rust-minidump. He also did a lot of the hard work of cleaning up all our server-side configuration scripts to handle any differences between the two implementations. (Although I spent a lot of time on compatibility, we both agreed this was a good opportunity to clean up old cruft and mistakes.)

Once all of this was set up, he turned it on in staging and we got our first look at how rust-minidump actually worked in ~production:

**Terribly!**

Our staging servers take in about 10% of the inputs that also go to our production servers, but even at that reduced scale we very quickly found several new corner cases and we were getting *tons* of crashes, which is mildly embarrassing for* the thing that handles other people’s crashes*.

Will did a great job here in monitoring and reporting the issues. Thankfully they were all fairly easy for us to fix. Eventually, everything smoothed out and things seemed to be working just as reliably as the old implementation on the production server. The only places where we were completely failing to produce any output were for horribly truncated minidumps that may as well have been empty files.

We originally *did* have some grand ambitions of running socc-pair on everything the staging servers processed or something to get *really* confident in the results. But by the time we got to that point, we were completely exhausted and feeling pretty confident in the new implementation.

Eventually Will just said “let’s turn it on in production” and I said “AAAAAAAAAAAAAAA”.

This moment was pure terror. There had always been *more* corner cases. There’s no way we could just be *done*. This will probably set all of Mozilla on fire and delete Firefox from the internet!

But Will convinced me. We wrote up some docs detailing all the subtle differences and sent them to everyone we could. Then the moment of truth finally came: Will turned it on in production, and I got to really see how well it worked in production:

**dramatic drum roll**

It worked fine.

After all that stress and anxiety, we turned it on and it was *fine*.

Heck, I’ll say it: it ran *well*.

It was faster, it crashed less, and we even knew it fixed some issues.

I was in a bit of a stupor for the rest of that week, because I kept waiting for the other shoe to drop. I kept waiting for someone to emerge from the mist and explain that I had somehow bricked *Thunderbird* or something. But no, it just worked.

So we left for the holidays, and I kept waiting for it to break, but it was *still fine*.

I am honestly still shocked about this!

But hey, as it turns out we really did put a *lot* of careful work into testing the implementation. At every step we found new problems but that was *good*, because once we got to the final step there were no more problems to surprise us.

**And the fuzzer still kicked our butts afterwards.**

But that’s part 2! Thanks for reading!


## One comment

UlrichJune 14th, 2022 at 11:09