---
title: 'Screencast: CSS 3D rollover with fallback for older browsers – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2011/11/screencast-css-3d-rollover-with-fallback-for-older-browsers/
author: Chris Heilmann
published: '2011-11-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Here’s a quick screencast how to create a 3D image rollover and still give a useful interface to browsers that do not support 3D transforms. If you want to see the effect in Firefox get the latest Aurora or Nightly. Check the following video to see what it looks like (first with a browser without CSS 3D transport, then with a newer one):

The screencast is on YouTube:

The main procedure to achieve the effect is simple. First we need a semantically valuable way to show these images, in our case a HTML list with figures and figcaptions. Notice that images still need an alternative text as the figcaption can apply to several images:

```
```

-

**Mittens**loves to play with yarn and stuff.

We then position the caption absolutely inside the list item, give the list item dimensions and an overflow of hidden and move the caption outside of the visible space. When the user hovers over the list item (or focuses it with a keyboard) we move the caption to the right place and lower the opacity of the image.

```
.positioned {
list-style: none;
width: 300px;
height: 200px;
position: relative;
}
.positioned figcaption {
position: absolute;
background: rgba( 0, 0, 0, 0.7 );
color: #fff;
border-radius: 5px;
left: 65px;
bottom: 10px;
width: 230px;
}
.positioned img {
opacity:0.4 ;
}
.positioned figcaption strong {
display: block;
color: lime;
font-weight: normal;
font-size:22px;
padding: 5px 0;
}
.positioned figcaption p {
display: block;
color: white;
padding: 5px;
}
.interactive {
overflow: hidden;
}
.interactive img {
opacity: 1;
}
.interactive figcaption {
left: 300px;
}
.interactive:hover img, .interactive:focus img {
opacity: 0.4;
}
.interactive:hover figcaption, .interactive:focus figcaption {
left: 75px;
}
```

We make the effect smooth by adding transitions. Notice that it makes sense to list all the browser prefixes and set a prefix-less fallback. That way we don’t need to re-write code when a new browser supports them.

```
.smooth img {
-webkit-transition: all 1s;
-moz-transition: all 1s;
-o-transition: all 1s;
-ms-transition: all 1s;
transition: all 1s;
}
.smooth figcaption {
-webkit-transition: all 1s;
-moz-transition: all 1s;
-ms-transition: all 1s;
-o-transition: all 1s;
transition: all 1s;
}
```

In order to rotate the kitty in 3D space, we need to give the list item a perspective and rotate the image and shift it in 3D space with translate3D to avoid clipping:

```
.threed {
-webkit-perspective: 800px;
-moz-perspective: 800px;
-ms-perspective: 800px;
-o-perspective: 800px;
perspective: 800px;
}
.threed:hover img, .threed:focus img {
-webkit-transform: rotateY( 50deg ) rotateX( 10deg )
translate3d( 80px, -20px, -100px );
-moz-transform: rotateY( 50deg ) rotateX( 10deg )
translate3d( 80px, -20px, -100px );
-o-transform: rotateY( 50deg ) rotateX( 10deg )
translate3d( 80px, -20px, -100px );
-ms-transform: rotateY( 50deg ) rotateX( 10deg )
translate3d( 80px, -20px, -100px );
transform: rotateY( 50deg ) rotateX( 10deg )
translate3d( 80px, -20px, -100px );
}
```

That’s it. By adding all the browser prefixes, falling back to a simple rollover and by making sure you do the effect on hover and on focus you support all the browsers and bring the cool to the newest ones.

More reading and resources:

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 4 comments

JoeNovember 16th, 2011 at 00:52RicNovember 17th, 2011 at 03:09BoNovember 22nd, 2011 at 06:55SteelOctober 30th, 2012 at 10:21