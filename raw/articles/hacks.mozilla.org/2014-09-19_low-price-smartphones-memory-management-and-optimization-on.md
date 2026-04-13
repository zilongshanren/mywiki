---
title: Low price smartphones – memory management and optimization on Firefox OS –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/09/low-price-smartphones-memory-management-and-optimization-on-firefox-os/
author: Mozilla
published: '2014-09-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We know how to generate memory a footprint to debug memory leaks and to prevent abusing memory resources. Now, we would like to introduce the memory management and optimizations under the limited memory resources on [Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS).

## How to get more memory on Firefox OS?

There are three types of events which can get more memory when there is not enough memory on Firefox OS:

- Low memory killer (LMK)
- Memory pressure event
- Out of memory (OOM)

### Low memory killer (LMK)

LMK is a policy to obtain memory resources by killing processes in Android; we integrate it into Firefox OS. When cache size or available memory is lower than a specified threshold, the system will trigger LMK to kill the process with `oom_adj`

higher than 0 and to get some memory resources.

The thresholds are defined in `b2g/app/b2g.js`

. Let’s take the following table as an example:

- When cache size and available memory are both lower than 20MB, the process with
`oom_adj`

as 10 (BACKGROUND) will be killed by LMK - When cache size and available memory are both lower than 8MB, the process with
`oom_adj`

as 8 (BACKGROUND_HOMESCREEN) will be killed by LMK - When cache size and available memory are both lower than 4MB, the process, named b2g with oom_adj as 0 (MASTER) will be killed by LMK

By the way, LMK kills processes one-by-one, so we can be sure that memory leakage happens once b2g was killed by LMK.

```
// The kernel can only accept 6 (OomScoreAdjust, KillUnderKB) pairs. But it is
// okay, kernel will still kill processes with larger OomScoreAdjust first even
// its OomScoreAdjust don't have a corresponding KillUnderKB.
pref("hal.processPriorityManager.gonk.MASTER.OomScoreAdjust", 0);
pref("hal.processPriorityManager.gonk.MASTER.KillUnderKB", 4096);
pref("hal.processPriorityManager.gonk.MASTER.Nice", 0);
pref("hal.processPriorityManager.gonk.PREALLOC.OomScoreAdjust", 67);
pref("hal.processPriorityManager.gonk.PREALLOC.Nice", 18);
pref("hal.processPriorityManager.gonk.FOREGROUND_HIGH.OomScoreAdjust", 67);
pref("hal.processPriorityManager.gonk.FOREGROUND_HIGH.KillUnderKB", 5120);
pref("hal.processPriorityManager.gonk.FOREGROUND_HIGH.Nice", 0);
pref("hal.processPriorityManager.gonk.FOREGROUND.OomScoreAdjust", 134);
pref("hal.processPriorityManager.gonk.FOREGROUND.KillUnderKB", 6144);
pref("hal.processPriorityManager.gonk.FOREGROUND.Nice", 1);
pref("hal.processPriorityManager.gonk.FOREGROUND_KEYBOARD.OomScoreAdjust", 200);
pref("hal.processPriorityManager.gonk.FOREGROUND_KEYBOARD.Nice", 1);
pref("hal.processPriorityManager.gonk.BACKGROUND_PERCEIVABLE.OomScoreAdjust", 400);
pref("hal.processPriorityManager.gonk.BACKGROUND_PERCEIVABLE.KillUnderKB", 7168);
pref("hal.processPriorityManager.gonk.BACKGROUND_PERCEIVABLE.Nice", 7);
pref("hal.processPriorityManager.gonk.BACKGROUND_HOMESCREEN.OomScoreAdjust", 534);
pref("hal.processPriorityManager.gonk.BACKGROUND_HOMESCREEN.KillUnderKB", 8192);
pref("hal.processPriorityManager.gonk.BACKGROUND_HOMESCREEN.Nice", 18);
pref("hal.processPriorityManager.gonk.BACKGROUND.OomScoreAdjust", 667);
pref("hal.processPriorityManager.gonk.BACKGROUND.KillUnderKB", 20480);
pref("hal.processPriorityManager.gonk.BACKGROUND.Nice", 18);
```

### Memory pressure event

When the memory pressure event was triggered, the services that are registered as memory pressure event observers will execute corresponding actions, such as eliminating or minimizing cache (temporary data of b2g). The threshold of the memory pressure event is configured in `b2g/app/b2g.js`

, and the default value (`notifyLowMemUnderKB`

) is 14MB.

```
// Fire a memory pressure event when the system has less than Xmb of memory
// remaining. You should probably set this just above Y.KillUnderKB for
// the highest priority class Y that you want to make an effort to keep alive.
// (For example, we want BACKGROUND_PERCEIVABLE to stay alive.) If you set
// this too high, then we'll send out a memory pressure event every Z seconds
// (see below), even while we have processes that we would happily kill in
// order to free up memory.
pref("hal.processPriorityManager.gonk.notifyLowMemUnderKB", 14336);
```

### Out of memory (OOM)

The Linux kernel provides the OOM policy. When available memory is lower than a specified threshold, OOM will decide which process to kill through the score which is calculated by memory usage and `oom_score_adj`

. The whole operation will obtain more memory resources to satisfy the demands of system. The default threshold (`min_free_kbytes`

) of free memory to trigger OOM is 1352KB.

## How to make these three memory policies work smoothly and reach excellent performance on Firefox OS?

Let me introduce some possible problems first. What will happen if there were conflicts among these three policies?

**Problem 1**. The system will be sluggish if LMK thresholds are lower than the expected ones. With the lower threshold, the system cannot kill any process to get more memory when the memory is not enough. Then the performance will be influenced due to triggered[kswapd](http://www.science.unitn.it/~fiorella/guidelinux/tlk/node39.html)and heavily consumed CPU. If the thresholds are higher than what’s expected, users will feel inconvenient because applications could be killed easily.**Problem 2**. The activities of eliminating and minimizing cache will be too aggressive if the threshold of the memory pressure event is high. When memory is enough, the relevant activities will waste CPU resources and will make performance poor. If the threshold is low, the system cannot be able to release memory on time.**Problem 3**. It will cause crashes or fatal errors when OOM is triggered earlier than LMK is. B2g or other system applications will be killed before background/foreground applications if OOM has been triggered first. When memory is not enough, the system should kill background/foreground applications rather than b2g or system applications.

For the problems mentioned, we need a set of parameters to fix them:

- To experience good performance, we allow to kill background for more memory, and it will make foreground applications operate smoothly. So we increase the value of
`BACKGROUND_HOMESCREEN.KillUnderKB`

and`BACKGROUND.KillUnderKB`

to kill homescreen and background easily. - We should trigger the memory pressure event before killing perceivable background applications. That is to say, it’s better to set the value of
`notifyLowMemUnderKB`

between the ones of`BACKGROUND_HOMESCREEN.KillUnderKB`

and`BACKGROUND_PERCEIVABLE.KillUnderKB`

. - To solve problem 3, LMK must start working before OOM, which means the value of
`min_free_kbytes`

should be lower than the one of`MASTER.KillUnderKB`

.

Let’s take the [Tarako](https://developer.mozilla.org/en-US/Firefox_OS/Developer_phone_guide/Phone_specs) (sc6821, 128MB memory device) as an example. The memory settings which were dumped by adb shell b2g-info are:

```
Low-memory killer parameters:
notify_trigger 14336 KB
oom_adj min_free
0 4096 KB
1 5120 KB
2 6144 KB
6 7168 KB
8 16384 KB
10 18432 KB
```

## Tips for quick memory adjustment

Firefox OS also provides an efficient way to verify your modified memory settings except modifying parameters in `b2g/app/b2g.js`

. Developers can add his/her own modified settings by modifying `/system/b2g/defaults/pref/dev-pref.js`

on the device. The parameters in this file will overwrite the default value in `b2g/app/b2g.js`

.

Still, there are quite a few ways of optimizing memory for low price smartphones. We have more detailed technique discussions on [bugzilla](https://bugzilla.mozilla.org/show_bug.cgi?id=929945). Let’s join Firefox OS development and rock the world!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

jbruggemSeptember 22nd, 2014 at 01:57LukeSeptember 22nd, 2014 at 19:50