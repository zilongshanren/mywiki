---
title: Learn & Master cocos2d for iPhone Game Development
url: http://www.learn-cocos2d.com/knowledge-base/xcode-objective-c-faq/learn-cocos2d-public-content/manual/xcode/14122-why-are-my-project-build-settings-not-used-by-my-targets/
published: '2010-05-14'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# FAQ: Xcode & Objective-C

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

**No images? Reload page, wait and try again.****PDF download broken? Reload page, try again.**- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!

- Note: please do not share direct download links to PDF files, the download links expire after a couple minutes!


Read up on [Xcode's Layered Build Settings](http://developer.apple.com/Mac/library/documentation/DeveloperTools/Conceptual/XcodeBuildSystem/300-Build_Settings/bs_build_settings.html#//apple_ref/doc/uid/TP40002691-SW5) to learn more about this Xcode feature or just read my short summary.

### Build Settings in Bold are defined at the current Layer

Here we have an example many developers trip over. This is the Get Info dialog for one of my Targets. The Code Signing Property is set to iPhone Distribution even though i have it set to iPhone Developer in my Project Build Settings. What's wrong here?

Do you see how the Setting is printed in bold letters? This means that this build setting is defined at this layer, the Target. I can change it any way i want in the Project build settings, it won't change in the Target anymore. I could just set it back in the Target settings but we actually want to keep the code signing or any global build setting at the project level.

Many developers will simply advise you to change the xxx setting in both Project and Target build settings "just to be sure" or because "it's stupid but that's how it works". Ignore them. Instead, if you want to be able to reliably change a build setting in the Project Build Settings you can just delete the definition at the Target Level.

### Delete Definition at Target Level

In the Target Build Settings, select the Build Setting that you want to be controlled at the Project Level. You can see that the Target overrides the project's setting when it is printed in bold letters.

### Definition Deleted at Target Level

After you've deleted the Definition at the Target Level notice that it is no longer printed in bold letters and has changed back to the value that i've set in the Project Build Settings.

So instead of frantically changing your build settings in all Targets, delete those definitions in the Targets which you want to be controlled by the Project settings instead.