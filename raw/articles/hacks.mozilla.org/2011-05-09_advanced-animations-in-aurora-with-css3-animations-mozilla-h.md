---
title: Advanced animations in Aurora with CSS3 Animations – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2011/05/advanced-animations-in-aurora-with-css3-animations/
author: Louisremi
published: '2011-05-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 4 came with CSS3 Transitions (ability to animate CSS properties from an initial value to a final one). In Firefox Aurora, we are experimenting with [CSS3 Animations](https://developer.mozilla.org/en/CSS/CSS_animations): a more powerful way to animate your content with CSS.

### Defining the animation

The first thing is to define the intermediary CSS values of the properties to be animated, what is called keyframes in the specification. Users of Adobe Flash authoring tools should be familiar with this concept.

### Applying an animation

While Transitions trigger implicitly when property values change, animations are explicitly executed when the animation properties are applied.

### More properties

The [specification](http://dev.w3.org/csswg/css3-animations/) defines other animation properties that opens a broad range of possibilities:

- with
`animation-timing-function`

it is possible to take advantage of easings to make animations feel more natural (see demo below) `animation-direction: alternate;`

is the*auto-reverse*of CSS3 Animations. See how it is used to create the loader below.- without
`animation-fill-mode: forwards;`

, the properties will be set back to their initial values at the end of the animation - and guess what setting
`animation-play-state`

to`paused`

would do…

### Demo!

You should be using [Firefox Aurora](http://www.firefox.com/channel), Chrome or Safari 5 to see those demo.

*animated translations*


*zero-image, gracefully degrading loader*


*a complex animated scene*

View [Madmanimation](http://www.animatable.com/demos/madmanimation/) with a compatible browser, or watch a [screencast of the animation](http://www.youtube.com/watch?v=fUdu6ey4lCg).

You’ve already used CSS3 animations? Let us know in the comment below or submit your demo in the [Studio](https://developer.mozilla.org/en-US/demos/).

## About
[
louisremi ](http://twitter.com/louis_remi)

Developer Relations Team, long time jQuery contributor and Open Web enthusiast. [@louis_remi](http://twitter.com/louis_remi)

## 9 comments

Salman AbbasMay 9th, 2011 at 12:25BrianMBMay 9th, 2011 at 13:41Girish MonyMay 9th, 2011 at 19:42louisremiMay 10th, 2011 at 06:11Girish MonyMay 10th, 2011 at 07:41Ken SaundersMay 10th, 2011 at 10:59Webstandard BlogJune 2nd, 2011 at 12:02Gaurav MJune 21st, 2011 at 23:450dpJuly 24th, 2011 at 06:11