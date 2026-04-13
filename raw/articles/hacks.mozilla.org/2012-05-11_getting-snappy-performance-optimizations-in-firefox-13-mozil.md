---
title: Getting snappy – performance optimizations in Firefox 13 – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2012/05/getting-snappy-performance-optimisations-in-firefox-13/
author: Lawrence Mandel
published: '2012-05-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Back in the fall of 2011, we took a targeted look at Firefox responsiveness issues. We identified a number of short term projects that together could achieve significant responsiveness improvements in day-to-day Firefox usage. Project Snappy kicked off at the end of the year with the goal of improving Firefox responsiveness.

Although Snappy first contributed fixes to Firefox 11, Snappy’s most noticeable contributions to date are landing with Firefox 13. [Currently in beta](http://www.mozilla.org/beta), this release includes a number of responsiveness related fixes, most notably tabs-on-demand, cycle collector improvements, and start-up optimization.

## Tabs -on-Demand

Tabs-on-demand is a feature that reduces start-up time for Firefox windows with many tabs. In Firefox 12, all tabs are loaded on start-up. For windows with many tabs this may cause a delay before you can interact with Firefox as each tab must load its content. In Firefox 13, only the active tab will load. Loading of background tabs is deferred until a tab is selected. This results in Firefox starting faster as tabs-on-demand reduces processing requirements, network usage, and memory consumption.

## Cycle Collector

As you interact with the browser and Web content, memory is allocated as needed. The Firefox cycle collector works to automatically free some of this memory when it is no longer needed. This action reduces Firefox’s memory usage. In Firefox 13, the cycle collector is more efficient, spending less time examining memory that is still in use, which results in less pauses as you use Firefox.

## Start-up

Firefox start-up time is visible to all users. Our investigation into start-up has identified a number of unoptimized routines in the code that executes before what we call “first paint”. “First paint” signifies when the Firefox user interface is first visible on your screen. In Firefox 13 we have optimized file calls, audio sessions, drag and drop, and overall IO, just to name a few. We are continuing to profile the Firefox start-up sequence to identify further optimizations that can be made in future releases.

There are numerous other Snappy fixes in Firefox 13 including significant improvements to IO contention, font enumeration, and livemark overhead. All of these fixes contribute to a more responsive experience. We are already working on further responsiveness fixes for future Firefox releases. You can expect to see Snappy improvements in upcoming releases in areas such as memory usage, shutdown time, network cache and connections, menus, and graphics.

## About
[
Lawrence Mandel ](http://lawrencemandel.com/)

Firefox Engineering Program Manager

## 61 comments

AndyMay 11th, 2012 at 03:49Abhay RanaMay 11th, 2012 at 07:06AlecMay 11th, 2012 at 04:51HansMay 28th, 2012 at 10:38smaugMay 11th, 2012 at 06:35pdMay 11th, 2012 at 07:54Lawrence MandelMay 11th, 2012 at 08:43Mysterious AndyMay 15th, 2012 at 09:29Steve PriceMay 11th, 2012 at 08:15kwiersoMay 11th, 2012 at 18:38Mike BMay 11th, 2012 at 08:32Mike BMay 11th, 2012 at 08:38Lawrence MandelMay 11th, 2012 at 08:51Mike BMay 11th, 2012 at 14:35Mike BMay 11th, 2012 at 19:57RamiMay 11th, 2012 at 08:46WayneMay 11th, 2012 at 12:37cuz84dMay 11th, 2012 at 13:07cuz84dMay 11th, 2012 at 13:15SuggestionMay 11th, 2012 at 13:08AlexJune 5th, 2012 at 15:12HogartMay 11th, 2012 at 13:43taylerzMay 12th, 2012 at 06:01ErunnoMay 12th, 2012 at 11:25ToddMay 12th, 2012 at 07:14AhmadMay 12th, 2012 at 11:16Jean-Yves PerrierMay 13th, 2012 at 00:28SandroMay 12th, 2012 at 07:25eddieMay 12th, 2012 at 14:23FerdinandMay 14th, 2012 at 22:14alexleducMay 28th, 2012 at 07:58EnriqueMay 13th, 2012 at 02:28Christopher ThomasMay 13th, 2012 at 08:33Ken VermetteMay 13th, 2012 at 10:59sulfideMay 13th, 2012 at 11:47WesMay 13th, 2012 at 15:24edmMay 24th, 2012 at 14:59John MeherMay 13th, 2012 at 23:21benjamirMay 14th, 2012 at 00:55Lawrence MandelMay 14th, 2012 at 09:14JosephMay 14th, 2012 at 10:52Walid DamounyMay 14th, 2012 at 09:31DineshMay 14th, 2012 at 23:10brightsmithMay 15th, 2012 at 13:37alexleducMay 28th, 2012 at 10:04Narcélio FilhoMay 16th, 2012 at 11:48FerdinandJune 5th, 2012 at 15:16BrightsmithMay 16th, 2012 at 17:29Walid DamounyMay 17th, 2012 at 00:01leeoniyaMay 17th, 2012 at 09:22JKJune 6th, 2012 at 13:04Lawrence MandelJune 6th, 2012 at 14:01FerdinandJune 6th, 2012 at 22:55JasjotJune 7th, 2012 at 00:13ShankarJune 14th, 2012 at 23:32ShankarJuly 3rd, 2012 at 01:04samarendraJune 29th, 2012 at 03:57BillJuly 18th, 2012 at 10:45WesJuly 18th, 2012 at 12:49EnriqueAugust 5th, 2012 at 07:16MarkSeptember 16th, 2012 at 19:25