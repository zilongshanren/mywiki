---
title: 'Firefox 7: Telemetry – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2011/09/firefox-7-telemetry/
author: Mozilla Hacks
published: '2011-09-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Based on a blog post originally posted here by Taras Glek, Firefox Developer. *

Firefox 7 marks a turning point in how we measure Firefox performance. Traditionally we measured Firefox performance on individual developer machines and our build & release infrastructure. However it turns out synthetic benchmarks do not correspond to real-world Firefox usage: it is difficult to model a “typical” computer in a lab environment. Surprisingly slow consumer hardware, changes in usage patterns, preinstalled bloatware all affect Firefox performance in surprising ways.

Firefox 7 telemetry will prompt users to opt-in to reporting performance data to Mozilla. This data will supplement our existing benchmarking infrastructure to help us optimize future Firefox releases. Telemetry performance metrics are very lightweight and will not negatively impact Firefox performance.

In addition to transmitting data via SSL, [Mozilla privacy team](http://blog.mozilla.com/privacy/2011/09/27/building-privacy-into-telemetry/ ) worked tirelessly to ensure that no personally-identifiable information is sent via telemetry. Whereas many other software projects stamp this kind of data with a unique per-user id, we opted for a per-session id which is reset every time the browser restarts. Telemetry is also disabled while in private-browsing mode.

The following telemetry data will be gathered in Firefox 7:

Memory usage

CPU core count

Cycle collection times

Startup speed

Use the about:telemetry extension to check on your browser performance. The following screenshot shows how to enable telemetry:

![1](http://people.mozilla.com/~tglek/telemetry/telemetry-ff7.jpg)


I’m very excited that Firefox finally joins the ranks of cars, airplanes and other software projects in making performance decisions based on real evidence gathered in the wild.

## 7 comments

Stephan SokolowSeptember 27th, 2011 at 07:59Eric PerretSeptember 27th, 2011 at 17:07Fernando TakaiSeptember 27th, 2011 at 19:05Stephan SokolowSeptember 28th, 2011 at 04:12Joseph RedickOctober 3rd, 2011 at 20:42Web Design PhoenixNovember 18th, 2011 at 04:30Web Design New YorkNovember 23rd, 2011 at 02:28