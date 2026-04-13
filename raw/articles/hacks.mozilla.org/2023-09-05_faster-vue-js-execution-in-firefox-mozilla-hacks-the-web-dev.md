---
title: Faster Vue.js Execution in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2023/09/faster-vue-js-execution-in-firefox/
author: Brian Grinstead
published: '2023-09-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Speedometer 3](https://twitter.com/mozhacks/status/1603435347190419456) is a cross-industry effort to build a modern browser benchmark rooted in real-world user experiences. Its goal is to focus browser engineering effort towards making the Web more smooth for actual users on actual pages. This is hard to do and most browser benchmarks don’t do it well, but we see it as a unique opportunity to improve responsiveness broadly across the Web.

This requires a deliberate analysis of the ecosystem — starting with real user experiences and identifying the essential technical elements underlying them. We built several new tests from scratch, and also updated some existing tests from Speedometer 2 to use more modern versions of widely-used JavaScript frameworks.

When the Vue.js test was updated from Vue 2 to Vue 3, we [noticed](https://github.com/WebKit/Speedometer/pull/114#issuecomment-1479368671) some performance issues in Firefox. The root of the problem was [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) object usage that [was introduced in Vue 3](https://vuejs.org/guide/extras/reactivity-in-depth.html#how-reactivity-works-in-vue).

Proxies are hard to optimize because they’re generic by design and can behave in all sorts of surprising ways (e.g., modifying trap functions after initialization, or wrapping a Proxy with another Proxy). They also weren’t used much on the performance-critical path when they were introduced, so we focused primarily on correctness in the original implementation.

Speedometer 3 developed evidence that some Proxies today are well-behaved, critical-path, and widely-used. So we [optimized these](https://bugzilla.mozilla.org/show_bug.cgi?id=1824051) to execute completely in the JIT — specializing for the shapes of the Proxies encountered at the call-site and avoiding redundant work. This makes reactivity in Vue.js significantly faster, and we also anticipate improvements on other workloads.

This change landed in Firefox 118, so it’s currently on Beta and will ride along to Release by the end of September.

Over the course of the year Firefox has improved [by around 40%](https://bugzilla.mozilla.org/show_bug.cgi?id=1824051#c25) on the Vue.js benchmark from work like this. More importantly, and as we hoped, we’re observing real user metric improvements across all page loads in Firefox as we optimize Speedometer 3. We’ll share more details about this in a subsequent post.