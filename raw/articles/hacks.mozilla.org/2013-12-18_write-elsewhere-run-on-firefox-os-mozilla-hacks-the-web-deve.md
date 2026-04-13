---
title: Write Elsewhere, Run on Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/12/write-elsewhere-run-on-firefox/
author: Mark Coggins
published: '2013-12-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Over the last year we’ve been recruiting developers who’ve already built apps for various Open Web and HTML5 platforms: apps for native platforms built with PhoneGap, Appcelerator Titanium or hand-coded wrappers; HTML5 apps built for Amazon Appstore, Blackberry Webworks, Chrome Dev Store, Windows Phone, and WebOS; and C++ apps translated to JavaScript with [Emscripten](https://developer.mozilla.org/en-US/docs/Emscripten). We’ve supported hundreds of developers and shipped devices all over the world to test and demo Firefox Apps. If you have a well-rated, successful HTML5 app on any platform we urge you to port it to Firefox OS: We’re betting it will be worth your while.

In November, Firefox OS launched in Hungary, Serbia, Montenegro and Greece. Earlier this month we launched in Italy. In 2014, we launch in new locales with new operators, with new devices in new form factors. We anticipate more powerful cross-platform tools in 2014, and closer integration with PhoneGap and Firefox Developer Tools. It is the best of times for first-mover advantage.

Here’s a look at just a few successful ports. We spoke with skilled HTML5 app developers who’ve participated in “app port” programs and workshops and asked them to describe their Firefox app porting experience.

![RunOnFirefoxOS](../../assets/5fcc8bcb01667e52.jpg)

*Captain Rogers, by Andrzej Mazur; Reditr by Dimitry Vinogradov & David Zorycht; Aquarium Plants by Diego Lopez*

[Aquarium Plants (](https://hacks.mozilla.org#Aquarium Plants)**Android w/ hand-coded native wrapper**)[Calc (](https://hacks.mozilla.org#Calc)**iOS w/ hand-coded native wrapper**)[Calcula Hipoteca (](https://hacks.mozilla.org#Calcula Hipoteca)**Amazon Appstore**)[Captain Rogers (](https://hacks.mozilla.org#Captain Rogers)**HTML5 Desktop**)[Cartelera Panama (](https://hacks.mozilla.org#Cartelera Panama)**Appcelerator Titanium**)[Fresh Food Finder (](https://hacks.mozilla.org#Fresh Food Finder)**PhoneGap**)[Picross (](https://hacks.mozilla.org#Picross)**WebOS**)[Reditr (](https://hacks.mozilla.org#Reditr)**Chrome Dev Store**)[Speed Cube Timer (](https://hacks.mozilla.org#Speed Cube Timer)**Blackberry Webworks**)[Squarez (](https://hacks.mozilla.org#Squarez)**C++**)[Touch 12i (](https://hacks.mozilla.org#Touch 12i)**Windows Phone/ HTML5**)

### Aquarium Plants (Android w/ hand-coded native wrapper)

**App:** [Aquarium Plants](https://marketplace.firefox.com/app/aquarium-plants)

**Developer: **Diego Lopez

Original platform: [Google Play Store](https://play.google.com/store/apps/details?id=com.golgorz.aquariumplantsfree)

#### Time:

*Aquarium Plants is written with our own JavaScript code and simple HTML5 code: we just used two common JavaScript frameworks (Zepto.js and TaffyDB.js). It took me about 3 hours or less. Most of the time was reading forums and documentation.*

#### Recommendations:

*It is extremely easy to build/port apps for Firefox OS. It is great that we can use web tools and frameworks to create native apps for Firefox OS. I recommend that other developers start developing Firefox Apps; it is almost effortless and a great experience.*

#### Challenges:

*The only challenge I had was finding out how to build the package. It was amazing when I realized that building for Firefox OS was as easy as creating a zip with the app files and manifest.*

### Calc (iOS w/ hand-coded native wrapper)

**App:** [Calc](https://marketplace.firefox.com/app/calc-by-lancio/)

**Developer:** Markus Greve

Original platform: [iOS w/ hand-coded native wrapper](https://itunes.apple.com/app/us/calc-for-ipad/id418755167)

#### Time:

*It was really easy. That’s why I would sign the claim “Write Elsewhere, Run on Firefox OS.” I think it took about two evenings with night #1 getting the app to run and night #2 doing some fine-tuning for display size of the simulator and Keon. Afterwards another evening for app icon and deployment to the Marketplace ;-) . *

#### Recommendations:

*I would recommend that developers give it a try to see how easy it really is. I think Mozilla.org is doing a great job and your support for developers is excellent. I already made a short presentation about how to create FirefoxOS Apps as a documentation of my experiences. You can see it here: A Firefox OS app in five minutes (in English). There’s also a blog post called App Entwicklung fur den Feuerfuchs that documents my experience in German. *

#### Challenges:

*1. I use OSX 10.9 Mavericks, and the Simulator crashed with the old plugin and ran more stably with Firefox 1.26b and app-manager.
2. The need to have a subdomain per app — it seems there’s an open issue with this.
3. Data types in JSON Manifest (I tried “fullscreen”: true instead of “fullscreen”: “true”). My fault: Solved by sticking to the documentation.
4. I have the feeling that the icon sizes are different in the documentation to the sizes really needed for the Marketplace. Also, it’s not sensible to offer a Photoshop-Template for a 60×60 pixel Icon when you need much bigger files elsewhere (256×256 for the store I think). It would be better if you provided a template for 1024 and the user then shrank the images afterwards.
5. Suggestion: The correlation between navigator.mozApp.checkInstalled() and .install() could be explained more comprehensively.*

### Calcula Hipoteca (Amazon Appstore)

**App:** [Calcula Hipoteca](https://marketplace.firefox.com/app/calcula-hipoteca)

**Developer:** Emilio Baena

Original platform: [Amazon Appstore](http://www.amazon.com/liodevel-Calcula-Hipoteca/dp/B00F2GDV94)

#### Time:

*It was easy. I took a few hours.*

#### Recommendations:

*You are doing good work with this platform.*

#### Challenges:

*I had problems with manifest.webapp, I think that I missed having more documentation about this type of file. *

### Captain Rogers (HTML5 Desktop)

**App: **[Captain Rogers](https://marketplace.firefox.com/app/captain-rogers/)

**Developer: **Andrzej Mazur

Original platform: [HTML5 Desktop](http://enclavegames.com/games/captain-rogers/)

#### Time:

*The whole process of porting Captain Rogers for the Firefox OS platform took me only two weeks of development with an additional two weeks of testing and bug-fixing. In the core concept the game was supposed to be simple so I could focus on the process of polishing it for Firefox OS devices and publishing it in the Firefox Marketplace.*

#### Challenges:

*There weren’t any big problems, because basically building for Firefox OS is just building for the Web itself. Firefox OS devices are the long-awaited hardware for the mobile web — it is built using JavaScript and HTML5 after all. My main focus on making the game playable on the Firefox OS device was put on the manifest file. I had some problems with getting the orientation to work properly, but during the Firefox OS App Workshop in Warsaw I received great help from Jason Weathersby and at the end of the day the first version of the game was working very smoothly and a few days later it was accepted into the Firefox Marketplace. *

For optimizing the code I recommend this [handy article by Louis Stowasser and Harald Kirschner](https://hacks.mozilla.org/2013/05/optimizing-your-javascript-game-for-firefox-os/) — it was very helpful for me. Also, the Web Audio API is still a big problem on mobile, but it works perfectly in Captain Rogers, launched on the Firefox OS phone.

#### Recommendations:

*The main message is simple: if you’re building HTML5 games for Firefox OS, you’re building them for the Open Web. Firefox OS is the hardware platform that the Web needs and in the long run everybody will benefit from it, as the standards and APIs are battle-tested directly on the actual devices by millions of people. *

If you want to know more about HTML5 game development I can recommend my two creations: my [Preparing for Firefox OS article](http://mobile.tutsplus.com/tutorials/firefox-os/preparing-for-firefox-os/) and [HTML5 Gamedev Starter list](http://html5devstarter.enclavegames.com/). You should also read this [great introduction by Austin Hallock](https://hacks.mozilla.org/2013/09/getting-started-with-html5-game-development/). The community is very helpful, so if you have any problems or issues, check out the [HTML5GameDevs](http://www.html5gamedevs.com/) forums for help and you will definitely receive it. It’s a great time for HTML5 game development, so jump in and have fun!.

### Cartelera Panama (Appcelerator Titanium)

**App:** [Cartelera Panama](https://marketplace.firefox.com/app/cartelerapanama/)

**Developer: **Demostenes Garcia

Original platform/wrapper: [Appcelerator Titanium](http://www.cartelera.com.pa/)

#### Time:

*It was pretty easy to get up to speed on the development flow for Cartelera. The development for Firefox OS is easy, since it’s well documented and HTML5 + JavaScript makes it *really* easy to make apps.*

#### Challenges:

*Our UX/UI team at Pixmat Studios is very centered on usability, and that’s why we choose Titanium over PhoneGap (better user experience) so our main challenge was to make it look as a real Firefox OS application. In the end, we decided to go with real Firefox OS Building Blocks, instead of using Titanium for the UI. We decided to:*

- Extract all the business logic for the App (which handles the schedules, movies, listings, etc.) to its own Git repository/module. Then we reuse everything on Titanium and Firefox OS, using native user experience for all the three platforms we now accept.
- Another issue we had was to actually implement an OAuth client on our phone in a good way. However
[Jason Weathersby](https://hacks.mozilla.org/author/jasonweathersby/)pointed out good resources on that matter for us.

#### Recommendations:

*Firefox OS and the environment (debug, etc) is easy for a regular web developer, so we didn’t need extra knowledge for making real mobile apps.*

- Use Firefox OS Building Blocks for UI. It’s easy to get a native UI experience with no fuzz.
[Firefox OS at the Mozilla MDN](https://developer.mozilla.org/en-US/Firefox_OS)will be your best friend :-).- GitHub has some good projects to learn from, so create an account (if you still don’t have one) and look for demo projects.

### Fresh Food Finder (PhoneGap)

**App:**[Fresh Food Finder](https://marketplace.firefox.com/app/fresh-food-finder/)

**Developer: **Andrew Trice

Original platform/wrapper: [PhoneGap](http://www.tricedesigns.com/2013/07/09/fresh-food-finder-featured-in-self-magazine/)

#### Time:

*PhoneGap support is coming for Firefox OS, and in preparation I wanted to become familiar with the Firefox OS development environment and platform ecosystem. So… I ported the Fresh Food Finder, minus the specific PhoneGap API calls. The best part (and this really shows the power of web-standards based development) is that I was able to take the existing PhoneGap codebase, turn it into a Firefox OS app AND submit it to the Firefox Marketplace in under 24 hours! *

#### Recommendations:

*Basically, I commented out the PhoneGap-specific API calls, added a few minor bug fixes, and added a few Firefox-OS specific layout/styling changes (just a few minor things so that my app looked right on the device). Then you put in a mainfest.webapp configuration file, package it up, then submit it to the Marketplace. If you’re interested, you can check out progress on Firefox OS support in the Cordova project, and it will be available on PhoneGap.com once it’s actually released. (Editor’s note: Look for release news in early 2014.)*

### Picross (WebOS)

[ ]**App:** [Picross](https://marketplace.firefox.com/app/picross/)

**Developer:** Owen Swerkstrom

Original platform: [WebOS](https://developer.palm.com/appredirect/?packageid=net.penduin.picross)

#### Time:

*Picross was installed and running on FxOS within minutes of getting my hands on a device.*

#### Challenges:

*I did have to make some touch API tweaks, but that just meant some quick reading.*

#### Recommendations:

*My favorite quote was “You’re not porting to FirefoxOS, you’re porting to the Web!” Also, Firefox OS (and Firefox browser) Canvas support is sensational. My next game will use Canvas, for sure. In my case, the “porting” path was really simple. My game already ran in a browser, and it had originally been designed to run on the Palm Pre, a device with the exact same resolution as the lowest-end FirefoxOS phone. But the concept of installing an app involves nothing more than visiting a website: that’s what really made it painless, and that is what’s really unique about FirefoxOS. It has an “official” app marketplace, but unlike every other smartphone ever made, it doesn’t _need_ one! As a user, this is liberating. I can install any web app, from any site I want. As a developer, the story’s even better. I don’t even need Mozilla’s permission to publish an app on this platform. I don’t need to put my device into a special developer mode, or buy any toolkit, or build on any specific platform. If I can put up a website, I’m good to go. *

Even though I just called it “unnecessary”, the Firefox Marketplace has given me nothing but good experiences. I don’t need to bundle up, sign, and upload any package — I just enter a URL and type up some descriptive blurbs. Review times have always been short, and are even quicker now than when I started. When I submitted [Halloween Artist](https://marketplace.firefox.com/app/halloween-artist), it was approved almost immediately, and the reviewer suggested that I write up a blog entry for Mozilla Hacks about how I’d put it together. This is both a traditional “marketplace” with the featured apps etc, and a community of geeks celebrating interesting code and novel ideas. That is absolutely the world I want my apps to live in.

Before I went to the Mozilla workshop, I was considering what approach to take for an action/adventure game that I’m still working on. I was torn between writing some C OpenGL code, waiting for the not-yet-released-at-the-time SDL 2.0, or, as a longshot, doing at least some prototyping in HTML5 canvas. After learning that Canvas operations on a FirefoxOS phone basically go right to the framebuffer, and after trying some experiments and seeing for myself the insane performance I could get out of these cheap little ARM devices, I knew I’d be ditching C for the project and writing the game as a web app. I’d highly recommend investigating Canvas for your next game, even if you’ve mostly done Flash or SDL etc. before.


### Reditr (Chrome Dev Store)


**App:** [Reditr](https://marketplace.firefox.com/app/reditr/)

**Developer:** Dimitry Vinogradov & David Zorycht

Original platform:[Chrome Dev Store](https://chrome.google.com/webstore/detail/reditr-web-app-the-best-r/ejmiceoebcclihjdpnmmkdcmcboekibc?hl=en)

#### Time:

*It took us about a week to port everything over from Chrome to Firefox OS. *

#### Challenges:

*One challenge we faced when creating Reditr for Firefox OS was the content security policy (CSP). One of the great things about web applications for users is that they can see an entire overview of the permissions that a given app requires. For developers though, it can take some time to learn how to create a content security policy. For Reditr, it took us several days of trial and error to learn how the security policy effected our app.*

#### Recommendations:

*Make sure you understand how your app deals with the content security policy. Check to see if the APIs you use have oAuth support since this can help remedy CSP issues.*

### Speed Cube Timer – Blackberry Webworks


**App:** [Speed Cuber Timer](https://marketplace.firefox.com/app/speed-cube-timer-1/)

**Developer:** Konstantinos Mavrodis

Original platform: [Blackberry Webworks](https://appworld.blackberry.com/webstore/content/28652891)

#### Time:

*It took about half an hour to make the exported web app compatible with Firefox OS. (Insanely fast, don’t you think? :) )*

#### Challenges:

*No real challenges here that I can recall of. Everything was almost a piece of cake!*

#### Recommendations:

*My recommendation to fellow devs would be them to port their HTML5 apps to Firefox OS as soon as possible! Porting a Web app has never been easier. Firefox OS is a promising OS that shows the great power of Web Development!*

### Squarez (C++)


**App:** [Squarez](https://marketplace.firefox.com/app/squarez?)

**Developer:** Patrick Nicolas

**Original platform:** [C++ with Emscripten](http://squarez.meumeu.org/)

#### Emscripten and C++ usage:

*I have always preferred statically typed and compiled languages as they fit better with my way of organizing software. There are several options with Emscripten, and I have decided to write the game logic in C++ and the user interface in HTML/CSS/JavaScript. All the logic code is in C++, and for multiplayer mode, server can reuse everything and only has roughly 500 additional lines of code.*

#### Time:

*The game has always been a web project: the initial development, from scratch, took nearly 1 month. Porting it to be a Firefox application only took a couple of days, in order to make the manifests and icons. Performance tweaking has been a complex task and took nearly as much time as the rest of development.*

#### Challenges:

*Squarez is the first game I have ever written and it is the first time I have used Emscripten, that was the first challenge. Writing a web application is not really a challenge any more, because good quality documentation is available everywhere. Second challenge was tweaking performance, once I had received the Geeksphone Keon, I saw that the game was so slow that it was almost unplayable. I have used performance tools from native compiled code and both desktop Firefox and Chromium to find the bottlenecks. *

Because of Emscripten JavaScript generation, it was not very easy to track the faulty functions, I had to deal with partially mangled names in profile view. The following step was to optimize CSS, and I have only found tools to check time spent in selector processing. It is impossible to know which specific animation is taking time, I had to use very manual methods and try disabling individual ones, guess what is taking time and change it blindly.

#### Recommendations:

*My recommendation for other developers is to choose technologies they like; I wanted structured and statically typed code, so Emscripten/C++ was a great solution. I would also discourage creating an application that only works in Firefox OS, but take advantage of standards to make it available to any browser and have Web APIs used to enhance the application. If you want to also include a link to the code repository, it is available at squarez.git. Everything is GPLv3+, fork it if you want.*

### Touch 12i (**Windows Phone**)


**App:** [Touch 12i](https://marketplace.firefox.com/app/touch-12i)

**Developer:** Elvis Pfutzenreuter

Original platform: [HTML5 for Windows Phone (and other platforms)](http://www.windowsphone.com/en-us/store/app/touch12i/73fe78f0-2756-45b8-9183-f4b54768a5b9)

#### Time:

*It took one day to do the bulk of the work, and another day for final details, including registration in Marketplace. Later, I added payment receipt checking which took me the best part of a day since it needs to be well tested. But this effort could be reused readily for another app (Touch 11i).*

#### Challenges:

*In general, porting was very easy. I put it to work in one day. The biggest problem was the viewport: that works differently in other platforms (all Webkit-based). For Firefox, I had to use a CSS transform-based approach to fit the calculator in screen. Touch 12i is an HTML5 app that runs on Windows Phones and it works in the same way for Android and iOS too: a “shell” of native code with a Web component that cradles the main program. Currently the Firefox version is the only one that is “purely” HTML5. (I used to have a pure Web-based version for iOS as well, but this model has been toned down for iOS.) I’ve written a detailed blog post called Playing With Firefox OS, about my experience participating in the Phones for App Ports program. *

And that’s a wrap. Thanks for reading this far. If you’re a Firefox OS App porter, a web developer or simply a curious reader, we’d love to hear from you. Leave a comment or send us a note at [appsdev@mozilla.com](mailto:appsdev@mozilla.com).

## About
[
Mark Coggins ](http://cogswells.tumblr.com/)

Mark is the former SVP of Engineering at Actuate, a public company in the Business Intelligence space. He is co-founder of the BIRT open source project at the Eclipse Foundation, and is the author of six crime novels set in the Silicon Valley.

## 6 comments

Havi HoffmanDecember 18th, 2013 at 08:34Ivan DejanovicDecember 18th, 2013 at 13:42Robert Nyman [Editor]December 19th, 2013 at 06:40Aras Balali MoghaddamDecember 18th, 2013 at 15:48Robert Nyman [Editor]December 19th, 2013 at 06:39SteveDecember 20th, 2013 at 03:35