---
title: Firefox’s New Memory Tool – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/11/firefoxs-new-memory-tool/
author: Dan Callahan
published: '2015-11-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox Developer Edition 44, [released last week](https://hacks.mozilla.org/2015/11/developer-edition-44-creative-tools-and-more/), includes a brand new [memory tool](https://developer.mozilla.org/docs/Tools/Memory) to help you understand how your web applications are using and retaining memory. This is especially useful for developers targeting the mobile web, and thus working with constrained resources. [Baptiste Kaenel](https://linkedin.com/in/baptiste-kaenel-aba56798), a freelance Creative Designer and Mozilla community member from France, put together a fantastic video demonstrating how to use this powerful new tool.

The Memory tool works by taking snapshots of everything in memory, and presenting them as a tree/table with various grouping settings. By default, the contents are grouped by “**coarse type**,” where each thing in memory falls into one of four classifications:

**Objects**: JavaScript objects. Further grouped by each object’s internal [[Class]] name.**Scripts**: The JavaScript source text loaded by the web application and its resulting executable machine code produced by SpiderMonkey’s JIT compiler, IonMonkey.**Strings**: JavaScript strings used by the web application.**Other**: Miscellaneous structures that do not fit in the above categories.

You can also group the snapshot by “**object class**,” which groups by their JavaScript [[Object]] class, or by “**internal type**,” which groups things by their C++ type names. This latter view is mostly useful for Firefox platform developers.

Perhaps most interesting is the fourth and final grouping option: “**allocation stack**.” You have to turn this option on manually by ticking the “record allocation stacks” checkbox at the top of the Memory panel, since tracking allocations can degrade the application’s performance while the box is checked. The payoff, however, is worth it: this view groups the things in the heap by the source location in your JavaScript code. Unlike other groupings, this view directly ties items in memory back to the code that actually created them.

The list of snapshots also includes the total MB of memory accounted for in the snapshot. You can take several snapshots to help determine at a glance whether your application’s memory usage is growing or shrinking over time.

To learn more, check out the [Memory tool documentation](https://developer.mozilla.org/docs/Tools/Memory) on MDN, and remember, we want to hear from you! Download [Firefox Developer Edition](https://firefox.com/developer) today, and let us know what tools or enhancements you want to see next by leaving a comment or tweeting at [@FirefoxDevTools](https://twitter.com/FirefoxDevTools).

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## About
[
Nick Fitzgerald ](http://fitzgeraldnick.com)

I like computing, bicycles, hiphop, books, and pen plotters. My pronouns are he/him.

## 4 comments

ValentinNovember 13th, 2015 at 07:46Dan CallahanNovember 13th, 2015 at 08:29Francis KimNovember 16th, 2015 at 18:09RachaticiNovember 24th, 2015 at 07:24