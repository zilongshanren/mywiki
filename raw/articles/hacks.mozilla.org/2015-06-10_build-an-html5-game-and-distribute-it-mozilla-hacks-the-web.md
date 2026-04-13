---
title: Build an HTML5 game—and distribute it – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/06/build-an-html5-game-and-distribute-it/
author: Mozilla
published: '2015-06-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last year, Mozilla and Humble Bundle brought great indie titles like FTL: Faster Than Light, Voxatron, and others to the Web through the Humble Mozilla Bundle promotion. This year we plan to go even bigger with developments in JavaScript such as support for [SIMD](https://docs.google.com/presentation/d/1yc2NDzFJ-0yD980URiTcV3oE_2cQDVzXuH4Rss1fG8s/present#slide=id.p19) and SharedArrayBuffer. Gaming on the Web without plugins is great; the user doesn’t have to install anything they don’t want, and if they love the game, they can share a link on their social media platform du jour. Imagine the kind of viral multiplayer networking possibilities!

Lately, [I’ve been focusing on real-time rendering with WebGL](https://nickdesaulniers.github.io/RawWebGL/#/) and while it is quite powerful, I wanted to take a step back and look at the development of game logic and explore various distribution channels. I’ve read a few books on game development, but I most recently finished *Build an HTML5 Game* by Karl Bunyan and thought I’d share my thoughts on it. Later, we’ll take a look at some alternative ways other than links to share and distribute HTML5 games.

### Book review: *Build an HTML5 Game*

is meant for developers who have programmed before; have written HTML, CSS, and JavaScript; know how to host their code from a local server; and are looking to make a 2D casual game. The layout presents a good logical progression of ideas, starting small, and building from work done in previous chapters. The author makes the point that advanced 3D visuals are not discussed in this book (as in WebGL). Also, the design of familiar genres of game play mechanics are avoided. Instead, the focus is on learning how to use HTML5 and CSS3 to replace Flash for the purpose of casual game development. The game created throughout the chapters is a bubble shooter (like the Bust A Move franchise). Source code, a demo of the final game itself, and solutions to further practice examples can be found online at:

[Build an HTML5 Game (BHG)](http://buildanhtml5game.com/)

[buildanhtml5game.com](http://buildanhtml5game.com/).

I would recommend this book to any junior programmer who has written some code before, but maybe has trouble breaking up code in to logical modules with a clean separation of concerns. For example, early on in my programming career, I suffered from “monolithic file” syndrome. It was not clear to me when it made sense to split up programs across multiple files and even when to use multiple classes as is typical in object-oriented paradigms. I would also recommend this book to anyone who has yet to implement their own game.

The author does a great job breaking up the workings of an actual playable game into the Model-View-Controller (MVC) pattern. Also, it’s full of source code, with clearly recognizable diffs of what was added or removed from previous examples. If you’re like me and like to follow along writing the code from technical books while reading them, the author of this book has done a fantastic job making it easy to do.

The book is a great reference. It exposes a developer new to web technologies to the numerous APIs, does a good job explaining when such technologies are useful, and accurately weighs pros and cons of different approaches. There’s a small amount of trigonometry and collision detection covered; two important ideas that are used frequently in game development.

Another key concept that’s important to web development in general is graceful degradation. The author shows how [Modernizr](http://modernizr.com/) is used for detecting feature support, and you even implement multiple renderers: a canvas one for more modern browsers, with a fallback renderer that animates elements in the DOM. The idea of multiple renderers is an important concept in game development; it helps with the separation of concerns (separating rendering logic from updating the game state in particular); exposes you to more than one way of doing things; and helps you target multiple platforms (or in this case, older browsers). Bunyan’s example in this particular case is well designed.

Many web APIs are covered either in the game itself or mentioned for the reader to pursue. Some of the APIs, patterns, and libraries include: [Modernizr](http://modernizr.com/), [jQuery](http://jquery.com/), CSS3 [transitions](https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Using_CSS_transitions)/[animations](https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Using_CSS_animations)/[transforms](https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Using_CSS_transforms), [Canvas 2D](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API), [audio tags](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio), Sprite Atlases, DOM manipulation, [localStorage](https://developer.mozilla.org/en-US/docs/Web/Guide/API/DOM/Storage#localStorage), [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame), [AJAX](https://developer.mozilla.org/en-US/docs/AJAX), [WebSockets](https://developer.mozilla.org/en-US/docs/WebSockets), [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers), [WebGL](https://developer.mozilla.org/en-US/docs/Web/WebGL), [requestFullScreen](https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullScreen), [Touch Events](https://developer.mozilla.org/en-US/docs/Web/API/Touch_events), [meta viewport tags](https://developer.mozilla.org/en-US/docs/Mozilla/Mobile/Viewport_meta_tag), [developer tools](https://developer.mozilla.org/en-US/docs/Tools), security, obfuscation, “don’t trust the client” game model, and (the unfortunate world of) vendor prefixes.

The one part of the book I thought could be improved was the author’s extensive use of absolute CSS positioning. This practice makes the resulting game very difficult to port to mobile screen resolutions. Lots of the layout code and the collision detection algorithm assume exact widths in pixels as opposed to using percentages or newer layout modes and measuring effective widths at run time.

### Options for distributing your game

Now let’s say we’ve created a game, following the content of *Build an HTML5 Game*, and we want to distribute it to users as an app. Personally, I experience some form of cognitive dissonance here; native apps are frequently distributed through content silos, but if that’s the storefront where money is to be made then developers are absolutely right to use app stores as a primary distribution channel.

Also, I get frequent questions from developers who have previously developed for Android or iOS looking to target Firefox OS. They ask,*“Where does my binary go?”* — which is a bit of a head-scratcher to someone who’s familiar with standing up their own web server or using a hosting provider. For instance, one of the more well known online storefronts for games, Steam, [does not even mention HTML5 game submissions](http://www.steampowered.com/steamworks/FAQ.php)!

#### A choice of runtimes

I’d like to take a look at two possible ways of “packaging” up HTML5 games (or even applications) for distribution: [Mozilla’s Web Runtime](https://developer.mozilla.org/en-US/Apps/Build/Architecture#Web_runtime) and [Electron](http://electron.atom.io/).

[Mozilla’s Web Runtime](https://developer.mozilla.org/en-US/Apps/Build/Architecture#Web_runtime) allows a developer with no knowledge of platform/OS specific APIs to develop an application 100% in HTML5. No need to learn anything platform specific about how windows are created, how events are handled, or how rendering occurs. There’s no IDE you’re forced to use, and no build step. Unlike [Cordova](http://cordova.apache.org/), you’re not writing into a framework, it’s just the Web. The only addition you need is an [App Manifest](https://developer.mozilla.org/en-US/Apps/Build/Manifest), which is in the standards body within the [W3C currently](http://www.w3.org/2008/webapps/manifest/).

An example manifest from [my IRC app](https://marketplace.firefox.com/app/firesea-irc):

```
{
"name": "Firesea IRC",
"version": "1.0.13",
"developer": {
"name": "Mozilla Partner Engineering",
"url": "https://github.com/nickdesaulniers/fxos-irc/graphs/contributors"
},
"description": "An IRC client",
"launch_path": "/index.html",
"permissions": {
"tcp-socket": {
"description": "tcp"
},
"desktop-notification": {
"description": "privMSGs and mentions"
}
},
"icons": {
"128": "/images/128.png"
},
"type": "privileged"
}
```


Applications developed with [Mozilla’s Web Runtime](https://developer.mozilla.org/en-US/Apps/Build/Architecture#Web_runtime) can be distributed as links to the manifest to be installed with [a snippet of JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/DOMApplicationsRegistry/install) called “[hosted apps](https://developer.mozilla.org/en-US/Marketplace/Options/Hosted_apps),” or [links to assets archived in a zip](https://developer.mozilla.org/en-US/docs/Web/API/DOMApplicationsRegistry/install) file called “[packaged apps](https://developer.mozilla.org/en-US/Marketplace/Options/Packaged_apps).” Mozilla will even host the applications for you in [https://marketplace.firefox.com](https://marketplace.firefox.com/), though you are [free to host your apps yourself](https://developer.mozilla.org/en-US/Marketplace/Options/Self_publishing). Google is also implementing the W3C manifest spec, though there are a few subtleties between implementations, currently, such as having a launcher rather than a desktop icon.

Here’s the snippet of JavaScript used to install a hosted app:

```
var request = window.navigator.mozApps.install(manifestUrl);
request.onsuccess = function () {
console.log('Installed!');
};
request.onerror = function () {
console.error(this.error.name);
};
```


A newer io.js (Node.js fork)-based project is [Electron](http://electron.atom.io/), formerly known as Atom Shell and used to build projects like [the Atom code editor](https://atom.io/) from [GitHub](https://github.com/atom) and the [Visual Studio Code](https://code.visualstudio.com/) from [Microsoft](http://www.microsoft.com/). [Electron](http://electron.atom.io/) allows for more flexibility in application development; the application is split into two processes that can post messages back and forth. One is the browser or content process, which uses the Blink rendering engine (from Chromium/Chrome), and the main process which is io.js. All of your favorite Node.js modules can thus be used with Electron. Electron is based off of [NW.js](http://nwjs.io/) (formerly node-webkit, *yo dawg, heard you like forks*) with [a few subtleties of its own](https://github.com/atom/electron/blob/master/docs/development/atom-shell-vs-node-webkit.md#technical-differences-to-nwjs-formerly-node-webkit).

Once installed, Mozilla’s Web Runtime will link against code from an installed version of Firefox and load the corresponding assets. There’s a potential tradeoff here. Electron currently ships an entire rendering engine for each and every app; all of Blink. This is potentially ~40MB, even if your actual assets are significantly smaller. Web Runtime apps will link against Firefox *if* it’s installed, otherwise will prompt the user to install Firefox to have the appropriate runtime. This cuts down significantly on the size of the content to be distributed at the cost of expecting the runtime to already be installed, which may or may not be the case. Web Runtime apps can only be installed in Firefox or Chromium/Blink, which isn’t ideal, but it’s the best we can do until browser vendors agree on and implement the standard. It would be nice to allow the user to pick which browser/rendering engine/environment to run the app in as well.

While I’m a big fan of the Node.js ecosystem, I’m also a big fan of the strong guarantees of security provided by the browser. For instance, I personally don’t trust most applications distributed as executables. Call me paranoid, but I’d really prefer if applications didn’t have access to my filesystem, and only had permission to make network requests to the host I navigated to. By communicating with Node.js, you bypass the strong guarantees provided by browser vendors. For example, browser vendors have created the [Content Security Policy (CSP)](https://developer.mozilla.org/en-US/Apps/Build/Building_apps_for_Firefox_OS/CSP) as a means of shutting down a few Cross Site Scripting (XSS) attack vectors. If an app is built with Electron and accesses your file system, hopefully the developer has done a good job sanitizing their inputs!

On the other side of the coin, we can do some really neat stuff with Electron. For example, some of the newer [Browser APIs developed in Gecko and available in Firefox and Firefox OS](https://developer.mozilla.org/en-US/Apps/Build/App_permissions) are not yet implemented in other rendering engines. Using Electron and its message-passing interface, it’s actually possible to polyfill these APIs and use them directly, though security is still an issue. Thus it’s possible to more nimbly implement APIs that other browser vendors haven’t agreed upon yet. Being able to gracefully fallback to the host API (rather than the polyfill) in the event of an update is important; let’s talk about updates next.

#### Managing updates

Updating software is a critical part of security. While browsers can offer stronger security guarantees, they’re not infallible. “Zero days” exist for all major browsers, and if you had the resources you could find or even buy knowledge of one. When it comes to updating applications, I think Mozilla’s Web Runtime has a stronger story: app assets are fetched every time, but defer to the usual asset caching strategy while the rendering engine is linked in. Because Firefox defaults to auto updating, most users should have an up-to-date rendering engine (though there are instances where this might not be the case). The runtime should check for updates for packaged apps daily, and updates work well. For Electron, I’m not sure that the update policy for apps is built in. The high value of exploits for widely installed software like rendering engines worries me a bit here.

Apps for Mozilla’s Runtime work currently anywhere where Firefox for desktop or mobile does: Windows, OS X, Linux, Android, or Firefox OS. Electron supports desktop platforms like Windows, OS X, or Linux. Sadly, neither option currently supports iOS devices. I do like that Electron allows you to generate actual standalone apps, and it [looks like tools to generate the expected .msi or .dmg files are in the works](https://github.com/loopline-systems/electron-builder).

Microsoft’s [manifold.js](http://www.manifoldjs.com) might be able to bridge the gap to all these different platforms and more. Though I ran into a few road bumps while trying it out, I would be willing to give it another look. For me, one potentially problematic issue is requiring developers to generate builds for specific platforms. Google’s Native Client (NaCl) had this issue where developers would not build their applications for ABIs ([application binary interfaces](http://en.wikipedia.org/wiki/Application_binary_interface)) they did not possess hardware to test for, and thus did not generate builds of their apps for them. If we want web apps to truly run everywhere, having separate build steps for each platform is not going to cut it; and this to me is where Mozilla’s Web Runtime really shines. Go see for yourself.

### In conclusion

If I missed anything or made any mistakes in regards to any of the technologies in this article, please let me know via comments to this post. I’m more than happy to correct any errata. More than anything, I do not want to spread fear, uncertainty, or doubt (FUD) about any of these technologies.

I’m super excited for the potential each of these approaches hold, and I enjoy exploring some of the subtleties I’ve observed between them. In the end, I’m rooting for the Web, and I’m overjoyed to see lots of competition and ideation in this space, each approach with its own list of pros and cons. What pros and cons do you see, and how do you think we can improve? Share your (constructive) thoughts and opinions in the comments below.

## 9 comments

Vangelis MisirlisJune 11th, 2015 at 12:48Richard J TurnerJune 11th, 2015 at 23:28Nick DesaulniersJune 12th, 2015 at 09:26Richard J TurnerJune 15th, 2015 at 11:57Nick DesaulniersJune 15th, 2015 at 12:45Richard J TurnerJune 15th, 2015 at 13:07huhhJune 16th, 2015 at 15:45Nick DesaulniersJune 17th, 2015 at 10:32Pedro SuzaJune 18th, 2015 at 09:41