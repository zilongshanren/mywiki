---
title: Rofox, a CSS3 Animations demo – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/06/rofox-a-css3-animations-demo/
author: Paul Rouget
published: '2011-06-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Firefox 5 was released last week. This release comes with CSS3 Animations. Here is a demo made by Anthony Calzadilla.*

To illustrate what you can achieve with CSS3 Animations, we have been working on demo with [Anthony Calzadilla](http://www.anthonycalzadilla.com/) ([@acalzadilla](http://twitter.com/#!/acalzadilla)), famous for his awesome [Animation projects](http://www.anthonycalzadilla.com/2010/10/css3-animation-hit-list/).

Check out the [demo on the Mozilla Demo Studio](https://developer.mozilla.org/en-US/demos/detail/rofox-css3-animation-by-anthony-calzadilla).

And it works on Firefox Mobile too:

The whole animation is orchestrated in CSS ([keyframe](https://developer.mozilla.org/en/CSS/CSS_animations#Defining_the_animation_sequence_using_keyframes)) and the moves are animated transformations ([transforms](https://developer.mozilla.org/En/CSS/Using_CSS_transforms)). The images are nested divs. If you translated a div and rotate its child, the transformations are combined. You can see the elements being transformed (bounding boxes) if you activate the debug mode.

```
#arm-rt {
/* ARM SLIDING OUT FROM BODY */
transform-origin: 0 50%;
/* The syntax is:
animation: name duration timing-function delay count direction
*/
animation: arm-rt-action-01 60s ease-out 10s 1 both;
}
@keyframes arm-rt-action-01 {
/* This part of the animation starts after 10s and lasts for 60s */
0% { transform : translate(-100px,0) rotate(0deg); }
5% { transform : translate(0,0) rotate(0deg); }
6% { transform : translate(0,0) rotate(-16deg); }
21% { transform : translate(0,0) rotate(-16deg); }
22% { transform : translate(-100px,0) rotate(0deg); }
100% { transform : translate(-100px,0) rotate(0deg); }
}
```

![Rofox](https://hacks.mozilla.org/wp-content/uploads/2011/06/s-500x417.png)


**Tip:** If you want to avoid some performance issues, we encourage you to use bitmap images. SVG images can make the animation a bit shoppy.

Want to see more CSS3 Animations? Check out Anthony’s website: [www.anthonycalzadilla.com](http://www.anthonycalzadilla.com). And feel free to submit your CSS3 Animations demos to the [Mozilla Demo Studio](https://developer.mozilla.org/en-US/demos/detail/rofox-css3-animation-by-anthony-calzadilla).

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 6 comments

JasonJune 27th, 2011 at 19:48NigelJuly 1st, 2011 at 04:36Gaurav MishraJuly 3rd, 2011 at 23:44wangmengJuly 5th, 2011 at 19:24Chico Web DesignAugust 29th, 2011 at 16:25MarkMarch 21st, 2012 at 09:04