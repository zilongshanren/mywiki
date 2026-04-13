---
title: Develop HTML5 games using actionscript and Jangaroo
url: https://www.sebaslab.com/develop-html5-games-without-js-and-dom-for-flash-developers-part-2-jangaroo/
author: Sebastiano Mandalà
published: '2012-08-05'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

The reason why I called the [first tutorial](http://blog.sebaslab.com/haxehtml5/) of this series Part 1 is because I knew there were other alternatives around to develop HTML5 games, carefully avoiding javascript.

However after some researches it turned out that the only really working alternative suitable for actionscript developers is [Jangaroo](http://www.jangaroo.net/home/).

![](../../assets/b215b037421e4708.img)


Let’s talk a little bit about it. Jangaroo is an open-source project mainly used by the German company [Coremedia](http://www.coremedia.com/). The smart guys from Coremedia hate javascript so much that they decided to create a compiler capable to convert actionscript 3 to javascript and they called it Jangaroo.

However Jangaroo has not been created with the intent to support Flash libraries (including the display list), what the developers had in mind was just to have a way to create web applications with a language different from Javascript.

Jangaroo is for actionscript 3 what HaxeJS is for Haxe, that is a way to entirely map a language into another. In fact Jangaroo is mainly used with pre-existent and remapped javascript libraries, that is more or less what happens with HaxeJS.

This part of Jangaroo is supposed to be quite stable, in fact it has been already used for several internal projects at Coremedia. It is also interesting to note that several open-source [applications have been made with it](http://www.jangaroo.net/applications/). Among these projects we can find the porting of the 2D engine [Flixel](https://github.com/fwienber/flixel/tree/beta) and the physic engine [Box2D](https://github.com/jangaroo/Box2DFlashAS3).

The [main source code of Jangaroo](https://github.com/CoreMedia) and all the applications can be found on several github repositories.

The first impact I had when I read the clear (but a little bit outdated) [tutorial ](http://www.jangaroo.net/tutorial/)was: woah woah woah, what? Do I have to install Maven to run it?! Seriously?! It must be a pain! Thus, since for a long while now I wanted to try [Realaxy](http://realaxy.com/) IDE (man, it is not really easy to remember how to spell it) and since I knew that the beta version 1.1 is supporting jangaroo to convert the actionscript code to JS, I decided to install it thinking it would have been a smart decision.

Instead few minutes using it were enough to understand that it was a big mistake! First it is java based = a pachydermic piece of software as slow as the other incredibly overrated IDE Eclipse (and its cousin Flash Builder), second it lightly decided to delete my project folder, including all the code I have manually converted from the previous [Haxe version of my experiment](http://blog.sebaslab.com/haxehtml5/), that of course I did not back up urggghhh.

By the way, this is something that could be interesting: I actually tried to convert the Haxe code to actionscript 3 using the automatic method that Haxe provides, but it failed in several ways and so I had to spend more or less an hour to manually convert the source code.

At this point I decided to go for Maven and surprisingly everything worked out smoothly and painlessly. What Jangaroo asks to install in order to work is just the last version of Java Runtime Environment and [Maven](http://maven.apache.org/), nothing else.

The only thing to pay attention to (as explained in the tutorial) is to set the JAVA_HOME environment variable that must point to the folder where the JRE is installed.

Now everything is set to follow the aforementioned Jangaroo tutorial, which explains in few steps how to create the first “hello world” application without using flash libraries. With the knowledge gathered so far, you will be able to create a javascript based application using actionscript 3, but you will not be able to use the display list to make games.

Although the goal of this tutorial is to show to the reader how to use the Display List in jangaroo to make HTML5 games, let’s be clear: I am not a fan of the Display List and I do not think it is a good data structure to use for HTML5 games. So even if Jangaroo, as we will find out, has some flaws in converting the display list related code, I would not say this is a great limitation. The real problem is that from now on the documentation become very scarce. Your main source of information will be [GitHub](https://github.com/fwienber) and the [Jangaroo group on google](https://accounts.google.com/ServiceLogin?service=groups2&passive=1209600&continue=http://groups.google.com/group/jangaroo-users&followup=http://groups.google.com/group/jangaroo-users&authuser=0). They are both managed by Frank Wienberg, who is the most active Coremedia employee developing and maintaining the project.

Honestly, while Frank is a great guy willing to help as much as he can, the fact that he is alone is another relatively big limitation of the project. In my opinion Jangaroo needs a bigger community to become really successful and I think it even deserves it. More people should at least give it a try, that’s also why I am happy to write this article.

In order to work with the DisplayList, the next step is to extend the pom.xml file. The pom.xml is a config file needed by Maven to understand what to do and which libraries to use. I do not think it is necessary at this point to explain every single node inside the XML, since the jangaroo tutorial is quite simple to understand. However in order to get more information two options are available: One is to use the [template example](https://github.com/fwienber/jooflash-app-template) in github, the other one is to use [FlashDevelop](http://www.flashdevelop.org/) and download the [template to create a working jangaroo project](https://github.com/fwienber/jooflash-fd-project).

Once the template is installed and the project is created, the pom.xml will be generated automatically inside the project folder; just be careful that Flashdevelop uses the JAVA_HOME variable as well, but it is NOT compatible with the 64bit version of JRE. In case you have both the 32bit and the 64bit versions installed and you decided to use the 64bit version to run maven, I suggest to edit the FD jvm.config file to instruct it to use JRE 32bit.

Do not be afraid to open the xml file, it is quite self-explanatory. The only attributes you need really to take care of are * jangaroo_version *node and

*node*

**jangaroo_libs_version****.**The value inside must be kept updated with the latest version of the libraries available. Maven will automatically download it the first time the project will be compiled. Totally awesome!

I guess that the

[Maven repository](http://mvnrepository.com/artifact/net.jangaroo/jangaroo-maven-plugin)is a good place where to check the latest Jangaroo version (the preview versions seems to not support the flash libraries yet).

Other two important nodes of the Pom.xml file are the * dependencies* and the

*nodes.*

**resources**The dependencies node tells Maven which other libraries to use while compiling the source code. For this article sake, it is important to know that the jooflash extension, which enables the flash library, is not part of the standard jangaroo library, but it is among the extra ones and so it must be included inside the dependencies node.

## <dependencies>

## <dependency>

## <groupId>net.jangaroo</groupId>

## <artifactId>jooflash</artifactId>

## <version>${jangaroo_libs_version}</version>

## <type>jangaroo</type>

## </dependency>

## </dependencies>


Jooflash is a side project developed exclusively by Frank Wienberg, therefore it is not as stable or as complete as the main Jangaroo library.

the resources node is instead useful if you want to embed resources using the meta tag [Embed(source = “…”)]

## <resources>

## <resource>

## src/main/assets

## <includes>

## <include>**/*.png</include>

## <include>**/*.jpg</include>

## </includes>

## joo/assets

## </resource>

## <resource>

## <directory>webapp</directory>

## </resource>

## </resources>


Ok, I think I have said everything is needed to say to let you work with Jangaroo. Now let’s talk about my results. My intent was to compare the performance of Jangaroo against the Jeash performance using the incredibly bad code I wrote for the [shoot’em’up](https://bitbucket.org/sebas77/haxe-demo) I have created for the first tutorial of this series. However in this case bad code adds value to the experiment, because it can be used to gauge how good the compiler is.

The results are quite interesting. At first it seems that Jeash beats Jangaroo in every aspect. Jeash is infact much faster (60fps against 30fps) and more compatible across the browsers (the game works on every modern browser known using Jeash, while the Jangaroo version behaves quite differently and in some cases wrongly). Jeash seems to use pretty neat CSS tricks to incredibly optimize the performance. However there is a very important aspect to take in consideration: Canvas blitting. In this case Jangaroo seems way better than Jeash. Both version of FlashPunk and Flixel, as the flash coders know already, use only bitmap blitting to render the entire screen without using the flash display list at all. It is pure old school 2D blitting.

[@teormech](https://twitter.com/teormech) on Twitter is currently porting [Flixel to Haxe](https://github.com/Beeblerox/HaxeFlixel) and experimenting with Jeash as well. He found out that the Jangaroo[ Flx invasion demo ](http://www.jangaroo.net/files/examples/flash/flxinvaders/)runs 3 times faster than his Jeash porting. According my profiling the Jangaroo version of the game takes approximately 3ms to render the 640×480 screen, while the Jeash version takes about 12ms!!! That means that for pure canvas application currently Jeash performance is very disappointing.

This is all! And this is very likely my last article regarding HTML5 technology. I have always been skeptical about HTML5 as platform for videogame developers and the current performance on desktop, but especially on mobile, demonstrate that HTML5 is not ready for professional game development.

Note: My first article and the considerations about Jeash written in this second one are based on the last version of Jeash (0.8.7) before it has been merged to HaxeNME. Unfortunately as today, the jeash version included in HaxeNME appears to be broken. Jeash seems to be sensibly worse than the previous version I worked with.


Jeash Bitmaps currently have a serious overhead which certainly explains your performance results: the Bitmap creates a temporary canvas where BitmapData’s canvas is copied over when it is modified – you can imagine the disaster.

That said I agree that fullcreen canvas performance on mobile is still not there.

Hello Philippe,

thank you for stopping by. Yeah I hope the NME guys will improve jeash, I really like the whole project and I understand the difficulties to maintain it. However I believe that Jeash is a very important module of the NME framework.

Hi Sebastiano, thanks for blogging about Jangaroo with a focus on JooFlash! It is totally true that documentation becomes scarce when it comes to JooFlash (in contrast to Jangaroo itself), so sharing your experience and giving tips is very useful for others! It’s a pity you do not provide an online version of the JooFlash version of your shoot’em’up (or did I miss that part?) so that people can try it out and compare themselves. I understood you got it to run, eventually, and rotation only did not work in Opera? You are also right about the need for a… Read more »

WOW, I say WOW…the performance is much higher than I expected with single canvas rendering!

About the project, you are right the results did not convince me. However I will create a new repository on github in order to let the people try it.

We just released Jangaroo / JooFlash 1.0.0, including the “single-canvas” rendering solution. Currently, you have to set stage.cacheAsBitmap = true to enable that mode. Maybe we should have used it as default, because it actually works much better than the old mode, except for interactive DisplayObjects like TextField etc. See “shootemup” running with JooFlash 1.0.0 at http://jangaron.net/shootemup/1.0.0/ I’d push the Jangaroo version of your shootemup project on github, but since it contains your original source code, I’ll wait for your agreement. Actually, if I remember correctly, the only change to your source code is the line given above to enable… Read more »

I tried the last link on my PC with chrome, but there is something wrong with the size. The ship is not centered and the sprites are not clipped. It is like the game area is way bigger than the background.

Great, thank you very much for the update! I just uploaded the code on github, but I did not test it, it should be the last one though. if you have any problem, please let me know! https://github.com/sebas77/haxe-jangaroo-html5benchmarks

It’s rather that your background image is too small… 😉

The game area now uses the whole available size, but the background image size is limited and it does not repeat, so it looks awkward.

well, the problem is that the game was designed for a specific size. I mean the game area size must be optional and of course decided by the developer. I do not want always to be able to play the game in full screen. Let me know what you think about it.

You are right, it was rather an experiment to set your game to “100%” for both width and height in the HTML wrapper. Of course, like in “real” Flash, you can still specify a concrete pixel width and height, and the game will not be resized. The behavior also depends on stage.scaleMode, while I did not yet implement the exact semantics of scaleMode like in Flash.