---
title: Building The Ultimate Cocos2D Project
url: http://www.learn-cocos2d.com/2011/02/building-ultimate-cocos2d-project/
author: Tweets that mention New Cocos
published: '2011-02-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Put simply: [Kobold2D](http://www.kobold2d.com/) is designed to make Cocos2D developers more productive.

#### Original Post

First Friday update after [the teaser post](../../../2011/02/teaser/). I’m working on a new project. I’m still fleshing out the details of the “killer-feature” and making tests, so I can’t really talk about that. But I can tell you what I have already up and running.

#### The Ancestor: cocos2d-project

You may remember the [Xcode Cocos2D project tutorial](../../../knowledge-base/tutorial-professional-cocos2d-xcode-project-template/) I wrote almost a year ago. The goal of that was to use Cocos2D as an external library in order to be able to update Cocos2D simply by pulling a new version from git, or just by replacing the Cocos2D folder. I gave the resulting project a boring, uninteresting, generic name (so typical for a programmer): [cocos2d-project](https://github.com/GamingHorror/cocos2d-project).

The new and improved cocos2d-project not only has a spiffy name (to be announced) but also raises the bar not one but two or maybe even three levels, depending on perceived value. It’s definitely leaps and bounds ahead of the Cocos2D distribution project, especially if you care for how source code projects should be composed.

#### One Xcode project for both iOS & Mac OS X Targets

One thing that really bothered me when Cocos2D became capable to build Mac OS X applications was that it required a separate Xcode project for each platform. If you’ve ever done cross-platform development you know this isn’t going to make you happy. Every action needs to be done twice, add a resource in one project, then you must also add it in the other. Change a build setting in one project, also change it in the other. Build and run in one project, then build and run the other project with a completely different window layout and probably duplicating all the floating windows aka “Is that the Mac OS debugger or is it the one for the iOS project?”. You name it.

![Screen shot 2011-02-25 at 19.35.27](../../../wordpress/wp-content/uploads/Screen-shot-2011-02-25-at-19.35.27-217x300.png)


I did some research, then a test, and It turns out: it’s entirely possible to target both the Mac OS X and iOS platform from within the same Xcode project. It works like a charm!

Really the only thing you need to keep in mind is that Xcode doesn’t give you the option to change the Active SDK by default. But if you click the Overview dropdown while holding down the Option key, you can select any SDK that’s installed on your system (see the image). The key here is to first change the Active Target to the Mac target, then Option-Click again and select Mac OS X 10.6 as the Active SDK. And the other way around to change back to iOS. So it’s a two step process but still way more comfortable than managing two seperate Xcode projects.

#### XCConfig Build Configuration

Behind the scenes there’s an additional step required to make this work, which I’ve been wanting to do for a long time: to use XCConfig files for build settings. Cocoaphony has a blog post [Abandoning the Build Panel](http://robnapier.net/blog/build-system-1-build-panel-360) describing the technique. The good part is: there’s less confusion between project-wide and target-specific build settings. Even more importantly, if you build several different libraries you want to build them with the exact same settings - with XCConfig files this is easy to do, manually changing the build settings of several projects with multiple targets simply isn’t practical.

Plus you can document each setting and you can still use the Build Settings Panel for your own needs while allowing me to use system-critical changes to the Build Settings. For example, if a certain build setting causes issues (eg like the switch to LLVM GCC) then I can change the setting and release a new version of the project, or just the build config file separately. You can then replace that file and it should fix the build (assuming you haven’t change that exact setting in the Build Panel). All of your customized Build Settings will remain untouched of course.

Those are only two very fundamental improvements on a system engineering level which probably won’t excite you too much if you focus on making games with any means necessary. I’m keeping the good stuff for a future update, hopefully in 3 to 4 weeks I’ll be able to give you some first details about the “killer-feature”. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. **Help me help you** by browsing the products in the **Learn Cocos2D Store**.
|

[…] This post was mentioned on Twitter by MagnetiCat, Steffen Itterheim. Steffen Itterheim said: New #Cocos2D #iDevBlogADayWL post: Building The Ultimate Cocos2D Project - http://tinyurl.com/4lsrpj8 […]

Awesome! Definitely looking forward to this. Will it also work from the command-line with xcodebuild?

I’m sure it will. It’s an Xcode project so I don’t see why it shouldn’t.

[…] week I wrote that I’m Building The Ultimate Cocos2D Xcode Project. In today’s weekly update I wanted to give you some more details on the use of libraries in […]