---
title: JAL – Just Another Loader for JavaScript – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/11/jal-just-another-loader-for-javascript/
author: Helgi Kristjansson
published: '2012-11-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A long time ago I saw the film "Interview with the vampire" starring Tom Cruise, Brad Pitt and Kirsten Dunst. The scene that struck me the most is when Pitt's character realizes that Lestat is using him in order to adapt to the current age. For a developer this is not a very bad rule. In fact it is actually quite good. If you want to keep up and stay on top, follow the bleeding edge, experiment and copy what others are doing. Reverse engineering and reinventing the wheel is a bliss. Apply this to open source and we – developers, hackers, designers – have a wide array of tools at our hands. Just think of "View Source" in the Web Browsers. Without it we wouldn't be where we are today. Copying is learning. Inventing is impossible without standing on the shoulders of our predecessors.

The company where I work, [Tail-f Systems](http://www.tail-f.com) has just recently open sourced a small JavaScript library called [JAL](https://github.com/tail-f-systems/JAL), which is an acronym for *Just Another Loader*. This is an infant project, it lacks certain features but does the job and does it well. It is, as the name implies, a tool for parallel conditional dependency loading of resource files. We use it in our Web UI for loading scripts and CSS files. It is there for one reason only: To speed things up!

We tested [YepNope](http://yepnopejs.com/), which is a great loader, but felt it could be faster. It also had features we didn't really need. So we wrote our own. We reinvented the wheel. How hard could it be? Well, it was pretty hard.

What we needed was a resource loader that could load, not only JavaScript but stylesheets as well. It also needed to be able to load resources in parallel and in groups to handle dependencies, such as loading jQuery before loading a jQuery plugin. The final requirement was conditional loading, i.e. load JSON.js if the browser is lacking native JSON support.

## Parallel dependency loading

A typical setup looks something like this:

```
$loader
.load('js/shape.js')
.load([
'js/circle.js'
, 'js/rectangle.js'
])
.load('js/square.js')
.ready(function() {
// Start app
})
```

There are three dependency groups set up. The first one loads a shape. The second loads a circle and a rectangle, which are dependent on shape. The last group contains a square which is derived from a rectangle. In this trivial example, the speedup happens in the second group since the circle and the rectangle are loaded in parallel. Now, imagine you have a large number of scripts with different dependencies in your application. The traditional way is to concatenate all the scripts into one large bundle and then minify that bundle. What you are actually doing is that you are loading your scripts the old fashioned way, one after another. Modern browser are capable of loading scripts and resources in parallel. They actually open up multiple connections to a web server and load multiple resources all at the same time. So if you have a script that takes, say, 5 seconds to load and you break that into 5 pieces and load the pieces in parallel the loading time becomes, theoretically, 1 second. That is five times faster than before!

## Conditional loading

Now to conditional loading. Conditional loading is where you load a resource if a certain condition is met. Does the browser have native JSON support? No? Well, we'll fix that! Here's an example of loading a JSON polyfill:

```
$loader
.when(typeof window.JSON === 'undefined', function(loader) {
loader.load('js/json.js')
})
```

## Done is done

Once a resource group has loaded, JAL allows you execute code. Here is an example where the "ready" event in jQuery is halted until all scripts have loaded.

```
$loader
.load('js/jquery.min.js')
.done(function(){
// Stop jQuery from triggering the "ready" event
$.holdReady(true)
})
.load([
'js/script-one.min.js'
, 'js/script-two.min.js'
])
.ready(function() {
// Allow jQuery to trigger the "ready" event
$.holdReady(false)
// Start app
})
```

## How it was done

Writing JAL was both challenging and fun. The most difficult part was to make sure that the load order was respected between the groups. This was tricky since things were happening fast and there was a big performance difference between the browsers.

JAL was implemented using a resource queue and a polling function. The queue is locked until a resource group has been loaded. Once loaded the "done" event is fired. This allows you to inject one or more resource groups to the front of the queue, if you ever need that. After the "done" event has been triggered the queue is unlocked and the poller is free to load the next resource group.

The poller itself is started once the loader sequence has been executed. This is done by pushing the poller to the top of the script stack using `setTimeout`

with a timeout of 0 milliseconds. It's a classic example of how the single threaded model of a web browser’s JavaScript engine can be used.

## Closing words

Do you have a large concatenated JavaScript file? Is it minified and gzipped? Is it loading fast? Do you want faster? Then minify and gzip your resource files individually and use a conditional parallel dependency loader instead.

## About Helgi Kristjansson

Helgi Kristjansson is a JavaScript viking hailing from Iceland. He invaded Sweden in 1998 where he has worked mainly developing web based user interfaces in hardware related industries. His current employer is [Tail-f Systems](http://www.tail-f.com) - a Stockholm based company. You can reach Helgi on Twitter at [@djupudga](https://twitter.com/djupudga)

## 7 comments

Colin JackNovember 22nd, 2012 at 04:54JohanNovember 22nd, 2012 at 05:24Helgi KristjanssonNovember 22nd, 2012 at 07:17Steve SoudersNovember 22nd, 2012 at 11:49Helgi KristjanssonNovember 22nd, 2012 at 13:13JorisWNovember 23rd, 2012 at 07:52Brett ZamirNovember 28th, 2012 at 21:27