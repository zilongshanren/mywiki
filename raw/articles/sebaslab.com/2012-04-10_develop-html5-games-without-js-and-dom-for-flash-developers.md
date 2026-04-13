---
title: 'Develop HTML5 games without JS and DOM for flash developers - Part I: Haxe
  - Seba''s Lab'
url: https://www.sebaslab.com/haxehtml5/
author: Sebastiano Mandalà
published: '2012-04-10'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

Before I start talking about my first “HTML5” experience, let me say something: after 15 years of c++ game development today I make games at the company where I work and I experiment at home using ActionScript 3, C# (Unity) and Haxe.

Do I miss the C++ times? Not really, actually what I love about the aforementioned languages is that they allow me to focus on code design instead of lower level problems and you know what? I turned out to be a code design freak.

In fact I love following the [SOLID principles](http://en.wikipedia.org/wiki/SOLID_(object-oriented_design)), recognize patterns in my code, develop frameworks, solve issues related to modularity, encapsulation, uncoupling, communication, dependency injection and such; all stuff that can be properly managed with concepts introduced with such high level languages.

With this preamble you could guess why I never wanted to mess up with javascript. I do not want to spend much words about the reasons why I do not like js; it is enough for me to know that it is quite similar to actionscript 2 and I used to work long enough with actionscript 2 to say, without fear to be much wrong, that javascript is surely a good option to write websites and simple games, but it is not good enough to develop and maintain complicated projects and guess who agrees with me? Sure Google does.

Google has some experience with javascript based projects and indeed they are trying to kill it in every way, at least in its current form. [GWT](https://developers.google.com/web-toolkit/), [Dart ](http://www.dartlang.org/)and [playN ](http://code.google.com/p/playn/)are proofs that I am not so far from the truth.

I also currently do not care much about learning how CSS 3 and the HTML DOM work. So consider this article a solution to be able to work in HTML5 without be forced to know the technology behind it.

All that said, when I heard for the first time that Haxe could export to HTML5, I was already quite excited. After other projects started to appear and among them the most interesting to me were the ones able to convert actionscript code to javascript.

While I have the intention to test them in the future, this article focuses only on the experiment I made with Haxe.

I like Haxe, I like it at lot. It is what ActionScript 4 is supposed to be for me. There are some glitches, sure, but they will be very likely addressed with the next major release. However what can be more lovely than an actionscript looking like language with generic support?! C#? Yeah, sure, but currently there are not free [solutions](http://sharpkit.codeplex.com/) to export to javascript (at least that I know of).

how Haxe code looks like:

import flash.display.Bitmap import flash.display.BitmapData import flash.events.Event import flash.geom.Point import flash.geom.Rectangle import mylittleframework.Vector2D; class Explosion extends Bitmap { var _stripe:BitmapData; var _worldPos:Vector2D; var _lastTime:Float; var _index:Int; public function new(worldPos:Vector2D) { super (); _stripe = nme.Assets.getBitmapData ("assets/images/explosion.png"); bitmapData = new BitmapData(48, 48); bitmapData.copyPixels(_stripe, new Rectangle(0, 0, 48, 48), new Point(0, 0)); _worldPos = worldPos; x = mod(_worldPos.x - (Camera.bound.x)) - 24; y = mod(_worldPos.y - (Camera.bound.y)) - 24; this.addEventListener(Event.ENTER_FRAME, onEnterFrame); //I was lazy and I did this ,but it should be avoided to improve the performance _lastTime = flash.Lib.getTimer(); _index = 0; } }

However the real question could be: is Haxe good enough to be used for a professional project? Well this question is harder to answer and I searched for the answer developing a simple project.

Haxe is the fruit of Nicolas Cannasse’s mind, who must be a sort of genius. I say this because I do not see how otherwise he can successfully manage so many projects! Surely he is helped by another bunch of guys, but not many.

So can such a project have enough support to guarantee a smooth professional development? Well, one consequence of the fact that Nicolas cannot control time is that the documentation is not very detailed. Although it is good enough to understand most of the language paradigms, sometime it is frustrating to find information even if the Haxe[ group](https://groups.google.com/forum/#!forum/haxelang) is full of users willing to help.

I must add that there are also several [libraries ](http://lib.haxe.org/)developed by third party authors already available, but most of them are not really multiplatform, so they must be chosen carefully.

The nice thing is that the most supported and useful libraries can be easily installed using the command line [Haxelib](http://haxe.org/doc/haxelib/using_haxelib) that makes everything very straightforward.

Enough talk, let’s get started:

First you need an IDE. Although a [good number of IDEs](http://haxe.org/com/ide) support Haxe, my favourite currently is [Flashdevelop](http://www.flashdevelop.org/), also because I do not know the other ones. Nevertheless it is a great IDE, light and fast. Grab it and install it and remember that it works only on windows. If you use linux or mac-os, a free [alternative](http://www.joshuagranick.com/blog/2012/04/06/flashdevelop-for-maclinux-part-1/) seems coming soon based on monodevelop.

Now it is the time to install Haxe and its libraries, however I suggest to use the NME installer in place of the Haxe one, I will explain you why in a bit. It is available [here](http://www.haxenme.org/download/) (leave everything ticked when you install it).

Keep in mind that this article is based on my development experience on windows 7 platform and it assumes that the reader knows already Flash framework, if not it will probably be not enough to start developing with Haxe.

Once installed, you pretty much have everything needed to start. All the Haxe files and libs will be under the folder c:Motion-Twin

Let me now introduce [NME](http://www.haxenme.org/). Haxe on its own includes the language, the compiler and a framework. Some subsets of this framework are platform dependent. Haxe can target many platforms and it is possible to find specific classes for c++, Flash, js, neko and php as you can see here: [http://Haxe.org/api](http://haxe.org/api).

However only Flash and js related libraries are able to render graphic on the screen. They do it in two complete different ways.

The former using an approach identical to the original Flash, that means using the display list structure, the latter using the HTML DOM. [HaxeJS ](http://www.haxejs.org/)focuses on the second approach. Talking about HaxeJS is beyond the purposes of this article, but I say I would personally use it in place of JS even to create simple projects/web pages.

Keep in mind that HaxeNME is then oriented to who, like me, does not want to learn how to use the CSS/DOM and does not want to mess up with javascript. If instead the reader goal is to learn html5 technology avoiding (in part) javascript, then HaxeJS is the best choice.

NME is a multiplatform graphical library written in Haxe and created by [Hugh Sanderson](http://twitter.com/#!/gamehaxe), [Joshua Granick](http://twitter.com/#!/singmajesty) (please follow his [blog](http://www.joshuagranick.com/blog/)) and [Niel Drummond](http://twitter.com/#!/grumpytoad) (Jeash creator). It is an [almost ](http://www.haxenme.org/documentation/features/)total Haxe porting of Flash framework and it just works with all the Haxe targets available! Using NME makes a multiplatform game development a piece of cake.

For the purposes of this article we are interested in [Jeash](http://jeash.com/). Jeash has been only recently officially added into the NME suite, being so far an independent project and it includes the NME porting to javascript. The developer implemented several optimizations, but I will talk about it later.

Let’s now setup our first HaxeNME project.

From the FlashDevelop IDE choose Project->New Project and then Haxe -> NME Project. FD will create the project folder structure for us together with the application.nmml file.

NMML file is an xml file which describes parameters and dependencies of our project. It is pretty simple to understand, but more explanations can be found [here.](http://www.haxenme.org/developers/documentation/nmml-project-files/) Just remember that this file gives the directives to the compiler, so, for example, every time a new library is used, it must be added in this file.

If you want to test an already made project, you can download the experiment I made. Of course it is a shoot’em’up (what else? 🙂 ) and it is nothing special too, but enough to test the performances and let me understand how good the HaxeNME development flow can be. By the way, if you play it, remind that it is not needed to click to shoot, the ship shoots automatically while it decelerates.

the demo can be downloaded, together with the code repository, including the haxe project, at [https://bitbucket.org/sebas77/Haxe-demo](https://bitbucket.org/sebas77/haxe-demo).

If you created a project from the scratch as explained and you are not using mine, you should be now able to compile and run the demo and play right away the Flash version. This is great, because with FD IDE is possible to debug directly Flash code with breakpoints and everything else, while it is not possible to do it with javascript code.

This means that every time a problem is found, HaxeNME gives us the option to debug the Flash version, which most of the time is enough to find easily and conveniently the problem.

This is already a great benefit compared to pure javascript, even if chrome is a good tool for debugging.

In order to run the javascript version, just one project setting must be changed. On the project panel (usually on the right), click on the title of your project with the right button and select “Properties”.

Where there is written “Test Project”, click on the Edit button and in place of “flash” write “html5” (or the other way around if you started with my project so you can test the flash version).

The project can now run in javascript! PRETTY DAMN EASY. The equivalent command line should be: haxelib run nme build “PRJPATHapplication.nmml” html5.

The current version of Jeash (0.8.7) has some bugs that I helped to catch. So if you want to see my demo running properly, please download the latest trunk from this page: [https://github.com/grumpytoad/jeash](https://github.com/grumpytoad/jeash) and copy the code in the folder c:Motion-Twinhaxelibjeash,8,7. The author pretty much updates the trunk almost everyday and most of the time he fixed the bugs before I could even had the chance to report them. So I think that Niel is doing a great job.

Once started coding, it is possible to notice some details that could make one confused. The first I noticed is that the intellisense shows you up to three options for each Flash class one wants to import.

In fact, if for example we type import Sprite we can see the following options available: flash.display.Sprite, nme.display.Sprite and jeash.display.Sprite.

Theoretically the NME one should be used because it is the multiplatform version of the Flash library porting. However I chose the Flash version to help the FD intellisense and it should work as well.

If instead you have troubles compiling, you could add the following line to the compiler options: –remap Flash:jeash -lib jeash

In any case, I suggest to add the folder c:Motion-TwinHaxelib to the FD Global classpath so that the intellisense can properly work in every occasion (and so you can use NME package if you wish).

It is important to notice that there is difference between the Debug and Release version of the output even targeting html5. In debug mode a sort of stack structure is added to trace the functions stack and so the code generated is bigger and slower.

Another important aspect about HaxeNME development is how simple managing asset can be, in fact there are several options available. The one I chose is to import my png files using the nme.Assets.getBitmapData function and the NMML tag.

Thetag allows to choose the folders where the assets are located and tell the compiler to embed them. The getBitmapData will be able to return the BitmapData from the embedded image. To be honest I did not understand how the images are embedded in the html5 version yet, for me it is just important that it works.

HaxeNME even supports SWF assets (no bytecode) for most of the platforms (no html5 yet 🙁 ) as well as asynchronous loading (no embedding).

So now that the game runs both as Flash and as html5 project, I want to share my final impressions:

**Debugging**

As already said, every time I found a bug I needed to debug, I just switched to the flash version so that I could easily use breakpoints, stack, local and watch variables. It is true that Google chrome has a pretty good debugger and the code generated by Haxe is quite readable as well, so if one wants to make some experience with Google Chrome debugger, it could be used as well, but flash develop is surely faster and easier to use.

Although Jeash library did not reach version 1.0 and some NME features are not implemented yet, I had everything I needed to create my demo, so I have nothing to complain about it.

**Performance**


Jeash performance is in my opinion pretty good. My demo use several big sprites and most of all, it rotates them! Rotating is quite an expensive operation without hardware acceleration and jeash exploit some optimizations (like css transformation caching) to get the maximum performance available. This is not easily achievable in a pure javascript engine, so I think jeash could perform well most of the time.

I had a look at the code and I think Niel can still optimize it. I do not know the performance of the string operations in javascript, but the code heavily relies on them even for real time operations, so this probably should be taken in consideration.

Using the amazing Google Chrome profile it is simple to see that the graphical rendering is the biggest bottleneck even if the rotation is disabled, so more attention should be put on it.

Another consideration to make is that the display list is not the best structure to be used in an HTML5 context in my opinion, but Jeash (like the flash framework) allows us to get rid of it. In fact we could simulate the old school bitmap blitting, without any hierarchical structure, using the Bitmapdata blitting operations.

At this [address ](http://blog.iainlobb.com/2011/02/bunnymark-compiled-from-actionscript-to.html)some numbers shown can give an idea about the potential performance difference, even if the author was not using jeash but another actionscript to javascript approach.

Finally I want to point out this interesting [article](http://mikecann.co.uk/personal-project/more-html5-haxe-speed-tests/) as well, where the author found out that while the overhead introduced by the current version of Jeash allegedly impact the performance compared the use of straight javascript, using HaxeJS with canvas surprisingly resulted to be the fastest solution.

The resulting file dimension is another point to be considered. My simple demo already generates a js script file bigger than 400 kb. However this big dimension is due to the fact that the entire NME project is injected in the js file, so the overhead size is not dependent by the size of the haxe project itself. Personally, if I have to develop a game, I would not probably care about this size, although very likely I would use an obfuscator which could save some kilobytes.

Last thing I want to talk about is the difference of performance between browsers and mobile/desktop versions.

First it must be taken in consideration that soon all the browsers will support hardware accelerated canvas rendering, although IE will be the last one to support it with the new version 10 (available only on windows 8).

My demo runs quite well under Opera, Chrome and Safari, while I had some troubles with firefox, maybe due to drivers incompatibility. Internet explorer 9, while is able to run it, does not perform well in terms of frame rate. In every case it is important to highlight how haxe and jeash are able to guarantee an exceptional inter browser compatibility, since all the demo features are working on all the browsers.

Quite disappointing is the performance on mobile. Apple, which pushes so much html5, did a great job optimizing safari for iOS (the iOS 5 version runs up to 8x faster than the iOS 4 version), but iPhone 4 is not able to render the game at more than 30 fps.

So, is Haxe ready to be used to develop web social/casual game in HTML5? If the performance is not a critical issue for the game, in my opinion yes. Haxe can be used successfully to develop web based social/casual game in HTML5. Would I develop HTML5 games? Even if this question is not related to the article purposes, I would say no, I do not see the reason to do it unless, maybe, I want a web experience to be completely uniform across all the platforms, but this, because of performance issues, cannot happen today.

If you are interested in an alternative I talked about Jangaroo on this post: [http://blog.sebaslab.com/develop-html5-games-without-js-and-dom-for-flash-developers-part-2-jangaroo/](http://blog.sebaslab.com/develop-html5-games-without-js-and-dom-for-flash-developers-part-2-jangaroo/)

This is a very thorough walkthrough!

It sounds like Jeash has been improving. Its great to hear it is performing well across each browser. I agree, fortunately haxe and NME give us options so we ae not limited by a single technology. Like you said, though Apple has impoved their HTML5 performance, it still is much slower than native (up to 40 times slower than a native NME application)

I’m thankful we can take advantage of a high-level language, and all the productivity it brings, while also benefiting from the performance of C++ 🙂

sure, in fact for mobile I would use haxecpp 🙂

/// public function shootLikeIfThereIsNoTomorrow

Nice touch. 😀

Great article! And thank you very much for publishing the full source. It’s a great way to learn how to do things for a newbie like myself. 🙂

Cheers, Marcus

Thanks for sharing, haxe comunity is the best and is geting bigger and bigger every single day. Its a joy and a pleasure program in haxe.

Nice article, thanks for sharing!

One question. I’ve tried to compile the test for windows/android and it is something wrong with getBounds calls in that case.

src/SpaceShip.hx:100: characters 46-60 : SpaceShip has no field getBounds

src/Bullet.hx:38: characters 10-27 : flash.display.Bitmap has no field getBounds

src/Enemy.hx:55: characters 28-42 : Enemy has no field getBounds

Do you know a workaround for such an issue?

NME is ported on every platform by different developers and some little differences could be present unluckily. Jeash does not implement getRect yet so I switched to getBounds, it is possible that for android it is the other way around. I would check on the HaxeNME forum/mailing list for more info.

Hi,

very interesting article – i am following haxenme for quite some time and the latest improvements making it possible to use swf assets are very interesting.

One question: you briefly mention that this feature is available on all platforms. The haxenme.org website states that for the html5 target swf libraries are not working yet. Did this change recently?

Kind regards

Sebastian

hmm I think you are right, I did not test it personally so I cannot be sure, but it can be very true, I will change the article.

[…] reason why I called the first tutorial of this series Part 1 is because I knew there were other alternatives around to develop HTML5 […]

Hi, just tried your sample project but wonder how to make it rebuild the html5 part as well.

Building from FD only updates the swf but not the js output

I did not test the demo recently, but this should be enough (from the article itself):

“In order to run the javascript version, just one project setting must be changed. On the project panel (usually on the right), click on the title of your project with the right button and select “Properties”.

Where there is written “Test Project”, click on the Edit button and in place of “flash” write “html5” (or the other way around if you started with my project so you can test the flash version).”