---
title: CSS Scroll Snap Updated in Firefox 68 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/06/css-scroll-snap-updated-in-firefox-68/
author: Rachel Andrew
published: '2019-06-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When Firefox 68 goes to general release next month, it will ship with an updated [CSS Scroll Snap specification](https://www.w3.org/TR/css-scroll-snap-1/). This means that Firefox will support the same version of the specification as Chrome and Safari. Scroll snapping will work in the same way across all browsers that implement it.

In this post, I’ll give you a quick rundown of what scroll snapping is. I will also explain why we had a situation where browsers had different versions of the specification for a time.

## What is CSS Scroll Snap?

The CSS Scroll Snap specification gives us a way in CSS to snap between different elements in a page or scrolling component, in a very similar fashion to how native apps work on phones and tablets.

Scroll snapping can happen on the `x`

or `y`

axis. This means that you can swipe in both the inline and the block direction depending on your requirements. In the example below I demonstrate a very simple use of scroll snapping. I have a scrolling box, which has a vertical scrollbar due to `overflow-y`

being specified, and the box being given a height. I have then added the property `scroll-snap-type: y mandatory`

, which gives us mandatory scrolling on the y axis. You can see this example in the CodePen.

```
.scroller {
height: 300px;
overflow-y: scroll;
scroll-snap-type: y mandatory;
}
```


*Mandatory* scrolling means that the browser has to snap to a scroll point, no matter where in the content the user is. The other available keyword is *proximity*. Proximity causes the browser to only snap to the scroll point when the scroll is near that point. This prevents situations where the user is unable to scroll to a certain point because that point is outside the visible area.

In addition to the `scroll-snap-type`

property on the scroll container, I need to add the `scroll-snap-align`

property to define the point that the scroll will snap to. This property takes a value of `start`

, `center`

, or `end`

, which defines where in the child container the scroll should snap to:

```
.scroller section {
scroll-snap-align: start;
}
```


For many use cases, these key properties will be all that you need to get your scroll snapping to work. However, the specification defines a way to add padding and/or margins to the scroll point. This can help in certain cases where you don’t want the scroll to snap right to the edge of the scrollable area.

For example, below I have used the `scroll-padding-top`

property to leave a gap. This makes space for the fixed element at the top of the container. If I didn’t do this, I would risk content ending up underneath that bar.

```
h1 {
position: sticky;
top: 0;
}
.scroller {
height: 300px;
overflow-y: scroll;
scroll-snap-type: y mandatory;
scroll-padding-top: 40px;
}
.scroller section {
scroll-snap-align: start;
}
```


On MDN we have [pages for the various Scroll Snap properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap). [A guide to using Scroll Snap](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap/Basic_concepts) offers lots of additional examples. The property pages all show the status of browser support for these properties.

## What has changed in Firefox 68?

Firefox 68 implements the version of scroll snap as described above, according to the current version of the specification. This matchs the Chrome implementation. If you have implemented scroll snap to work in Chrome, then you don’t need to do anything — your scroll snapping will now work in Firefox.

If you used the old version of the specification as it was implemented in Firefox in version 39, you should update that code to use the new version. In addition to implementing the new spec, Firefox 68 [will remove support for properties from the old version of the spec](https://www.fxsitecompat.com/en-CA/docs/2019/legacy-css-scroll-snap-syntax-support-has-been-dropped/).

If you have used `scroll-snap-type-x`

and `scroll-snap-type-y`

, then you are using the old spec. These properties are removed in Firefox 68. `scroll-snap-type`

is now used to set the `x`

or `y`

direction along with the type of scroll snapping.

## Why were there two versions of scroll snap?

CSS specifications are developed in an iterative way, and browsers begin to implement specifications while they are in the process of being developed. This is an important step. The CSS Working Group needs to know that it is possible to implement the specification in browsers. Test implementations let web developers try out a new spec and file issues against it. Often these implementations happen behind a browser flag. In the past we’ve used vendor-prefixed versions to expose them for testing. Sometimes, however, a specification is in a seemingly good state and therefore implemented, but then changes need to be made. Such is the way of developing new browser features.

In some cases, a change like this means that the old and new properties have to be supported forever. The `grid-gap`

property is a good example. The property has been renamed to `gap`

. Due to significant usage in the wild, the `grid-gap`

property is being maintained as an alias. In the case of Scroll Snap, usage of that old experimental spec was very low, and therefore the `scroll-snap-type`

property has been updated in a non-backwards compatible way. This means that the old version will be removed at this point.

## Backwards compatibility and scroll snap

Scroll Snap is one of those specifications that can act as a nice enhancement in many cases. If the browser does not support scroll snapping, then regular scrolling will happen instead. We have information on MDN which can help you to [implement the old specification as a fallback](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Scroll_Snap/Browser_compat) for old Firefox versions, if your analytics show this is necessary. For most use cases this is unlikely to be required.

It’s great to see another CSS specification get wide browser implementation. If you have used JavaScript to get a scroll snapping effect in the past, it might be a good time to take a look at the CSS version! You are likely to find that it performs far better than a JavaScript solution.

## About
[
Rachel Andrew ](https://rachelandrew.co.uk)

Rachel Andrew is a front and back-end web developer, one half of the company behind Perch CMS, and Editor in Chief of Smashing Magazine. She is a Google Developer Expert for web technologies and a member of the CSS Working Group representing Fronteers, where she is co-editor of the Multi-column Layout spec. Author of 22 books, and a frequent public speaker at conferences worldwide, you can find out what she is up to at https://rachelandrew.co.uk.