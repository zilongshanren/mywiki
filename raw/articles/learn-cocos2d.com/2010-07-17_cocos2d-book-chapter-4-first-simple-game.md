---
title: 'cocos2d Book, Chapter 4: First Simple Game'
url: http://www.learn-cocos2d.com/2010/07/cocos2d-book-chapter-4-simple-game/
author: Blenderificus says
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 4 - First Simple Game

After Chapter 3 covered the fundamentals of the cocos2d game engine, this chapter will put to use what you’ve learned. The simple game is all about droping enemies that you have to avoid via accelerometer controls. Sort of like an inverse Doodle Jump. But it’s not just about the gameplay itself, I want the game to be reasonably complete with a main menu, scene transitions, game over and of course audio.

The chapter will be submitted on Friday, July 23rd.

### Do you have any suggestions for the game?

What do you think should be in a first cocos2d game? Let me know!

### Summary of working on Chapter 3 - Essentials

When I started the chapter I wasn’t really sure about its focus and progress was a little slow. Eventually it clicked and I found myself ending up having written more pages than needed and still having a great number of things left untold. The key was looking at the cocos2d API reference documentation and remembering what it was like when I was a beginner. Sure, every class, method and property is there but for a beginning cocos2d developer the API reference is just a huge list of names. In other words, if your experience was or is anything like mine was, it’s frustrating to work with the API reference.

I ended up writing about the cocos2d engine design and its scene graph first, the remaining 80% of the chapter explain in detail with lots of code samples how to use those darn CCNode classes. All the important ones are covered: CCNode, CCScene, CCLayer, CCSprite, CCLabel, CCMenu, CCMenuItem* as well as the Director, Transitions and Actions. Besides the code samples and how-to I’ve added numerous caveats, common mistakes, best practices and other nodes which are so very much needed to make any documentation complete.

For example, how Layers are best used for grouping other nodes together and of course how to enable touch and accelerometer input by adding the required functions which aren’t mentioned in the API reference since they are part of the iPhone SDK API. There’s also some weird recommendation floating around not to use too many Layers because they’re slow. I can’t find the source but what I did find was that this is only true if the Layers enable touch or accelerometer input, because that’s what costs a lot of performance. So what you don’t want to have is several layers accepting input, otherwise use as many Layers as you need - which shouldn’t be many anyway. And if you do need multiple Layers accepting input, why not just use one master Layer (possibly using a Targeted Touch handler) which forwards the input events appropriately to the other Layers?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[accelerometer](http://www.learn-cocos2d.com/tag/accelerometer/)•

[actions](http://www.learn-cocos2d.com/tag/actions/)•

[best practices](http://www.learn-cocos2d.com/tag/best-practices/)•

[caveats](http://www.learn-cocos2d.com/tag/caveats/)•

[CCLabel](http://www.learn-cocos2d.com/tag/cclabel/)•

[CCLayer](http://www.learn-cocos2d.com/tag/cclayer/)•

[CCMenu](http://www.learn-cocos2d.com/tag/ccmenu/)•

[CCMenuItem](http://www.learn-cocos2d.com/tag/ccmenuitem/)•

[CCNode](http://www.learn-cocos2d.com/tag/ccnode/)•

[CCScene](http://www.learn-cocos2d.com/tag/ccscene/)•

[CCSprite](http://www.learn-cocos2d.com/tag/ccsprite/)•

[chapter 3](http://www.learn-cocos2d.com/tag/chapter-3/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[code samples](http://www.learn-cocos2d.com/tag/code-samples/)•

[design](http://www.learn-cocos2d.com/tag/design/)•

[Director](http://www.learn-cocos2d.com/tag/director/)•

[documentation](http://www.learn-cocos2d.com/tag/documentation/)•

[Essentials](http://www.learn-cocos2d.com/tag/essentials/)•

[game engine](http://www.learn-cocos2d.com/tag/game-engine/)•

[how-to](http://www.learn-cocos2d.com/tag/how-to/)•

[Layers](http://www.learn-cocos2d.com/tag/layers/)•

[sample](http://www.learn-cocos2d.com/tag/sample/)•

[scene](http://www.learn-cocos2d.com/tag/scene/)•

[scene graph](http://www.learn-cocos2d.com/tag/scene-graph/)•

[scene transitions](http://www.learn-cocos2d.com/tag/scene-transitions/)•

[simple game](http://www.learn-cocos2d.com/tag/simple-game/)•

[source](http://www.learn-cocos2d.com/tag/source/)•

[transition](http://www.learn-cocos2d.com/tag/transition/)•

[Transitions](http://www.learn-cocos2d.com/tag/transitions/)

nice to hear your finishing another chapter. Going with a doodle jump style game seems like a good introductory example for iPhone dev IMO

Your book is getting great! Does have some way to buy it now and get access to the chapters right after you finish writing them? Please?![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I’m checking with my editor to see if the book will be in Apress’ alpha program. If it is I’ll let everyone know.

This book looks every time more interesting!

I would like to find somewhere in the book an implementation of a reliable d-pad and relative explanation…

Why do you say “reliable”? Are there unreliable or unstable d-pad solutions?

With relative explanation I assume you mean positions of child nodes relative to their parent node. I made a small example Xcode project for chapter 3 to show the effect of relative positioning and rotation.

I don’t know if there are unreliable or unstable d-pad solutions![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I just wish a crystal-clear pre-cooked sample easy to re-use.

But I think the topic is outside the scope of the book

Maybe that helps, Joystick implementation with code and other people’s solutions too:

http://www.cocos2d-iphone.org/forum/topic/1418

Just came across this by chance and thought you might be interested in that.

Thank you![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


SCROLLING!!![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Yes of course but in a later chapter. I plan to show parallax scrolling too.

Steffen, is your book going to cover using either Box2d or chipmunk with Cocos2d?

I have spent so many hours just trying to wrap my head around Cocos2d and I can’t wait to get my hands on this book when it done.

Yes, one chapter to get the basics of both Chipmunk and Box2D on the table and for everyone to decide which physics engine is more likable, then another chapter with a simple but fun physics game made with Box2D which I think is the more popular choice.

Hi,

I hate to nag, because I know it’s an alpha, but I am noticing a lot of little things missing in the book (specifically this chapter). These include things such as where you’re initializing the “spiders” array, and where the “spiderMoveDuration” variables should be initialized. Just wondering if those are going to be included in future releases or not?

Thanks,

.d

Due to the complexity I had to take a few shortcuts. But those little things are all in the code and most of it is documented too.

I heard that it’s not possible to get the source code for alpha chapters. I hope to get more on that from my editor by next week. Not sure what their policy about source code & alpha is. Hopefully it’s only because the code hasn’t been tech reviewed yet.

I too was a bit lost in following Chapter 4; I reached the Object Collision section where it said to test out the game (before collision was implemented) but due to the lack of complete code included in the chapter I could not even run it. Numerous variables and the array were never initialized (I subsequently initialized them in the header file) and the chapter did not indicate where or how to call the initSpiders method (I subsequently added [self initSpiders] to the main init).

Each method called (e.g., [self resetEnemies] in initEnemies) also returns a warning, for instance: “GameScene” may not respond to ‘-resetSpiders’ — I am quite new to the world of cocos2d/objective C but is this supposed to happen?

I’ll look into that after the chapter has been through editorial review. I’ll give the code samples in this case more attention so they can be run from straight the book.

The warnings about “may not respond to selector” should not happen in the book source code. You can avoid them by adding this above the @implementation in GameScene.m:

@interface GameScene (PrivateMethods)

-(void) resetSpiders;

@end

This is the way to declare private methods of a class in Objective-C, and to avoid said warnings, by declaring the private methods in a Category. The label (PrivateMethods) is completely arbitrary but should be descriptive, and the @interface should not contain any brackets {} since Categories can’t add member variables.

Thanks! I’m still new to Objective C and Cocos2d coding. Obviously the source code accompanying the book would/will clarify a lot, whenever that code becomes available.

I’m glad to see others cannot get the alpha code to work either.

In the interface .h I had to add:

-(void) resetSpiders;

-(void) initSpiders;

and in the .m -(id) init

[self initSpiders];

Still the spiders don’t move. When I changed the variables so they start on screen (to see if they’re even appearing), they just disappear every few seconds but never move. I couldn’t get the movement to work.

Another thing I had to do was change the order of my methods to avoid a warning.

It’s too bad it doesn’t work because so far I like your approach. I can compare it more with my knowledge of Flash AS3. The iPhoneGameKit is excellent, but too abstract for my level of knowledge right now.

It will become clearer as soon as the source code is available. I’m hoping next week.

I’m looking forward to it. Will the alpha book be updated or will you post it on this site somewhere?

The updates will be available from Apress.

I hope the code from the book will work fine becos its very difficult to follow if the code does not work. When will the book targeted to complete?

Think i’ll have to put it down and wait for the source code to be made available before i continue. It’s very discouraging for a beginner when I cannot figure out what’s wrong with the code.

I understand, the code should be available soon. I wrote the book with a mindset that everyone would have access to the source code, so it’s rather unfortunate that the code wasn’t available at the same time as the Alpha Book.

I’m getting messages about CCBitmapFontAtlas being deprecated. The code will not compile. Is there a replacement call for this for the scoreLabel? Looking in the cocos2d folders, I find a CCLabelAtlas class as well as a CCLabelBMFont class. Is one better than the other? The CCLabelAtlas class takes a lot of parameters when creating a new instance.

I decided to try the CCLableBMFont class and that worked quite well.