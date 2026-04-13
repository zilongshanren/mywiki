---
title: CSS 3D transformations in Firefox Nightly – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/10/css-3d-transformations-in-firefox-nightly/
author: Chris Heilmann
published: '2011-10-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When the first 3D transformations in CSS got support on Webkit browsers people got incredibly excited about them. Now [that they have matured](http://dev.w3.org/csswg/css3-3d-transforms/) we also support 3D CSS in Firefox. To see it for yourself, check out [one of the latest nightly builds](http://nightly.mozilla.org).

You can see them in action in [this demo of a rotating HTML5 logo](http://thewebrocks.com/demos/html5-3d-css) and the screencast below:

This means now that we need your support in trying out CSS 3D examples in Firefox and add other extensions than `-webkit-`

to your CSS 3D products and demos. To show that this is possible, we took the well-known [webkit-only “poster circle” demo](http://www.webkit.org/blog-files/3d-transforms/poster-circle.html) and made it work with Firefox nightly by adding the -moz- (and of course the other prefixes and one set of instructions without browser prefixes). Here is a slight excerpt:

```
-webkit-transform-style: preserve-3d;
-moz-transform-style: preserve-3d;
-o-transform-style: preserve-3d;
-ms-transform-style: preserve-3d;
transform-style: preserve-3d;
```

You can see this in action in the screencast below alongside Chrome and you [try the demo out yourself](http://thewebrocks.com/demos/postercircle/). The slight jerkiness is actually my MacBook Air impersonating a starting jet every time I use ScreenFlow and not the browser.

To celebrate the release and to show how CSS 3D can be applied as subtle effect, have a [game of pairs using your favourite browsers (and a cat)](http://thewebrocks.com/demos/browsermemory/) :

Oleg Romashin also spent some time to [convert a few CSS 3D demos to work with Mozilla](http://romaxa.bolshe.net/css3d/) and you can [check the 3D city](http://m8y.org/tmp/cubiq.org/dropbox/3dcity/index2.html) for more “wow”.

If you are new to CSS 3D transformations [here’s a good beginner course](http://24ways.org/2010/intro-to-css-3d-transforms) and [a tool to create them](http://www.westciv.com/tools/3Dtransforms/index.html).

The rotating HTML5 logo demo also shows how you can check if the currently used browser supports 3D transforms. Instead of repeating the animation frames for all the prefixes we test in JavaScript and create the CSS on the fly:

```
function checksupport() {
var props = ['perspectiveProperty', 'WebkitPerspective',
'MozPerspective', 'OPerspective', 'msPerspective'],
i = 0,
support = false;
while (props[i]) {
if (props[i] in form.style) {
support = true;
pfx = props[i].replace('Perspective','');
pfx = pfx.toLowerCase();
break;
}
i++;
}
return support;
}
if (checksupport()) {
var s = '';
styles = document.createElement('style');
s += '#stage{-'+ pfx +'-perspective: 300px;}'+
'#logo{-'+ pfx +'-transform-style: preserve-3d;position:relative;}'+
'#logo.spin{-'+ pfx +'-animation: spin 3s infinite linear;}'+
'@-'+ pfx +'-keyframes spin {'+
'0% {'+
'-'+ pfx +'-transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);'+
'}'+
'100% {'+
'-'+ pfx +'-transform: rotateX(0deg) rotateY(360deg)'+
' rotateZ(360deg);'+
'}}';
styles.innerHTML = s;
document.querySelector('head').appendChild(styles);
}
```

For more information on creating your own pages that use 3D transformations, take a look at the [draft specification](http://dev.w3.org/csswg/css3-3d-transforms/)

As always, If you find any bugs, please report them at [bugzilla.mozilla.org](https://bugzilla.mozilla.org)!

So please reward our hard work bringing the third dimension to Firefox’s CSS engine by supporting and testing. Cheers!

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 39 comments

loffiniOctober 26th, 2011 at 13:27Chris HeilmannOctober 26th, 2011 at 13:29paulo333October 26th, 2011 at 14:50ZéflingOctober 26th, 2011 at 13:57Jesse RudermanOctober 26th, 2011 at 14:03Karl BöhlmarkOctober 26th, 2011 at 14:45Beben KobenOctober 26th, 2011 at 15:10RichardOctober 26th, 2011 at 15:38Omega XNovember 1st, 2011 at 16:50AdamTOctober 27th, 2011 at 01:00woodsyOctober 27th, 2011 at 03:44JonathanOctober 27th, 2011 at 02:04MattOctober 27th, 2011 at 03:38mekalOctober 27th, 2011 at 03:46GerbenOctober 27th, 2011 at 09:12Ken SaundersOctober 27th, 2011 at 12:51Paul IrishOctober 29th, 2011 at 21:40shirokoffNovember 1st, 2011 at 01:12Matt WoodrowNovember 1st, 2011 at 22:44MarkNovember 2nd, 2011 at 08:54MichaelNovember 11th, 2011 at 20:06nemoNovember 16th, 2011 at 12:36Konrad PerkoNovember 16th, 2011 at 09:41nemoNovember 16th, 2011 at 12:36VinciNovember 17th, 2011 at 10:56MichaelNovember 19th, 2011 at 04:07VinciNovember 20th, 2011 at 00:39nemoNovember 20th, 2011 at 15:27SToto98November 21st, 2011 at 12:34is-realDecember 14th, 2011 at 19:09SamuelDecember 30th, 2011 at 14:09JoelJanuary 11th, 2012 at 21:38ForkoffFebruary 3rd, 2012 at 05:50MichaelJanuary 12th, 2012 at 23:57AndiFebruary 10th, 2012 at 16:05Orlando LeiteFebruary 21st, 2012 at 12:33OswaldFebruary 22nd, 2012 at 18:37nemoJune 6th, 2012 at 08:00pendragonJuly 10th, 2012 at 10:12