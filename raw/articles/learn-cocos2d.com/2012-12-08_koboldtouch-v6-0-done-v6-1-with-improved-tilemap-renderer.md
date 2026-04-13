---
title: KoboldTouch v6.0 Done – v6.1 with improved Tilemap Renderer
url: http://www.learn-cocos2d.com/2012/12/koboldtouch-v60-v61-improved-tilemap-renderer/
published: '2012-12-08'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I completed [KoboldTouch v6.0](http://www.koboldtouch.com/) today. Time to let you know what changed and what will be coming for v6.1.

#### KoboldTouch v6.0 - Foundation

This version mostly included changes moving from Kobold2D to KoboldTouch. I had already **removed superfluous libraries**, so KT now only includes Cocos2D with CocosDenshion and the Cocos2D extensions project, the Kobold2D and KoboldTouch source code obviously and Box2D.

But there’s more of course:


The installer now installs KoboldTouch to /Applications where it belongs. From /Applications/KoboldTouch-6.x.x you merely create or upgrade projects with the starter and upgrader tools, or open the offline documentation files. Your projects are completely separate from the KT installation.

There’s also **two flavors of the installer** now: with or without offline HTML and Xcode docset documentation files. One is a 200 MB download, the other is just 7 MB - while the size of the documentation files more than doubled after upgrading doxygen & dot, the size of KoboldTouch itself shrank by removing everything that isn’t strictly necessary to build projects (ie unit tests, demo projects, example resource files, unused code, etc).

The project starter tool now **creates new projects in a custom folder** of your choosing, likewise the project upgrader will upgrade projects in custom locations. The custom folder locations and the **trimming of the project size** - new project sizes are typically less than 10 MB - are a tremendous improvement for those who use source control.

For my own convenience I improved the tool that creates the installer. It now also uploads the installer, updates the download page and the API reference documentation. I merely have to start the process (takes 1-2 hours) instead of wasting time managing it myself.

#### KoboldTouch v6.1 - Better Tilemap Renderer

The KoboldTouch users have voted for a better (orthogonal) tilemap renderer. It won the vote (16) against Box2D Objective-C API (8) and OS integration (5). I’ll start working on it next week, and expect to complete the task by February/March.

Better how?

Cocos2D’s tilemap renderer is extremely limited. It draws all tiles of the tilemap, whether they’re on screen or not. Performance suffers even for moderately sized tilemaps. The KoboldTouch tilemap renderer fixes that, it **only renders the visible tiles**.

Scrolling in general and **parallax scrolling of tilemap layers** specifically will be built-in. You just tell it where to scroll to, and how fast. **Retina resolution support and arbitrary scaling** is also built-in. No need to rescale TMX files, no need to create multiple versions of the same tilemap. Just provide -hd / -ipad / -ipadhd tileset image files as needed.

The KT Tilemap renderer will use documented properties editable in Tiled to help you customize the Tilemap from within Tiled, for example to **spawn objects**, **animate tiles**, etc.

You’ll even be able to **use .pvr.ccz textures** with KT tilemaps for faster loading times. Members have suggested that streaming tilemaps is something they like to be able to do, so using .pvr.ccz will come in handy since they load several times faster than PNG files.

Whether I’ll get to actually implement a true streaming tilemaps in v6.1 depends on how much time the other tasks take. I’ll certainly **look into automating tilemap transitions** tilemaps - for example if you leave a tilemap to one side, there’ll be a way to specify which tilemap to load next. Perhaps loading the other tilemap is so fast it can be used as a way to divide the world seamlessly into submaps.

While implementing these features I’ll develop an actual (albeit simple) game around it as both a **starting template** and to eat my own dogfood. At the end I’ll write a **tutorial detailing how the example game was constructed**.

Of course the tilemap renderer and example game project will be built within the KoboldTouch MVC framework implementing MVC best practices.

#### Join KoboldTouch

If you’re even remotely interested in using tilemaps for your game, [join KoboldTouch](http://www.koboldtouch.com/) and help steer development in the right direction. I’m working on what KoboldTouch members need first and foremost.

I’m now working full-time on KoboldTouch. Expect lots of progress. You can [keep track of KoboldTouch development here](https://www.pivotaltracker.com/projects/678389) or by following [@Kobold2D_Dev](https://twitter.com/Kobold2D_Dev).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |