---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/14336-installing-the-file-new-project-template-for-xcode/
author: Carl says
published: '2011-09-30'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Proj.](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Installing the "File -> New Project" Template for Xcode

**All the experiences described in this tutorial have been utilized to help create the**

[Kobold2D](http://www.kobold2d.com/)game engine.[Kobold2D](http://www.kobold2d.com/)you can bypass this tutorial and instead rely on a working solution with many improvements not described in this tutorial.

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

Tim Soliday, who is blogging about his iPhone programming experiences on his [FatFingerStudios blog](http://www.fatfingerstudios.com/) was kind enough to turn my Xcode Project into a ___Template___ Project that can be installed into Xcode, so that it is available when you choose File -> New Project from the Xcode menu.

### Unzip the "cocos2d Application.zip" file

Unzip the file anywhere, then right or control click on the folder and select Copy "cocos2d Application". Make sure to copy the whole folder.

### Paste it to ...

Paste the "cocos2d Application" folder to the following path:

**/Developer/Platforms/iPhoneOS.platform/Developer/Library/Xcode/Project Templates/Application**

Make sure you don't accidentally select iPhoneSimulator.platform.

### Select New Project in Xcode

You can do this from the "File -> New Project" menu or from the Startup Splash Screen as shown above.

### Et voilá!

Under iPhoneOS select Applications and there you should see a "cocos2d Application" project type.

Note that while creating new cocos2d projects this way may be more convenient than copying the project folder on disk and subsequently renaming the project, it does defy the purpose of using source control to keep a common base project in source control. However it still allows you to stay in synch with the cocos2d-iphone game engine files so i'm sure 95% of all users will benefit from using this Xcode Template.

**Again, thanks a lot to Tim Soliday for creating the Xcode Template based on this Tutorial!**

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

I think your problem was optimization level, believe it or not. If you’re using the LLVM compiler, and you set optimization level to “none” (-O0), then a call to glColor4ub() in CCLabelAtlas will kernel fault on the device, but not in the simulator. Since adding the view controller to the window is what kicks off the render loop, and since every app has a CCLabelAtlas in it (the framerate counter), how this manifests itself is that you do the addSubview call and suddenly your app crashes without a stack trace. Deuced hard to track down.

The fix (apart from using the old GCC compiler, which is really not a good idea anymore-Apple is close to deprecating it) is simply to set optimization to -Os. I realize it’s bizarre for the *lower* optimization level to introduce bugs.

Oh, but be sure you delete the target-level build settings before you do this, as Steffen described above. The “Debug” configuration of the Cocos2D project sets optimization to -O0 on each target individually.

Hi Steffen

To upgrade a project created with your template from e.g. 0.99.5 rc1 to the final 0.99.5 I just need to copy over the cocos2d-IPhone folder?

I would assume yes but thought of asking since it does not clearly covered in the main points/links at the top of this tutorial

Correct, although you should keep a copy of the old folder just in case.

I receive a lot of EAGLView may not respond to …xxx warnings, and I believe these are the undeclared selectors you are mentioning in your comment. How can I fix it? Only with turning off the treat warning as error option or also by changing the code?

I didn’t understand where to implement the code from your comment on this tutorial.

BTW, the entire tutorial is really great!!

If you get these errors then it’s because the EAGLView has changed in the latest cocos2d version. It should work with the cocos2d-project that you can get from github: https://github.com/GamingHorror/cocos2d-project

Hi Steffen!

I am trying to implement the Spacemanager for quite some time now, but it doesn’t work.

I can compile the example project of the Spacemanager package without any problem, but in this template I receive following error:

“SpaceManager.mm:749: error: could not convert ‘cpSpaceSegmentQuery((*(cpSpace**)(((char*)self) + OBJC_IVAR_$_SpaceManager._space)), start, end, layers, group, ((void (*)(cpShape*, cpFloat, cpVect, void*))collectAllSegmentQueryShapes), ((void*)array))’ to ‘bool’

”

Do you know a solution?

Thanks!

Mehdi

Hi

1st: GREAT job on this PDF. Realllly appreciated.

I just did the first part up to Helloworld with the 99.5 version. (up to page 43 of pdf)

You might want to update a bit, the part where we get the AppDelegate from Helloworld sample : since in 99.5 Cocos changed the samples so that for exemple main.m does not exists main() is in the delegate.m file.

Continue the great work.

Dude, you ruuuuuuuuuuuuuuuuuuule! Thanx a lot for this great tutorial!

My goodness, this is a very precious article, every line of the PDF is important and will save hours of repletion in your build cycles.

Thanks Steffan.

Regards Sree

[...] Knowledge Base [...]

Can you update this for XCode 4?

Yup, work in progress: http://www.learn-cocos2d.com/tag/kk/

Kobold2D is going to replace this? if so can how can anyone get access to it since i understand its still a work in progress?

Thanks

With patience.


best guide u will find on the whole internet!

Hi Steffen,

Thank you for the fantastic Tutorials,.

)

I saw your facebookHelper file, and it would be fantastic to get a tutorial to make a similar File for the actual API

Greetings

Anselm

hi! i have problems with xcode 4 and the cross-project references.

When i “Add Target Dependencies” (in xcode4 is : Select Target: Build Phases: Target Dependencies: “+”:cocos2d) i have this error:

ASSERTION FAILURE in /SourceCache/IDEXcode3ProjectSupport/IDEXcode3ProjectSupport-269/Xcode3Sources/XcodeIDE/Frameworks/DevToolsBase/pbxcore/PBXContainerItemProxy.m:33

Details: Assertion failed: portal != ((void*)0)

Object:

Method: -initWithType:portal:remoteGlobalIDString:remoteInfo:

Thread: {name = (null), num = 1}

Hints: None

Backtrace:

[removed for clarity]

Any ideas for fix it?

Xcode 4 has a better concept than cross-project references: workspaces. Kobold2D uses a workspace to get the various projects together.

Although the cross-project references still work in Xcode 4. Maybe upgrading to Xcode 4.1 or 4.2 (beta) will help.