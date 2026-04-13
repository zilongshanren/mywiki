---
title: How to properly install the Cocos2D Xcode Project Templates
url: http://www.learn-cocos2d.com/2011/01/properly-install-cocos2d-xcode-project-templates/
author: Carlos Rivera says
published: '2011-01-04'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

You can get Kobold2D from [www.kobold2d.com](http://www.kobold2d.com/) which is an easy to use wrapper (and installer) for cocos2d and related libraries plus many example projects. If you want to support development of the new, modernized version of Kobold2D then please [consider joining KoboldTouch](http://www.learn-cocos2d.com/store/koboldtouch/).

#### Installing Cocos2D Xcode Templates

If all you want to do is to install one of the latest cocos2d version’s Xcode templates, type this in a Terminal window:

First, change to the cocos2d-iphone directory using the cd command, for example if you unpacked cocos2d to ~/Documents the command would be:

|
1 |
cd ~/Documents/cocos2d-iphone-2.0 |


Then run the Xcode templates installer script, -f forces overwrite of any existing cocos2d templates:

|
1 |
./install-templates.sh -f |


You can find more details in my blog post about [enabling ARC in a cocos2d project](http://www.learn-cocos2d.com/2012/04/enabling-arc-cocos2d-project-howto-stepbystep-tutorialguide/).

If you’re new to cocos2d or Objective-C programming, **make sure you enable ARC in all your projects**! Not using ARC will be a painful experience, it makes it harder to write correct Objective-C code, it will slow you down, it might even demotivate you. Use nothing but ARC. Please. I still see way too many cocos2d related questions on [stackoverflow.com](http://stackoverflow.com/) which would not be an issue if the users had simply enabled ARC.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

An installer for this would be awesome.

… and here’s the Cocos2D installer:

http://cocos2d-central.com/files/file/6-installer-for-cocos2d-for-ios-mac-os-x/

Hi Steffen,

I recently purchased your book on cocos2d game development and having issues trying to get cocos2d to work on my Mac. You see the install worked like a charm, but when I run a new app or even a template app from he cocos2d library, there are no default file installed, it’s as if they don’t exists. I’ve even tried to add them to project, even though this did work to some extent, I can’t see why I would have to do this tedious work time and time again every time I try to build a new cocos2d project. Why aren’t my files which are in the cocos2d templates directory being seen by Xcode. I’ve done the install several times now and still nothing. HELPPPPP…. lol

The templates of the stable version (cocos2d v0.99.5) don’t work with Xcode 4. I’ll update the installer to include the v1.0 beta which includes Xcode 4 templates.

When i try to create a new cocos2d application on Xcode4 with iOS 4.3, the projectname_AppDelegate.m and .h should be automatically created, but these files are not getting created and also classes directory is not created under cocos2d project

I’ve tried both the version cocos2d-iphone-1.0.0-rc3 and cocos2d-iphone-0.99.5, none of them worked.

Please can anyone help me out in this, exhausted 2 sleepless night for this but no solution.

-Naren

Have you tried re-installing the Xcode templates?

If you aren’t using my installer, you might want to try it because it installs the templates as well with the correct parameters:

http://cocos2d-central.com/files/file/6-installer-for-cocos2d-for-ios-mac-os-x/

Thanks for quick response, Mr Steffen

I’ve also tried re-installing the Xcode templates and tried installing you installer, but I’m still facing the problem.

Tried re-installing Xcode, no solution.

Missing projectname_AppDelegate.m and .h and classes folder in Xcode project

Here is my box details:

Mac version 10.6.7

Xcode version 4.0 Build 4A304a

iOS SDK 4.3

Please let me know if i miss anything.

thanks

In v1.0 projects the files are simply called AppDelegate.h / .m

Maybe you have corrupt templates that can’t be overwritten for some reason. Go to this folder:

~/Library/Application Support/Developer/Shared/Xcode/Project Templates/

Then delete all folders starting with “cocos2d” from that folder, and try re-installing the templates. If that still doesn’t help, do the same in this folder:

/Developer/Library/Xcode/Templates/Project Templates/