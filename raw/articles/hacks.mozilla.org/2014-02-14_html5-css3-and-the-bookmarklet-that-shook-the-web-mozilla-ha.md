---
title: HTML5, CSS3, and the Bookmarklet that Shook the Web – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2014/02/html5-css3-and-the-bookmarklet-that-shook-the-web/
author: Hari Ananth
published: '2014-02-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

On Valentine’s Day last year we released a bookmarklet that went viral riding the popularity of the Harlem Shake meme. On the anniversary of its release we’d like to take a moment look back at the technical nuts and bolts of the bookmarklet as a case study in applying HTML5. In fact, the HTML, JavaScript, and CSS we used wouldn’t have worked on a single browser a few years ago. What follows is a technical discussion on how we took advantage of recent browser developments to shake up the web.

## Background

Last year the [Harlem Shake meme](http://en.wikipedia.org/wiki/Harlem_Shake_%28meme%29) forced itself on to nearly every screen under the sun and, like everyone else, we had joked about doing our office version of the video. After tossing around a few bad video ideas, Ishan half-jokingly suggested a bookmarklet that made a web page do the Harlem Shake. Omar and Hari immediately jumped on the ingenuity of his idea and built a prototype within an hour that had the entire office LOLing. After pulling a classic all nighter we released it on February 14th, declaring [“Happy Valentine’s Day, Internet! Behold, the Harlem Shake Bookmarklet”](https://www.moovweb.com/blog/happy-valentines-day-internet-behold-the-harlem-shake-bookmarklet/).

Pretty soon it was picked up by news outlets like [TechCrunch](http://techcrunch.com/2013/02/14/i-swear-this-is-the-last-harlem-shake-post-we-do/) and [HuffingtonPost](http://www.huffingtonpost.com/jason-gilbert/harlem-shake-bookmarklet-_b_2687818.html), and our traffic skyrocketed. Meanwhile the bookmarklet offered a new avenue of expression in the watch-then-remix cycle that is the lifeblood of a viral meme like the Harlem Shake. Instead of creating a video of people dancing, developers could now remix this [symbiotic meme](http://techcrunch.com/2013/02/18/what-is-the-harlem-shake-so-popular/) in code. Startups like [PivotDesk](http://blog.pivotdesk.com/525/startups/pivotdesk-does-the-harlem-shake-and-how-you-can-to/#.UvydPUJdVzA) incorporated the bookmarklet into their websites, and [HSMaker](http://hsmaker.com/) used the code to build a Harlem-Shake-As-A-Service website. Eventually, [YouTube](http://techcrunch.com/2013/03/01/youtube-lays-easter-egg-in-tribute-of-harlem-shake-meme/) even built their own version as an easter egg on their site.

## So, how does it work?

Once you click the Harlem Shake bookmark, a snippet of JS is evaluated on the webpage, just as you’d see by entering `javascript:alert(“Hi MozHacks!”);`

in your address bar. This JavaScript will play the Harlem Shake audio, “shake” DOM nodes (according to timing events attached to the audio), and remove all DOM changes afterward.

## How did we attach the audio to the page and get the timing for the shakes just right?

HTML5’s extensive audio support made this implementation fairly easy. All that was required was inserting an `<audio>`

tag with the src pointed to the Harlem_Shake.ogg file. Once inserted into the DOM, the file would begin downloading, and playback begins once enough of the file has been buffered.

HTML5 timed audio events allow us to know exactly when playback begins, updates, and ends. We attach a listener to the audio node which evaluates some JS once the audio reaches certain time. The first node starts shaking once the song is beyond 0.5s. Then, at 15.5s, we flash the screen and begin shaking all of the nodes. At 28.5s, we slow down the animations, and once the audio has ended, we stop all animations and clean up the DOM.

```
audioTag.addEventListener("timeupdate", function() {
var time = audioTag.currentTime,
nodes = allShakeableNodes,
len = nodes.length, i;
// song started, start shaking first item
if(time >= 0.5 && !harlem) {
harlem = true;
shakeFirst(firstNode);
}
// everyone else joins the party
if(time >= 15.5 && !shake) {
shake = true;
stopShakeAll();
flashScreen();
for (i = 0; i < len; i++) {
shakeOther(nodes[i]);
}
}
// slow motion at the end
if(audioTag.currentTime >= 28.4 && !slowmo) {
slowmo = true;
shakeSlowAll();
}
}, true);
audioTag.addEventListener("ended", function() {
stopShakeAll();
removeAddedFiles();
}, true);
```

## How did we choose which parts of the page to shake?

We wrote a few helpers to calculate the rendered size of a given node, determine whether the node is visible on the page, and whether its size is within some (rather arbitrary) bounds:

```
var MIN_HEIGHT = 30; // pixels
var MIN_WIDTH = 30;
var MAX_HEIGHT = 350;
var MAX_WIDTH = 350;
function size(node) {
return {
height: node.offsetHeight,
width: node.offsetWidth
};
}
function withinBounds(node) {
var nodeFrame = size(node);
return (nodeFrame.height > MIN_HEIGHT &&
nodeFrame.height < MAX_HEIGHT &&
nodeFrame.width > MIN_WIDTH &&
nodeFrame.width < MAX_WIDTH);
}
// only calculate the viewport height and scroll position once
var viewport = viewPortHeight();
var scrollPosition = scrollY();
function isVisible(node) {
var y = posY(node);
return (y >= scrollPosition && y <= (viewport + scrollPosition));
}
```

We got a lot of questions about how the bookmarklet was uncannily good at iniating the shake on logos and salient parts of the page. It turns out this was the luck of using very simple heuristics. All nodes are collected (via document.getElementsByTagName(“*”)) and we loop over them twice:

- On the first iteration, we stop once we find a single node that is within the bounds and visible on the page. We then start playing the audio with just this node shaking. Since elements are searched in the order they appear in the DOM (~ the order on the page), the logo is selected with surprising consistency.
- After inserting the audio, we have ~15 seconds to loop through all nodes to identify all shakeable nodes. These nodes get stored in an array, so that once the time comes, we can shake them.

```
// get first shakeable node
var allNodes = document.getElementsByTagName("*"), len = allNodes.length, i, thisNode;
var firstNode = null;
for (i = 0; i < len; i++) {
thisNode = allNodes[i];
if (withinBounds(thisNode)) {
if(isVisible(thisNode)) {
firstNode = thisNode;
break;
}
}
}
if (thisNode === null) {
console.warn("Could not find a node of the right size. Please try a different page.");
return;
}
addCSS();
playSong();
var allShakeableNodes = [];
// get all shakeable nodes
for (i = 0; i < len; i++) {
thisNode = allNodes[i];
if (withinBounds(thisNode)) {
allShakeableNodes.push(thisNode);
}
}
```

## How did we make the shake animations not lame?

We utilized and tweaked [Animate.css](http://daneden.github.io/animate.css/)’s library to speed up the process, its light and easy to use with great results.

First, all selected nodes gets a base class ‘harlem_shake_me’ that defines animation parameters for duration and how it should apply the styles.

```
.mw-harlem_shake_me {
-webkit-animation-duration: .4s;
-moz-animation-duration: .4s;
-o-animation-duration: .4s;
animation-duration: .4s;
-webkit-animation-fill-mode: both;
-moz-animation-fill-mode: both;
-o-animation-fill-mode: both;
animation-fill-mode: both;
}
```

The second set of classes that defines the animation’s behavior are randomly picked and assigned to various nodes.

```
@-webkit-keyframes swing {
20%, 40%, 60%, 80%, 100% { -webkit-transform-origin: top center; }
20% { -webkit-transform: rotate(15deg); }
40% { -webkit-transform: rotate(-10deg); }
60% { -webkit-transform: rotate(5deg); }
80% { -webkit-transform: rotate(-5deg); }
100% { -webkit-transform: rotate(0deg); }
}
@-moz-keyframes swing {
20% { -moz-transform: rotate(15deg); }
40% { -moz-transform: rotate(-10deg); }
60% { -moz-transform: rotate(5deg); }
80% { -moz-transform: rotate(-5deg); }
100% { -moz-transform: rotate(0deg); }
}
@-o-keyframes swing {
20% { -o-transform: rotate(15deg); }
40% { -o-transform: rotate(-10deg); }
60% { -o-transform: rotate(5deg); }
80% { -o-transform: rotate(-5deg); }
100% { -o-transform: rotate(0deg); }
}
@keyframes swing {
20% { transform: rotate(15deg); }
40% { transform: rotate(-10deg); }
60% { transform: rotate(5deg); }
80% { transform: rotate(-5deg); }
100% { transform: rotate(0deg); }
}
.swing, .im_drunk {
-webkit-transform-origin: top center;
-moz-transform-origin: top center;
-o-transform-origin: top center;
transform-origin: top center;
-webkit-animation-name: swing;
-moz-animation-name: swing;
-o-animation-name: swing;
animation-name: swing;
}
```

## Shake it like a polaroid picture

What started a joke ended up turning into its own mini-phenomenon. The world has moved on from the Harlem Shake meme but the bookmarklet is still inspiring developers to get [creative with HTML5](http://www.ampagency.com/building-cheerify-it/).

```
```[@moovweb](https://twitter.com/Moovweb) used your harlem shake button as a stating point for our holiday card this year. Wrote about it [http://t.co/IkQ3Tp9Zkg](http://t.co/IkQ3Tp9Zkg)

— Jon Bishop (@JonDBishop) [December 19, 2013](https://twitter.com/JonDBishop/statuses/413769148381278208)


If you want to see the full source code or have suggestions, feel free to contribute to [the Github repo](https://github.com/moovweb/harlem_shaker)!

## About Hari Ananth

Hari is a Software Engineer at Moovweb working on the Moovweb SDK and mobile applications. Hari has a degree in EECS from UC Berkeley and is outrageously tall.

## About Omar Jalalzada

Omar Jalalzada is a designer of digital products based in San Francisco. Omar is passionate about human behaviors and works with brands to elevate the human attributes of their product and to make them more accessible to their consumers.

## About Ishan Anand

Ishan Anand is Director of New Products at Moovweb. He has been launching mobile products for the iPhone since the day it was released, and his work has been featured on TechCrunch, ReadWriteWeb and LifeHacker. Ishan holds dual-degrees in electrical engineering and mathematics from MIT.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 11 comments

Caspy7February 15th, 2014 at 15:58Erwan d’OrgevilleFebruary 16th, 2014 at 14:19voracityFebruary 17th, 2014 at 21:32Robert Nyman [Editor]February 18th, 2014 at 02:36Joshua SmithFebruary 18th, 2014 at 13:02RodolpheFebruary 20th, 2014 at 03:57Grant KempFebruary 20th, 2014 at 14:49Ishan AnandFebruary 22nd, 2014 at 10:34RayMarch 3rd, 2014 at 17:12Alex JonesMarch 4th, 2014 at 13:27Arun EBMarch 12th, 2014 at 08:25