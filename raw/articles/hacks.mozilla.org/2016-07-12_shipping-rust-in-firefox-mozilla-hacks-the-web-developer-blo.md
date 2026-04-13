---
title: Shipping Rust in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/07/shipping-rust-in-firefox/
author: Dave Herman
published: '2016-07-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**TL;DR: Starting with Firefox 48, Mozilla is shipping its first production Rust code, with more to come!**

## Mozilla ❤ Rust

It’s hard to believe it’s been almost seven years since Mozilla Research first began sponsoring the development of [Rust](https://www.rust-lang.org/en-US/), at the time little more than an ambitious research experiment with a small but devoted community. Remarkably, despite a long history of inventions and discoveries, Rust’s key principles have remained constant. The Rust core team’s original vision—a safe alternative to C++ to make systems programmers more productive, mission-critical software less prone to memory exploits, and parallel algorithms more tractable—has been central to Mozilla’s interest in backing the Rust project and, ultimately, using Rust in production.

An equally promising development has been the fact that Rust’s safety and modern features are attracting new people to systems programming. For Mozilla, where community-based development is quite literally [our mission](https://www.mozilla.org/en-US/mission/), widening our circle is vital.

So I’m pleased to mark an important milestone:** with Firefox 48, Mozilla will ship our first Rust component to all desktop platforms**, and with Android support coming soon.

## Building Rust into Mozilla’s media stack

One of the first groups at Mozilla to make use of Rust was the Media Playback team. Now, it’s certainly easy to see that media is at the heart of the modern Web experience. What may be less obvious to the non-paranoid is that every time a browser plays a seemingly innocuous video (say, a [chameleon popping bubbles](https://www.youtube.com/watch?v=xn54TvpGu7E)), it’s reading data delivered in a complex format and created by someone you don’t know and don’t trust. And as it turns out, media formats are known to have been used to trick decoders into exposing [nasty security vulnerabilities](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3870) that exploit memory management bugs in Web browsers’ implementation code.

This makes a [memory-safe programming language](https://air.mozilla.org/guaranteeing-memory-safety-in-rust/) like Rust a compelling addition to Mozilla’s tool-chest for protecting against potentially malicious media content on the Web. For this reason, Ralph Giles and Matthew Gregan built Mozilla’s [first Rust media parser](https://github.com/mozilla/mp4parse-rust). And I’m happy to report that their code will be the first Rust component shipping in Firefox. For the Rust community as well, this is a real achievement: **Rust code shipping to hundreds of millions of Firefox users**. Our preliminary measurements show the Rust component performing beautifully and delivering identical results to the original C++ component it’s replacing—but now implemented in a memory-safe programming language.

![Telemetry data for Firefox's first Rust component](../../assets/35ec2833f707b4be.png)


![Telemetry data for Firefox's first Rust component](../../assets/35ec2833f707b4be.png)

## More to come!

Many people deserve huge thanks for getting us to this point. Ralph Giles and Matthew Gregan implemented the component, and Nathan Froyd, Nick Nethercote, Ted Mielczarek, Gregory Szorc, and Alex Crichton have been instrumental in integrating Rust into the Firefox build and tooling system and ensuring it can ship on all of our platforms.

Rust itself is the product of a tremendous, vibrant community. None of this work would have been possible without the incredible contributions of [issues](https://github.com/rust-lang/rust/issues), [design](https://github.com/rust-lang/rfcs), [code](https://github.com/rust-lang/rust), and [so much more](https://www.rust-lang.org/en-US/contribute.html) of Rustaceans worldwide. As a [Rustacean myself](http://calculist.org/blog/2015/12/23/neon-node-rust/), I’d encourage you to come play with Rust. It’s a great time to [get started](https://doc.rust-lang.org/book/getting-started.html), and increasingly, to [get involved with a Mozilla project using Rust](https://wiki.mozilla.org/Oxidation).

Seeing Rust code ship in production at Mozilla feels like the culmination of a long journey. But this is only the first step for Mozilla. Watch this space!

## About
[
Dave Herman ](http://calculist.org)

Dave Herman is a Principal Researcher and Director of Strategy at Mozilla Research.

## 24 comments

Felix SchwarzJuly 12th, 2016 at 07:43Nick AnsteeJuly 12th, 2016 at 12:07Felix SchwarzJuly 13th, 2016 at 00:26Lars BergstromJuly 12th, 2016 at 12:31markJuly 12th, 2016 at 14:45StephanieJuly 13th, 2016 at 11:22Gregory SzorcJuly 12th, 2016 at 16:54DanielJuly 12th, 2016 at 16:58EmilJuly 13th, 2016 at 00:18Russell Irvin JohnstonJuly 12th, 2016 at 10:41Lars BergstromJuly 12th, 2016 at 12:36RohitJuly 13th, 2016 at 03:29Jack MoffittJuly 15th, 2016 at 08:09GabrielaJuly 12th, 2016 at 15:49Lars BergstromJuly 12th, 2016 at 17:12GabrielaJuly 14th, 2016 at 20:18RustyKrabJuly 12th, 2016 at 19:10Walid DamounyJuly 13th, 2016 at 13:49Igor TupiJuly 12th, 2016 at 19:33Foxy RustaceanJuly 13th, 2016 at 09:17Xidorn QuanJuly 14th, 2016 at 07:35Jack MoffittJuly 15th, 2016 at 08:12GabrielaJuly 30th, 2016 at 10:47LonamiAugust 5th, 2016 at 10:47