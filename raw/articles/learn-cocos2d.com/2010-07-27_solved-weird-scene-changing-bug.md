---
title: '[Solved] weird scene changing bug…'
url: http://www.learn-cocos2d.com/2010/07/weird-scene-changing-bug/
author: Chris Cockcroft says
published: '2010-07-27'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I need help. I’ve run into strange problems with a very simple cocos2d v0.99.4 project created from the cocos2d project template. It’s two scenes with a layer each, much like the regular HelloWorldScene layer. Each scene is simply supposed to replace itself with the other scene, on touch. What happens is that the first scene started with runWithScene is never deallocated after the first scene change. So it stays in memory and keeps receiving the touches, which means a touch is always behaving as if switching from the first to the second scene.

What’s more, if I add the onEnter and onEnterTransitionDidFinish methods to the first scene, without adding any code to them, the first scene/layer doesn’t receive any touch events at all. The second scene doesn’t show this behavior and works fine with these methods implemented.

Maybe I’m just overlooking the very obvious, if you could take a look and let me know if there’s anything I’m doing wrong with this code please let me know! Thank you.

Download the code here: [ScenesAndLayers02](https://www.learn-cocos2d.com/wordpress/wp-content/uploads/ScenesAndLayers02.zip)

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hey Steffen,

Your missing your calls to ‘super’ in -onEnter, -onEnterTransitionDidFinish, and -onExit - drop those in and everything runs great.

Chris

Great!! That’s it! I knew it was something stupid I was forgetting. I’ll be sure to mention that in the book, it’s one of the many caveats you only learn by making the mistake.

Oh - and I think the simulator always leaks something. The device should be fine (though I didn’t test it).

Chris