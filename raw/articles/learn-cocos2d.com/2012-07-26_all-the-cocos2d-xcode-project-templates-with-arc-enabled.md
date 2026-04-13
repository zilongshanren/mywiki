---
title: All The Cocos2D Xcode Project Templates With ARC Enabled
url: http://www.learn-cocos2d.com/2012/07/cocos2d-xcode-project-templates-arc-enabled/
author: Gary Ash says
published: '2012-07-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![](../../../wikipedia/commons/b/b8/Arc_de_triomphe_frontsimple.jpg)

Example ARC project. Pretty awesome.

[how to enable ARC for a cocos2d project](http://www.learn-cocos2d.com/2012/04/enabling-arc-cocos2d-project-howto-stepbystep-tutorialguide/), I neglected to include an actual working project. I mean why read and follow a long tutorial if all you

**really**need is a working project to get started with?

Therefore I decided to enable ARC in all **twelve** standard cocos2d Xcode project templates for both cocos2d versions (v1.1 and v2.0), both platforms (iOS and Mac OS), both physics engines (Box2D and Chipmunk) and publish them on github.

You can download the [ARC-enabled cocos2d template projects](https://github.com/LearnCocos2D/cocos2d-iphone-arc-templates) either as [ZIP file](https://github.com/LearnCocos2D/cocos2d-iphone-arc-templates/zipball/master) or [TAR file](https://github.com/LearnCocos2D/cocos2d-iphone-arc-templates/tarball/master).


#### How to use the Cocos2D ARC Template Projects?

This is really simple. The cocos2d version (v1.x or v2.x), the target platform (iOS or Mac) and the physics engine (Box2D, Chipmunk or none) are coded into each project’s name. For example cocos2d-2.x-Chipmunk-Mac includes cocos2d-iphone v2.0 and the Chipmunk physics engine targetting the Mac OS X platform.

1. Make a copy of the desired project’s folder

2. Open the .xcodeproj in Xcode.

3. (optional) Rename the project to your liking.

4. Start writing ARC code with cocos2d.

That’s all. Enjoy the summer! Stay inside where it’s cool (relatively) and dark (mandatory). ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Thanks, you’ve save me (and others I’m sure) a lot of time and hassle

Hi Steffen,

Is it easy enough to convert IOS project to storyboards?

I tried few tutorials but there are lot of compiling errors ,Do you have any advice for me?

I haven’t done integration with Storyboards yet. You might want to check this link: http://stackoverflow.com/questions/11550437/how-to-incorporate-storyboards-into-a-cocos2d-2-0-project

Hi Steffen,

Thanks for your reply , I managed to add storyboard after reading few tutorials .

I used one of your templates and converted it to a storyboard project.

I cant find a complete tutorial for this so I decided to do a complete writeup about how to use cocos2d with ARC and Storyboard .

If it ok if I add reference to your tutorial and templates in my blog?

Absolutely, let me know when the article is online, I’ll retweet it.

Any chance of getting a download of this template?

So are these templates fairly easy to convert/install into actual Xcode templates? I’m not sure where to begin there, I’m a Visual Studio guy just learning Xcode.

No. Xcode templates are a beast. Even a simple template can take hours to create from scratch. Cocos2D for example relies on a script to create their template projects, because once your project has a dozen files or more, it becomes a nuisance to create and update Xcode templates.

If you’re really interested check out the documentation I wrote on Xcode template creation: http://www.learn-cocos2d.com/store/xcode4-template-documentation/

But you don’t really need Xcode templates. Whether you create a new project from within Xcode, or copy an existing project and rename it is essentially the same thing, and it takes barely any additional time or effort to do the latter.

Any progress with the tutorial? I’ve spent the past few hours trying tutorials and failing, I’m after ARC, Cocos2D 2.x and Storyboards, targeting iOS 6 as a minimum preferably.

Cheers, David.

When I build with your templates the aurto rotation does not work. I did not edit the project whatsoever but once I build it the orientation stays in portait. When I rotate the iPhone simulator the orientation stiil stays the same. I checked the app delegate.m file and made sure landscape was the only setting I had in the project settings but yet the simulator is rotated but the scene remains in portrait. Any ideas on why this is happening and anyway to fix it?

May be the old issue with cocos2d 2.0 and iOS 6. Upgrading to v2.1 might help.

Would i still be following your other blog on how to enable ARC for “cocos2d-2.1”? And if so, when I enable Arc, can i just save the project with no edits the same way you did with these so I can easily copy the folder later on, rename the project, and write my programs?

Either that or read the post about updating cocos2d.

Yes, definitely make a copy of the entire project folder so you can keep reusing the project.

Thanks. I just updated cocos2d and followed your tutorial on enabling ARC. Now I use those as templates.