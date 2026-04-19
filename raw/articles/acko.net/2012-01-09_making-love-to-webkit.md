---
title: Making Love to WebKit
url: https://acko.net/blog/making-love-to-webkit/
author: Steven Wittens
published: '2012-01-09'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![Making Love to WebKit](../../assets/5258486fd7b3d5ac.jpg)

# Making Love to WebKit

## Parallax, GPUs and Technofetishism

If the world is going to end in 2012, Acko.net will at least go out in style: I've redesigned. Those of you reading through RSS readers will want to [enter through the front door](http://acko.net/) in a WebKit-browser like Chrome, Safari or even an iPad.

The last design was meant to feel spacious, the new design *is* spacious, thanks to generous use of CSS 3D transforms.

### CSS 3D vs. WebGL

This idea started with an accidental discovery: if you put a CSS perspective on a scrollable <DIV>, then 3D elements inside that <DIV> will retain their perspective while you scroll. This results in smooth, native parallax effects, and makes objects jump out of the page, particularly when using an analog input device with inertial scrolling.

This raises the obvious question: how far can you take it? Of course, this only works on WebKit browsers, who currently have the only CSS 3D implementation out of beta, so it's not a viable strategy by itself yet. IE10 and Firefox will be the next browsers to offer it. There's WebGL in Chrome and Firefox that can be used to do similar things, but WebGL is its own sandbox: you can't put DOM elements in there, or use native interaction. And any amount of WebGL rendering in response to e.g. scrolling is going to involve some amount of lag. Still, I wasn't going put a lot of effort into making a CSS 3D-only design without some backup.

That's why I actually built the whole thing on top of [Three.js](https://github.com/mrdoob/three.js/), mrdoob's excellent JavaScript 3D engine. Aside from providing a comprehensive standard library for 3D manipulation, it also lets you swap out the rendering component. Out of the box, it can render to a 2D canvas, a WebGL canvas, or SVG.

### The DOM Scenegraph

So I augmented it with a CSS 3D renderer ([GitHub](https://github.com/unconed/CSS3D.js)). It reads out the scene and renders each object using DOM elements, shaped and transformed into the right 3D position, orientation and appearance. They sit ‘in’ the page, and the browser projects and composits them for you. Of course, this only works for simple geometric shapes like lines or rectangles, but luckily that's all I need.

It would be too slow to have to render out new elements for every frame, so the CSS 3D renderer's elements persist. Moving or rotating an object involves just changing a CSS property. Same for the camera: the entire scene is wrapped in a <DIV> that has its own 3D transform.

So it's VRML all over again, but this time, it actually sort of performs. With our browsers being actual 3D engines, it's not a huge leap from here to having a <MESH> tag in HTML6, can-of-worms-factor not withstanding.

Having built a quick prototype, I was satisfied with how well it worked, particularly in Safari on OS X, where the cross-pollination from the iPhone's mature tile-based GPU renderer has clearly paid off and there is no lag at all.

### Design Process

Now all that was needed was a design. Last time I drew out a manual perspective drawing in Illustrator, which was tedious, but still basically came down to designing a flat image. This time, it would have to work in 3D. I started with a quick sketch to get a feel for the perspective, now that it no longer needed to double as a flat frame for the site's content.

Simple geometric shapes, parallel lines, consistent angles. Simple enough. But if real perspective was involved, I would have to place items so they would look good from multiple angles, and each would need convincing depth and shading. To do this all by hand, typing out coordinates and perpetually refreshing the page, would take forever.

So instead I built a simple editor to speed up the process. It's super ghetto, and basically just exists to manipulate the colors, positions and orientations of objects in a Three.js scene. It spits out a JSON object describing them, which can then be unserialized again into a scene.

This also helped maintain a consistent palette. The colors are built from a few base tints, brightened or darked in linear RGB—i.e. before gamma correction. This ensures even tones and allowed for easy color adjustments.

The editor is almost entirely keyboard operated, but with its minimum amount of features I was at least able to place items in 3D, copy/paste objects and see it from any angle or position I wanted. To 'save', I just copied the output into a .JS file, where I could make manual tweaks too if necessary.

As for the actual site and content, I wanted to keep it much more sober. Like many others these days, I want to treat blogging more like publishing. That way I can focus on crafting each post more like an article with illustrations and asides rather than just a text blog.

Hence, while there's a big party upstairs, it's all [typography](http://www.amazon.com/Elements-Typographic-Style-Robert-Bringhurst/dp/0881791326) down below. The font of choice is [Klavika](http://processtypefoundry.com/fonts/klavika/), a humanist/geometric sans-serif with just the right kind of “Dutch Art Museum Signage” meets “Cyberpunk” I was looking for. The layout is a responsive multi-column grid that collapses down for smaller screens and devices. Finally, a strict vertical rhythm is enforced in the lines to keep everything nice and tidy.

#### Controls

`Click`+`Drag`— Orbit camera`Enter`— New object`Space`— Clone object`Backspace`— Delete object`Tab`/`Shift`+`Tab`

Cycle through objects`W``A``S``D``Q``E`

Move object`Shift`+`W``A``S``D``Q``E`

Resize object`Ctrl`+`W``A``S``D``Q``E`

Move camera`[``]`— Lower/raise units`Z``X`

Orbit distance`T`/`T`/`U`

Tag/untag/untag all

### She cannae take the power cap'n!

307 objects later it was finished, and not a single image was used. Unfortunately, as you can see there are tons of glitches in the editor—though some objects only have one side by design, and it works a lot better in a separate window. CSS 3D was never meant to do this, and you often see incorrect depth layering and flickering. Luckily most of these are caused by the floating grid markers and aren't a problem in the final view. The rest was resolved by splitting up objects or dual layering problematic surfaces, but some minor problems remain. Also for some reason, the background <DIV>'s click areas extend beyond their visible area, causing some click layering issues that I had to work around. Text resizing in the browser also leads to breakage, though multi-touch zoom works in Safari.

Performance in Safari is wonderfully smooth too, but Chrome OS X starts to lag a bit. Luckily the effects are turned off as soon as they go off screen, so any lag should be confined to the top of the page. Finally, there's also a random bug where sometimes the page will refuse to scroll if the mouse is over a 3D object, which is unfortunate, but also near-impossible to reproduce reliably.

In theory the iPad would perform second, but it has its own issues. The use of page-in-page scrolling disables inertia, but this is entirely beyond my control. The other issue is that sometimes, the iPad will decide to render the page content at lower resolution, making it hard to read. I guess the CSS wizardry confuses its GPU texture management. A refresh usually fixes this.

I also discovered some funny ways of abusing CSS 3D for weird effects. If you have a WebKit browser, scroll to the top and enter the Konami code for an impressionistic version of the same thing.

I guess I'm now the proud owner of the first unofficial CSS 3D ‘ACID’ test. I'm eager to see how the next browser handles it. If it ends up being a silly idea in the long run, I can always just switch the output to WebGL, but for now I'm willing to run with it. I put in a universal CSS 3D detector and prefixes for all the major browsers.

For non-CSS 3D browsers, I simply rendered the header into a static image. It's not as fun without the shifting perspective, but it adds its own kind of optical illusion as you scroll down.

### Putting it all together

To power the site, I got rid of Drupal and replaced it with the nimble [Jekyll](http://jekyllrb.com/). Hat tip to [James Walker](http://walkah.net/), who did the same thing just a few days earlier and put all the code on GitHub to learn from.

I've been really impressed with Jekyll's simple workflow, and though it's all static HTML, it's a refreshing change of pace. And thanks to client-side JS, it doesn't preclude adding interactive elements at all. I can treat my site as just a database of documents retrievable over HTTP, and wrap the logic around that.

So I created a nice client-side navigator that transitions between pages, using 2D transforms, which also work on Firefox. It uses the HTML5 pushState API and replaces regular links with AJAX requests. Aside from being a faster way to navigate around, it also lets me link up multiple articles in a series elegantly. When you go back to a previous screen, it literally presses the browser's back button, thus avoiding creating a long, useless history trail. You go back exactly the way you came, scrolling back to where you were, just like the real back/forward buttons do. For example, click over to my [Making Worlds](https://acko.net/blog/making-worlds-introduction/) series of posts. You can come back right away.

I didn't use any libraries or router frameworks for this, simply because I wanted to have done it all myself at least once. As it now says on my [About page](https://acko.net/about), quoting Feynman: *"What I cannot create, I do not understand"*. The only way to grok the intricacies of something like browser history state, which we all use every day, is to dive in and replicate it. Otherwise, you'll just take carefully choreographed behavior for granted and your mental model will be incomplete.

To keep code size down, I compiled a custom build of Three.js with only the parts I need. I also used YUI compressor to minify the CSS and JS. However, I don't mean to obfuscate the code: the important bits will make their way onto Github soon enough.

*Update: The CSS 3D renderer and editor are now available on GitHub.*

### And Done?

I migrated over most of the content and did some house cleaning while I was at it. Most things should be back, but further fixes will be made. I also haven't implemented any commenting solution so far, but I'll be adding it back somehow as soon as I figure something out. In the mean time, there's [a Google Plus thread](https://plus.google.com/112457107445031703644/posts/HDJMgpDRAey).

The final result looks like something that would perhaps once unironically be labeled **The Information Superhighway** in a magazine from the 90s, though with less neon green. I like it.