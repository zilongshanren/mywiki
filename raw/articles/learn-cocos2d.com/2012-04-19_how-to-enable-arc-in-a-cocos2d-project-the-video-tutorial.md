---
title: 'How to enable ARC in a Cocos2D Project: The Video Tutorial'
url: http://www.learn-cocos2d.com/2012/04/enable-arc-cocos2d-project-video-tutorial/
author: Max says
published: '2012-04-19'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Enabling ARC in a Cocos2D project isn’t as straightforward as it should be. I already explained all the necessary steps and precautions in the [Enable ARC in a Cocos2D Project guide](http://www.learn-cocos2d.com/2012/04/enabling-arc-cocos2d-project-howto-stepbystep-tutorialguide/).

For this post I wanted to actually show you what’s needed to enable ARC in a cocos2d project as a video. Because it may not be as complex as you think. And because I wanted to experiment making tutorial videos. If you like the video (please let me know in the comments), there will be more video tutorials in the future!

I understand the introduction is a bit lengthy, I should have gotten to the point quicker. Feel free to skip forward to 02:20 where I begin with the instructions.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen!![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Thanks for great tutorials, especially about ARC-enabling cocos2d.

I read both of your books from cover to cover to get familiar with that coco

It was a little 1-day epic challenge to ARC-enable cocos2d+box2d first previously ready project. Allocs fallen from 160Mbs to 22Mbs on iPad1.

I’ve noticed one interesting trait which could to useful for other challengers. When lib group is used as separate target you need to add a few lines to Info.plist for CCLabelTTF to work properly with custom fonts:

UIAppFonts

Arial.ttf

Then use as usual.

In other cases no need to add fonts into plist.

Hmmm I never needed to use that and I’ve definitely used CCLabelTTF with Arial while cocos2d was compiled to a static lib. I’ve used that setup since over 2 years. But you do need to register custom fonts, ie if you actually add a custom font file named Arial.ttf to your app bundle’s resources.

Hi Steffen,

Have you tested this with Cocos2d version 2.1 Beta 2? I have tried and I cannot get it to work for some reason.

Posted a bit of information here:

http://www.cocos2d-iphone.org/archives/2043#comments

BR Kim

Hi, I’m on Xcode 4.6 and there is no option for User Header Search Paths. When I skip that step and try to build it fails. Let me know what I can do to fix this. Thank you!

I’m on Xcode 4.6 too and User Header Search Paths still exists. You find both in Build Settings under “Search Paths”, but not directly next to each other (User Header is at the bottom of the “Search Paths” section).

Hi steffan…

I see these posts are pretty old. Do you perhaps have some advice as to where to find a working Cocos2d(with Arc and storyboards) template(Kobold2d).

Reason being…I have tried every possible way for a week now…and still ..I get stuck at the refactoring step.

My app is fine not using cocos2d…but i need to pull frame animations from plist files….I cannot use the nsMutable array option where the individual png files just gets loaded and start animating. I need to use touchesBegan to trigger some of them. There are a lot of deprecated issues regarding that in cocos2d.

I’m sure by now you have gathered that i’m a newb/noob!

The process is still the same. Perhaps post the description of the problem with any error messages to stackoverflow.com. I’m around there a lot, and so are others who might be able to help given a good error description.

Hi Steffen,

I will do that. Thanks so much for all the help and good stuff!