---
title: Variable Fonts Arrive in Firefox 62 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/09/variable-fonts-arrive-in-firefox-62/
author: Dan Callahan
published: '2018-09-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 62, which lands in general release this week, adds support for [Variable Fonts](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Fonts/Variable_Fonts_Guide), an exciting new technology that makes it possible to create beautiful typography with a single font file. Variable fonts are now [supported in all major browsers](https://caniuse.com/#feat=variable-fonts).

## What *are* Variable Fonts?

Font families can have dozens of variations: different weights, expanded or condensed widths, italics, etc. Traditionally, each variant required its own separate font file, which meant that Web designers had to balance typographic nuance with pragmatic concerns around page weight and network performance.

Compared to traditional fonts, variable fonts contain additional data, which make it possible to *generate* different styles of the font on demand. For one example, consider *Jost***,* an [open-source](https://github.com/indestructible-type/Jost), Futura-inspired typeface from [indestructible type*](http://indestructibletype.com). Jost* comes in nine weights, each with regular and italic styles, for a total of eighteen files.

Jost* also comes as a single variable font file which is able to generate not only those same eighteen variations, but also any intermediate weight at any degree of italicization.

## Design Axes

Jost* is an example of a “two-axis” variable font: it can vary in both **weight** and *italics*. Variable fonts can have any number of axes, and each axis can control any aspect of the design. Weight is the most common axis, but typographers are free to invent their own.

One typeface that invented its own axis is [Slovic](https://v-fonts.com/fonts/slovic-variable). Slovic is a Cyrillic variable font with a single axis, `style`

, that effectively varies *history*. At one extreme, characters are drawn similarly to how they appear in 9th century manuscripts, while at the other, they adopt modern sans-serif forms. In between are several intermediate styles. Variable font technology allows the design to adapt and morph smoothly across the entire range of the axis.

The sky’s the limit! To see other examples of variable fonts, check out [v-fonts.com](http://v-fonts.com/) and [Axis Praxis](http://www.axis-praxis.org/).

## Better Tools for Better Typography on the Web

Great features deserve great tools, and that’s why we’re hard at work building an all new [Font Editor](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/View_fonts) into the Firefox DevTools. Here’s a sneak peek:

You can find the Font Editor as a panel inside the Page Inspector in the Dev Tools. If you have enough space on your screen, it’s helpful to enable [3-pane mode](https://developer.mozilla.org/docs/Tools/Page_Inspector/3-pane_mode) so you can see the DOM tree, CSS Rules, and Font Editor all side-by-side.

When you click on an element in the DOM tree, the Font Editor updates to show information about the selected element’s font, as well as tools for editing its properties. The Font Editor works on all fonts, but really shines with variable ones. For instance, the weight control subtly changes from stepped slider to continuous one in the presence of a variable font with a weight axis.

Similarly, each design axis in a variable font gets its own widget in the editor, allowing you to directly customize the font’s appearance and immediately see the results on your page.

The new Font Editor will arrive with [Firefox 63](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/63) in October, but you can use it today by downloading [Firefox Nightly](https://www.mozilla.org/firefox/channel/desktop/#nightly). Let us know what you think! Your feedback is an essential guide as we continue to build and refine Firefox’s design tools.

*Editor’s note:* Attention MacOS users — variable fonts require MacOS 10.13+

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.