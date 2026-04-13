---
title: 'The Ultimate Cocos2D Project: Libraries'
url: http://www.learn-cocos2d.com/2011/03/the-ultimate-cocos2d-project-libraries/
author: Justin says
published: '2011-03-04'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Put simply: [Kobold2D](http://www.kobold2d.com/) is designed to make Cocos2D developers more productive.

#### Original Post

Last week I wrote that I’m [Building The Ultimate Cocos2D Xcode Project](http://www.learn-cocos2d.com/2011/02/building-ultimate-cocos2d-project/). In today’s weekly update I wanted to give you some more details on the use of libraries in that project.

### Cocos3D included

So there happens to be a [Cocos3D](http://brenwill.com/cocos3d/) now. Rather than being part of the Cocos2D distribution, it’s an extension project. Guess what that means? Right, installing Cocos3D means fumbling with the dreaded install-templates.sh script (see [this Cocos3D tutorial](http://sree.cc/iphone/how-to-setup-and-build-your-first-cocos3d-hello-world-project)). Of course the first user reactions were: how do I install it? Installation failed, what am I doing wrong? And so on …

The Ultimate Cocos2D Project wouldn’t be ultimate if it didn’t include Cocos3D out of the box. And unmodified of course, as with all included libraries I want to make it as simple as possible to replace one library version with another. Once you get to half a dozen of included libraries, maintaining them all can become a hassle, so the very least I can do is to make it easy for everyone to upgrade specific libraries.

### Obviously: Cocos2D included

Of course Cocos2D is also included as a static library as opposed to cluttering your project with all of its source files. Xcode project references make it very convenient to add external code and keeping it seperate. I’ve described the process in detail in my [Cocos2D Xcode Project tutorial](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/) but since then I’ve learned a couple more things about how to make this even better.

For example, I no longer include cocos2d-iphone directly, instead there’s a seperate Xcode project in between so that I have full control over build settings (using XCConfig files) and make it possible to build both iOS and Mac OS targets in the same Xcode project. I will also include the current version of Cocos2D in the download because my goal is to make everything work out of the box.

No fumbling with install scripts, no additional downloads necessary, no need to modify any Xcode build settings - including developer certificates and header search paths. Build configurations for Ad Hoc and App Store release builds are also included, which will create .IPA and .ZIP files for you ready for Ad Hoc distribution respectively upload on iTunes Connect.

### Popular libraries included

Now let’s get to the juicy part. Early on I realized that Cocos2D users often needed (or wanted) to include other libraries. Some of them have become so popular among the Cocos2D crowd that they could as well be part of the official distribution. Alas, they’re not. That’s a service I want to provide.

Often those libraries require special and non-obvious steps to successfully add them to an existing project. All too often those steps are either undocumented, untested, hard to follow, refer to outdated versions of Xcode, iOS SDK, etc. and generally require technical expertise of project configuration and compiler settings.

This is all taken care of for you. Here’s the list of libraries that are already included in the Ultimate Cocos2D Xcode Project:

[Cocos2D](http://www.cocos2d-iphone.org/)(iOS & Mac OS in the same project)[Cocos3D](http://brenwill.com/cocos3d/)(ready to use of course)[Wax](https://github.com/probablycorey/wax/wiki)&[Lua](http://www.lua.org/)(Wax is enabled and setup, essential Lua functions have an ObjC interface)[ObjectAL](https://kstenerud.github.com/ObjectAL-for-iPhone/)- “iOS Audio, minus the headache” (has[excellent documentation](https://kstenerud.github.com/ObjectAL-for-iPhone/documentation/index.html)!)[iSimulate](http://www.vimov.com/isimulate/)- lib included with permission, requires separate[iSimulate Lite App](http://itunes.apple.com/us/app/isimulate-lite/id351339630?mt=8)or[full version](http://itunes.apple.com/app/isimulate/id306908756?mt=8)- Cocos2D Gems:
[GameKitHelper](http://www.learn-cocos2d.com/2011/01/game-kit-data-sendreceive-demo-project/),[ClippingNode](http://www.learn-cocos2d.com/2011/01/cocos2d-gem-clippingnode/),[Multiple Update Selectors](http://www.learn-cocos2d.com/2011/03/scheduling-multiple-update-selectors/),[FrameOrFile](http://www.learn-cocos2d.com/2011/01/helpful-ccsprite-code-gem/), more… [iAd](http://advertising.apple.com/)(already setup in RootViewController, just enable it)[Chipmunk SpaceManager](https://code.google.com/p/chipmunk-spacemanager/)(ObjC interface for Chipmunk physics)[SneakyInput](https://github.com/sneakyness/SneakyInput)(or alternative Joypad library if there is one)[Objective-C Optimized Singleton Macro](https://github.com/cjhanson/Objective-C-Optimized-Singleton)(gets rid of[@synchronized](http://www.thaesofereode.info/clocFAQ/#sync-what)to improve speed)[LOG_EXPR](https://github.com/VTPG/CommonCode/blob/master/VTPG_Common.h)(logs any statement, no format strings needed:**LOG_EXPR([self contentSize])**)- … did I miss an essential library? Please leave a comment!

That is quite a list. All you need to do to use these libraries is to either enable them in code or merely include the header file and start using them. If you worry that all these libraries will bloat your App, rest assured that Xcode is very clever: if you don’t actually make use of a static library (eg don’t include any of its header files), it will not be linked with your App and not waste any space or performance. I verified that.

### Update policy

These are a lot of libraries to keep up to date. I plan to make about 4-8 point releases each year, usually triggered by a major (speak: non-beta) release of Cocos2D. If updating other libraries justifies an update depends on the library’s importance and the significance of the update.

### Your libraries

Adding your own libraries to the project will be easy and the process will be documented. This will encourage code-sharing because your library will just work with other user’s project, it only needs to follow a few simple guidelines to become plugin-capable. This opens the door for better and tighter integration of 3rd party code into your projects. Even if you don’t intend to share your code, you’ll still benefit because your code will be easier to re-use and maintain.

Also, if you like you can make a request for a specific library or additional source code that should be included in the project, please leave a comment. I’ll see what I can do. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[Chipmunk](http://www.learn-cocos2d.com/tag/chipmunk/)•

[ClippingNode](http://www.learn-cocos2d.com/tag/clippingnode/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[cocos2d-iphone](http://www.learn-cocos2d.com/tag/cocos2d-iphone/)•

[cocos2d-project](http://www.learn-cocos2d.com/tag/cocos2d-project/)•

[GameKitHelper](http://www.learn-cocos2d.com/tag/gamekithelper/)•

[isimulate](http://www.learn-cocos2d.com/tag/isimulate/)•

[KK](http://www.learn-cocos2d.com/tag/kk/)•

[libraries](http://www.learn-cocos2d.com/tag/libraries/)•

[Library](http://www.learn-cocos2d.com/tag/library/)•

[Lua](http://www.learn-cocos2d.com/tag/lua/)•

[SneakyInput](http://www.learn-cocos2d.com/tag/sneakyinput/)•

[SpaceManager](http://www.learn-cocos2d.com/tag/spacemanager/)•

[static library](http://www.learn-cocos2d.com/tag/static-library/)•

[Wax](http://www.learn-cocos2d.com/tag/wax/)•

[Xcode](http://www.learn-cocos2d.com/tag/xcode/)

Super cool. For each project, I was thinking that it might be better to bundle its static lib (.a) and its headers (.h) into a single, versioned, “static” framework. (see http://goodliffe.blogspot.com/2009/09/code-creating-framework-for-iphone.html )

Any thoughts?

Frameworks will be useful if you have a commercial library and you want to share the framework for free and sell the source code.

For the existing open source libraries that would create two problems: you no longer have source code you can step into because the framework is only a static library. And I would be solely responsible for updating each library, since creating a framework from a library is out of the question for most developers. I’d rather give them the ability to simply replace the folder with a new version of the library and unless there were substantial changes it should just work, or require little extra work (eg add new files to the project).

I guess I’m not understanding the implementation details. From your description I think you are saying that the “ultimate” project will have many library folders, and inside each library folder will be the entire source code for the given library. Furthermore, the project will have a whole bunch of static library targets, and the main project target will just include them as dependencies (but the default linker magic only includes them in the product if they are used). Correct?

Essentially that’s it. Each library is built to a static library and referenced in the main project. Additional code glues it together. The build settings are controlled via XCConfig files, so changes in build settings can be applied quickly and globally.

Wow! Nice work you have pulled off here again, I guess it’s yourmprevious template but now on steroids!

If all these libraries are included by default will it make our binaries hevier? Or Xcode works out what is used and only includes used libraries?

Thanks

On steroids it is.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


As I said, Xcode knows when a library is in use and when it is not. I have been adding all these libraries to the project, but the App size only changes when I actually make use of one of these libraries (including a header file in some cases is enough, in others you have to actually make calls to a function of the library). Furthermore I read that Xcode (respectively the GCC linker) even strips out the parts of a used library that aren’t needed for the app, but I haven’t verified that.

Totally awesome, you are a champion! Keep up the great work. This is escalating cocos to a new level!

And you do that with Xcode 4 of course? Sooner or later this will be the only Xcode we may use to submit apps to Apple.

Once Xcode 4 is out I’ll look into it. Ideally I want to make the project compatible with both Xcode 3.2 and 4.0 during the transition phase.

Ok, out now![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Sounds amazing!

Could i suggest AdWhirl/AdMob library to go along with the iAd support.

David

Sure you can.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Sounds great - when will it be available and how do i get it?

Hey Steffen,

How’s progress coming along? And when should we expect to see this final release?

Sounds cool!![:-)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Box2D is missed I guess

Well, Box2D and Chipmunk are both part of Cocos2D. But on closer inspection I realized they aren’t complete. For example, the Objective-Chipmunk demo is completely missing from the Cocos2D distribution. So I’m toying with the idea of simply creating separate libraries for those physic engines using the official distributions.