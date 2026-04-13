---
title: Fuzzing rust-minidump for Embarrassment and Crashes – Part 2 – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2022/06/fuzzing-rust-minidump-for-embarrassment-and-crashes/
author: Aria Beingessner
published: '2022-06-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is part 2 of a series of articles on rust-minidump. For part 1, see [here](https://hacks.mozilla.org/2022/06/everything-is-broken-shipping-rust-minidump-at-mozilla/).

So to recap, we rewrote breakpad’s minidump processor in Rust, wrote a ton of tests, and deployed to production without any issues. We killed it, perfect job.

And we *still* got massively dunked on by the fuzzer. Just absolutely destroyed.

I was starting to pivot off of rust-minidump work because I needed a bit of palette cleanser before tackling round 2 (handling native debuginfo, filling in features for other groups who were interested in rust-minidump, adding extra analyses that we’d always wanted but were too much work to do in Breakpad, etc etc etc).

I was still getting some PRs from people filling in the corners they needed, but nothing that needed too much attention, and then[ @5225225](https://github.com/5225225) smashed through the windows and released a bunch of exploding fuzzy rabbits into my office.

I had no idea who they were or why they were there. When I asked they just lowered one of their seven pairs of sunglasses and said “Because I can. Now hold this bunny”. I did as I was told and held the bunny. It was a good bun. Dare I say, it was a true *bnnuy*: it was[ libfuzzer](https://www.llvm.org/docs/LibFuzzer.html). (Huh? You thought it was gonna be[ AFL](https://github.com/google/AFL)? Weird.)

As it turns out, several folks had built out some *really nice* infrastructure for quickly setting up a decent fuzzer for some Rust code:[ cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz). They even wrote[ a little book that walks you through the process](https://rust-fuzz.github.io/book/cargo-fuzz.html).

Apparently those folks had done such a good job that 5225225 had decided it would be a really great hobby to just pick up a random rust project and implement fuzzing for it. And then to fuzz it. And file issues. And PRs that fix those issues. And then implement even more fuzzing for it.

Please help my office is drowning in rabbits and I haven’t seen my wife in weeks.

As far as I can tell, the process seems to genuinely be pretty easy! I think their[ first fuzzer for rust-minidump](https://github.com/luser/rust-minidump/pull/405) was basically just:

- checked out the project
- run cargo fuzz init (which autogenerates a bunch of config files)
- write a file with this:

#![no_main] use libfuzzer_sys::fuzz_target; use minidump::*; fuzz_target!(|data: &[u8]| { // Parse a minidump like a normal user of the library if let Ok(dump) = minidump::Minidump::read(data) { // Ask the library to get+parse several streams like a normal user. let _ = dump.get_stream::<MinidumpAssertion>(); let _ = dump.get_stream::<MinidumpBreakpadInfo>(); let _ = dump.get_stream::<MinidumpCrashpadInfo>(); let _ = dump.get_stream::<MinidumpException>(); let _ = dump.get_stream::<MinidumpLinuxCpuInfo>(); let _ = dump.get_stream::<MinidumpLinuxEnviron>(); let _ = dump.get_stream::<MinidumpLinuxLsbRelease>(); let _ = dump.get_stream::<MinidumpLinuxMaps>(); let _ = dump.get_stream::<MinidumpLinuxProcStatus>(); let _ = dump.get_stream::<MinidumpMacCrashInfo>(); let _ = dump.get_stream::<MinidumpMemoryInfoList>(); let _ = dump.get_stream::<MinidumpMemoryList>(); let _ = dump.get_stream::<MinidumpMiscInfo>(); let _ = dump.get_stream::<MinidumpModuleList>(); let _ = dump.get_stream::<MinidumpSystemInfo>(); let _ = dump.get_stream::<MinidumpThreadNames>(); let _ = dump.get_stream::<MinidumpThreadList>(); let _ = dump.get_stream::<MinidumpUnloadedModuleList>(); } });

And that’s… it? And all you have to do is type cargo fuzz run and it downloads, builds, and spins up an instance of[ libfuzzer](https://www.llvm.org/docs/LibFuzzer.html) and finds bugs in your project overnight?

Surely that won’t find anything interesting. Oh it did? It was largely all bugs in code I wrote? **Nice.**

cargo fuzz is clearly awesome but let’s not downplay the amount of bafflingly incredible work that 5225225 did here! Fuzzers, sanitizers, and other code analysis tools have a *very bad* reputation for drive-by contributions.

I think we’ve all heard stories of someone running a shiny new tool on some big project they know nothing about, mass filing a bunch of issues that just say “this tool says your code has a problem, fix it” and then disappearing into the mist and claiming victory.

This is not a pleasant experience for someone trying to maintain a project. You’re dumping a lot on my plate if I don’t know the tool, have trouble running the tool, don’t know exactly how you ran it, etc.

It’s also very easy to come up with a huge pile of issues with very little sense of how significant they are.

Some things are only vaguely dubious, while others are horribly terrifying exploits. We only have so much time to work on stuff, you’ve gotta help us out!

And in this regard 5225225’s contributions were just, bloody beautiful.

Like, shockingly fantastic.

They wrote really clear and detailed issues. When I skimmed those issues and misunderstood them, they quickly clarified and got me on the same page. And then they submitted a fix for the issue before I even considered working on the fix. And quickly responded to review comments. I didn’t even bother asking them to squashing their commits because damnit they *earned* those 3 commits in the tree to fix one overflow.

Then they submitted a PR to merge the fuzzer. They helped me understand how to use it and debug issues. Then they started asking questions about the project and started writing more fuzzers for other parts of it. And now there’s like 5 fuzzers and a bunch of fixed issues!

I don’t care how good cargo fuzz is, that’s a lot of friggin’ really good work! Like I am going to cry!! This was so helpful??? 😭

That said, I will take a *little* credit for this going so smoothly: both Rust itself and rust-minidump are written in a way that’s very friendly to fuzzing. Specifically, rust-minidump is riddled with assertions for “hmm this seems messed up and shouldn’t happen but maybe?” and Rust turns integer overflows into panics (crashes) in debug builds (and index-out-of-bounds is always a panic).

Having lots of assertions everywhere makes it *a lot* easier to detect situations where things go wrong. And when you *do* detect that situation, the crash will often point pretty close to where things went wrong.

As someone who has worked on detecting bugs in Firefox with sanitizer and fuzzing folks, let me tell you what really sucks to try to do anything with: “Hey so on my machine this enormous complicated machine-generated input caused Firefox to crash *somewhere* this *one time*. No, I can’t reproduce it. You won’t be able to reproduce it either. Anyway, try to fix it?”

That’s not me throwing shade on anyone here. I am all of the people in that conversation. The struggle of productively fuzzing Firefox is all too real, and I do not have a good track record of fixing those kinds of bugs.

By comparison I am absolutely *thriving* under “Yeah you can deterministically trip this assertion with this tiny input you can just check in as a unit test”.

And what did we screw up? Some legit stuff! It’s Rust code, so I am fairly confident none of the issues were *security* concerns, but they were definitely quality of implementation issues, and could have been used to at very least denial-of-service the minidump processor.

Now let’s dig into the issues they found!

**#428: Corrupt stacks caused infinite loops until OOM on ARM64**

As noted in the background, stackwalking is a giant heuristic mess and you can find yourself going backwards or stuck in an infinite loop. To keep this under control, stackwalkers generally require *forward progress*.

Specifically, they require the stack pointer to move down the stack. If the stack pointer ever goes backwards or stays the same, we just call it quits and end the stackwalk there.

However, you can’t be *so* strict on ARM because leaf functions *may not change the stack size at all*. Normally this would be impossible because every function call *at least* has to push the return address to the stack, but ARM has the *link register* which is basically an extra buffer for the return address.

The existence of the link register in conjunction with an ABI that makes the callee responsible for saving and restoring it means leaf functions *can* have 0-sized stack frames!

To handle this, an ARM stackwalker must allow for there to be no forward progress for the *first* frame of a stackwalk, **and then become more strict**. Unfortunately I hand-waved that second part and ended up allowing infinite loops with no forward progress:

// If the new stack pointer is at a lower address than the old, // then that's clearly incorrect. Treat this as end-of-stack to // enforce progress and avoid infinite loops. // // NOTE: this check allows for equality because arm leaf functions // may not actually touch the stack (thanks to the link register // allowing you to "push" the return address to a register). if frame.context.get_stack_pointer() < self.get_register_always("sp") as u64 { trace!("unwind: stack pointer went backwards, assuming unwind complete"); return None; }

So if the ARM64 stackwalker ever gets stuck in an infinite loop on one frame, it will just build up an infinite backtrace until it’s killed by an OOM. This is very nasty because it’s a potentially very slow denial-of-service that eats up all the memory on the machine!

This issue was actually originally discovered and fixed in[ #300](https://github.com/luser/rust-minidump/issues/300) *without* a fuzzer, but when I fixed it for ARM (32-bit) I completely forgot to do the same for ARM64. Thankfully the fuzzer was evil enough to discover this infinite looping situation on its own, and the fix was just “copy-paste the logic from the 32-bit impl”.

Because this issue was actually encountered in the wild, we know this was a serious concern! Good job, fuzzer!

(This issue specifically affected minidump-processor and minidump-stackwalk)

**#407: MinidumpLinuxMaps address-based queries didn’t work at all**

MinidumpLinuxMaps is an interface for querying the dumped contents of Linux’s /proc/self/maps file. This provides metadata on the permissions and allocation state for mapped ranges of memory in the crashing process.

There are two usecases for this: just getting a full dump of all the process state, and specifically querying the memory properties for a specific address (“hey is this address executable?”). The dump usecase is handled by just shoving everything in a Vec. The address usecase requires us to create a RangeMap over the entries.

Unfortunately, a comparison was flipped in the code that created the keys to the RangeMap, which resulted in every *correct* memory range being discarded AND invalid memory ranges being accepted. The fuzzer was able to catch this because the invalid ranges tripped an assertion when they got fed into the RangeMap (hurray for redundant checks!).

// OOPS if self.base_address < self.final_address { return None; }

Although tests were written for MinidumpLinuxMaps, they didn’t include any invalid ranges, and just used the dump interface, so the fact that the RangeMap was empty went unnoticed!

This *probably* would have been quickly found as soon as anyone tried to actually use this API in practice, but it’s nice that we caught it beforehand! Hooray for fuzzers!

(This issue specifically affected the minidump crate which technically could affect minidump-processor and minidump-stackwalk. Although they didn’t yet actually do address queries, they may have crashed when fed invalid ranges.)

**#381: OOM from reserving memory based on untrusted list length.**

Minidumps have lots of lists which we end up collecting up in a Vec or some other collection. It’s quite natural and more efficient to start this process with something like Vec::with_capacity(list_length). Usually this is fine, but if the minidump is corrupt (or malicious), then this length could be impossibly large and cause us to immediately OOM.

We were broadly aware that this was a problem, and had discussed the issue in[ #326](https://github.com/luser/rust-minidump/issues/326), but then everyone left for the holidays. #381 was a nice kick in the pants to actually fix it, and gave us a free simple test case to check in.

Although the naive solution would be to fix this by just removing the reserves, we opted for a solution that guarded against obviously-incorrect array lengths. This allowed us to keep the performance win of reserving memory while also making rust-minidump fast-fail instead of vaguely trying to do something and hallucinating a mess.

Specifically, @Swatinem introduced a function for checking that the amount of memory left in the section we’re parsing is *large enough* to even hold the claimed amount of items (based on their known serialized size). This should mean the minidump crate can only be induced to reserve O(n) memory, where n is the size of the minidump itself.

For some scale:

- A minidump for Firefox’s main process with about 100 threads is about 3MB.
- A minidump for a stackoverflow from infinite recursion (8MB stack, 9000 calls) is about 8MB.
- A breakpad symbol file for Firefox’s main module can be about
**200MB**.

If you’re symbolicating, Minidumps probably won’t be your memory bottleneck. 😹

(This issue specifically affected the minidump crate and therefore also minidump-processor and minidump-stackwalk.)

**The Many Integer Overflows and My Greatest Defeat**

The rest of the issues found were relatively benign integer overflows. I claim they’re benign because rust-minidump should *already* be working under the assumption that all the values it reads out of the minidump could be corrupt garbage. This means its code is riddled with “is this nonsense” checks and those usually very quickly catch an overflow (or at worst print a nonsense value for some pointer).

We still fixed them all, because that’s shaky as heck logic and we want to be robust. But yeah none of these were even denial-of-service issues, as far as I know.

To demonstrate this, let’s discuss the most evil and embarrassing overflow which was definitely my fault and I am *still* mad about it but in a like “how the heck” kind of way!?

The overflow is back in our old friend the stackwalker. Specifically in the code that attempts to unwind using frame pointers. Even more specifically, when offsetting the supposed frame-pointer to get the location of the supposed return address:

let caller_ip = stack_memory.get_memory_at_address(last_bp + POINTER_WIDTH)?; let caller_bp = stack_memory.get_memory_at_address(last_bp)?; let caller_sp = last_bp + POINTER_WIDTH * 2;

If the frame pointer (last_bp) was ~u64::MAX, the offset on the first line would overflow and we would instead try to load ~null. All of our loads are explicitly fallible (we assume everything is corrupt garbage!), and nothing is ever mapped to the null page in normal applications, so this load would reliably fail as if we had guarded the overflow. Hooray!

…but the overflow would panic in debug builds because that’s how debug builds work in Rust!

This was actually found, reported, and fixed *without* a fuzzer in[ #251](https://github.com/luser/rust-minidump/issues/251). All it took was a simple guard:

(All the casts are because this specific code is used in the x86 impl *and* the x64 impl.)

if last_bp as u64 >= u64::MAX - POINTER_WIDTH as u64 * 2 { // Although this code generally works fine if the pointer math overflows, // debug builds will still panic, and this guard protects against it without // drowning the rest of the code in checked_add. return None; } let caller_ip = stack_memory.get_memory_at_address(last_bp as u64 + POINTER_WIDTH as u64)?; let caller_bp = stack_memory.get_memory_at_address(last_bp as u64)?; let caller_sp = last_bp + POINTER_WIDTH * 2;

And then it was found, reported, and fixed **again** *with a fuzzer* in[ #422](https://github.com/luser/rust-minidump/issues/422).

Wait what?

Unlike the infinite loop bug, I *did* remember to add guards to all the unwinders for this problem… but I did the overflow check in 64-bit *even for the 32-bit platforms*.

**slaps forehead**

This made the bug report especially confusing at first because the overflow was like 3 lines away from *a guard for that exact overflow*. As it turns out, the mistake wasn’t actually as obvious as it sounds! To understand what went wrong, let’s talk a bit more about pointer width in minidumps.

A single instance of rust-minidump has to be able to handle crash reports from *any* platform, even ones it isn’t natively running on. This means it needs to be able to handle both 32-bit and 64-bit platforms in one binary. To avoid the misery of copy-pasting everything or making everything generic over pointer size, rust-minidump prefers to work with 64-bit values wherever possible, even for 32-bit plaftorms.

This isn’t just us being lazy: the minidump format itself does this! Regardless of the platform, a minidump will refer to ranges of memory with a[ MINIDUMP_MEMORY_DESCRIPTOR](https://docs.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_memory_descriptor) whose base address is a 64-bit value, even on 32-bit platforms!

typedef struct _MINIDUMP_MEMORY_DESCRIPTOR { ULONG64 StartOfMemoryRange; MINIDUMP_LOCATION_DESCRIPTOR Memory; } MINIDUMP_MEMORY_DESCRIPTOR, *PMINIDUMP_MEMORY_DESCRIPTOR;

So quite naturally rust-minidump’s interface for querying saved regions of memory just operates on 64-bit (u64) addresses unconditionally, and 32-bit-specific code casts its u32 address to a u64 before querying memory.

That means the code with the overflow guard *was* manipulating those values as u64s on x86! The *problem* is that after all the memory loads we would then go back to “native” sizes and compute caller_sp = last_bp + POINTER_WIDTH * 2. This would overflow a u32 and crash in debug builds. 😿

But here’s the really messed up part: *getting to that point meant we were successfully loading memory up to that address*. The first line where we compute caller_ip reads it! So this overflow means… we were… loading memory… from an address that was beyond u32::MAX…!?

Yes!!!!!!!!

The fuzzer had found an absolutely *brilliantly evil input*.

It abused the fact that MINIDUMP_MEMORY_DESCRIPTOR *technically* lets 32-bit minidumps define memory ranges beyond u32::MAX *even though they could never actually access that memory!* It could then have the u64-based memory accesses succeed but still have the “native” 32-bit operation overflow!

This is so messed up that I didn’t even *comprehend* that it had done this until I wrote my own test and realized that it wasn’t actually failing because I *foolishly* had limited the range of valid memory to the mere 4GB a normal x86 process is restricted to.

And I mean that quite literally: this is exactly the issue that creates[ Parallel Universes in Super Mario 64](https://youtu.be/kpk2tdsPh0A?t=638).

But hey my code was probably just bad. I know google loves sanitizers and fuzzers, so I bet google breakpad found this overflow ages ago and fixed it:

uint32_t last_esp = last_frame->context.esp; uint32_t last_ebp = last_frame->context.ebp; uint32_t caller_eip, caller_esp, caller_ebp; if (memory_->GetMemoryAtAddress(last_ebp + 4, &caller_eip) && memory_->GetMemoryAtAddress(last_ebp, &caller_ebp)) { caller_esp = last_ebp + 8; trust = StackFrame::FRAME_TRUST_FP; } else { ...

Ah. Hmm. They don’t guard for any kind of overflow for those uint32_t’s (or the uint64_t’s in the x64 impl).

Well ok GetMemoryAtAddress does actual bounds checks so the load from ~null will generally fail like it does in rust-minidump. But what about the Parallel Universe overflow that lets GetMemoryAtAddress succeed?

Ah well surely breakpad is more principled with integer width than I was–

virtual bool GetMemoryAtAddress(uint64_t address, uint8_t* value) const = 0; virtual bool GetMemoryAtAddress(uint64_t address, uint16_t* value) const = 0; virtual bool GetMemoryAtAddress(uint64_t address, uint32_t* value) const = 0; virtual bool GetMemoryAtAddress(uint64_t address, uint64_t* value) const = 0;

Whelp congrats to 5225225 for finding an overflow that’s portable between two implementations in two completely different languages by exploiting the very nature of the file format itself!

In case you’re wondering what the implications of this overflow are: it’s still basically benign. Both rust-minidump and google-breakpad will successfully complete the frame pointer analysis and yield a frame with a ~null stack pointer.

Then the outer layer of the stackwalker which runs all the different passes in sequence will see something succeeded but that the frame pointer went backwards. At this point it will discard the stack frame and terminate the stackwalk normally and just calmly output whatever the backtrace was up to that point. Totally normal and reasonable operation.

I expect this is why no one would notice this in breakpad even if you run fuzzers and sanitizers on it: nothing in the code actually does anything *wrong*. Unsigned integers are defined to wrap, the program behaves reasonably, everything is *kinda* fine. We only noticed this in rust-minidump because *all* integer overflows panic in Rust debug builds.

However this “benign” behaviour *is* slightly different from properly guarding the overflow. Both implementations will normally try to move on to *stack scanning* when the frame pointer analysis fails, but in this case they give up immediately. It’s *important* that the frame pointer analysis properly identifies failures so that this cascading can occur. Failing to do so is definitely a bug!

However in this case the stack is partially in a parallel universe, so getting any kind of useful backtrace out of it is… dubious to say the least.

So I totally stand by “this is totally benign and not actually a problem” but also “this is sketchy and we should have the bounds check so we can be confident in this code’s robustness and correctness”.

Minidumps are *all* corner cases — they literally get generated *when a program encounters an unexpected corner case*! It’s *so* tempting to constantly shrug off situations as “well no reasonable program would ever do this, so we can ignore it”… but YOU CAN’T.

You would not have a minidump at your doorstep if the program had behaved reasonably! The fact that you are trying to inspect a minidump means something messed up happened, and you need to just deal with it!

That’s why we put so much energy into testing this thing, it’s a nightmare!

I am *extremely* paranoid about this stuff, but that paranoia is based on the horrors I have seen. There are always more corner cases.

There are *ALWAYS* more corner cases. **ALWAYS**.


## 2 comments

Sora2555June 23rd, 2022 at 16:35U101June 27th, 2022 at 02:30