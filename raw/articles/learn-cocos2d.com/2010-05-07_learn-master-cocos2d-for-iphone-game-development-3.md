---
title: Learn & Master cocos2d for iPhone Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13801-how-to-get-the-xcode-project-template/13843/resolve-true/
author: Receptor says
published: '2010-05-07'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Features of the cocos2d Xcode Project Template

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**No images? Reload page, wait and try again.****PDF download broken? Reload page, try again.**- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!


We'll create a professionally setup Xcode Project Template for cocos2d for iPhone. This is the feature list.

### Features of the cocos2d Xcode Project Template

- 4 Build Configurations (Debug, Release, Ad Hoc Distribution and App Store Distribution)

- IPA Files automatically created for your Ad Hoc Distribution builds

- ZIP Files automatically created for your App Store Distribution builds

- correct debug symbol stripping for App Store Distribution and debugging crash logs

- cocos2d-iphone referenced by Project, allowing you to keep cocos2d-iphone up to date with the least amount of work

- Build Targets to build regular iPhone/iPod and iPad Apps in both Full and Lite Versions

- additional Build Targets to debug memory crashes effectively and running the Static Analyzer

- Preprocessor Macros to differentiate the different build targets in your code

- Aggregate Target to build all your regular Targets at once

- properly configured precompiled Prefix Headers, reducing your compile times

- supports both Physics engines: Chipmunk and box2d

- all build settings optimized for maximum performance and building quality code, and taking into account Xcode's layered Build Settings

Hi, I really liked this tutorial. It’s very well written!

One question though. From the title I thought I would end up with an actual XCode template that I can find when I choose New Project. Did I misunderstand or miss something?

Thanks!

No, apparently i was blissfully unaware of the actual Xcode ___TEMPLATE___ structure developers expect. It’s still a template in my eyes but i was rather thinking of using it together with source control. Meaning the project template is a base project that you can branch off of via source control software, then make changes to either the new or the base project and when you need it you can integrate the changes back.

If you don’t use source control simply make a copy of the project in the same folder, then rename it. Other than that you have to use Xcode’s “Rename Project” functionality there’s no difference to an actual project template, nor does a real Xcode Template provide you with more or better features other than that you can select it from New Project and name it, instead of making a copy of the folder. So i don’t see the big gain of having a Project Template you can select from Xcode itself and if you use source control, it’s actually a hindrance.

PS: one user just sent me a real __TEMPLATE__ … i’ll have a look at it and will post it here if it works.

Hey Steffen

I’m a Graphic Designer and Illustrator who has would like to get into and use Cocos2D to create a game. I have some knowledge of HTML and CSS, but that’s as far as my programming skills go. I have read about Objective C and downloaded Xcode and the iPhone SDK, however I feel there are some basics I still can’t find explained anywhere, such as class, object, how to debug. I have also tried several online tutorials, but keep hitting obstacles in the form of errors. I believe some of the reading I have done is simply outdated, while some of it is just too complicated.

What do you think is the best way to learn to use Cocos2D completely from scratch, and do you know any resources that would be a good read for someone in my position? Any help would be appreciated.

Cheers

Magnus

Hi Magnus,

since you have little programming experience you should try it with books. Granted, you can learn from the Web but as you experienced it, things can be outdated, or just plain wrong, and instead of a learning curve you’re facing a tour de force. I can recommend “Learn Objective-C on the Mac” from Apress, it’ll also help you understand the concepts of classes, properties and things like that. From there you can step up to “Beginning iPhone Development”, also from Apress.

For a quickstart in Objective-C i can recommend this link: http://cocoadevcentral.com/d/learn_objectivec/

I agree that for debugging there are little good tutorials and there are as many techniques as there are errors/bugs/crashes. Here it’s not so much about the tools and how they work but more about when to use which tool and how depending on the type of problem you’re having. Maybe i can shed some light on this, i made a note in my todo list.

Btw, i can totally relate to your position because you’re not just facing to learn cocos2d as a game engine but also Xcode, Objective-C and general programming techniques. So it can be overwhelming, i was facing something similar even as an experienced programmer when i had to build a tool on my own, with half a dozen new technologies and new programming mehodologies. While it may be frustrating and painful, stick to it. You’ll learn a lot! I wouldn’t want to repeat the pain but more than that i wouldn’t want to miss what i’ve learned so painfully. And it always helps to partner up, even if it’s just on a forum. I believe one of the most effective ways to solve a problem is to try to ask someone for an answer - i’ve written many emails i’ve never sent because in the process i realized what i hadn’t tried yet.

Broken img links on this tutorial.

Hmmm they work for me. But you’re the second person to report broken images. Could it be an adblocker? I took a look at the image names and they all have this in their name: “Upgrade_Target_for_iPad.png”. Harmless until you consider that the filename ends in “ad.png” and if your adblocker is overly aggressive i’m sure it’ll filter that.

It’s been working fine until this morning, I was going thru your tutorial again since I did something wrong when I use the template. I keep getting errors when I build it, it says; Cocos2d.h : No such file or directory.

I’m going over your tutorial over and over again to see if I missed any details, but I cant find anything. I’ve not been doing programing since C64 was hot, so it’s been a while….by the way sound like I’m a hundred y/old, I’m 32.

Would be nice with a tutorial about how to go about when sketching out the idea, graphics design etc, all pre-work that goes into the project before you start programing.

Check again that your path to cocos2d-iphone is set and named correctly in Xcode:

http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13471-configure-xcode-for-cross-project-referencing

If it can’t find cocos2d.h it doesn’t know where it is, so either the path above is broken or you moved it or renamed the folder or any parent folder that it’s in. I hope this helps.

Hmmm … a Tutorial about Preproduction and even before that what we call “Discovery”. Good idea, i like it. There’s too little written about it and even big (huge) companies can just totally not get it right.![;)](../../../../../../../../wordpress/wp-includes/images/smilies/icon_wink.gif)


Noted…

want to see images!

Can you try again please? There seem to be temporary broken images, i’m still trying to figure out what’s causing it. In the meantime, waiting a few minutes and refreshing the page seems to fix the images.

Thanks for putting up the project. I’m getting close to finishing my first app, and was thrilled to see an easy way to update the cocos2d libraries, so I’ve moved everything over.

The app builds, but I’m having one problem. I’m using the simpleAudioEngine and am having absolutely no luck linking to it. I’ve added the CocosDenshion dependency to the targets, am including SimpleAudioEngine.h like I always had, but still get

Undefined symbols:

“.objc_class_name_SimpleAudioEngine”, referenced from:

literal-pointer@__OBJC@__cls_refs@SimpleAudioEngine in edgeMates_SpanishAppDelegate.o

literal-pointer@__OBJC@__cls_refs@SimpleAudioEngine in tile.o

ld: symbol(s) not found

collect2: ld returned 1 exit status

Could you tell me what I’m missing?

Thanks

You need to add CocosDenshion both as a Dependency and Linked Library. If you choose Get Info on a Target and select the General Tab, under Direct Dependencies it should list “CocosDenshion (from cocos2d-iphone.xcodeproj)” and below under Linked Libraries the file “libCocosDenshion.a” must also be listed. You probably forgot one of these two steps, probably the latter. To add libCocosDenshion find the file by selecting the cocos2d-iphone project in the Groups & Files and then drag & drop it onto a Target. Repeat for each Target. I hope this helps, let me know!

That was exactly it! I read and re-read that section several times, but didn’t look deeply enough to find the .a file. Really looking forward to using your memdebug build. I knew I was going into optimization blind.

thanks,

bob

This is a great tutorial! I made template for my game project, and everything was Ok until i’ve tried to import Box2D.h. This leads to multiple errors like:”Box2D/Common/b2Settings.h: No such file or directory”. Can you help me, please?

I also see tons of errors caused by Box2D.h - I’m using cocos2d .99.2

It’s very unfortunate, as the rest of the tutorial went smooth as butter and it looks really, really great !

Yes, i’m getting the same error. I’m sorry, i haven’t tried importing box2d.h header myself. I tried the obvious, adding the box2d path as User Header Search Path but that didn’t seem to be enough. I’ll investigate and when i know what needs to be done i’ll update the Tutorial. I’m sorry for this oversight on my part.

ha ! found it


In the Build Settings in the Header Search Paths you need to add “$(COCOS2D_SOURCE)/.” - that will do the trick

Ah, i put it in “User Header Search Path” but that didn’t work, adding it to “Header Search Path” worked but now i get a ton of compile errors.

NOTE: I’ve added a lesson that details the box2d fixes. Read more about the latest Tutorial changes in this blog post:

http://www.learn-cocos2d.com/2010/05/xcode-project-tutorial-updates-box2d-template/

I have been building a game, and I recently ported all my files over to your template. It built and ran before, but now I am getting conversion errors EVERYWHERE saying “Implicit conversion shortens 64-bit value into a 32-bit value.” HELP!

Please review the build warnings here: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13730-tweaking-our-build-settings/

This setting generates the warnings you get:

(2) Implicit Conversion to 32 Bit Type: on

Depending on the code this can be pointing to programming errors, such as using math functions that return double when you only need float precision (which is also a performance issue). Also, don’t use double datatypes unless you absolutely have to, as they require more memory and computations are slower.

GCC 4.2 Code Generation tab not showing up in my “cocos2dXrefTest” Info tab. What should I do?

It must be there. Make sure you’re on the build settings tab and the search textbox (upper right on the dialog) is empty.

libz.dylib doesn’t show up in my Frameworks list either…what should I do?

That is strange. It should be there unless you select a different lib category in the dialog where you can choose a library/framework (when you click on the + button). If it’s still not there maybe Xcode isn’t installed properly but that’s just a guess. Are you using the Xcode 3.2.2 version?