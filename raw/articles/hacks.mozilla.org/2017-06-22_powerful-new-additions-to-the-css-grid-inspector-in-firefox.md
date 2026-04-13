---
title: Powerful New Additions to the CSS Grid Inspector in Firefox Nightly – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/06/new-css-grid-layout-panel-in-firefox-nightly/
author: Gabriel Luong
published: '2017-06-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[CSS Grid is revolutionizing](https://www.youtube.com/watch?v=HpqqRBidAQc) web design. It’s a flexible, [simple design standard](https://www.youtube.com/watch?v=16enLRDbOyY) that can be used across all browsers and devices. Designers and developers are rapidly falling in love with it and so are we. That’s why we’ve been working hard on the Firefox Developer Tools Layout panel, adding powerful upgrades to the CSS Grid Inspector and Box Model. The latest improvements are now available in [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/?utm_source=hacks&utm_campaign=layout_panel#nightly).

## Layout Panel Improvements

The new Layout Panel lists all the available CSS Grid containers on the page and includes an overlay to help you visualize the grid itself. Now you can customize the information displayed on the overlay, including grid line numbers and dimensions.

This is especially useful if you’re still getting to know CSS Grid and how it all works.![](../../assets/52c9d5d945683f55.gif)


There’s also a new interactive grid outline in the sidebar. Mouse over the outline to highlight parts of the grid on the pages and display size, area, and position information.

The new “Display grid areas” setting shows the bounding areas and the associated area name in every cell. This feature was inspired by [CSS Grid Template Builder](https://codepen.io/anthonydugois/full/RpYBmy), which was created by [Anthony Dugois](http://anthonydugois.com/).

Finally, the Grid Inspector is capable of visualizing transformations applied to the grid container. This lets developers accurately see where their grid lines are on the page for any grids that are translated, skewed, rotated or scaled.

## Improved Box Model Panel

We also added a Box Model Properties component that lists properties that affect the position, size and geometry of the selected element. In addition, you’ll be able to see and edit the top/left/bottom/right position and height/width properties—making live layout tweaks quick and easy.

Finally, you’ll also be able to see the offset parent for any positioned element, which is useful for quickly finding nested elements.

As always, we want to hear what you like or don’t like and how we can improve Firefox Dev Tools. Find us on [Discourse](https://discourse.mozilla-community.org/c/devtools?utm_source=hacks&utm_campaign=layout_panel&utm_content=discourse) or [@firefoxdevtools](https://twitter.com/FirefoxDevTools?utm_source=hacks&utm_campaign=layout_panel&utm_content=twitter) on twitter.

## Thanks to the Community

Many people were influential in shipping the CSS Layout panel in Nightly, especially the Firefox Developer Tools and Developer Relations teams. We thank them for all their contributions to making Firefox awesome.

We also got a ton of help from the amazing people in the community, and participants in programs like [Undergraduate Capstone Open Source Projects](http://ucosp.ca/) (UCOSP) and [Google Summer of Code](https://developers.google.com/open-source/gsoc/) (GSoC). Many thanks to all the contributors who helped land features in this release including:

[Micah Tigley](https://tigleym.github.io/) – Computer science student at the [University of Lethbridge](https://www.uleth.ca/), Winter 2017 [UCOSP](http://ucosp.ca/) student, Summer 2017 [GSoC](https://developers.google.com/open-source/gsoc/) student. Micah implemented the interactive grid outline and grid area display.

[Alex Lockhart](http://alexlockhart.ca/) – [Dalhousie University](https://www.dal.ca/) student, Winter 2017 [UCOSP](http://ucosp.ca/) student. Alex contributed to the Box Model panel with the box model properties and position information.

[Sheldon Roddick](https://github.com/roddicks) – Student at [Thompson Rivers University](http://www.tru.ca/), Winter 2017 [UCOSP](http://ucosp.ca/) student. Sheldon did a quick contribution to add the ability to edit the width and height in the box model.

If you’d like to become a contributor to Firefox Dev Tools hit us up on [GitHub](https://github.com/firefox-devtools) or [Slack](https://devtools-html-slack.herokuapp.com/) or #devtools on irc.mozilla.com. Here you will find all the resources you need to get started.

## About Gabriel Luong

Making the Inspector the best on Firefox Developer Tools. Feedback and complaints always welcomed :D

## About Dustin Driver

Journalist, tech writer, and video producer helping Mozilla keep the Web open and accessible for everyone.

## 2 comments

LucJune 23rd, 2017 at 00:16Dustin DriverJune 23rd, 2017 at 13:42