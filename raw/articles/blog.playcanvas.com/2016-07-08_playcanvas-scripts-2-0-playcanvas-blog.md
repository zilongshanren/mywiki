---
title: PlayCanvas Scripts 2.0 | PlayCanvas Blog
url: https://blog.playcanvas.com/playcanvas-scripts-2-0
author: Dave Evans
published: '2016-07-08'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

We've just launched "Scripts 2.0", a complete re-design and re-implementation of the scripting system for PlayCanvas applications. Our goals were to fix an array of small irritations that had built up over using the PlayCanvas scripting for the last few years and take the opportunity to clean up the interface and simplify the creation and usage of scripts.

Here's a list of the improvements you can enjoy with the new script system:

- rapid iteration by hot-swapping code at run-time
- real-time collaborative code editing
- script concatenation and minification for publishing
- better error handling and fault tolerance
- full folder support for script assets
- multiple script definitions in a single file
- simpler interface and boilerplate

### Live Hot-swapping[](https://blog.playcanvas.com#live-hot-swapping)

If you choose to, you can now allow your scripts to update all running instances of your application. We dynamically reload scripts after they change. By implementing a single `swap()`

function, you can transfer state into your new script instance and carry on as if nothing had happen. Except you've got all your new code!

### Real-time Collaborative Code Editing[](https://blog.playcanvas.com#real-time-collaborative-code-editing)

Now that scripts are first-class assets, we now support real-time collaboration in the Code Editor. This means you're no longer in danger overwriting other people's code. In fact, you can see it appear as they type.

To help support this, we've also improved the error handling and fault tolerance of scripts while they're running. This means bad scripts won't bring your game screeching to a halt, preventing everyone from working.

### Script Concatenation[](https://blog.playcanvas.com#script-concatenation)

With the new script format we now support multiple script definitions in a single JavaScript file. We've added the option to concatenate and minify all your scripts into one file when you publish. This will save you many HTTP requests and reduces the size of your application, making for a much quicker start up time.

### Try it Now[](https://blog.playcanvas.com#try-it-now)

Scripts 2.0 is live right now and any new projects you create will have the new script system enabled. However, if you're not quite ready to move to the new system or you need some of the features that are currently only available with the old system, you can still create projects using the "Legacy Script System". Look for the option in the new project dialog.

If you haven't tried PlayCanvas before: