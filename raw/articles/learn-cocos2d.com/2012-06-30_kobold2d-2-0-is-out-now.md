---
title: Kobold2D 2.0 is out now!
url: http://www.learn-cocos2d.com/2012/06/kobold2d-20/
author: Student says
published: '2012-06-30'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Busted! Eight Reasons not to use ARC](http://www.learn-cocos2d.com/2012/06/mythbusting-8-reasons-arc/)

[Newsflash: Game Development Costs Rising Beyond Reasonable Levels](http://www.learn-cocos2d.com/2012/07/newsflash-game-development-costs-rising-reasonable-levels/)

### Go grab it here:


[Download Kobold2D 2.0](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download) and [read the Release Notes here](http://www.kobold2d.com/display/KKDOC/Kobold2D+v2.0.0+Release+Notes).

You can use the Kobold2D API References even if you’re not using Kobold2D, since the API References of the 3rd party libraries are unmodified. For example this includes the only [Box2D API Reference](http://www.learn-cocos2d.com/api-ref/latest_2.x/Box2D/html/index/) that’s available online, and separate API References for [cocos2d (iOS)](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/index/) and [cocos2d (Mac)](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/index/).


#### Additional Release Notes

Obviously Kobold2D 2.0 **uses cocos2d-iphone 2.0** (rc2) now.

The **Project Upgrader** tool works for v1.x projects but please understand that the Cocos2D API has undergone many cosmetic and some radical internal changes from v1.0 to v2.0. The Project Upgrader can’t auto-magically fix your code to interface correctly with the latest cocos2d-iphone version. However, I tried upgrading several simple projects using only basic Cocos2D features and much to my surprise they built and ran fine. So definitely give it a shot.

I also **improved the package installer**. Several users complained about Kobold2D folders having read/write permission only for system and root/admin users, which causes a numnber of problems. I found a loophole in the installer that caused Kobold2D to be installed to /Kobold2D (root folder of the HD) instead of ~/Kobold2D in the user’s home directory. In that case, the currently logged in user had no write permissions to that folder. Now the installer should only allow installation to ~/Kobold2D. After installation you can then of course move the folder to anywhere else on your system.

Although I found this [great PackageMaker Problems & Solutions article](http://simx.me/technonova/tips/packagemaker_and_installer.html), I could not find a solution for the “user has no write permission” issue if I allowed installation to custom folders. PackageMaker is one big §$&%/§! Well actually it’s not that bad, it’s just not very well documented, in particular concerning side effects and behavior on different OS versions and the various modes (flat or non-flat; package or distribution; patch, update or new install).

For those of you who rely on **Cocos3D or Chipmunk Spacemanager**: Cocos3D is incompatible with cocos2d 2.0 and therefore not included. Chipmunk Spacemanager is not fully compatible with cocos2d 2.0 either - it generally works but it won’t rotate sprites. I still included the Spacemanager, hoping that a fix is forthcoming.

The **automatic Ad banner feature is currently disabled**. I had no time to re-integrate it with CCDirectorIOS now being the new UIViewController. The KKAdBanner class is still available however but I’m not sure if it needs any updates. Maybe it’s just as simple as adding it as a view to CCDirectorIOS, I haven’t tried that.

Finally, **CCDirector doesn’t have the setDeviceOrientation** method anymore. Instead use [UIDevice currentDevice].orientation. The enums are the same, just using a different prefix (UI instead of CC). You have to use the Supported Device Orientations toggle buttons in your project’s target Info pane to enable/disable the available orientations. If you select more than one supported orientation your app will autorotate automatically. You can override this behavior by adding the **-(BOOL) shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation** method to your project’s AppDelegate.m file and returning YES for the (currently) allowed orientations.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[autorotate](http://www.learn-cocos2d.com/tag/autorotate/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[cocos2d-iphone](http://www.learn-cocos2d.com/tag/cocos2d-iphone/)•

[KKAdBanner](http://www.learn-cocos2d.com/tag/kkadbanner/)•

[Kobold](http://www.learn-cocos2d.com/tag/kobold/)•

[kobold2d](http://www.learn-cocos2d.com/tag/kobold2d-2/)•

[PackageMaker](http://www.learn-cocos2d.com/tag/packagemaker/)•

[update](http://www.learn-cocos2d.com/tag/update/)•

[upgrade](http://www.learn-cocos2d.com/tag/upgrade/)

What really cocos2d 2.0 offers? Except shaders.

And when Kobold2D 1.1 will update to include new iPad retina?

Shaders for the most part. I’ll make an update to Kobold2D 1.1 soon, it’s not using the beta 2 yet.

Am totally new to game development. If I want to start my journey, can I go straight to kobold2d without any cocos2d knowledge, have a basic understanding of objective c though?

Sure, you’ll probably find it easier to get started with than cocos2d.

Hi Steffen, btw thanks for your reply. Just wondering what book to get if i want to learn kobold2d, I never saw a book titled kobold2d, Is your latest book, learn cocos2d, release Sept. 2012 the book to get?

Bear in mind I have no knowledge of cocos2d at all.

Yes that’ll be Learn cocos2d 2. It explains Kobold2D as well, and where it’s different from cocos2d. Actually it explains mostly what you need to do manually in order to get the same functionality as in Kobold2D, for example enabling ARC.

Hi Steffen!

I purchased your book and it realy helped me setting up my game much cleaner.

Thank you for writing it 😀

Can you tell when Cocos2d 2.1 will be supporte?

Kind regards,

Gerard Oudenampsen

The Netherlands

When it’s no longer a beta. Cocos2D 2.0 is still fine, the big majority of the changes in 2.1 are just about Javascript anyway.