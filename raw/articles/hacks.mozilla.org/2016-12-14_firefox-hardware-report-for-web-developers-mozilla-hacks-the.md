---
title: Firefox Hardware Report for Web Developers – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/12/firefox-hardware-report/
author: Andre Vrignaud
published: '2016-12-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Suppose you’re developing a sophisticated web game or application, and you’re wondering — will it actually be able to run? What hardware should I be targeting to get the widest possible audience? Existing hardware reports (such as those from [Valve](http://store.steampowered.com/hwsurvey/) and [Unity](http://hwstats.unity3d.com/web/)) are excellent, but represent a different group of hardware users than the majority of people who use the web.

We’ve been working on the [next-generation web game platform](https://blog.mozilla.org/futurereleases/2015/12/07/mozilla-pioneered-asm-js-and-webgl-achieve-milestone-as-the-unity-game-engine-provides-full-support-for-webgl-titles) for years now, and often receive questions from web developers about the hardware market. Today we’re releasing the [Firefox Hardware Report](https://metrics.mozilla.com/firefox-hardware-report) to help answer those questions and inform your development decisions.

On this site you’ll find a variety of data points showing what hardware and OSes Firefox web users are using on the web, and trends over time. This includes CPU vendors, cores, and speeds; system memory; GPU vendors, models, and display resolution; Operating System architecture and market share; browser architecture share, and finally, Flash plugin availability. Some charts (such as the GPU models) have an expanded view showing all of the models captured. You’ll also discover all sorts of interesting stats — like 30% of Firefox users have 4 GB of RAM; that Intel makes 86% of users’ CPUs and 63% of their GPUs; or that the most popular screen resolution (with 33% of users) is 1366×768.

The [Firefox Hardware Report ](https://metrics.mozilla.com/firefox-hardware-report)is a public report of the hardware used by a representative sample of the population from [Firefox’s desktop release channel](https://www.mozilla.org/en-US/firefox/all/). The source data for the Hardware Report was collected through the [Firefox Telemetry system](https://blog.mozilla.org/metrics/fhr-faq/), which automatically collects browser and platform information from machines using Firefox. We use this data to prioritize development efforts and to power this report.

Once data is collected, we aggregate and anonymize it. During the aggregation step, less common screen resolutions and OS versions are handled as special cases — resolutions are rounded to the nearest hundred and version numbers are collapsed together in a generic group. Any reported configurations that account for less than 1% of the data are grouped together in an “Other” bucket. At the end of the process, the aggregated, anonymized data is exported to a JSON file and published on the report website.

To learn more about how we created this report, take a look at our [blog post](https://medium.com/@rweiss/https-medium-com-mozilla-tech-how-its-built-the-firefox-hardware-survey-5a44dc167315#.4ezwc0vu7) on the Mozilla Tech Medium. The code used to generate the reported data and website is [available on GitHub](https://github.com/mozilla/firefox-hardware-survey).

This is just our first step, and we hope to expand this data set over time. In the meanwhile, please let us know what you think — is this data useful? What other data points might be helpful in the future? Do you have visualization suggestions? We look forward to [your email feedback](mailto:firefox-hardware-report-feedback@mozilla.com), with thanks!

## About Andre Vrignaud

Andre Vrignaud is the Head of Platform Strategy for Mozilla’s Mixed Reality Program, where he guides the strategy for Mozilla's efforts to enable an open, sustainable 3D web and ecosystem. With a side of net neutrality and privacy advocacy.

## About Rebecca Weiss

Rebecca is the manager of the Product Data Science team for Firefox. Her team aims to add a dose of empiricism to product strategy and also advance the state of data literacy about the web and beyond.

## 2 comments

MehdyDecember 15th, 2016 at 21:21J. Lester Novros IIDecember 18th, 2016 at 07:28