---
title: Migrating to cocos2d-iphone v3 – Tips & Tricks
url: http://www.learn-cocos2d.com/2014/03/migrating-cocos2diphone-v3-tips-tricks/
author: Benny says
published: '2014-03-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[The Mobile 2D Game Engine Popularity Index – January 2014](http://www.learn-cocos2d.com/2014/02/mobile-2d-game-engine-popularity-index-january-2014/)

[Let’s have a QuickLook: how to use Xcode’s latest debugging feature](http://www.learn-cocos2d.com/2014/03/quicklook-xcodes-latest-debugging-feature/)

This is a collection of Tips & Tricks for users who are migrating to cocos2d-iphone v3 from v2. Mostly refers to questions posted on [stackoverflow.com](http://stackoverflow.com/).

Please excuse the short, bullet-pointed format. I’m a little short on time but didn’t want to miss out on another biweekly post like I did two weeks ago (first time in about 4 years, ouch).

## General Tips

**Many classes have been renamed…**

“Use the source, Luke!” If you don’t find what you are looking for:

- Check the[ cocos2d API class reference](http://www.cocos2d-iphone.org/api-ref)

- Start typing the class or method name, see what suggestions Xcode autocomplete has for you

- Use part of the class name (ie “repeatforever”) and perform a “Find in Project” to search through all source code files

**Tutorial XYZ won’t work with v3!**

Yes, it won’t. Most likely it was written for cocos2d-iphone v2.

Question is: do you **have** to use v3? And do you have to use it right now?

Because if you’re in the process of learning cocos2d it’ll be easier to learn from and with v2 tutorials/books for the time being until more v3 tutorials have been published.

**How to upgrade an existing cocos2d v2 project to v3?**

[process as before](http://www.learn-cocos2d.com/2011/05/update-cocos2d-iphone-existing-project/) but expect a host of problems due to massive changes to the cocos2d API. The larger the project the less feasible porting to v3 is.

Tip: Finish the project with v2 and start your next project with v3. Consider that v3.0 brings significant changes and v3.1 will feature a radically overhauled renderer, so you may want to (what I’m really saying: should) wait out these changes if you’re in the middle of a development cycle.

**Send messages directly instead of CCCallFunc**

I noticed some users use runAction with CCCallFunc where they could simply send a message to the object. Also seen this done by Sprite Kit users.

[This explains what I mean](http://stackoverflow.com/a/22048733/201863).

**Don’t forget to call [super ..] in your AppDelegate methods**

Case in point: [applicationDidBecomeActive did not resume cocos2d](http://stackoverflow.com/a/21970180/201863) without calling its super implementation.

## Specific Tips

**How to find a Node by tag?**

Tags have been replaced by CCNode [name property](http://www.cocos2d-iphone.org/api-ref/3.0-rc1/Classes/CCNode.html#//api/name/name).

There are corresponding removeChildByName: etc methods available.

**Where is CCSomeAction?**

Most CCAction classes have been renamed. All follow consistent naming scheme by starting with “CCAction..”

Example: [CCRepeatForever is now named CCActionRepeatForever](http://stackoverflow.com/a/21554019/201863)

**Argh! CCCallBlockN, CCCallBlockND are gone. And so are CCActionCallFuncN and CCActionCallFuncND.**

They were never really needed. And CCActionCallFuncN and ND were in fact dangerous to use with ARC.

[Use CCCallBlock as described here](http://stackoverflow.com/a/22039128/201863), replaces all of the 4 above without any loss in functionality due to the way blocks work (they have access to variables in scope).

Alternatively [schedule an update selector](http://stackoverflow.com/a/22141289/201863).

**How to use Sprite frame animations?**

The API has changed. There are plenty of examples: [here](http://stackoverflow.com/a/21649464/201863), [here](http://stackoverflow.com/a/21600010/201863), [here](http://stackoverflow.com/a/21843802/201863) and [here](http://stackoverflow.com/a/22041094/201863).

**CCNodeColor is always opaque**

The [opacity property has been changed](http://stackoverflow.com/a/22117289/201863) from byte (0-255 value range) to CGFloat (0.0 to 1.0 value range). That means values greater than 1 will make the color node opaque. Divide your value by 255, for example 128 / 255 = 0.5

**How to enable touch input and accelerometer?**

self.accelerometerEnabled, self.touchEnabled have been removed. Use [self.userInteractionEnabled instead](http://stackoverflow.com/a/21870485/201863). Or [migrate to Sprite Kit](http://stackoverflow.com/a/14304895/201863), that works too. 😉

Also note [CCResponder](http://www.cocos2d-iphone.org/api-ref/3.0-rc1/Classes/CCResponder.html) is now the base class of all nodes which provides a similar functionality to UIResponder/NSResponder in terms of user input.

Here’s a [cocos2d v3 touch handling tutorial](https://www.makegameswith.us/gamernews/366/touch-handling-in-cocos2d-30).

**How to enable Multi-Touch?**

**Where are CCMenu, CCMenuItem, etc?**

Gone. [Replaced by CCButton](http://stackoverflow.com/a/21686709/201863) and others. Look into cocos2d-ui folder for more UI classes. Here’s an example for [CCButton with different color when pressed](http://stackoverflow.com/a/22023961/201863).

**How to play sounds/music in v3?**

CocosDenshion / SimpleAudioEngine have (thankfully) been replaced by ObjectAL / OALSimpleAudio, examples [here](http://stackoverflow.com/a/21846984/201863) and [here](http://stackoverflow.com/a/21798773/201863).

[More about ObjectAL](http://kstenerud.github.io/ObjectAL-for-iPhone/) and [ObjectAL documentation / reference](http://kstenerud.github.io/ObjectAL-for-iPhone/documentation/index.html).

**Where is my favorite scene transition?**

Yes, some transitions are missing from [CCTransition](http://www.cocos2d-iphone.org/api-ref/3.0-rc1/Classes/CCTransition.html) in v3 RCx.

**What is cocos2d’s UIViewController?**

CCDirector is! Some examples [here](http://stackoverflow.com/a/21891621/201863) and [here](http://stackoverflow.com/a/22024305/201863) and here’s how to present another view controller on top of cocos2d:

|
1 |
[[CCDirector sharedDirector] presentModalViewController:myView animated:NO]; |

**How to get director’s winSize?**

CCDirector winSize property is now named [viewSize](http://stackoverflow.com/a/21846016/201863).

**Where’s the AppController?**

It’s been [renamed back to AppDelegate](http://stackoverflow.com/a/21858653/201863).

**How to integrate iAd in cocos2d-iphone v3?**

[Here’s an example](http://stackoverflow.com/a/21797037/201863) and here’s [how to hide an iAd banner view](http://stackoverflow.com/a/21871818/201863).

**How to use a custom shader program with CCSprite?**

|
1 |
#import "CCNode_Private.h" |

Here is one [example](http://stackoverflow.com/a/22020715/201863) and [another one](http://stackoverflow.com/a/21612872/201863).

**Warning:** there’s a reason why this API is now private, use with caution. Also v3.1 will have a different renderer, so this method of accessing the shader property is likely to change with v3.1.

**How to set Portrait orientation**

**What’s a Chipmunk replacement for Box2d’s mouse joint?**

**How to make a UIScrollView pass-through touches to a CCButton?**

## Missing or unclear

**How to put a camera view in the background**

Should be the same procedure as in v2 but [users are having issues applying v2 code to v3](http://stackoverflow.com/questions/21931263/put-camera-in-background-in-cocos2d-3-0).

Maybe it doesn’t work anymore, or maybe it just needs someone to figure out how to make it work.

**Where are the Javascript bindings?**

[They have been removed and won’t come back](http://stackoverflow.com/a/21912919/201863).

PS: For JS development with cocos2d you could use cocos2d-x / cocos2d-html5 but there are a number of very good JS cross-platform development solutions out there so unless you’re fixated on cocos2d you should research other JS game engines and decide which one best fits your purpose.

**Where’s the Box2D template (integration)?**

None. Box2D template/integration may or may not be coming in the future.

It’s definitely not a high priority because cocos2d physics focus is on Chipmunk integration. Adding another physics engine would double the work done in both cocos2d and SpriteBuilder, so I find it very unlikely that cocos2d will integrate Box2D as much as it does Chipmunk currently. You can however always add the Box2D files to your project and start using it, but synchronizing sprite position/rotation with physics bodies and memory management of bodies will be up to you.


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[API](http://www.learn-cocos2d.com/tag/api/)•

[box2d](http://www.learn-cocos2d.com/tag/box2d/)•

[CCDirector](http://www.learn-cocos2d.com/tag/ccdirector/)•

[CCMenu](http://www.learn-cocos2d.com/tag/ccmenu/)•

[CCMenuItem](http://www.learn-cocos2d.com/tag/ccmenuitem/)•

[Chipmunk](http://www.learn-cocos2d.com/tag/chipmunk/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[cocos2d-iphone](http://www.learn-cocos2d.com/tag/cocos2d-iphone/)•

[cocos2d-iphone-3.x](http://www.learn-cocos2d.com/tag/cocos2d-iphone-3-x/)•

[CocosDenshion](http://www.learn-cocos2d.com/tag/cocosdenshion/)•

[documentation](http://www.learn-cocos2d.com/tag/documentation/)•

[iAd](http://www.learn-cocos2d.com/tag/iad/)•

[idevblogaday](http://www.learn-cocos2d.com/tag/idevblogaday/)•

[Javascript](http://www.learn-cocos2d.com/tag/javascript/)•

[migrate](http://www.learn-cocos2d.com/tag/migrate/)•

[objectal](http://www.learn-cocos2d.com/tag/objectal/)•

[physics](http://www.learn-cocos2d.com/tag/physics/)•

[solution](http://www.learn-cocos2d.com/tag/solution/)•

[touch](http://www.learn-cocos2d.com/tag/touch/)•

[transition](http://www.learn-cocos2d.com/tag/transition/)•

[tutorial](http://www.learn-cocos2d.com/tag/tutorial/)•

[upgrade](http://www.learn-cocos2d.com/tag/upgrade/)•

[view controller](http://www.learn-cocos2d.com/tag/view-controller/)

maybe not quite relevant to this post. Does anybody blog the v3 enhancements over v2?

If I opt to finish my current project with v2, how do I get it to build with ios 7.0?

Depends on the issue. Search on Stackoverflow.com or ask there if it’s not on there.

My app is in its fourth year, and I developed it with cocos2d v1.0, then later upgraded to v1.1, where I’ve stayed. Now that I’m looking at systems such as Apportable and Marmalade to port it to Android, I’ve run into many problems.

As such, I’ve created a new project with cocos2d v3 and have started slowly bring my classes in, and you’re right - there are major api changes! But the good news is, the small test app works with apportable (although it shows a small image for the background, but that’s details).

Here’s my question for you, since you’re an expert in cocos2d and know the inner workings better than anyone I know, and you have a pulse on things. Would you recommend that I try to work with the folks at Marmalade (who have offered to help) and port my cocos2d v1.1 game? Or would you suggest continuing the migration to cocos2d v3 and apportable? I will be creating many more features in 2014 and may branch off to one or two related apps.

thanks!

Sorry, I can’t recommend one way or the other, not knowing or having followed Marmalade at all and I have no idea what porting a v1.x game to v3 (and possibly ARC as well) might be like, or the issues occuring thereafter.

If you are still looking to port your cocos2d app to android you should definitively try #myAppConverter. here it’s their website.

http://www.myappconverter.com

They took out support for keyboard when using the template for osx games. They said the support is not really planned for the future. Do you think they’re planning to phase out osx support entirely to focus solely on iOS? If that would happen, are osx developers limited to closed-source engines like SpriteKit and unity? I’m sure there are other open-source engines out there but cocos2d brings a very high level of quality and a very big community.

I don’t know, but certainly iOS support has simply higher priority. However keyboard support isn’t something one needs to have built into cocos2d, you can just register for the keyboard events from OS X directly. Cocos2d v2 and earlier didn’t do much besides rerouting these events to CCLayer anyway, similar to accelerometer events.

Is cocos2d v3 compatible with iOS 5.x?

Yes, I think it goes as far back as iOS 4 even.

But iOS 5 is only needed for a handful of still-in-use iPad 1’s and a dozen or so iPods (3rd gen) anyway. Given how many cool (and some commonly used) new API features were introduced with iOS 6 you need to be very aware as to what API calls you are making and whether they run on iOS 5. You should really consider whether it’s still worth supporting iOS 5 by the time the app is ready for release.

I guess I’m catching up late with the v3 transition. I thought it would be easy for me, since I don’t use a lot of Cocos2d special features. And indeed most things seem to have converted without two much trouble. But I am getting strange sprite colors and have noticed that CCSprite used to have unsigned byte values for color, but now they seem to be float or double. They are also ‘red’,’green’ and ‘blue’ instead of ‘r’, ‘g’, ‘b’, so maybe there’s a clue there.

I appreciate your comments about ‘opacity’. I may have to do something there.

And I’m wondering about the Particle Engine I use for explosions from a British company with a number that I can’t recall at the moment. I think it just produced sprite sheets that I used somehow, so maybe when I get around to that it will just work or not require too much change.

I switched to v3 because it seemed more up-to-date and there were things in v2 that needed improvement, I thought. Maybe I acted in haste.

Bruce

Just doing the opacity the new way seems to have solved the sprite color problems. There must have been some interaction somehow. Thanks.