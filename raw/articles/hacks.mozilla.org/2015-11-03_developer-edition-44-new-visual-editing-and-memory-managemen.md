---
title: 'Developer Edition 44: New visual editing and memory management tools – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/11/developer-edition-44-creative-tools-and-more/
author: Dave Camp
published: '2015-11-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This month marks the one-year anniversary of [Firefox Developer Edition](https://firefox.com/developer). To celebrate, we’re excited to show you some new tools – and some improvements to existing tools – that let you work with the Web in a visual and intuitive way.

As the Web becomes a more dynamic, interactive and mobile experience, visual designers are more than ever experimenting with animation – and the latest Firefox Developer Edition has tools to make working with animations faster and easier. Firefox Developer Edition now gives visual designers and animators a set of visual editing tools that work like they do. We are addressing the technically challenging aspects of animation with a set of visceral, powerful, interactive tools that are comfortable for designers to use. Visual editing tools should appeal to animators, not just to programmers.

## DevTools Challenger

Reading about our new tools is great, but trying them out yourself is even better! To help you get started, we partnered with acclaimed Web animation engineer and advocate [Rachel Nabors](http://rachelnabors.com/) to create [DevTools Challenger](http://devtoolschallenger.com/). Check out DevTools Challenger for hands-on exercises with all of our new visual design tools. Remember to keep scrolling until you get to the ocean floor!

## Animation & CSS Filter Tools

The Page Inspector’s [animation panel](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Work_with_animations) makes it easy to scrub, pause, and visualize each animation on a webpage. Thanks to its tight integration in the DOM inspector, you can switch between a global view of every animation, or drill down to just a few nodes.

Once you’ve found the animation you want, our visual cubic-bezier editor is just a click away. Packed with useful presets, the editor will ensure your animation moves perfectly.

We’ve also built a similar editor for [CSS filters](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Edit_CSS_filters), allowing you to visually add, remove, re-order, and adjust filters with live feedback from the page.

## Measurements & Colors

Firefox Developer Edition also features two brand new tools for fine-tuning layout: you can now enable [pixel rulers](https://developer.mozilla.org/docs/Tools/Rulers) along the page margins, or use our new measurement tool to drag-and-measure arbitrary regions of the page.

The Inspector now defaults to displaying CSS colors “as authored,” and shift-clicking on a color swatch cycles between authored styles and equivalent hex, rgb, and hsl values. There’s even an [eyedropper tool](https://developer.mozilla.org/docs/Tools/Eyedropper) to pick colors right from the page.

## Memory Snapshots

The new Memory tool helps front-end engineers better understand and optimize the way pages allocate and retain memory. The tool works by taking a snapshot of the heap, then allows you to drill down by retained object type, allocation stack, or internal representation. We think you’ll like it, and we’ve got many more features and enhancements in the works!

## WebSocket Debugging API

Lastly, we’re extremely excited to announce that Firefox now exposes an API for monitoring WebSocket frames ([Bug 1203802](https://bugzilla.mozilla.org/show_bug.cgi?id=1203802)), which is the first step on the path to a full-fledged WebSocket inspection tool. Developer Tools engineer Jan Odvarko has built [an experimental add-on](https://github.com/firebug/websocket-monitor/wiki) for inspecting WebSocket traffic. Install the add-on and give it a try, we’d love your feedback.

Firefox Developer Edition is available at [firefox.com/developer](https://firefox.com/developer). Let us know what you think about these features by commenting below or following [@FirefoxDevTools](https://twitter.com/FirefoxDevTools) on Twitter!

## About Dave Camp

Dave Camp is Director of Engineering for Firefox at Mozilla.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 22 comments

Chris HNovember 3rd, 2015 at 07:59Samiullah KhanNovember 3rd, 2015 at 08:40EHNovember 3rd, 2015 at 10:51guestNovember 3rd, 2015 at 18:07Dan CallahanNovember 3rd, 2015 at 18:17IngeborgNovember 4th, 2015 at 04:29Dan CallahanNovember 4th, 2015 at 04:59dormeNovember 4th, 2015 at 23:27guirongNovember 5th, 2015 at 20:00JessNovember 6th, 2015 at 14:17Dan CallahanNovember 6th, 2015 at 15:02DenisNovember 8th, 2015 at 09:40Francis KimNovember 9th, 2015 at 05:56MarcoNovember 12th, 2015 at 00:56TonyNovember 12th, 2015 at 16:00jeremyNovember 14th, 2015 at 18:30Pramod PantulaNovember 15th, 2015 at 09:39Ahmed Abd El-AaalNovember 15th, 2015 at 10:23ConstantineNovember 19th, 2015 at 05:16Dan CallahanNovember 19th, 2015 at 09:05Rene PilonNovember 24th, 2015 at 20:34Geovani dos SantosNovember 25th, 2015 at 12:09