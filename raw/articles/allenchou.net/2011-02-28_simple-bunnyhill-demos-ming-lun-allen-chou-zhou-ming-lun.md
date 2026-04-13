---
title: Simple Bunnyhill Demos | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/02/simple-bunnyhill-demos/
author: Allen Chou
published: '2011-02-28'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

As you may have heard, Flash Player Incubator is available now. This means you can view Flash contents powered by the Molehill API! Yeah for GPU-accelerated Flash movies!?[Richard Davey](http://www.photonstorm.com/) has posted [an article](http://www.photonstorm.com/archives/1172/flash-player-11-molehill-monster-link-round-up) full of awesome Flash Player 11 Molehill demos. Be sure to check out the stunning 3D visuals.?In order to view the Molehill-powered Flash contents, you’ll need to download and install the Flash Player Incubator, available at [Adobe Labs](http://labs.adobe.com/technologies/flashplatformruntimes/incubator/).

I’ve created two simple demos for Bunnyhill, my upcoming 2D rendering engine based on the Molehil API. One demonstrating the scene graph structure of Bunnyhill, and one demonstrating the integration of [Stardust](https://allenchou.net/code.google.com/p/stardust-particle-engine/) with Bunnyhill.

You may download the current revision of Bunnyhill [here](http://www.cjcat.net/wp-content/uploads/2011/02/Bunnyhill.zip) ([CJSignals](http://code.google.com/p/cjsignals/) is also required). Please notice that this revision is still a work in progress, so anything is subject to future change. This source should only be used to compile the following two demos.

Also, you need to do some setup for FlashDevelop in order to make it work properly.?[Michael Baczynski](http://lab.polygonal.de) posted an [article](http://lab.polygonal.de/2011/02/27/simple-2d-molehill-example/) on how to set things up.

**Bitmap Drawing**

[View online](http://www.cjcat.net/wp-content/2011/02/20110228/DrawBitmap/index.html) (requires Flash Player 11)

This demo shows the scene graph structure in Bunnyhill. Each renderer has a scene graph, which is traversed by the render visitor on each render call.

Here’s a code snippet from the main class. A `Group`

node acts as the root node and contains several `Transform`

nodes, which all contain a common `DrawBitmapData`

child node.

group = new Group(); group.add(new Clear()); draw = new DrawBitmapData(new Pic2().bitmapData); for (var i:int = 0; i < 8; ++i) { for (var j:int = 0; j < 8; ++j) { var t:Transform = new Transform(draw); t.rotation = 22.5 * (j + i * 4); t.position.set(125 * i + 62.5, 100 * j + 50); t.center.set(125, 100); group.add(t); } } renderer.rootNode = group;

The root node in this demo is a?`Group`

node, which simply pass the render visitor to its children. The `Transform`

node pushes a transform matrix onto the render visitor’s matrix stack, pass the render visitor to its only child, and then pops the matrix out off the stack. Finally, the `DrawBitmapData`

node is what draws things onto the stage, it draws images based on the top matrix of the matrix stack.

Notice how only one `DrawBitmapData`

node is used in the scene graph, being a common child of all `Transform`

nodes. This is the power of scene graph structure, saving unnecessary memory usage. This is different from Flash Player’s native display list structure, which forces each display object to have only one parent. So if you want to draw two identical shapes onto the stage at different locations, you’ll need to instantiate two such objects.

**Nova**

[View online](http://www.cjcat.net/wp-content/2011/02/20110228/Nova/index.html) (Flash Player 11 required)

Bunnyhill currently provides a quick implementation of a particle handler to work with Stardust. This demo uses this particle handler to link both libraries together.

var group:IGroup = new Group(); emitter.particleHandler = new BHGroupHandler(group); renderer.rootNode = new Group( new Clear(), new BlendAdd(), group );

That’s it. I’m pretty happy to see how far Molehill has gone. I’ll keep working on Bunnyhill in order to provide an easy-to-use, GPU-accelerated 2D rendering API.

hi i am using the fp11 beta (not the incubator) and i have a blank screen 🙁

This example was targeted for the FP11 prerelease version one year ago, so many things might have changed.

Wow, this looks great. If I didn’t have game projects already going, I’d dive directly into this FP11 stuff. Can’t wait for the real FP11 release so I can make money from Molehill powered games!

Sorry.. still having problems 🙁

idv.cjcat.bunnyhill.shaders folder is empty so my Bunnyhill swc won’t compile the same as yours.

RenderBufferPool.as getKey returns a uint instead of a String.

_visitor is still null in line 115 of “_visitor.onStageResize.dispatch(_width, _height);” or Renderer.as

I’m fairly sure I cranked it up with the newest versions of everything.

Hmm…That’s weird. I’ve re-uploaded everything again. See if this works for you. As for the error, I’ve never encountered it before; don’t know what’s going on 🙁

You rock! I’ll check it out straight away 🙂

That helped 🙂

Still Renderer.as line 115 null object. It’s bedtime so no debugging for me until morning 🙂

Could you put up a link to BitmapDrawing with the swcs or source included?

I’ve updated the zip files. The required Bunnyhill source and SWC files are included, and the example FlashDevelop projects compile correctly.

Also, for your convenience, I’ve uploaded two HTML pages (see the new links in the post) in which you can directly view the SWF files online.

Can I grab this file from you? [Fault] exception, information=VerifyError: Error #1014: Class idv.cjcat.signals::ISignal could not be found.

Seems that not everything is included in the revision of Bunnyhill to compile the demos.

Can’t wait to get it working though!

Oh, I forgot to include the required SWC file for CJSignals. You can find it here. http://code.google.com/p/cjsignals/

Pingback: Uza's Blog – Adobe Flash & AIR » Incubator News Roundup (Molehill)

Great work! Would love if your able to post videos of it’s progress. I know it’s a hassle, but it allows us to quickly see your progress without having to setup an install. Massive MASSIVE props for working on a 2D engine.

Yeah, I’m planning on doing that after Bunnyhill goes public.