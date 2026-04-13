---
title: Kobold2D v1.0.2 now available
url: http://www.learn-cocos2d.com/2012/01/kobold2d-v102/
author: Bill Day says
published: '2012-01-27'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

**Kobold2D v1.0.2** is now available from the [Kobold2D Download page](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download)!

Read the [Release Notes](http://www.kobold2d.com/display/KKDOC/Kobold2D+v1.0.2+Release+Notes) for detailed list of changes. Most of them are minor as this is a **maintenance release**, but there’s a bug fix in KKInput’s gesturePanRecognizer that fixes the incorrect translation and velocity values. If you’re using the pan gesture I recommend to upgrade.

I’ve also taken the time to attempt to clarify [ what Kobold2D is about](http://www.kobold2d.com/display/KKSITE/Kobold2D+Features) with this … imagram:

I’ve been reading and enjoying [blah blah blah](http://www.danroam.com/) (not to be confused with [blah blah blah](http://blahblahbook.com/)) which prompted me to try a more visual approach. I highly recommend reading Dan Roam’s book! I’m sure you can’t draw either, but [you should do it anyway](http://xkcd.com/). Or try [Xmind](http://www.xmind.net/).

Hmmm … have you ever noticed how many great things start or end with an x?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Purchased the iPhone Game Kit, and was happy with the purchase. Got the logic of my new game running, and began working on the UI. This process took a few weeks, and then when I tried to build, I got a Mach-o linker error. Upgraded to Xcode 4.2.1, build 4D502 — no help. I was running against iPad 5.0 Simulator, and so installed the 4.3 Simulator and re-ran — no help.

So then I downloaded Kobold2D 1.0.2. Installed it to its default location (my user folder). Opened Kobold2D Project Starter.app, and created a workspace/project using the User-Input template. Clicked Create Project from Template. When the workspace opened, I clicked Run, and got a Mach-o linker error as “/Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/clang failed with exit code 1”.

Found a post that addressed something like 8 reasons why a Mach-o linker error could occur, and made sure none of those applied. Also, saw a couple posts in StackOverflow about Mach-o linker errors, and none of them seem to apply.

So, it seems for some reason, I am getting a Mach-o linker error “out of the box.” Not sure if I have something wrong, or if there is an error in Kobold2D 1.0.2, but, as I said, EVERYTHING about this last test was straight out of the box. Any help greatly appreciated.

I hope that was an oversimplification when you said you worked on this for weeks, and then you tried to build it? Usually the first thing is to figure out the most recent changes you made between the latest successful and the first failing build. If you can remember that, that would certainly help.

Do you get any other message besides “exit code 1”? In Xcode when you go to the Debug Log Navigator (must be in View menu) you can get more details on each entry, including the command line parameters that were passed to the compiler/linker. Sometimes this gives you an important clue, or you may spot something out of the ordinary.

Since your game is working but adding the UI caused the error, I would suggest stripping the UI temporarily, and then adding it back in one by one. This may be your best bet at resolving this issue, because obviously something introduced the linker error while you were working on the UI, so the problem is most likely with the UI.

You should also verify that you are using the default Build Settings. I know it can be tempting to tweak this or that but ultimately, unless you know exactly what each setting does it’s more likely to cause harm. For example, enabling “Link-Time Optimization” often causes “object too large” and other linker errors.

Also, and I mention this only because I’ve seen it done before, there is also a limit to what the linker can handle. This is specifically regarding ultra-large implementation files, something like 30.000 lines of code or more in a single source code file.

Hi Steffen,

Thanks for the answer. Unfortunately, I don’t see how it helps.

Yes, I made many oversimplifications. I have probably built at least 200 times. But, I think all of that is irrelevant, because of the following.

Once I got the problem, and tried MANY things, I decided to start over. I did the following, in the exact order shown, with no intervening steps; this is what I need help with.

Trashed my Kobold2D folder.

Trashed my Kobold2D.pkg.

Downloaded a new Kobold2D.pkg.

Ran the installer — installed to the default location (my user folder).

Created a project using the User-input template, named ProjectTest.

Opened Kobold2D.xcworkspace.

Ran ProjectTest-iOS > iPad 4.3 Simulator.

Got the following Mach-o linker error:

ld: file not found: /Users/bday/Kobold2D/Kobold2D-1.0.2/ProjectTest/build/Debug-iphonesimulator/libkobold2d-ios.a

Command /Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/clang failed with exit code 1

Went to the stated folder, and verified that libkobold2d-ios.a is not present. The file that is present is ProjectTest-iOS.app.

I have looked thru my build settings, and the only mention I see of libkobold2d-ios.a is a FORCE_LOAD_KOBOLD2D setting under User-Defined. But, I did nothing to set or change this.

So, this looks like an “out-of-the-box” problem with Kobold2D. It must be the case that there is something in my setup that is causing this problem, but I have no idea what. I do have other Kobold2D folders in my user folder, but not inside this Kobold2D folder we are addressing here, so I am assuming these others are not part of the problem.

To reiterate, NONE of my code is involved in the build addressed here, but the Mach-o error is occurring.

Are you absolutely sure you opened the .xcworkspace file, and not the .xcodeproj file? Because Kobold2D only works from the .xcworkspace file which combines your project with the Kobold2D Libraries project.

Yes. I am absolutely, 100%, sure.

Hmmm, what about the projects that came with Kobold2D, do you get the same error with these as well?

In case you haven’t read it yet, I recommend the Kobold2D FAQ entry about “exit code 1” errors and possible solutions: http://kobold2d.com/pages/viewpage.action?pageId=919841

I have read the FAQ entry (I actually mentioned it in my first post). Anyway, here are the answers to those issues:

1. ProjectTest looks just like the example.

2. only 1 .xcworkspace is open.

3. the .xcworkspace is open.

4. As I have said, no changes have been made to the project.

5. Archive build — irrelevant.

6. Kobold2D-libraries is not missing.

7. Kobold2D-Libraries.xcodeproj is not contained within ProjectTest.

8. Build Location is (and was) Location Specified by Targets. Changed DerivedData folder to /Users/bday — no change. Hard Drive has over 43Gb available. Xcode and User Folder and Kobold are on this drive.

I don’t quite know what you mean by “the projects that came with Kobold2D. Do you mean the ones that came with the iPhone Game Kit? If so, those projects have no .xcworkspace connected to them; does it matter which template I use to create one?

I Spotlighted libkobold2d-ios.a, and found it in /Users/bday/Kobold2D/Kobold2D-1.0.2/__Kobold2D__/build/Debug-iphonesimulator, not /Users/bday/Kobold2D/Kobold2D-1.0.2/ProjectTest/build/Debug-iphonesimulator. Is this a build setting issue?

By “projects that came with Kobold2D” I meant any of the templates. But rereading your initial post you already mentioned that that’s what you did.

Looks like something is broken on your system if you can’t compile any project. You might want to experiment with new projects created from Apple’s or cocos2d’s project templates though. If all of them exhibit this behavior it may be necessary to re-install Xcode.

Before I go and re-install Xcode, could you please address the fact that the Mach-o error is because libkobold2d-ios.a is in the __Kobold2D__ folder and not the ProjectTest folder (all other components of the path being the same); is this a build settings problem? If so, can you tell me what setting?

That’s the build location setting in Xcode preferences. By default it should be in a DerivedData folder but since you tried the suggestions in the FAQ it’s now placed in the project folder. Don’t worry about this too much, there is no location where the file *should* be respectively Xcode won’t put it in a place where it can’t find it.

Hi Steffen,

I have now trashed and re-installed Xcode and the iPhone SDK. I also trashed my ProjectTest project. I secure emptied my Trash before reinstalling anything. Created a new Kobold2D workspace/project named ProjectTestTwo, and get a Mach-o error as: ld: file not found: /Users/bday/Kobold2D/Kobold2D-1.0.2/ProjectTestTwo/build/Debug-iphonesimulator/libkobold2d-ios.a

Command /Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/clang failed with exit code 1. Spotlighted libkobold2d-ios.a, and found it in the __Kobold2D__ folder (as before). In other words, nothing has changed, except that the problem is not Xcode.

What build setting controls where YOUR template project looks for libkobold2d-ios.a?

Hi Steffen,

I went in to __Kobold2D__/build/Debug-iphonesimulator, and copied all the .a files found there (which includes kobold2D-ios.a), and copied them to ProjectTestTwo/build/Debug-iphonesimulator, and ran, and the build was successful and the project ran in the correct simulator. So, the issue here is the difference between Xcode looking for these .a files in ProjectTestTwo/build/Debug-iphonesimulator and these files BEING in __Kobold2D__/build/Debug-iphonesimulator. So, the question I need you to answer is, what build setting needs to change to fix this?

“What build setting controls where YOUR template project looks for libkobold2d-ios.a?”

There’s no build setting for that. A reference to each .a file is added in the “Link Binary with Libraries” build phase. Xcode 4 finds dependent libraries automatically.

I’ve been unable to reproduce the creation of libkobold2d-ios.a in the __Kobold2D__ folder, regardless of which setting I use for Xcode Preferences -> Locations -> Derived Data or its Advanced settings. My build output files are always put in a DerivedData folder with several subfolders.

Please do a “Product -> Clean” and then build the project again. Then send me the entire build log (copy it as described here: http://www.kobold2d.com/pages/viewpage.action?pageId=918902) by mail to steffen at learn-cocos2d.com. Maybe the log can help shed some light on this.

Btw, are you running Snow Leopard or Lion?

“what build setting needs to change to fix this?”

It’s the Xcode Preferences -> Locations -> Derived Data setting. Try the Default setting, then click the Advanced button and make sure the setting suffixed as (Recommended) is selected. To be sure, remove the “build” folder from Kobold2D as well as the location where Xcode seems to find the libraries. You may also want to use the Product -> Clean while holding down the option key, so that Clean changes to “Clean Build Folder”.

The comments here are not the best place to discuss this further because we can’t directly reply to each other anymore. You can continue to make reports on Cocos2D Central or send me an email.

I see the same problem as Bill Day does with clang, etc, with fresh templates downloaded (I have never used Kobold2d).

Some libraries (notably 320) require the build directory in the old style build in the folder style build setting. This setting in Xcode appears to break the templates (at least the parallax game template I’ve tried so far).

I’ve narrowed down the problem above: Your assumption about the build products directory being the place to find the .a files is wrong for the case for systems with build folders in the old-style place. These lines in FameworksAndLibraries.xcconfig are the issue:

FORCE_LOAD_COCOS2D = -force_load $(BUILT_PRODUCTS_DIR)/libcocos2d-ios.a

FORCE_LOAD_KOBOLD2D = -force_load $(BUILT_PRODUCTS_DIR)/libkobold2d-ios.a

…

FORCE_LOAD_COCOS3D = -force_load $(BUILT_PRODUCTS_DIR)/libcocos3d-ios.a

They are evaluating to the build folder in the template’s build directory instead of the build folder in the Kobold2d folder…which is where the .a files are actually being built and left.

A workaround is copying the .a’s from one folder to the other, however a more permanent solution is likely possible with different paths

Changing back to the default setting for build directories isn’t an option for people who do apps at their day jobs requiring that setting (or libraries that require it)..

Good catch! At least now I know where I need to concentrate my efforts on, that’s very helpful! Do you know the steps to reproduce the issue on my system? Which build location settings do I need to use?

I was able to reproduce the “ld failed with exit code 1” issue on my build machine after setting the Location Preferences in Xcode to “Custom” and under Advanced “Locations Specified by Targets”.

I’m now trying to find a general fix for this issue.

Thanks for introducing me to Dan Roam. I’ve always felt this way. Sometimes language gets in the way. Sometimes visuals are too abstract. But language + visuals is the key.

I’ve been using MindNode Pro (similar to Xmind) for a few months. It is addictive to plan projects visually