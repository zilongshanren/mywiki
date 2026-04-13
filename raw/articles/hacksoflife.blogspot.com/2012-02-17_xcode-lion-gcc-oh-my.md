---
title: XCode, Lion, GCC Oh My!!
url: http://hacksoflife.blogspot.com/2012/02/xcode-lion-gcc-oh-my.html
author: Chris
published: '2012-02-17'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[is one.](http://anatomicwax.tumblr.com/post/8064949186/installing-xcode-3-2-6-on-lion-redux)

Basically, you just have to follow these simple steps:

- Mount the Xcode 3.2.6 DMG
- Open Terminal
- Enter the commands:
export COMMAND_LINE_INSTALL=1 open "/Volumes/Xcode and iOS SDK/Xcode and iOS SDK.mpkg"


Ok that gets me a working copy of XCode 3.2.6 as well as the SDKs that I need which are 10.5 and 10.6...but I'm not out of the woods yet because the X-Plane Scenery Tools requires the 10.5 SDK. I have it so there's no problem right? WRONG! The GCC being used by the system is in /Developer and if you take a look at /Developer/SDKs you'll see 10.6 and 10.7 but no 10.5. That's because 10.5 lives in /Developer-3.2.6 but GCC won't be looking there. My solution was to create a symbolic link (the linux kind ln -s, not the Mac Alias kind) in the /Developer/SDKs folder that points to the /Developer-3.2.6/SDKs folder. The actual command was:

ln -s /Developer-3.2.6/SDKs/MacOSX10.5.sdk /Developer/SDKs/MacOSX10.5.sdk

So now with that done, GCC now has access to the right SDKs. The finder view of /Developer/SDKs should look like this:

At this point, I tried to compile the libs necessary for the X-Plane Scenery Tools again but was hit with one more snag as it was failing to find bits/c++config.h as referenced by iostream.h and a dozen other files. It turns out that the new GCC is a darwin11 version of the compiler. That's fine but if you look at /Developer/SDKs/MacOSX10.5.sdk/usr/include/c++/4.2.1/ you'll notice that there are several folders that are named with respect to the GCC version they're designed for...the ones we care about are:

- i686-apple-darwin*
- x86_64-apple-darwin*

You'll notice that there's no version for darwin11 which is why the headers cannot be found. The solution once again is a symbolic link. You'll notice that darwin8 and darwin10 are actually really links to darwin9. All that I had to do now is create a symbolic link back to version 9 for the 32bit and 64bit paths. Here's the commands:

ln -s i686-apple-darwin9 i686-apple-darwin11

ln -s x86_64-apple-darwin9 x86_64-apple-darwin11

After these steps, the universe seemed to be back in order again. XCode 4 and XCode 3.2.6 co-exist properly and the scenery tools compile using the newer version of GCC even using the older 10.5 SDK.

Thanks for the info,





ReplyDeleteJust wanted to update that since Xcode 4.3.x /Developer directory was deleted and moved under Application under "Xcode.app" application dir.

This might be easier since we can just point the "/Developer" to "/Developer-3.2.x" directory using symbolic link, but it might be an issue when upgrading Xcode 4.3.x, it might remove the "/Developer" directory again...

I did not test this yet, but I just thought I'll let you know.

Snagar