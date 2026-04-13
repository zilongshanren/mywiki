---
title: Retained Display Lists for improved page performance – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2018/06/retained-display-lists/
author: Matt Woodrow
published: '2018-06-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Continuing Firefox Quantum’s investment in a high-performance engine, the [Firefox 61 release](https://developer.mozilla.org/en-US/Firefox/Releases/61) will boost responsiveness of modern interfaces with an optimization that we call *Retained Display Lists*. Similar to Quantum’s [Stylo](https://hacks.mozilla.org/2017/08/inside-a-super-fast-css-engine-quantum-css-aka-stylo/) and [WebRender](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/) features, developers don’t need to change anything on their sites to reap the benefits of these improvements.

I wrote about [this feature](https://mozillagfx.wordpress.com/2018/01/09/retained-display-lists/) on the Mozilla Graphics Team blog back in January, when it was first implemented in [Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly). Now it’s ready to ship with Firefox 61. If you’re already familiar with retained display lists and how this feature optimizes painting performance, you might want to skip ahead to read about the results of our efforts and the future work we’re planning.

## Working with the display list

Display list building is the process in which we collect the set of high-level items to display on screen (borders, backgrounds, text and much more), and then sort the list according to CSS painting rules into the correct back-to-front order. It’s at this point that we figure out which parts of the page are already visible on screen.

Currently, whenever we want to update what’s on the screen, we build a full new display list from scratch and then we use it to paint everything on the screen. This is great for simplicity: we don’t have to worry about figuring out which bits changed or went away. Unfortunately, the process can take a really long time. This has always been a performance problem, but as websites have become more complex and more users have access to higher resolution monitors, the problem has been magnified.

The solution is to retain the display list between paints—we build a new display list *only for the parts of the page that changed since we last painted* and then merge the new list into the old to get an updated list. This adds a lot more complexity, since we need to figure out which items to remove from the old list, and where to insert new items. The upside is that, in many cases, the new list can be significantly smaller than the full list. This creates the opportunity to improve perceived performance and save significant amounts of time.

## Motivation

As part of the lead up to the release of Firefox Quantum, we added new [telemetry to Firefox](https://wiki.mozilla.org/Telemetry) to help us measure painting performance, which therefore enabled us to make more informed decisions as to where to direct our efforts. One of these measurements defined a minimum threshold for a ‘slow’ paint (16ms), and recorded percentages of time spent in various paint stages when it occurred. We expected display list building to be significant, but were still surprised with the results: On average, display list building was consuming more than 40% of the total paint time, for work that was often almost identical to the previous frame. We’d long been planning to overhaul how we built and managed display lists, but with this new data we decided to make it a top priority for our Painting team.

## Results

Once we had everything working, the next step was to see how much of an effect we’d made on performance! We had the feature enabled for the first half of the Beta 60 cycle, and compared the results with and without it enabled.

The first and most significant change: The median amount of time spent painting (the full pipeline, not just display list building) dropped by more than 33%!

As you can see in the graph, the median time spent painting is around 3ms when retained display lists are enabled. Once the feature was disabled on April 18th, the paint time jumped up to 4.5ms. That frees up lots of extra time for the browser to spend on running JavaScript, doing layout, and responding to input events.

Another important improvement is in the frequency at which slow paints occurred. With retained display lists disabled, we miss the 16ms deadline around 7.8% of the time. With it enabled, this drops to 4.7%, an almost 40% reduction in frequency. We can see that we’re not just making fast paints faster, but we’re also having a significant impact on the slow cases.

## Future work

As mentioned above, we aren’t always able to retain the display list. We’ve spent time working out which parts of the page have changed; when our analysis shows that most of the page has changed, then we still have to rebuild the full display list and time spent on the analysis is time wasted. Work is ongoing to try detect this as early as possible, but it’s unlikely that we’ll be able to entirely prevent it. We’re also actively working to minimize how long the preparation work takes, so that we can make the most of opportunities for a partial update.

Retaining the display list also doesn’t help for the first time we paint a webpage when it loads. The first paint always has to build the full list from scratch, so in the future we’ll be looking at ways to make that faster across the board.

Thanks to everyone who has helped make this possible, including: Miko Mynttinen, Jet Villegas, Timothy Nikkel, Markus Stange, David Anderson, Ethan Lin, and Jonathan Watt.

## About
[
Matt Woodrow ](https://www.linkedin.com/in/matt-woodrow-124464166/)

Gecko Graphics and Layout engineer.