---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13803-get-the-latest-version-of-this-document-and-more/
author: Carl says
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Get the latest version of this document and more!

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

This document was created by Steffen Itterheim exclusively for [www.learn-cocos2d.com](http://www.learn-cocos2d.com/) --> Visit the Website for cocos2d for iPhone Starter Kits, Game Components, Tutorials, Frequently Asked Questions, Free Source Code and more!

Follow this link to [view or download the latest version of this document](http://www.learn-cocos2d.com/knowledge-base/) in the www.learn-cocos2d.com Knowledge Base.

### Join my Newsletter

[Join my Newsletter](http://ymlp.com/signup.php?id=gebusqsgmgj) to stay informed on any updates and additions to the www.learn-cocos2d.com website!

I get “cocos2d.h:No such file or directory” when trying to #import “cocos2d.h”

what am I missing?

ups, the path to the source code was wrong.

This tutorial is toooo long.

Is there a short version ? I spent two hours on this and as I expected nothing works.

For begininers its not going to work

Great info! Thanks! However, the script is building the .ipa file before it does the codesign step. Have things changed in Xcode? How do I get the script to run after the codesign step?

I tried twice to follow your tutorial step by step using cocos2d 0.99.5-rc1, Xcode 3.2.5 and iOS 4.2.1, but I keep having problems when building and running on device.

The weird thing is I have no problem at all running the template on simulator!

To be more clear:

I’m trying to build and run following the final step of “Getting our Project Template to build minimal cocos2d code” section.

Running on simulator works perfectly, running on device (iphone4) crashes after splash screen with this message on console:

“Program received signal: “EXC_BAD_ACCESS”.

warning: Unable to read symbols for /Developer/Platforms/iPhoneOS.platform/DeviceSupport/4.2.1 (8C148)/Symbols/Developer/usr/lib/libXcodeDebuggerSupport.dylib (file not found).

Previous frame inner to this frame (gdb could not unwind past this frame)”

By stepping with debugger I found the app crashes on line 98 of AppDelegate.m:

“// make the View Controller a child of the main window

[window addSubview: viewController.view];”

I see there are little differences from your (great) tutorial and Xcode/cocos2d new templates, mainly for the use of RootViewController, may this crash be related? (I already added RootViewController.* to my template)

Has anyone found a fix to this problem?

Please please please help me, this thing is driving me crazy =/

Thanks

It might be related. Have you tried the version on github? https://github.com/GamingHorror/cocos2d-project

That version is tested with 0.99.5

But I recently started getting those “could not unwind” errors … I was able to fix them by changing the compiler in all referenced projects back to GCC.

Bingo!

Thanks a lot, you point me to a fix.

I had already tried with your latest github version, without luck.

I followed your suggestion, changing the compiler to GCC 4.2 on all projects (both cocos2d-project and cocos2d-ios) and it worked!

I suppose the problem was in compiler setting for cocos2d-ios, it was set to LLVM compiler 1.6.

If I set compiler to different version for the two projects, I always get that crash, when using same gcc version, everything is ok.

I tried also with LLVM GCC4.2 on both projects and it works too.

Probably I never met this problem since using cocos2d built-in templates everything get compiled using gcc without further setting.


Thanks a lot for your tutorials… and for fast replying too

Hi Steffen

To upgrade a project created with your template from e.g. 0.99.5 rc1 to the final 0.99.5 I just need to copy over the cocos2d-IPhone folder?

I would assume yes but thought of asking since it does not clearly covered in the main points/links at the top of this tutorial

Correct, although you should keep a copy of the old folder just in case.

I receive a lot of EAGLView may not respond to …xxx warnings, and I believe these are the undeclared selectors you are mentioning in your comment. How can I fix it? Only with turning off the treat warning as error option or also by changing the code?

I didn’t understand where to implement the code from your comment on this tutorial.

BTW, the entire tutorial is really great!!

If you get these errors then it’s because the EAGLView has changed in the latest cocos2d version. It should work with the cocos2d-project that you can get from github: https://github.com/GamingHorror/cocos2d-project

Hi

1st: GREAT job on this PDF. Realllly appreciated.

I just did the first part up to Helloworld with the 99.5 version. (up to page 43 of pdf)

You might want to update a bit, the part where we get the AppDelegate from Helloworld sample : since in 99.5 Cocos changed the samples so that for exemple main.m does not exists main() is in the delegate.m file.

Continue the great work.