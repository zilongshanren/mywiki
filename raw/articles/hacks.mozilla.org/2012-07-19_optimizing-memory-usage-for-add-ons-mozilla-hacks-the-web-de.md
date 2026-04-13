---
title: Optimizing Memory Usage for Add-ons – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/07/firefox-15-optimizing-memory/
author: Nicholas Nethercote
published: '2012-07-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** This is a short excerpt from Nicholas Nethercote’s personal blog. Nicholas is a programmer from Melbourne, Australia, who works for Mozilla on improving the quality of software. Here’s the good news in a nutshell:

“Over the past year, Mozilla has made great progress in reducing Firefox’s memory consumption. However, the excessive memory consumption caused by add-ons with memory leaks has remained an ongoing problem.

Firefox 15 fixes that problem. We have confirmed, via in-house testing and from real-world telemetry data, that it prevents the vast majority of leaks that occur in existing add-ons.

Users who upgrade to Firefox 15 won’t have to upgrade their add-ons to see the benefits. While it is hard to predict the effect of this improvement on any individual user, many users should experience greatly reduced memory consumption, particularly on long browsing sessions. This should result in better performance, fewer pauses, and fewer crashes.

Mozilla’s MemShrink efforts are ongoing. We have various projects in the pipeline that aim to further reduce Firefox’s memory consumption, and help users understand better how Firefox is using memory. ”


## 7 comments

Justin LebarJuly 19th, 2012 at 16:24Havi HoffmanJuly 19th, 2012 at 16:30BastianJuly 20th, 2012 at 00:15pdJuly 22nd, 2012 at 07:40RandySeptember 5th, 2012 at 02:05Jean-Yves PerrierSeptember 6th, 2012 at 02:09AttilaSeptember 9th, 2012 at 19:26