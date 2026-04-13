---
title: Debugging GLSL
url: http://hacksoflife.blogspot.com/2010/01/debugging-glsl.html
author: Benjamin Supnik
published: '2010-01-27'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[past post](http://hacksoflife.blogspot.com/2006/01/debugging-opengl.html):

There are only two debugging techniques in the universe:Is that true when writing GLSL shaders? Yep. Commenting out things is natively available. What about printf? The GLSL equivalent of printf is

- printf.
- /* */

`gl_FragColor.rgba = vec4(stuff_i_want_to_see,...);`


That is, you simply output an intermediate product to the final color, run your shader, then view something else. This is how I debug some of the more complex shaders: I view each product in series to confirm that my intermediate values aren't broken. Since the sim is running at 30 fps, I can move the camera and confirm that the values stay sane through a range of values.The numeric output is often not in a visible range - to get around that I often use a mix of abs, fract (to see just the lowest bits), scaling, and normalize() to sanitize the output.

One app feature is critical: make sure you can reload your shaders in a heart-beat. In X-Plane we have a hidden menu command to do this. This way, you can move your printf, recompile the shaders, and see the change.

A visual debugger is a useful tool for debugging C/C++ because you don't have to commit to what you will view before compiling - you can just print any intermediate product from the debugger. For GLSL, make the recompile cycle fast, and you'll be able to simply edit the code in near-realtime.

Have you tried this?

ReplyDeletehttp://www.vis.uni-stuttgart.de/glsldevil/

It is a bit old (last version was in 2005) but GLIntercept has this "edit and continue" support for GLSL.

ReplyDeleteIs it really that hard for nVidia or the like to implement a "printf" function in shaders?

ReplyDeletemaybe it is

ReplyDeleteThe driver writers have to write code that is:

ReplyDelete- Perfectly correct.

- As fast as possible.

- Finished as soon as possible once the hardware is revved (read: every nine months).

So I would say: if X is possible in app-space, it is always harder for X to be done in driver space than app space, due to the unique requirements of driver writing.

I would like to know where this "hidden menu" can be found. Is it also available for external developers?

ReplyDeleteX-Plane's private commands for testing are not exposed to third parties - the plugin that brings up the UI is entirely proprietary.


ReplyDeleteFor parts of the internal interface that are useful to developers (e.g. the texture browser) they are exposed via private datarefs (which the public dataref editor tool will show you).