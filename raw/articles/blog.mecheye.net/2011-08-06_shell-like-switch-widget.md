---
title: Shell-like Switch Widget
url: https://blog.mecheye.net/2011/08/shell-like-switch-widget/
author: Jasper St Pierre
published: '2011-08-06'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

I’ve been tinkering with web development a lot lately as part of my work with [SweetTooth](http://www.youtube.com/watch?v=luZuhn5_b_8), the GNOME Shell extensions repository I’m working on for GNOME.

At the suggestion of [Vinicius Depizzol](http://vinicius.depizzol.com.br/blog/), who’s been doing a wonderful job redesigning the GNOME web sites, I tried my hand at creating a Shell-like switch widget to allow a user to click a button to turn extensions on and off. Using some precious combination of JS and CSS, I’ve finally made [a switch widget I think looks nice](http://magcius.mecheye.net/random/switch/). Go ahead: grab it, click on it, fling it around, try and break it! It should just feel “right”.

Figuring out whether the widget is activated and setting the appropriate style classes, the drag logic, and figuring out where to put the switch handle are the only responsibilities of the JS code: everything else is done with CSS, using a combination of border-radius, position: absolute, floats. The triple-line on the grab handle is “drawn” with CSS and manipulates the border styling properties to do its bidding. The animations to fade the background-color and slider position are all CSS3 transitions.

There’s still one unsolved problem, which is the flash and fade of the background color when loading the page, and as much as I tried, I couldn’t solve it. It’s a fallout from CSS thinking it has transitioned from one class to another, but in actuality, it’s just jQuery adding a style class after the node has been constructed. Feel free to yell at me I’m being stupid.

## The unnecessary details of my adventure

As usual, the hard part in concocting something like this is compatibility. The web truly isn’t meant for something pixel-perfect like this, and it shows. Browsers like IE, where compatibility is usually a pain, weren’t involved at all here (I haven’t bothered to test them — again, yell at me). Through poking people on IRC, I found that OS X has different font metrics for the “ON” and “OFF” labels

(A mini rant to the CSS WG: why can’t I create a new flow root/block formatting context to [contain floats](http://www.w3.org/TR/css3-box/#root-height) by asking for one, instead having to [rely on the side effects of other properties?](http://www.w3.org/TR/css3-box/#flow-root))

![SwitchDOM2](../../assets/34c79cf801088464.png)


The problem was that on some browsers and platforms, the text metrics are inconsistent. Unfortunately, the HTML specification gives no guarantee about text measurement, explicitly stating it to be agent-specific. I could deal with this, but ti would be nice if CSS had relative units for glyph widths or JS let you get at some arbitrary measurements of text. <canvas> lets you get at a [TextMetrics](http://www.whatwg.org/specs/web-apps/current-work/multipage/the-canvas-element.html#textmetrics) object, but the only current attribute there is width. For instance, even though I included a web font, WebKit on Mac (which uses CoreGraphics) looked terrible.

![SwitchDOM3](../../assets/1841047979c1edcd.png)


Welp. So, using some complicated trickery using width: 50%, floats, float containment, I finally got a DOM I wanted, and should hopefully be a bit more flexible. This one should make the box stretch in accordance to font weights and such: float containment means that the parent will expand to the container, and width: 50% means that the children will expand to fill half their container. Perfect.![SwitchDOM1](https://blog.mecheye.net/wp-content/uploads/SwitchDOM1.png)


I simultaneously love and hate web development because of things like this.