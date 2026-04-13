---
title: Taking steps() with CSS animations – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/09/taking-steps-with-css-animations/
author: Chris Heilmann
published: '2011-09-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

CSS animations are hot and a lot of experimentation is going on. A cool new feature of animations is the [steps()](http://dev.w3.org/csswg/css3-animations/#animation-timing-function) option which allows you to cut an animation into steps instead of a transition from one state to another in one go. While this seems counterproductive on first glance there is a lot you can do with it.

Inspired by the [making the perfect listing](http://gidsy.com/handbooks/making-the-perfect-listing/) web site [Lea Verou](http://twitter.com/leaverou) created a [Pure CSS3 typing animation](http://leaverou.me/2011/09/pure-css3-typing-animation-with-steps/).

Which then inspired [@simurai](http://twitter.com/simurai) to use the steps() feature to [create a sprite animation](http://jsfiddle.net/simurai/CGmCe/).

Especially the latter is very interesting as it allows for a scripted animation without JavaScript – remember when you had to re-animate GIFs in Photoshop and re-optimise them every time a client wanted them faster or slower?

For now the steps only divide the full length of the animation up. If you want different timings for different steps you still will need to create keyframes for each. Right now the steps feature works in Firefox and Webkit. Let’s hope others will follow, too.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 3 comments

Style ThingSeptember 9th, 2011 at 22:37simonleungSeptember 11th, 2011 at 08:23Gaurav MishraSeptember 12th, 2011 at 22:17