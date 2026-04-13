---
title: A cartoon intro to WebAssembly – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/02/a-cartoon-intro-to-webassembly/
author: Lin Clark
published: '2017-02-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebAssembly is fast. You’ve probably heard this. But what is it that makes WebAssembly fast?

In this series, I want to explain to you why WebAssembly is fast.

## Wait, so what is WebAssembly?

[WebAssembly](https://research.mozilla.org/webassembly/) is a way of taking code written in programming languages other than JavaScript and running that code in the browser. So when people say that WebAssembly is fast, what they are comparing it to is JavaScript.

Now, I don’t want to imply that it’s an either/or situation — that you’re either using WebAssembly or using JavaScript. In fact, we expect that developers will use both WebAssembly and JavaScript in the same application.

But it is useful to compare the two, so you can understand the potential impact that WebAssembly will have.

## A little performance history

JavaScript was created in 1995. It wasn’t designed to be fast, and for the first decade, it wasn’t fast.

Then the browsers started getting more competitive.

In 2008, a period that people call the performance wars began. Multiple browsers added just-in-time compilers, also called JITs. As JavaScript was running, the JIT could see patterns and make the code run faster based on those patterns.

The introduction of these JITs led to an inflection point in the performance of JavaScript. Execution of JS was 10x faster.

With this improved performance, JavaScript started being used for things no one ever expected it to be used for, like server-side programming with Node.js. The performance improvement made it feasible to use JavaScript on a whole new class of problems.

We may be at another one of those inflection points now, with WebAssembly.

So, let’s dive into the details to understand what makes WebAssembly fast.

*Background:*

*WebAssembly, the present:*

*WebAssembly, the future:*

## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.

## 22 comments

Andrew WooldridgeFebruary 28th, 2017 at 20:43MartinMarch 2nd, 2017 at 02:29Lin ClarkMarch 2nd, 2017 at 07:07newtonMarch 2nd, 2017 at 08:56MichaelaMarch 2nd, 2017 at 10:19Lin ClarkMarch 2nd, 2017 at 10:41erdeesMarch 2nd, 2017 at 11:00FRANK CARDENASMarch 2nd, 2017 at 17:06ducnguyen.infoMarch 2nd, 2017 at 17:13Abdul Rahman Bin BujangMarch 3rd, 2017 at 00:21Estelle BonillaMarch 3rd, 2017 at 10:03songwonMarch 3rd, 2017 at 20:460918nobitaMarch 4th, 2017 at 01:47Lin ClarkMarch 4th, 2017 at 06:560918nobitaMarch 5th, 2017 at 03:09Lin ClarkMarch 5th, 2017 at 08:15Eric DingMarch 7th, 2017 at 21:17ClemMarch 20th, 2017 at 04:46DavidMarch 21st, 2017 at 11:02Lin ClarkMarch 22nd, 2017 at 10:55DavidMarch 22nd, 2017 at 11:49Mohammad ElbannaMarch 25th, 2017 at 14:19