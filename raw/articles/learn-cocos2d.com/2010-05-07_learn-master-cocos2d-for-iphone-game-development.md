---
title: Learn & Master cocos2d for iPhone Game Development
url: http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/13733-upgrate-targets-to-ipad/
author: Receptor says
published: '2010-05-07'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Tutorial: cocos2d Xcode Project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/learn-cocos2d-public-content/manual/1601/): Upgrade Targets to iPad

#### Search my cocos2d for iPhone FAQs & Tutorials

*Please note that the blog search in the upper right corner doesn’t search my FAQs and Tutorials.*

In this lesson we'll upgrade our existing targets to iPad Targets. We'll do both the LITE and regular Target.

### Select desired Target

Simply select the target you want to convert to an iPad Target.

### Upgrade Target for iPad

In the Project menu choose "Upgrade Current Target for iPad".

### Select two device-specific applications

Since it doesn't make much sense for games to create a universal application, choose the "Two device-specific applications" setting and click OK.

Why not a universal application? The reason is simple: for the iPad version you want to have higher resolution graphics. But you don't want to include those high resolution graphics with your iPhone version because of the increase in size of the app bundle. So it is better to have two seperate targets each with their own set of device-specific resources.

### Get Info on the iPad Target

Select and right or control click the new iPad Target and "Get Info".

### Copy & Rename the Info.plist

Go into the project folder using Finder and copy the Info.plist file from the Resources folder to the newly created Resources-iPad folder. Rename the Info.plist to Info-iPad.plist and then change the path for the "Info.plist File" setting in all Build configurations to "Resources-iPad/Info-iPad.plist".

This is not strictly necessary but allows you to name your iPad version differently. Typically developers like to add an "HD" to their App's name.

### Enable Thumb

With All Configurations selected, enable "Compile for Thumb" and also check the box below for "Any SDK" and "ARMv6" and "ARMv7". We want to use Thumb code on the iPad because **Thumb is generally faster on the iPad**, contrary to the iPhone.

### Add iPad Preprocessor Macro

We want to be able to identify when building iPad code. While we can check for #if TARGET_OS_IPHONE and #if TARGET_IPHONE_SIMULATOR we have no way to conditionally compile code for the iPad, so we need to add a TARGET_IPAD macro.

Switch to the Debug Configuration and add a Preprocessor Macro TARGET_IPAD. Repeat this step for all Build Configurations (Debug, Release, Ad Hoc Distribution and App Store Distribution) seperately so that you don't overwrite configuration-specific settings.

### Create an iPad LITE Target

It seems you can only upgrade one Target in a project. If you need an iPad LITE version target, refer to the [Adding a LITE version Build Target](http://www.learn-cocos2d.com/) lesson to create a LITE version from the iPad Target.

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