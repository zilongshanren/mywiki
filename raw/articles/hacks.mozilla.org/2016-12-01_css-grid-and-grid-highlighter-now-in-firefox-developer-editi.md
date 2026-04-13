---
title: CSS Grid and Grid Highlighter Now in Firefox Developer Edition – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2016/12/css-grid-and-grid-highlighter-now-in-firefox-developer-edition/
author: Mozilla
published: '2016-12-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[CSS Grid](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Grids#Native_CSS_Grids_with_Grid_Layout) has just been uplifted to Firefox 52 Developer Edition ([download it here!](https://www.mozilla.org/en-US/firefox/developer/)). With [Chrome](https://groups.google.com/a/chromium.org/forum/#!topic/blink-dev/hBx1ffTS9CQ) (and hopefully Safari and Edge) implementations coming shortly, using grid to build websites will soon be possible in release browsers across the board.

Grid allows users to decouple HTML from layout concerns, expressing those concerns exclusively in CSS. It adapts to media queries and different contexts, making it a viable alternative to frameworks such as Twitter’s [Bootstrap](http://getbootstrap.com/2.3.2/) or [Skeleton](http://getskeleton.com/) which rely on precise and tightly coupled class structure to define a content grid.

Reducing the risks of fragility, code bloat, and high maintenance costs inherent in how we currently build on the web, grid really does have the potential to change the way we do layouts. Jen Simmons calls it [Real Art Direction for the Web](https://www.youtube.com/watch?v=5Z7lSSMwRgo) and Rachel Andrew has built [Grid by Example](http://gridbyexample.com/what/) to inform, share, and evangelize it. If you’re new to grid, be sure to have a look.

As you can see in the video, the grid highlighter tool will help get you started illustrating the grid in-page as you’re working. Additional tooling is planned for the near future to continually improve working with grid.

To access this tool, make sure you’re running an up-to-date version of [DevEdition](https://www.mozilla.org/en-US/firefox/developer/). Next, open a page that is known to have grid code—we recommend one of [these demos](http://labs.jensimmons.com/) for this. Open the *Inspector *via *Developer *→ *Inspector.* Select an element with the property display: grid;. To toggle grid lines, click the icon next to “grid” which will persist the lines permanently.

The Firefox Developer Tools team have planned a series of improvements to make working with grid easier in the future. You can follow our progress through these bugs:

- Making the
*Inspect Page*button automatically turn on grid highlighters when applicable ([bug 1297100](https://bugzilla.mozilla.org/show_bug.cgi?id=1297100)) - Extending the grid highlighters to our new
[responsive design mode](https://blog.nightly.mozilla.org/2016/11/07/simulate-slow-connections-with-the-network-throttling-tool/)and adding custom options to make displaying grids in responsive design mode easier, and - Creating a new
[panel to make working with grid more customizable](https://invis.io/3X87NEBYH#/179720294_Grid).

The metabug for tracking this work is [bug 1181227](https://bugzilla.mozilla.org/show_bug.cgi?id=1181227).

## 10 comments

VincentDecember 1st, 2016 at 10:32Helen V. HolmesDecember 6th, 2016 at 03:43Kyle McVayDecember 2nd, 2016 at 16:45isaac weathersDecember 2nd, 2016 at 18:38Helen V. HolmesDecember 6th, 2016 at 03:41Changhyun ChoDecember 2nd, 2016 at 21:26Helen V. HolmesDecember 6th, 2016 at 03:41Matt EnrightDecember 4th, 2016 at 13:32Richard Wale AderounmuDecember 5th, 2016 at 21:13Tiago CelestinoDecember 10th, 2016 at 15:08