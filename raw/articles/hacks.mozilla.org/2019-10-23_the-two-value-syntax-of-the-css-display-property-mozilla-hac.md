---
title: The two-value syntax of the CSS Display property – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2019/10/the-two-value-syntax-of-the-css-display-property/
author: Rachel Andrew
published: '2019-10-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

If you like to read release notes, then you may have spotted in the [Firefox 70 notes](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/70) a line about the implementation of the two-value syntax of the [ display CSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/display). Or maybe you saw a mention in yesterday’s

[Firefox 70 roundup post](https://hacks.mozilla.org/2019/10/firefox-70-a-bountiful-release-for-all/). Today I’ll explain what this means, and why understanding this two-value syntax is important despite only having an implementation in Firefox right now.

## The `display`

property

The `display`

property is how we change the **formatting context** of an element and its children. In CSS some elements are block by default, and others are inline. This is one of the first things you learn about CSS.

The `display`

property enables switching between these states. For example, this means that an `h1`

, usually a block element, can be displayed inline. Or a `span`

, initially an inline element, can be displayed as a block.

More recently we have gained [CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout) and [Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout). To access these we also use values of the `display`

property — `display: grid`

and `display: flex`

. Only when the value of `display`

is changed do the children become flex or grid items and begin to respond to the other properties in the grid or flexbox specifications.

### Two-value display – span with `display: flex`


What grid and flexbox demonstrate, however, is that an element has both an outer and an inner display type. When we use `display: flex`

we create a block-level element, with flex children. The children are described as participating in a flex formatting context. You can see this if you take a span and apply `display: flex`

to it — the span is now block-level. It behaves as block-level things do in relationship to other boxes in the layout. It’s as if you had applied `display: block`

to the span, however we also get the changed behavior of the children. In the CodePen below you can see that the string of text and the `em`

have become two flex items.

### Two-value display – span with `display: grid`


Grid layout behaves in the same way. If we use `display: grid`

we create a block-level element and a grid formatting context for the children. We also have methods to create an inline-level box with flex or grid children with `display: inline-flex`

and `display: inline-grid`

. The next example shows a div, normally a block-level element, behaving as an inline element with grid item children.

As an inline element, the box does not take up all the space in the inline dimension, and the following string of text displays next to it. The children however are still grid items.

## Refactoring `display`


As the above examples show, the outer `display`

type of an element is always block or inline, and dictates how the box behaves in the normal flow of the document. The inner `display`

type then changes the formatting context of the children.

To better describe this behavior, the CSS Display specification has been refactored to allow for `display`

to accept two values. The first describes whether the outer `display`

type is block or inline, whereas the second value describes the formatting of the children. This table shows how some of these new values map to the single values – now referred to as legacy values – in the spec.

| Single value | New value |
|---|---|
| block | block flow |
| flow-root | block flow-root |
| inline | inline flow |
| inline-block | inline flow-root |
| flex | block flex |
| inline-flex | inline flex |
| grid | block grid |
| inline-grid | inline grid |

There are more values of `display`

, including lists and tables; to see the full set of values visit the [CSS Display Specification](https://drafts.csswg.org/css-display/#typedef-display-legacy).

We can see how this would work for Flexbox. If I want to have a block-level element with flex children I use `display: block flex`

, and if I want an inline-level element with flex children I use `display: inline flex`

. The below example will work in Firefox 70.

Our trusty `display: block`

and `display: inline`

don’t remain untouched either, `display: block`

becomes `display: block flow`

– that is a block element with children participating in normal flow. A `display: inline`

element becomes `display: inline flow`

.

`display: inline-block`

and `display: flow-root`


This all becomes more interesting if we look at a couple of values of `display`

– one new, one which dates back to CSS2. Inline boxes in CSS are designed to sit inside a line box, the anonymous box which wraps each line of text in a sentence. This means that they behave in certain ways: If you add padding to all of the edges of an inline box, such as in the example below where I have given the inline element a background color, the padding applies. And yet, it does not push the line boxes in the block direction away. In addition, inline boxes do not respect width or height (or inline-size and block-size).

Using `display: inline-block`

causes the inline element to contain this padding, and to accept the width and height properties. It remains an inline thing however; it continues to sit in the flow of text.

In this next CodePen I have two span elements, one regular inline and the other inline-block, so that you can see the difference in layout that this value causes.

We can then take a look at the newer value of `display`

, `flow-root`

. If you give an element `display: flow-root`

it becomes a new block formatting context, becoming the root element for a new normal flow. Essentially, this causes floats to be contained. Also, margins on child elements stay inside the container rather than collapsing with the margin of the parent.

In the next CodePen, you can compare the first example without `display: flow-root`

and the second with `display: flow-root`

. The image in the first example pokes out of the bottom of the box, as it has been taken out of normal flow. Floated items are taken out of flow and shorten the line boxes of the content that follows. However, the actual box does not contain the element, unless that box creates a new block formatting context.

The second example does have flow-root and you can see how the box with the grey background now contains the float, leaving a gap underneath the text. If you have ever contained floats by setting overflow to auto, then you were achieving the same thing, as overflow values other than the default visible create a new block formatting context. However, there can be some additional unwanted effects such as clipping of shadows or unexpected scrollbars. Using flow-root gives you the creation of a [block formatting context (BFC)](https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Block_formatting_context) without anything else happening.

The reason to highlight `display: inline-block`

and `display: flow-root`

is that these two things are essentially the same. The well-known value of inline-block, creates an inline flow-root which is why the new two-value version of `display: inline-block`

*is* `display: inline flow-root`

. It does *exactly the same job* as the flow-root property which, in a two-value world, becomes `display: block flow-root`

.

You can see both of these values used in this last example, using Firefox 70.

## Can we use these two value properties?

With support currently available only in Firefox 70, it is too early to start using these two-value properties in production. Currently, other browsers will not support them. Asking for `display: block flex`

will be treated as invalid except in Firefox. Since you can access all of the functionality using the one-value syntax, which will remain as aliases of the new syntax, there is no reason to suddenly jump to these.

However, they are important to be aware of, in terms of what they mean for CSS. They properly explain the interaction of boxes with other boxes, in terms of whether they are block or inline, plus the behavior of the children. For understanding what display is and does, I think they make for a very useful clarification. As a result, I’ve started to teach display using these two values to help explain what is going on when you change formatting contexts.

It is always exciting to see new features being implemented, I hope that other browsers will also implement these two-value versions soon. And then, in the not too distant future we’ll be able to write CSS in the same way as we now explain it, clearly demonstrating the relationship between boxes and the behavior of their children.

## About
[
Rachel Andrew ](https://rachelandrew.co.uk)

Rachel Andrew is a front and back-end web developer, one half of the company behind Perch CMS, and Editor in Chief of Smashing Magazine. She is a Google Developer Expert for web technologies and a member of the CSS Working Group representing Fronteers, where she is co-editor of the Multi-column Layout spec. Author of 22 books, and a frequent public speaker at conferences worldwide, you can find out what she is up to at https://rachelandrew.co.uk.