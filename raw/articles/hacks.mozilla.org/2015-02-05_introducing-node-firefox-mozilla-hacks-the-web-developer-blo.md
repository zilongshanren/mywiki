---
title: Introducing node-firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/02/introducing-node-firefox/
author: Soledad Penadés
published: '2015-02-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**NOTE:** we presented this project last Sunday at FOSDEM, but not everyone could make it to Brussels, so here’s a post explaining what [node-firefox](https://github.com/mozilla/node-firefox) is and how can it help you **superturbocharge your Firefox OS app development**!

At Mozilla we’re always looking for ways in which we can make developers’ lives easier. When aspiring app developers told us that it was cumbersome to get started writing [Open Web Apps](https://developer.mozilla.org/Apps/Quickstart/Build/Intro_to_open_web_apps), we worked on turning [App Manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager) into a more beginner friendly environment, which in turn gave way to [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE). This tool simplifies many actions that were slow and tedious before, such as creating a new app, downloading and installing simulators or running and debugging apps.

But there was still a segment of developers that felt left out: power users! They already have their node.js-based build toolchains, with tasks such as asset optimisation, code hinting, or test running. They often also use tools such as [Browserify](http://browserify.org/), and perhaps they don’t even write JavaScript, favouring alternatives such as CoffeeScript instead, but all these goodies require you to build the app or website before you push it again to your device or reload the browser.

Essentially, we were telling these developers to leave their beloved command line (or editor shortcuts!) to go to WebIDE and click a button to deploy the app, and then go back to their editor of choice. And they most unanimously answered: “But we don’t like to click! We like the terminal!”

## How can we make this more efficient?

People didn’t like this because it implied changing contexts. It is inefficient, we are engineers, and if there one thing that engineers like more than building new things it is probably **optimising and streamlining processes**.

Since we already have a build script, the only step that is left in order to get our apps onto the runtime is **deploying**, and that’s what we are using WebIDE for. So the obvious question would be: can we do whatever WebIDE is doing to deploy, but programmatically?

## Servers and actors

Every Firefox runtime has something called the [remote debugger server](https://developer.mozilla.org/en-US/docs/Tools/Remote_Debugging). This is not enabled by default, for obvious security reasons, but when enabled, *clients* can connect to it and take advantage of its various functionalities, such as installing apps, accessing the console, etc. And this is what WebIDE does [internally](http://mxr.mozilla.org/mozilla-central/source/toolkit/devtools/apps/app-actor-front.js#235).

Each of these functionalities is provided by an actor. For example, suppose we want to list the installed apps. We would…

- first find the
`webApps`actor - then run the
`getAll`command - and get a list of apps in response

Another example would be installing a packaged app. The steps would be:

- first zip the app contents, using whatever library or way you like
- then get the
`webApps`actor - call the
`uploadPackage`command in the`webApps`actor with the contents of the ZIP file - the result of this call is a
`File`actor - call the
`install`command in the`webApps`actor with the returned`File`actor - done!

Therefore all the *magic* for installing apps is not in WebIDE—it is in the *servers*! We can take advantage of this magic programmatically, but building a client from scratch involves establishing TCP connections and parsing packets, which is **not** what you want to be doing: you want to write apps and push them to devices instead!

Despair not, as [node-firefox](https://github.com/mozilla/node-firefox) will abstract that for you. It is not a monolithic piece of code, but a series of node.js modules, each one of them performing a different task, hosted on its own separate repository and published to the [npm registry](https://www.npmjs.com/) like good module citizens. You can use as many of them as you need in your scripts or task runners, and thus you can *finally* build and run your app without ever leaving the command line.

## Show, don’t tell

But enough of talking and describing; let’s see how to write a script that starts a simulator!

First install the module in your project, using npm:

```
npm install --save node-firefox-start-simulator
```

And this would be the script:

```
var startSimulator = require('node-firefox-start-simulator');
startSimulator({ version: '2.2' })
.then(function(simulator) {
console.log('Listening in port', simulator.port);
});
```

That’s it! With just a few lines of code you are able to programmatically start a version 2.2 simulator. If you don’t care about the version, just don’t pass in any option to `startSimulator`, and it will start the first simulator it finds:

```
startSimulator().then(function(simulator) {
// your code
});
```

We can also see this in action. Here’s us starting a simulator, installing an app and launching it, all from a node.js script:

![Starting simulator, running app from node.js](../../assets/92edf84f521f761d.gif)


The code for this example is actually the example for the ` node-firefox-uninstall-app` module. Each of the

`node-firefox`modules come with an

`examples`folder so you can get started rather quickly.

As we mentioned at the beginning, many web developers that move to app development want to keep using their task runners, so we also wrote an example of how to use `node-firefox` with [gulp](http://gulpjs.com/).

Let’s run the `default-one` task. This starts a simulator, deploys an app, and for a bit more of a challenge, also keeps watching for CSS changes. If you edit and save any of the app’s stylesheets, the file watcher will detect the change, and send the new file contents to the runtime, which will replace them on the fly, without having to stop, push and relaunch the whole app. Look at me changing the background colour from austere dark blue to the timeless [Paul Rouget](http://paulrouget.com/) pink!

![Starting simulator, launching app with gulp](../../assets/59732aa27328a4eb.gif)


Live CSS reloading is really great to build and experiment with UI interfaces. Not having to reload the app and then navigate to the particular layout you want to work in saves lots of time—I wish I’d had that when I was programming Android apps!

But we can outdo this. The `default-all` task will do the same as `default-one`, but for all the simulators installed in your system, so you can see the effect of your CSS changes in all the simulators at the same time:

![Starting all simulators, launching app and live CSS reload with gulp.](../../assets/73cf6d07487adec0.gif)


Unfortunately there is [a bug](https://github.com/mozilla/node-firefox-reload-css/issues/1) in the 2.1 and 2.2 simulators, and those don’t reload the stylesheet changes, but it’s been filed and will be fixed.

## What can we do so far?

The current set of modules lets you [find ports where runtimes are listening](https://github.com/mozilla/node-firefox-find-ports), [find](https://github.com/mozilla/node-firefox-find-simulators) and [start simulators](https://github.com/mozilla/node-firefox-start-simulator); [connect](https://github.com/mozilla/node-firefox-connect) to runtimes; [find](https://github.com/mozilla/node-firefox-find-app), [install](https://github.com/mozilla/node-firefox-install-app), [uninstall](https://github.com/mozilla/node-firefox-uninstall-app) and [launch](https://github.com/mozilla/node-firefox-launch-app) apps, and [reload stylesheets](https://github.com/mozilla/node-firefox-reload-css).

## Philosophy

You might have noticed a pattern already, but just in case it wasn’t evident enough, we are trying to write **deliberately simple modules**. Each module should perform only one action, return a Promise and use as few dependencies as possible.

Small modules are easier to understand, use, and test. Also, most of the future Web APIs are designed to work with [Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), and we want to write code for the future, not for the past. In addition, reducing the number of dependencies also makes it easier for new people to get started on contributing to a module, as there are fewer new unfamiliar elements to understand.

Finally, since all the modules work the same way, when you know how to use one module you know how to use the rest—the only thing that changes is the parameters, and the result.

## Dream ideas (or: what we cannot do yet)

There’s a number of things that we’d like to see happen in the future. Some people call them features, but I call them ‘dream ideas.’

A recurrent one is the **WebCLI**: a counterpart equivalent to WebIDE, where everything you can do with WebIDE could be done with a command line tool. I keep switching back and forth between “this is a good idea” and “perhaps we don’t need this at all and a library of tasks will be enough”, but people seemed to like the idea, so maybe it’s not that bad!

Another great feature would be the ability to **attach the DevTools debugger** to an app that was launched from the command line but that just crashed. Launching apps from the command line is great, but command line debuggers are not that exciting! Why not use the best of both worlds?

Or maybe it would be neat to **control any browser from the command line**, interfacing via

[Valence](https://developer.mozilla.org/en-US/docs/Tools/Valence)!

And finally, there is my favourite dream idea: **Firefox OS custom editions**. Imagine if we could just write a script that would create an empty Firefox OS slate, pull in our favourite apps and settings, and generate a whole Firefox OS image that we could then flash to devices. And since it is not a binary blob but a *script*, we could just publish it on its repository, and other people could remix and build their own Firefox OS based editions.

## How do we get there?

There’s still a long way ahead of us, and lots of areas that need work. Perhaps the most urgent task is to get better multiplatform support. Currently we can only interact with runtimes through the network, but no physical devices. Also, support on platforms other than Mac OS is largely lacking.

Testing is another important aspect. If we test early, often and profusely we will be able to detect problems such as the CSS bug I stumbled upon when building the gulp demo. We want to have these modules running on several platforms and connecting to other different platforms, including physical devices.

Of course we need more modules, and more examples! To make sure no two people start writing the same module, we are discussing and proposing [new modules](https://github.com/mozilla/node-firefox/labels/new-module) in the top project issue tracker. And we’d love to see more examples, or even just *better* examples that hook existing functionality in other node modules with our code. For example, one could add manifest validation via the [firefox-app-validator-manifest](https://github.com/mozilla/firefox-app-validator-manifest) module.

And, as always, we need **you**. We are not *you*, so we cannot know what you need or what thoughts cross your mind. And we certainly cannot use software the same way you use it either. We need your input and your contributions!

We’re looking forward to seeing what you create with [node-firefox](https://github.com/mozilla/node-firefox). [File issues](https://github.com/mozilla/node-firefox/issues), or talk to us on irc if you have questions. We hang out mostly in the #apps and #devtools channels in irc.mozilla.org.

## Thanks

It would be dishonest not to thank Nicola Greco, whom I mentored last summer when he was interning at Mozilla. He came up with the initial idea of building individual node modules that would help you develop Firefox OS apps. Go check out [his final intern presentation](https://air.mozilla.org/nicola-greco-node-fxos-ninja-tools-for-firefoxos-development/), as it’s really entertaining and illustrative!

Many thanks to all the (infinitely patient) *DevToolers* Ryan Stinnet, Alexandre Poirot, Jeff Griffiths and Dave Camp, who helped us find our way around remote servers and actors and whatnot, and huge thanks to [Heather Arthur](https://github.com/harthur/) who wrote [firefox-client](https://github.com/harthur/firefox-client) and made writing `node-firefox` way more pleasant than it would have been otherwise.

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org

## 13 comments

HervéFebruary 5th, 2015 at 09:00Soledad PenadesFebruary 5th, 2015 at 09:43Ivan DejanovicFebruary 5th, 2015 at 12:15FritzFebruary 5th, 2015 at 15:08Ben AdamsFebruary 5th, 2015 at 18:07soleFebruary 9th, 2015 at 04:01Moez BouhlelFebruary 5th, 2015 at 23:40LucianFebruary 6th, 2015 at 02:43MartinFebruary 6th, 2015 at 04:26IvanFebruary 8th, 2015 at 11:48Soledad PenadesFebruary 9th, 2015 at 04:05Miguel MotaFebruary 7th, 2015 at 01:40BhumiFebruary 10th, 2015 at 03:35