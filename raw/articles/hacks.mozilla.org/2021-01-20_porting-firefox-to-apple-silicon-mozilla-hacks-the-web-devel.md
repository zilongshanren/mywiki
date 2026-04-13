---
title: Porting Firefox to Apple Silicon – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/01/porting-firefox-to-apple-silicon/
author: Gian-Carlo Pascutto
published: '2021-01-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The release of Apple Silicon-based Macs at the end of last year generated a flurry of news coverage and some surprises at the machine’s performance. This post details some background information on the experience of porting Firefox to run natively on these CPUs.

We’ll start with some background on the Mac transition and give an overview of Firefox internals that needed to know about the new architecture, before moving on to the concept of Universal Binaries.

We’ll then explain how DRM/EME works on the new platform, talk about our experience with macOS Big Sur, and discuss various updater problems we had to deal with. We’ll conclude with the release and an overview of various other improvements that are in the pipeline.

**Apple Silicon Approaching**

Speculation that Apple would switch its Mac lineup to use ARM CPUs had been ongoing in the industry for several years. As early as 2013, [Apple had referred to the custom ARM chips they were putting in the iPhone as “desktop-class” designs](https://www.apple.com/uk/newsroom/2013/09/10Apple-Announces-iPhone-5s-The-Most-Forward-Thinking-Smartphone-in-the-World/).

While the claim initially met some scepticism, near the end of 2018 computer hardware magazine AnandTech published the results of running the [industry-standard SPEC benchmark on the iPhone XS](https://www.anandtech.com/show/13392/the-iphone-xs-xs-max-review-unveiling-the-silicon-secrets/4), showing that even workloads that reflect real-world desktop use cases reached desktop chip performance, and were doing so at significantly better power efficiency. This provided us with some warning that Apple might be ready to start the transition to the ARM architecture in the near future.

From the perspective of Mozillla’s platform team, an area of particular interest for such an architecture change on macOS is Firefox’s use of macOS APIs. Firefox and Gecko’s roots go back to the Netscape codebase, which already supported the Mac as it was in 1994.

Although continuously updated, Firefox still uses a wide range of macOS APIs that followed the Mac’s evolution over the years (Carbon, Cocoa, HITheme, Quartz, …).

Apple has generally kept them — the code is there and working, after all — and has even added compatibility shims in some places where behavior has changed. But they’re not willing to keep compatibility forever, and in fact had removed 32-bit support in the previous macOS Catalina which had an impact on applications that were relying on this, among them many games.

As such, we were concerned that not all APIs would still be supported on the new architecture and we’d have to go in and rewrite some amount of widget, toolkit or theming code in short order.

Based on the performance from the aforementioned benchmarks and Apple’s historical release schedule, the platform team estimated in March that “macOS 10.16” was likely to appear around September or October 2020 and that there was a significant risk it could involve API changes in order to add ARM support, which we took into account in our planning.

**The Announcement**

On the 22nd of June 2020, Apple confirmed it would begin moving its Mac hardware to their own ARM chips – referred to as Apple Silicon. They also confirmed that the machines would ship with an Intel x64 emulator (Rosetta 2) and would support iOS apps.

The latter led to some guessing within Mozilla’s platform team as to whether the new Macs would have a touchscreen. While we were — and still are — quite ready to support it, at least the eventual first Apple Silicon-based Macs didn’t end up having one.

Together with the announcement of the transition, Apple also announced the availability of Developer Transition Kits (DTK), [essentially containing the iPad Pro’s chip in a Mac Mini housing](https://www.apple.com/newsroom/2020/06/apple-announces-mac-transition-to-apple-silicon/). What Apple didn’t share was when exactly the final machines were coming to market.

Based on the timing of the DTK availability and Apple’s hint that it would be “by the end of the year”, we guessed this was likely to be somewhat before the Christmas holidays.

Looking back, we noticed that Apple has very consistently been able to make hardware available near immediately after announcing it, so we figured that any next planned announcement should be taken as a release date.

When another announcement was planned for November 10th – about a month before our original estimate – we took it as the shipping date. And indeed, Apple did end up shipping the first hardware one week later on November 17th.

**First Steps**

Of all the work needed to support the new hardware, porting Firefox to the 64-bit ARM architecture was not actually something we needed to do: we’ve supported 64-bit ARM on Android and Linux for years.

We refrained from publishing the 64-bit Android builds until late 2019 because before that point our JavaScript JIT was not fully optimized for 64-bit ARM, and the resulting 64-bit version would have been slower than the 32-bit one. There wasn’t much demand for the browser to be able to use over 4GB of memory on phones either! In 2019, [we released the first Firefox version for Windows on 64 bit ARM](https://blog.mozilla.org/futurereleases/2019/04/11/firefox-beta-for-windows-10-on-qualcomm-snapdragon-always-connected-pcs-now-available/) which gave us some additional experience in exactly the kind of effort we were facing now.

[While Windows on ARM hardware has failed to catch on with our users so far,](https://data.firefox.com/dashboard/hardware) expectations were for the Apple transition to be very different. Not only was there a good reason to expect hardware performance to be groundbreaking as explained in the first section. Apple made it clear they were switching their entire lineup and not releasing a single device as a “feeler”. To top it off, they had a proven track record of successful architecture transitions on the Mac.

So with 64-bit ARM support already in the codebase, the first pass of work was to go through all the Firefox code, dependencies, and various third-party build systems to see if they correctly dealt with the novel idea that a Mac could have an ARM chip inside.

Secondly, we needed to adapt and fix the various parts of the Firefox codebase that deal with low-level calling conventions and particularly the interfaces between the JavaScript and C++ (and nowadays Rust) parts of the code.

Rust in particular was a concern. Firefox depends on Rust code, and we require a working Rust compiler to build the browser. Although [Apple Silicon support for Rust was underway](https://github.com/rust-lang/rust/issues/73908), it took until mid-August for there to be functional compiler builds, which limited the amount of progress possible for Firefox.

Once the compiler was working, a similar exercise needed to be done with all the Rust crates we depend on. The need to update the compiler and the reliance of some crates on the exact compiler version, especially parts dealing with SIMD support, would end up biting us later on as it made it hard to push Apple Silicon support forward to an earlier release of Firefox without potentially affecting other platforms.

**Universal Binaries**

An important decision to be made was whether to produce separate builds for Intel- and ARM-based Macs, or to generate [Universal Binaries](https://en.wikipedia.org/wiki/Universal_binary) which bundle both builds and select the correct version at runtime. Producing Universal Binaries is a bit more complicated, but we had existing tooling in place dating back to the time when Apple supported both 32-bit and 64-bit binaries, which could be adapted.

It greatly simplifies things for the user — there is no risk of downloading the wrong version — and also meant that our download pages and some infrastructure like localization could remain unchanged.

The main downside is the installer significantly increasing in size, not just for ARM users but also for Intel ones. As this only affects the initial install, and users typically receive new versions through updates that are much smaller, we felt that this was an acceptable downside and proceeded along this route.

**Netflix and DRM**

While we can port the open-source parts of Firefox to 64-bit ARM ourselves, Netflix and some other video streaming services such as Hulu, Disney+, or Amazon Prime require their video to be decoded with closed source, proprietary DRM software.

If the user visits such a site, [Firefox will automatically download and install such a proprietary EME/CDM module](https://support.mozilla.org/en-US/kb/enable-drm). This presented a problem to us as we would be dependent on those third-party vendors to publish ARM64 versions of those decoders.

We did not manage to get a commitment to a release date for such updates, and even if we did, there was no guarantee that they would be before the unknown release date of the Apple Silicon hardware. As a significant number of our users use the browser to watch video online, this presented a potential showstopper for a native Apple Silicon release.

We ended up leveraging a technique that we are also using for the Windows on ARM version of Firefox. The DRM video decoder already executes in a separate process so we can sandbox the proprietary code from the user’s system.

If we force this decoding process to run under emulation, we would be able to use the existing Intel x64 decoder modules and have them communicate with the main browser that was running natively.

There were a few catches to getting this to work: because the process that loads the Google Widevine DRM module itself depends on some runtime libraries, we needed Intel x64 copies of those as well.

Luckily, due to the Universal Binary containing both versions of Firefox, we were able to pick them up directly from the Application Bundle.

Secondly, Apple did not actually ship their Rosetta 2 emulator preinstalled on the Apple Silicon machines but its installation is triggered when the user tries to run an Intel application.

So while it is very likely in practice that Rosetta is installed on the user’s system, we could not rely on this always being the case. Triggering the installation of Rosetta programmatically works, but [some of our colleagues found out the hard way it is not very reliable](https://bugs.chromium.org/p/chromium/issues/detail?id=1150538), so we backed off on doing this in our first release and fell back to [referring people that hit the relevant error to a support article](https://support.mozilla.org/en-US/kb/netflix-hulu-disney-or-prime-error-mac-apple-silicon).

**macOS Big Sur**

The macOS Big Sur betas arrived independently of the Apple Silicon hardware and allowed us to get an early look at the compatibility story. To our relief, no APIs we depended on were deprecated and any backwards compatibility problems or missing shims were limited to small cosmetic issues, which we [typically managed to fix quickly](https://bugzilla.mozilla.org/show_bug.cgi?id=1648487). [Other open-source projects with a similarly old codebase were not as lucky](https://bugs.documentfoundation.org/show_bug.cgi?id=138122).

Bumping the version numbers from 10.x to 11.0 – somewhat predictably – produced errors [both in our code](https://bugzilla.mozilla.org/show_bug.cgi?id=1647816) and in [external websites relying on UA sniffing](https://bugzilla.mozilla.org/show_bug.cgi?id=1680516), despite Apple’s attempts to mitigate the problem by returning the old version number in apps built with older SDKs.

**Update Woes**

Pushing the updated Firefox application bundle to users – which was now a Universal Binary supporting both types of Apple hardware, instead of only Intel x64 as before – revealed some further complications.

During an update, after updating the files on disk, Firefox will relaunch the updated version of itself. Any application on Apple Silicon that is running under Intel x64 emulation and launches another process will also cause that process to be launched under emulation.

So when the old Firefox 83 – running under emulation – launches the new Firefox 84 with native support, it would not launch the new native binary but end up forcing it to be run under emulation as well, at least until the application was fully restarted.

While we [developed a workaround](https://bugzilla.mozilla.org/show_bug.cgi?id=1677036) for this, we didn’t feel it was sufficiently tested by the release date for the marginal benefit it gave and ended up simply [adding a release note to cover this case](https://support.mozilla.org/en-US/kb/upgrading-new-version-firefox-84-apple-silicon).

More of a concern was user reports that some antivirus software was flagging all our Universal Binaries as malware, and corrupting the Firefox installation the moment the update arrived.

The software was using machine learning techniques and presumably observed that our combined Universal Binaries didn’t quite look like any other legitimate software it had ever seen before.

Attempts to contact the vendor through regular support channels were unsuccessful so we ended up searching LinkedIn and managed to find an engineer working on the core antivirus detection.

They immediately understood the seriousness of the problem and took prompt action to get a fix shipped, thus preventing quite the disaster for the users of this product. It’s notable that without this last-ditch effort we would have been effectively blocked from releasing a native Apple Silicon version for an indefinite period.

This wouldn’t be the first time that [browser makers are exasperated](https://twitter.com/justinschuh/status/802491391121260544) at the [misaligned incentives for anti-virus vendors](https://twitter.com/justinschuh/status/803665580540633088) when anti-virus software and browsers [don’t get along](https://bugzilla.mozilla.org/show_bug.cgi?id=1682834).

**Release Calls**

Comparing the Firefox release schedule with the predicted release date from Apple meant that our Firefox 83 – scheduled for November 17th – aligned with the availability of release hardware.

While it would have been nice to announce native support in the stable version as soon as the first production machines arrived to customers, this would also have meant that it would be completely untested on the real hardware.

We decided to be conservative here and keep our initial support to the Firefox 84 beta, which was released the same day as Firefox 83, giving both us and our users a window of time to evaluate the stability of the product on the actual Apple Silicon hardware.

Though somewhat disappointed that after being one of the first to [announce native support in Nightly](https://twitter.com/MikeHommey/status/1327143370024738820) we ended up delaying a stable release slightly, the difficulties experienced by other browser vendors with shipping a working version supported our decision. Firefox with native Apple Silicon support went into the wider world when 84 beta rolled into the Firefox 84 release, on December 15th, 2020.

While most benchmarking of Apple Silicon indicated that the performance impact of Rosetta emulation was typically low and that [applications could be expected to run at about 70-80% of native performance](https://www.anandtech.com/show/16252/mac-mini-apple-m1-tested/6), we saw much larger gains when testing the native Firefox build, including doubled performance on some key benchmarks and a spectacular 2.5 times faster startup.

One reasonable explanation for this faster startup could be that many parts of Firefox itself are written in the web’s own languages – JavaScript, CSS, and HTML – and thus use a JavaScript JIT for much of its own functionality.

On startup, the JIT has to translate the JavaScript to machine code and while this is typically a very fast operation when running under emulation Rosetta has to then translate this JIT-generated machine code to machine code for another architecture.

Apple [introduced a translation cache](https://bugzilla.mozilla.org/show_bug.cgi?id=1651455#c3) that likely removes this overhead completely for most applications but it does not work for code that is output by a JIT. With the native build, this second translation is avoided completely and we’re back to having a snappy browser.

**Future Support**

With the initial release out, there are a number of further improvements that we can and will make to the Apple Silicon version, some of which will already be available in Firefox 85.

First of all, we had to disable [WebRender](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/) in the initial version because it triggered graphics driver bugs in the first Big Sur releases for Apple Silicon. Now that these have been addressed and we’ve validated WebRender on the final hardware, [we have re-enabled it](https://bugzilla.mozilla.org/show_bug.cgi?id=1679998) and it will ship in 85.

Secondly, Firefox currently uses the [baseline compiler for WebAssembly on 64-bit ARM](https://hacks.mozilla.org/2018/01/making-webassembly-even-faster-firefoxs-new-streaming-and-tiering-compiler/). There is a [faster optimizing compiler called Cranelift ](https://github.com/bytecodealliance/wasmtime/tree/main/cranelift)[available for testing on Firefox Nightly](https://bugzilla.mozilla.org/show_bug.cgi?id=1660944), and in a few weeks, we expect to finish the 64-bit ARM port of our own optimizing compiler, Ion, [which is likely to become the new default](https://bugzilla.mozilla.org/show_bug.cgi?id=1687626).

The Apple Silicon chips are one of the first desktop chips that are a heterogeneous design with distinct performance and efficiency cores. We’re [revising much of our core threading](https://bugzilla.mozilla.org/show_bug.cgi?id=1637592) and thread pooling architecture to [handle the distinction better](https://bugzilla.mozilla.org/show_bug.cgi?id=1672257), improve efficiency, and eventually be [able to schedule less performance-critical tasks on the efficiency cores](https://bugzilla.mozilla.org/show_bug.cgi?id=1678083).

Finally, we’re cleaning up and modernizing our usage of legacy macOS drawing APIs, and in some cases, [removing our custom drawing code entirely](https://bugzilla.mozilla.org/show_bug.cgi?id=34572). This is expected to help with some of the [outstanding glitches in dark mode support](https://bugzilla.mozilla.org/show_bug.cgi?id=1558086), as [the legacy macOS APIs simply don’t support it](https://trac.wxwidgets.org/ticket/18146) and the[ color values must be obtained via newer APIs](https://bugreports.qt.io/browse/QTBUG-68891). It will also remove some of our deprecation worries!

We hope you enjoyed this inside view of how the Firefox team experienced the Apple Silicon transition and we’re looking forward to pushing the Firefox experience on macOS to even higher levels in the year to come.


*Thanks to Mike Hommey and Haik Aftandilian for their substantial input to this post. They also did a lot of the engineering work described here. Further editorial suggestions were provided by Andrew Overholt, Sylvestre Ledru, and Selena Deckelmann.*


## 9 comments

Ja PatelJanuary 20th, 2021 at 20:43Juraj M.January 21st, 2021 at 01:50Tom KwongJanuary 21st, 2021 at 07:14Joe SteeleFebruary 16th, 2021 at 11:45K. R.January 21st, 2021 at 07:34Gian-Carlo PascuttoJanuary 21st, 2021 at 08:52Andrew MorrowJanuary 21st, 2021 at 09:56Gian-Carlo PascuttoJanuary 21st, 2021 at 10:22JamesJanuary 22nd, 2021 at 13:31