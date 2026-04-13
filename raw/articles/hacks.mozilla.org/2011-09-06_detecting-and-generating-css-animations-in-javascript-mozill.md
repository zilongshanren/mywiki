---
title: Detecting and generating CSS animations in JavaScript – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2011/09/detecting-and-generating-css-animations-in-javascript/
author: Chris Heilmann
published: '2011-09-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When writing of the [hypnotic spiral](https://developer.mozilla.org/en-US/demos/detail/hypnotic-spiral) demo the issue appeared that I wanted to use CSS animation when possible but have a fallback to rotate an element. As I didn’t want to rely on CSS animation I also considered it pointless to write it by hand but instead create it with JavaScript when the browser supports it. Here’s how that is done.

Testing for the support of animations means testing if the style attribute is supported:

```
var animation = false,
animationstring = 'animation',
keyframeprefix = '',
domPrefixes = 'Webkit Moz O ms Khtml'.split(' '),
pfx = '';
if( elm.style.animationName ) { animation = true; }
if( animation === false ) {
for( var i = 0; i < domPrefixes.length; i++ ) {
if( elm.style[ domPrefixes[i] + 'AnimationName' ] !== undefined ) {
pfx = domPrefixes[ i ];
animationstring = pfx + 'Animation';
keyframeprefix = '-' + pfx.toLowerCase() + '-';
animation = true;
break;
}
}
}
```

[Update - the earlier code did not check if the browser supports animation without a prefix - this one does]

This checks if the browser supports animation without any prefixes. If it does, the animation string will be 'animation' and there is no need for any keyframe prefixes. If it doesn't then we go through all the browser prefixes (to date :)) and check if there is a property on the style collection called browser prefix + `AnimationName`

. If there is, the loop exits and we define the right animation string and keyframe prefix and set animation to true. On Firefox this will result in `MozAnimation`

and `-moz-`

and on Chrome in `WebkitAnimation`

and `-webkit-`

so on. This we can then use to create a new CSS animation in JavaScript. If none of the prefix checks return a supported style property we animate in an alternative fashion.

```
if( animation === false ) {
// animate in JavaScript fallback
} else {
elm.style[ animationstring ] = 'rotate 1s linear infinite';
var keyframes = '@' + keyframeprefix + 'keyframes rotate { '+
'from {' + keyframeprefix + 'transform:rotate( 0deg ) }'+
'to {' + keyframeprefix + 'transform:rotate( 360deg ) }'+
'}';
if( document.styleSheets && document.styleSheets.length ) {
document.styleSheets[0].insertRule( keyframes, 0 );
} else {
var s = document.createElement( 'style' );
s.innerHTML = keyframes;
document.getElementsByTagName( 'head' )[ 0 ].appendChild( s );
}
}
```

With the animation string defined we can set a (shortcut notation) animation on our element. Now, adding the keyframes is trickier. As they are not part of the original Animation but disconnected from it in the CSS syntax (to give them more flexibility and allow re-use) we can't set them in JavaScript. Instead we need to write them out as a CSS string.

If there is already a style sheet applied to the document we add this keyframe definition string to that one, if there isn't a style sheet available we create a new style block with our keyframe and add it to the document.

You can see the detection in action and a fallback JavaScript solution [on JSFiddle](http://jsfiddle.net/codepo8/ATS2S/8/embedded/result/):

Quite simple, but also a bit more complex than I originally thought. You can also dynamically detect and change current animations as [this post by Wayne Pan](http://waynepan.com/2008/08/08/iphone-css-animations-thoughts-and-issues/) and [this demo by Joe Lambert](http://www.joelambert.co.uk/testcases/keyframes.html) explains but this also seems quite verbose.

I'd love to have a `CSSAnimations`

collection for example where you could store different animations in JSON or as a string and have their name as the key. Right now, creating a new rule dynamically and adding it either to the document or append it to the ruleset seems to be the only cross-browser way. Thoughts?

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 5 comments

Peter van der ZeeSeptember 6th, 2011 at 03:58MookSeptember 6th, 2011 at 21:35GerbenSeptember 6th, 2011 at 09:45Chris HeilmannSeptember 6th, 2011 at 10:17Joe LambertSeptember 7th, 2011 at 02:54