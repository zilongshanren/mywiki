---
title: Kobold2D v1.0.4 now available!
url: http://www.learn-cocos2d.com/2012/02/kobold2d-v104/
published: '2012-02-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

**Kobold2D v1.0.4** is available from the [Kobold2D Download page](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download)!

I’m terribly sorry for the hiccup with v1.0.3. There was an absolute path causing build failures for others, which of course worked on my systems so I didn’t catch it. I retracted v1.0.3 shortly after publishing it. The fixed version is now v1.0.4. If you happen to have downloaded v1.0.3 I recommend to upgrade to v1.0.4 right away.

The most important improvements in this version are **Xcode 4.3 compatibility** and working around a [“file not found ../libkobold2d-ios.a” issue](http://www.kobold2d.com/x/6QAi) caused by the Xcode 4 Build Location setting “Locations Specified by Targets” (in Xcode 4.3 this setting is now appropriately named “Legacy”).

The [Release Notes](http://www.kobold2d.com/display/KKDOC/Kobold2D+v1.0.4+Release+Notes) lists all the changes.


#### Bad Build Location, Bad!

**Pro Tip:** avoid using the “Locations Specified by Targets” / “Legacy” Build Location setting in Xcode unless you absolutely must use it for compatibility with an old project/library. That should be the only reason why you should ever consider using it in the first place. This is due to lingering linker errors, crashes and wasted time cleaning and rebuilding projects.

**If you do have to use this setting**, you can now uncomment a line in **Common-All.xcconfig** to allow Kobold2D to build successfully with this Build Location setting, albeit [with a few caveats](http://www.kobold2d.com/x/6QAi) to keep in mind.

**Kobold2D works fine with all other Build Location settings.** Hence the recommended fix for everyone else who is using the “by Targets” / “Legacy” is to use one of the other Build Location settings because there are no potential side-effects to worry about. These side-effects are **not** specific to Kobold2D by the way, they can appear in **any** project!

In case you have been using that setting but had no issues with it like I did, you may have changed that setting in Xcode 3 manually, most likely by modifying a .plist or by using the defaults tool. Unfortunately Xcode 4 uses the Xcode 3 setting if it exists, ignoring any changes to the setting in the Preferences panel. The only way to fix this is by deleting the **SYMROOT** key in **~/Library/Preferences/com.apple.dt.Xcode.plist** inside the **IDEApplicationwideBuildSettings** dictionary.

That is why I’ve been unable to reproduce this issue for months. I’m just happy that that’s out of the way now!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |