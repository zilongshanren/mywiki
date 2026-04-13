---
title: Improving Firefox stability with this one weird trick – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2022/11/improving-firefox-stability-with-this-one-weird-trick/
author: Gabriele Svelto
published: '2022-11-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The first computer I owned shipped with 128 KiB of RAM and to this day I’m still jarred by the idea that applications can run out of memory given that even 15-year-old machines often shipped with 4 GiB of memory. And yet it’s one of the most common causes of instability experienced by users and in the case of Firefox the biggest source of crashes on Windows.

As such, at Mozilla, we spend significant resources [trimming down Firefox memory consumption](https://bugzilla.mozilla.org/buglist.cgi?list_id=16239893&query_format=advanced&v1=MemShrink&classification=Client%20Software&classification=Developer%20Infrastructure&classification=Components&classification=Server%20Software&classification=Other&resolution=---&o1=substring&f1=status_whiteboard) and [carefully monitoring the changes](https://treeherder.mozilla.org/perfherder/alerts?hideDwnToInv=1&page=1&framework=4&status=-1). Some extra efforts have been spent on the Windows platform because Firefox was more likely to run out of memory there than on macOS or Linux. And yet none of those efforts had the impact of a cool trick we deployed in Firefox 105.

But first things first, to understand why applications running on Windows are more prone to running out of memory compared to other operating systems it’s important to understand how Windows handles memory.

All modern operating systems allow applications to allocate chunks of the address space. Initially these chunks only represent address ranges that aren’t backed by physical memory unless data is stored in them. When an application starts using a bit of address space it has reserved, the OS will dedicate a chunk of physical memory to back it, possibly swapping out some existing data if need be. Both Linux and macOS work this way, and so does Windows except that it requires an extra step compared to the other OSes.

After an application has requested a chunk of address space it needs to commit it before being able to use it. Committing a range requires Windows to guarantee it can always find some physical memory to back it. Afterwards, it behaves just like Linux and macOS. As such Windows limits how much memory can be committed to the sum of the machine’s physical memory plus the size of the swap file.

This resource – known as commit space – is a hard limit for applications. Memory allocations will start to fail once the limit is reached. In operating system speech this means that Windows does not allow applications to overcommit memory.

One interesting aspect of this system is that an application can commit memory that it won’t use. The committed amount will still count against the limit even if no data is stored in the corresponding areas and thus no physical memory has been used to back the committed region. When we started analyzing out of memory crashes we discovered that many users still had plenty of physical memory available – sometimes gigabytes of it – but were running out of commit space instead.

Why was that happening? We don’t really know but we made some educated guesses: Firefox tracks all the memory it uses and we could account for all the memory that we committed directly.

However, we have no control over Windows system libraries and in particular graphics drivers. One thing we noticed is that graphics drivers commit memory to make room for textures in system memory. This allows them to swap textures out of the GPU memory if there isn’t enough and keep them in system memory instead. A mechanism that is similar to how regular memory can be swapped out to disk when there is not enough RAM available. In practice, this rarely happens, but these areas still count against the limit.

We had no way of fixing this issue directly but we still had an ace up our sleeve: when an application runs out of memory on Windows it’s not outright killed by the OS, its allocation simply fails and it can then decide what it does by itself.

In some cases, Firefox could handle the failed allocation, but in most cases, there is no sensible or safe way to handle the error and it would need to crash in a controlled way… but what if we could recover from this situation instead? Windows automatically resizes the swap file when it’s almost full, increasing the amount of commit space available. Could we use this to our advantage?

It turns out that the answer is yes, we can. So we adjusted Firefox [to wait for a bit instead of crashing](https://bugzilla.mozilla.org/show_bug.cgi?id=1716727) and then retry the failed memory allocation. This leads to a bit of jank as the browser can be stuck for a fraction of a second, but it’s a lot better than crashing.

There’s also another angle to this: Firefox is made up of several processes and can survive losing all of them but the main one. Delaying a main process crash might lead to another process dying if memory is tight. This is good because it would free up memory and let us resume execution, for example by getting rid of a web page with [runaway memory consumption](https://nolanlawson.com/2021/12/17/introducing-fuite-a-tool-for-finding-memory-leaks-in-web-apps/).

If a content process died we would need to reload it if it was the GPU process instead the browser would briefly flash while we relaunched it; either way, the result is less disruptive than a full browser crash. We used a similar trick in Firefox for Android and Firefox OS before that and it worked well on both platforms.

This little trick shipped in Firefox 105 and had an enormous impact on Firefox stability on Windows. The chart below shows how many out-of-memory browser crashes were experienced by users per active usage hours:

![Firefox trick](../../assets/22c238a6800546ee.png)


You’re looking at a >70% reduction in crashes, far more than our rosiest predictions.

And we’re not done yet! Stalling the main process led to a smaller increase in tab crashes – which are also unpleasant for the user even if not nearly as annoying as a full browser crash – so [we’re cutting those down too](https://bugzilla.mozilla.org/show_bug.cgi?id=1785162).

Last but not least we want to improve Firefox behavior in low-memory scenarios by responding differently to cases where [we’re low on commit space and cases where we’re low on physical memory](https://bugzilla.mozilla.org/show_bug.cgi?id=1782178), this will reduce swapping and help shrink Firefox footprint to make room for other applications.

I’d like to send special thanks to my colleague Raymond Kraesig who implemented this “trick”, carefully monitored its impact and is working on the aforementioned improvements.

## 8 comments

Shawn McNaughtonNovember 22nd, 2022 at 07:34JB DoughertyNovember 22nd, 2022 at 10:47peterNovember 22nd, 2022 at 11:05SoraWithAnSNovember 22nd, 2022 at 15:31DonnyNovember 27th, 2022 at 12:43Miguel UsecheNovember 27th, 2022 at 18:57rvNovember 30th, 2022 at 20:26Gowri SankarDecember 2nd, 2022 at 12:50