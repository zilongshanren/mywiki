---
title: Scroll Anchoring in Firefox 66 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/03/scroll-anchoring-in-firefox-66/
author: Ryan Hunt
published: '2019-03-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 66 was released on March 19th with a feature called *scroll anchoring*.

It’s based on a [new CSS specification](https://drafts.csswg.org/css-scroll-anchoring/) that was first implemented by Chrome, and is now available in Firefox.


Have you ever had this experience before?

You *were* reading headlines, but then an ad loads and moves what you were reading off the screen.

Or how about this?!

You rotate your phone, but now you can’t find the paragraph that you were just reading.

There’s a common cause for both of these issues.

Browsers scroll by tracking the distance you are from the top of the page. As you scroll around, the browser increases or decreases your distance from the top.

But what happens if an ad loads on a page above where you are reading?

The browser keeps you at the same distance from the top of the page, but now there is more content between what you’re reading and the top. In effect, this moves the visible part of the page up away from what you’re reading (and oftentimes into the ad that’s just loaded).

Or, what if you rotate your phone to portrait mode?

Now there’s much less horizontal space on the screen, and a paragraph that was `100px`

tall may now be `200px`

tall. If the paragraph you were reading was `1000px`

from the top of the page before rotating, it may now be `2000px`

from the top of the page after rotating. If the browser is still scrolled to `1000px`

, you’ll be looking at content far above where you were before.

The key insight to fixing these issues is that users don’t care what distance they are from the top of the page. They care about their position relative to the content they’re looking at!

[Scroll anchoring](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-anchor/Guide_to_scroll_anchoring) works to *anchor* the user to the content that they’re looking at. As this content is moved by ads, screen rotations, screen resizes, or other causes, the page now scrolls to keep you at the same relative position to it.

## Demos

Let’s take a look at some examples of scroll anchoring in action.

Here’s a [page](https://eqrion.github.io/web-tests/scrolling/anchor-slider.html) with a slider that changes the height of an element at the top of the page. Scroll anchoring prevents the element above the viewport from changing what you’re looking at.

Here’s a [page](https://eqrion.github.io/web-tests/scrolling/anchor-animation.html) using CSS animations and transforms to change the height of elements on the page. Scroll anchoring keeps you looking at the same paragraph even though it’s been moved by animations.

And finally, here’s the original video of screen rotation with scroll anchoring disabled, in contrast to the view with scroll anchoring enabled.

Notice how we jump to an unrelated section when scroll anchoring is disabled?

## How it works

Scroll anchoring works by first selecting an element of the DOM to be the [anchor node](https://drafts.csswg.org/css-scroll-anchoring/#scroll-anchoring-anchor-node) and then attempting to keep that node in the same relative position on the screen.

To choose an anchor node, scroll anchoring uses the [anchor selection algorithm](https://drafts.csswg.org/css-scroll-anchoring/#anchor-node-selection). The algorithm attempts to pick content that is small and near the top of the page. The exact steps are slightly complicated, but roughly it works by iterating over the elements in the DOM and choosing the first one that is visible on the screen.

When a new element is added to the page, or the screen is rotated/resized, the page’s layout needs to be recalculated. During this process, we check to see if the anchor node has been moved to a new location. If so, we scroll to keep the page in the same relative position to the anchor node.

The end result is that changes to the layout of a page above the anchor node are not able to change the relative position of the anchor node on the screen.

## Web compatibility

New features are great, but do they break websites for users?

This feature is an [intervention](https://github.com/WICG/interventions). It breaks established behavior of the web to fix an annoyance for users.

It’s similar to how browsers worked to prevent popup-ads in the past, and the ongoing work to prevent autoplaying audio and video.

This type of workaround comes with some risk, as existing websites have expectations about how scrolling works.

Scroll anchoring mitigates the risk with several [heuristics](https://drafts.csswg.org/css-scroll-anchoring/#suppression-triggers) to disable the feature in situations that have caused problems with existing websites.

Additionally, a new CSS property has been introduced, [ overflow-anchor](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-anchor), to allow websites to opt-out of scroll anchoring.

To use it, just add `overflow-anchor: none`

on any scrolling element where you don’t want to use scroll anchoring. Additionally, you can add `overflow-anchor: none`

to specific elements that you want to exclude from being selected as anchor nodes.

Of course there are still possible incompatibilities with existing sites. If you see a new issue caused by scroll anchoring, please [file a bug](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=Layout%3A+Scrolling+and+Overflow)!

## Future work

The version of scroll anchoring shipping now in Firefox 66 is our initial implementation. In the months ahead we will continue to improve it.

The most significant effort will involve improving the algorithm used to select an anchor.

Scroll anchoring is most effective when it selects an anchor that’s small and near the top of your screen.

- If the anchor is too large, it’s possible that content inside of it will expand or shrink in a way that we won’t adjust for.
- If the anchor is too far from the top of the screen, it’s possible that content below what you’re looking at will expand and cause unwanted scroll adjustments.

We’ve found that our implementation of the specification can select inadequate anchors on pages with table layouts or significant content inside of `overflow: hidden`

.

This is due to a fuzzy area of the specification where we chose an approach different than Chrome’s implementation. This is one of the values of multiple browser implementations: We have gained significant experience with scroll anchoring and hope to bring that to the specification, to ensure it isn’t defined by the implementation details of only one browser.

The scroll anchoring feature in Firefox has been developed by many people. Thanks go out to Daniel Holbert, David Baron, Emilio Cobos Álvarez, and Hiroyuki Ikezoe for their guidance and many reviews.

## 5 comments

SteveMarch 28th, 2019 at 15:51mrvMarch 29th, 2019 at 08:39ŁukaszMarch 29th, 2019 at 12:45EricMarch 29th, 2019 at 13:09Solomon UckoApril 4th, 2019 at 16:27