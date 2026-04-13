---
title: Safely reviving shared memory – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/07/safely-reviving-shared-memory/
author: Anne van Kesteren
published: '2020-07-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

At Mozilla, we want the web to be capable of running high-performance applications so that users and content authors can choose the safety, agency, and openness of the web platform. One essential low-level building block for many high-performance applications is shared-memory multi-threading. That’s why it was so exciting to [deliver shared memory to JavaScript and WebAssembly](https://hacks.mozilla.org/2016/05/a-taste-of-javascripts-new-parallel-primitives/) in 2016. This provided extremely fast communication between threads.

However, we also want the web to be secure from attackers. Keeping users safe is paramount, which is why shared memory and high-resolution timers were effectively [disabled at the start of 2018](https://blog.mozilla.org/security/2018/01/03/mitigations-landing-new-class-timing-attack/), in light of [Spectre](https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)). Unfortunately, Spectre-attacks are made significantly more effective with high-resolution timers. And such timers can be created with shared memory. (This is accomplished by having one thread increment a shared memory location in a tight loop that another thread can sample as a nanosecond-resolution timer.)

## Back to the drawing board

Fundamentally, for a Spectre attack to work, an attacker and victim need to reside in the same process. Like most applications on your computer, browsers used to use a single process. This would allow two open sites, say `attacker.example`

and `victim.example`

, to Spectre-attack each other’s data as well as other data the browser might keep such as bookmarks or history. Browsers have long since become multi-process. With Chrome’s Site Isolation and Firefox’s [Project Fission](https://wiki.mozilla.org/Project_Fission), browsers will isolate each [site](https://html.spec.whatwg.org/multipage/origin.html#site) into its own process. This is possible due to the web platform’s retrofitted [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy).

Unfortunately, isolating each site into its own process is still not sufficient for these reasons:

- The same-origin policy has a number of holes, two of which strongly informed our thinking during the design process:
`attacker.example`

can fetch arbitrary`victim.example`

resources into`attacker.example`

’s process, e.g., through the`<img>`

element.- Due to the existence of
`document.domain`

, the minimal isolation boundary is a site (roughly the scheme and[registrable domain](https://url.spec.whatwg.org/#host-registrable-domain)of a website’s host) and not an[origin](https://html.spec.whatwg.org/multipage/origin.html#concept-origin)(roughly a website’s scheme, host, and port).

- At this point, we don’t know if it’s feasible to isolate each site into its own process across all platforms. It is still a challenging endeavor on mobile. While possibly not a long-term problem, we would prefer a solution that allows reviving shared memory on mobile
*soon*.

## Distilling requirements

We need to address the issues above to revive shared memory and high-resolution timers. As such, we have been working on a system that meets the following requirements:

- It allows a website to process-isolate itself from attackers and thereby shield itself from intra-process high-resolution timer attacks.
- If a website wants to use these high-performance features, it also needs to process-isolate itself from victims. In particular, this means that it has to give up the ability to fetch arbitrary subresources from any site (e.g., through an
`<img>`

element) because these end up in the same process. Instead, it can only fetch cross-origin resources from consenting origins. - It allows a browser to run the entire website, including all of its frames and popups, in a single process. This is important to keep the web platform a consistent system across devices.
- It allows a browser to run each participating origin (i.e., not site) in its own process. This is the ideal end state across devices and it is important for the design to not prevent this.
- The system maintains backwards compatibility. We cannot ask billions of websites to rewrite their code.

Due to these requirements, the system must provide an opt-in mechanism. We cannot forbid websites from fetching cross-origin subresources, as this would not be backwards compatible. Sadly, restricting `document.domain`

is not backwards compatible either. More importantly, it would be unsafe to allow a website to embed cross-origin documents via an `<iframe>`

element and have those cross-origin resources end up in the same process without opting in.

## Cross-origin isolated

### New headers

Together with others in the WHATWG community, we [designed a set of headers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer/Planned_changes) that meet these requirements.

The [ Cross-Origin-Opener-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy) header allows you to process-isolate yourself from attackers. It also has the desirable effect that attackers cannot have access to your global object if they were to open you in a popup. This prevents

[XS-Leaks](https://github.com/xsleaks/xsleaks)and various navigation attacks. Adopt this header even if you have no intention of using shared memory!

The [ Cross-Origin-Embedder-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy) header with value

`require-corp`

tells the browser to only allow this document to fetch cross-origin subresources from consenting websites. Technically, the way that this works is that those cross-origin resources need to specify the [header with value](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy)

`Cross-Origin-Resource-Policy`

`cross-origin`

to indicate consent.### Impact on documents

If the `Cross-Origin-Opener Policy`

and `Cross-Origin-Embedder-Policy`

headers are set for a top-level document with the `same-origin`

and `require-corp`

values respectively, then:

- That document will be cross-origin isolated.
- Any descendant documents that also set
`Cross-Origin-Embedder-Policy`

to`require-corp`

will be cross-origin isolated. (Not setting it results in a network error.) - Any popups these documents open will either be cross-origin isolated or will not have a direct relationship with these documents. This is to say that there is no direct access through
`window.opener`

or equivalent (i.e., it’s as if they were created using`rel="noopener"`

).

A document that is cross-origin isolated will have access to shared memory, both in JavaScript and WebAssembly. It will only be able to share memory with same-origin documents and dedicated workers in the same “tab” and its popups (technically, same-origin agents in a single [browsing context group](https://html.spec.whatwg.org/multipage/browsers.html#browsing-context-group)). It will also have access to the highest-resolution `performance.now()`

available. Evidently, it will not have access to a functional `document.domain`

.

The way these headers ensure mutual consent between origins gives browsers the freedom to put an entire website into a single process or put each of the origins into their own process, or something in between. While process-per-origin would be ideal, this is not always feasible on all devices. So having everything that is pulled into these one-or-more processes consent is a decent middle ground.

## Safety backstop

We created a safety backstop to be able to deal with novel cross-process attacks. And used an approach that avoids having to disable shared memory entirely to remain web compatible.

The result is Firefox’s [ JSExecutionManager](https://searchfox.org/mozilla-central/source/dom/workers/JSExecutionManager.h). This allows us to regulate the execution of different JavaScript contexts with relation to each other. The

`JSExecutionManager`

can be used to throttle CPU and power usage by background tabs. Using the `JSExecutionManager`

, we created a dynamic switch (`dom.workers.serialized-sab-access`

in `about:config`

) that prevents all JavaScript threads that share memory from ever running code concurrently, effectively executing these threads as if on a single-core machine. Because creating a high-resolution timer using shared memory requires two threads to run simultaneously, this switch effectively prevents the creation of a high-resolution timer without breaking websites.By default, this switch is off, but in the case of a novel cross-process attack, we could quickly flip it on. With this switch as a backstop, we can feel confident enabling shared memory in cross-origin isolated websites even when considering unlikely future worst-case scenarios.

## Acknowledgments

Many thanks to Bas Schouten and Luke Wagner for their contributions to this post. And also, in no particular order, many thanks to Nika Layzell, Tom Tung, Valentin Gosu, Eden Chuang, Jens Manuel Stutte, Luke Wagner, Bas Schouten, Neha Kochar, Andrew Sutherland, Andrew Overholt, 蔡欣宜 (Hsin-Yi Tsai), Perry Jiang, Steve Fink, Mike Conca, Lars Thomas Hansen, Jeff Walden, Junior Hsu, Selena Deckelmann, and Eric Rescorla for their help getting this done in Firefox!

## About
[
Anne van Kesteren ](https://annevankesteren.nl/)

Standards person with an interest in privacy & security boundaries, as well as web platform architecture · he/him

## 5 comments

blitmapJuly 21st, 2020 at 16:24Anne van KesterenJuly 22nd, 2020 at 01:26AnonymousJuly 22nd, 2020 at 02:25Anne van KesterenJuly 22nd, 2020 at 04:49FlimmJuly 22nd, 2020 at 04:20