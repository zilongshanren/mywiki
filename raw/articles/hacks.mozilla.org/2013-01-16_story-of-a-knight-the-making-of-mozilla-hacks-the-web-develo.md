---
title: 'Story of a Knight: the making of – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/01/story-of-a-knight-the-making-of/
author: Marco Sors
published: '2013-01-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [travel of a medieval knight through fullscreen DOM](https://developer.mozilla.org/demos/detail/story-of-a-knight). The ‘making of’ the demo that has [won the November Dev Derby](https://developer.mozilla.org/demos/devderby/2012/november).

Technologies used:

[Fullscreen API](https://developer.mozilla.org/docs/DOM/Using_fullscreen_mode)[Canvas](https://developer.mozilla.org/docs/HTML/Canvas)[Google Maps](https://developers.google.com/maps/)[Audio HTML5](https://developer.mozilla.org/docs/HTML/Using_HTML5_audio_and_video)[Font-face](https://developer.mozilla.org/docs/CSS/@font-face)[jQuery](http://jquery.com/):- Latest jQuery version
[Scrollpath by Joel Besada](https://github.com/JoelBesada/scrollpath)[jQuery-FullScreen by Martin Angelov](https://github.com/martinaglv/jQuery-FullScreen)


![](../../assets/969cae5133a5ae84.jpg)


## Markup And Style

Markup and style are organized in this way:

- An external wrapper that contains everything
- Three controls boxes with fixed positions and high z-index
- An internal wrapper that contains the Google Maps iframe, canvas path and 8
`div`

elements for the story

### The external wrapper and control boxes

The external wrapper contains:

- The audio tag with ogg and mp3 sources, on top left;
- The div which is populated with fullscreen switcher if the browser supports it, on top right;
- The navigation with numbers to move through the canvas path, on bottom right.

![](../../assets/45031dca8ca1aeb8.jpg)


```
```### The internal wrapper

The internal wrapper contains:

- The iframe with the big Google Map embedded, absolutely positioned with negative x and y;
- A div of the same size and the same absolute position of the map, but with a bigger z-index, which has a “background-size: cover” semi-transparent image of old paper to give a parchment effect;
- The canvas path (once activated the javascript plugin, it will be drawn here);
- The 8 divs that tells the story with texts and images, absolutely positioned.

![](../../assets/8ada7291625a36fb.jpg)



# ‡ Story of a Knight ‡

† Of Venetian lagoon AD 1213 †
He learnedthe profession of arms

in an Apennines' fortress.

...

## JavaScript

### The Scrollpath plugin

First we need to embed the jQuery library in the last part of the page


Then we can call the scrollpath.js plugin, the demo.js where we give the instructions to draw the canvas path and initiate it, the easing.js to have a smooth movement (also include the scrollpath.css in the head of the document).


Let’s see the relevant parts of the demo.js file:

- At the beginning there are the instructions for drawing the path, using the methods “moveTo”, “lineTo”, “arc” and declaring x/y coordinates;
- Then there’s the initialization of the plugin on the internal wrapper;
- Finally there’s the navigation implementation with smooth scrolling.

$(document).ready(init);
function init() {
/* ========== DRAWING THE PATH AND INITIATING THE PLUGIN ============= */
var path = $.fn.scrollPath("getPath");
// Move to 'start' element
path.moveTo(400, 50, {name: "start"});
// Line to 'description' element
path.lineTo(400, 800, {name: "description"});
// Arc down and line
path.arc(200, 1200, 400, -Math.PI/2, Math.PI/2, true);
...
// We're done with the path, let's initiate the plugin on our wrapper element
$(".wrapper").scrollPath({drawPath: true, wrapAround: true});
// Add scrollTo on click on the navigation anchors
$(".navigation").find("a").each(function() {
var target = this.getAttribute("href").replace("#", "");
$(this).click(function(e) {
e.preventDefault();
// Include the jQuery easing plugin (http://gsgd.co.uk/sandbox/jquery/easing/)
// for extra easing functions like the one below
$.fn.scrollPath("scrollTo", target, 1000, "easeInOutSine");
});
});
/* ===================================================================== */
}

### The jQuery-FullScreen plugin

To cap it all, the fullscreen. Include the jQuery-FullScreen plugin, then verify with a script if the browser supports the functionality: in case yes, it will append the switcher on the top right corner; then initialize it on the external wrapper to push everything fullscreen.


## Summary

The hardest part was to figure out which size/zoom level give to the Google Maps iframe and then where to position it in relation to the div with the canvas.

The other thing that has reserved some problems was the loading time: I had initially placed the video of a medieval battle in slow-motion along the path, but then I removed it because the page was loaded too slowly

As you have seen everything is very simple, the good result depends only on the right mix of technology, storytelling and aesthetics. I think that the front-end is entering in a golden age, a period rich of expressive opportunities: languages and browsers are evolving rapidly, so there’s the chance to experiment mixing different techniques and obtain creative results.

## About
[
Marco Sors ](http://www.web-expert.it)

Marco Sors is a freelance frontend developer interested in semantics, aesthetics and information design.
After studying communication he has done various things web-related: wireframing, copywriting, functional specifications writing, web applications testing, frontend development.
He currently works for young companies based in H-Farm, a start-up accelerator located in the beautiful Sile Valley near Venice, but also maintains relationships with other web-agencies of northern Italy.
He likes to experiment new technologies and mix them to generate creative visualizations.