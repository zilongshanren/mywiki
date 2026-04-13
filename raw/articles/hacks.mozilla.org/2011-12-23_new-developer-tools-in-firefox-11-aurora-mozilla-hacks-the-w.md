---
title: New Developer Tools in Firefox 11 Aurora – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/12/new-developer-tools-in-firefox-11-aurora/
author: Kdangoor
published: '2011-12-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## More Goodies for the Holidays!

Last month, I wrote a post for Hacks [introducing the new tools in Firefox 10 Aurora](http://hacks.mozilla.org/2011/11/developer-tools-in-firefox-aurora-10/). Those features have now moved to beta. Thanks for all of the great feedback so far!

In a dramatic turn at the end of that blog post, I [foreshadowed](http://en.wikipedia.org/wiki/Foreshadowing) that we had “more to come”. And, indeed here I am to tell you about the *new* developer tools features now in [Firefox Aurora](http://firefox.com/aurora). What you see here is slated for final release in March, 2012.

## Free-form Style Sheet Editing

In the last Firefox release, we introduced the Style Inspector. You can use the Style Inspector’s rules view to make changes to the CSS properties for an element. With this release, we’re adding a free-form Style Editor to the mix.

Select the Style Editor from the Web Developer menu, and you’re presented with a view that lists the style sheets for the page in one pane, and gives you an editor to make changes in another:

The Style Editor provides a friendly environment for working on your style sheets. Any changes you make are reflected instantly on the page. Once you’ve made your changes, you can save the file on your computer.

There are also a number of handy additional features. Click on the “eye” icon next to the style sheet and you can toggle the entire sheet on and off. If you’re working on a new page, you can create new style sheets on the fly or load a style sheet from disk.

If you want to take a look at how other sites on the web are styled, you can use the Style Editor to view the style sheets on any site. On public sites, the style sheets are often minified to reduce download time. The Style Editor will automatically prettify style sheets that it detects have been minified, but it will leave your source style sheets alone.

## “Tilt” 3D View of Web Page Structure

Open up the Page Inspector (Web Developer->Inspect from the menu, or Inspect Element in the context menu on the page), and you’ll see a new **3D** button on the toolbar **if your computer is compatible with WebGL**. Click that, and you’re presented with a *whole new perspective on web page structure*.

This 3D view (which was previously available in an add-on called [Tilt](http://hacks.mozilla.org/2011/10/debugging-and-editing-webpages-in-3d/)), stacks elements as they are nested in the DOM and lets you see elements that are hidden or off the page. You can zoom in and out, rotate and pan the view to see the page from any angle that is helpful to you.

The 3D view is fully integrated with the rest of the Page Inspector functionality. You can open the HTML view or the Style Inspector for more information about the element you’ve clicked on in the 3D view. You can also change selected elements using the breadcrumbs on the toolbar.

The controls for the 3D view are easy:

| Function | Mouse | Keyboard |
|---|---|---|
| Zoom | Scroll up/down | `+` and `-` |
| Rotate | Click and drag | `a` /`d` and `w` /`s` |
| Pan | right-click and drag | Arrow keys |

## Dozens of Other Improvements

Since the last release, we’ve landed dozens of refinements to our other developer features. A growing number of contributors are making the tools they use better by [getting involved](https://wiki.mozilla.org/DevTools/GetInvolved).

The Web Console, Scratchpad and Style Inspector have all had improvements since the last Firefox. Take a look, and [let us know what you think](https://lists.mozilla.org/listinfo/dev-apps-firefox)!

## Get it Now!

You don’t need to wait until March to get these great new features. Download [Firefox Aurora](http://firefox.com/aurora) today and see these and other improvements that are coming to final release soon.

## Updates+Screencast

Since I wrote this article, we’ve landed some fixes and improvements to these tools. I added the way to pan the Page Inspector 3D view (right-click and drag). Also, there is now a [screencast for these features](http://www.youtube.com/watch?v=tRriN8V45jk&context=C304a8ceADOEgsToPDskLDECBCODKvOjyBqq6eUuJy). Be sure to opt-in to [YouTube’s HTML5 video option](http://youtube.com/html5).

## 38 comments

Webstandard BlogDecember 23rd, 2011 at 13:28John99December 23rd, 2011 at 16:03ChrisDecember 23rd, 2011 at 17:27chrisDecember 23rd, 2011 at 17:55Kevin DangoorDecember 23rd, 2011 at 20:44MikaDecember 23rd, 2011 at 21:46Kevin DangoorDecember 23rd, 2011 at 22:28WpCultDecember 23rd, 2011 at 22:01Style ThingDecember 23rd, 2011 at 22:46fpiatDecember 24th, 2011 at 00:31Kevin DangoorDecember 24th, 2011 at 18:36StevetotheHFebruary 23rd, 2012 at 05:12KWiersoDecember 24th, 2011 at 01:33Amanjeet SinghDecember 27th, 2011 at 04:14mynthonDecember 30th, 2011 at 07:29Kevin DangoorJanuary 26th, 2012 at 07:18Joachim ThomasDecember 30th, 2011 at 08:32MikaJanuary 2nd, 2012 at 09:48Joachim ThomasJanuary 6th, 2012 at 12:54Victor PorofJanuary 9th, 2012 at 12:43SlimmyMarch 13th, 2012 at 12:12Kevin DangoorMarch 14th, 2012 at 07:05Richard CookMarch 15th, 2012 at 10:40Kevin DangoorMarch 15th, 2012 at 11:46Richard CookMarch 15th, 2012 at 13:50ErnestVMarch 15th, 2012 at 12:12ErnestVMarch 15th, 2012 at 12:20PercyMarch 27th, 2012 at 16:20Richard CookMarch 27th, 2012 at 16:39faycelMarch 15th, 2012 at 14:29StiMarch 22nd, 2012 at 07:01PercyMarch 27th, 2012 at 16:17Jean-Yves PerrierMarch 27th, 2012 at 16:38TamixesApril 14th, 2012 at 08:09ColacinoApril 16th, 2012 at 20:23DigitalMagickApril 25th, 2012 at 23:59Jean-Yves PerrierApril 26th, 2012 at 14:11olavAugust 28th, 2012 at 02:52