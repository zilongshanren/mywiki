---
title: Understanding the CSS box model for inline elements – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2015/03/understanding-inline-box-model/
author: Patrick Brosset
published: '2015-03-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In a web page, every element is rendered as a rectangular box. The [ box model](https://developer.mozilla.org/en-US/docs/Web/CSS/box_model) describes how the element’s `content`

, `padding`

, `border`

, and `margin`

determine the space occupied by the element and its relation to other elements in the page.

Depending on the element’s [ display](https://developer.mozilla.org/en-US/docs/Web/CSS/display) property, its box may be one of two types: a block box or an inline box. The box model is applied differently to these two types. In this article we’ll see how the box model is applied to inline boxes, and how a new feature in the

[Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/tools)can help you visualize the box model for inline elements.

## Inline boxes and line boxes

Inline boxes are laid out horizontally in a box called a line box:

If there isn’t enough horizontal space to fit all elements into a single line, another line box is created under the first one. A single inline element may then be split across lines:

## The box model for inline boxes

When an inline box is split across more than one line, it’s still logically a single box. This means that any horizontal padding, border, or margin is only applied to the start of the first line occupied by the box, and the end of the last line.

For example, in the screenshot below, the highlighted `span`

is split across 2 lines. Its horizontal padding doesn’t apply to the end of the first line or the beginning of the second line:

Also, any vertical padding, border, or margin applied to an element will not push away elements above or below it:

However, note that vertical padding and border are still applied, and the padding still pushes out the border:

If you need to adjust the height between lines, use [ line-height](https://developer.mozilla.org/en-US/docs/Web/CSS/line-height) instead.

## Inspecting inline elements with devtools

When debugging layout issues, it’s important to have tools that give you the complete picture. One of these tools is the highlighter, which all browsers include in their devtools. You can use it to select elements for closer inspection, but it also gives you information about layout.

In the example above, the highlighter in Firefox 39 is used to highlight an inline element split across several lines.

The highlighter displays guides to help you align elements, gives the complete dimensions of the node, and displays an overlay showing the box model.

From Firefox 39 onwards, the box model overlay for split inline elements shows each individual line occupied by the element. In this example the content region is displayed in light blue and is split over four lines. A right padding is also defined for the node, and the highlighter shows the padding region in purple.

Highlighting each individual line box is important for understanding how the box model is applied to inline elements, and also helps you check the space between lines and the vertical alignment of inline boxes.


## About
[
Patrick Brosset ](http://patrickbrosset.com)

Patrick manages the DevTools engineering team at Mozilla

## 2 comments

fvschMarch 25th, 2015 at 02:40κατασκευή ιστοσελίδων θεσσαλονίκηApril 3rd, 2015 at 12:50