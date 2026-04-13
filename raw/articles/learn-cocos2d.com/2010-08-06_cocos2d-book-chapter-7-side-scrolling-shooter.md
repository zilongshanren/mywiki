---
title: 'cocos2d Book, Chapter 7: Side-Scrolling Shooter'
url: http://www.learn-cocos2d.com/2010/08/cocos2d-book-chapter-7-sidescrolling-shooter/
author: Josh says
published: '2010-08-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 7 - Side-Scrolling Shooter

The shooter game will be controlled with a virtual joystick using SneakyInput. The background parallax scrolling will be implemented not with the CCParallaxLayer, as it does not support endless scrolling (as far as I know, please correct me if I’m wrong). The rest will be gameplay code, mostly spawning enemies, moving them and collision tests.

The chapter will be submitted on Friday, August 13th. Yup, Friday the 13th. Scary.

### Summary of working on Chapter 6 - Sprites In-Depth

I decided to rename this chapter to Sprites In-Depth as it deals mostly with Sprites, Sprite Batching (formerly known as Sprite Sheets), Texture Atlases and Zwoptex as well as general texture memory management. All the while laying the foundation for the game to be made in Chapter 7.

While working on this chapter I noticed that it’s awfully complex to create a CCAnimation class, especially if you’re not using a Texture Atlas. So I decided to illustrate how to add helper methods by adding them via a Objective-C Category to the CCAnimation class. Now you can create a CCAnimation with just one line of code, instead of around ten.![2010-08-06_23.34.54](../../../wordpress/wp-content/uploads/2010-08-06_23.34.54-300x156.png)


Once more I created some of my now famous doodle artworks. If anything this should show that even a programmer can do art. Or, well, at least something that vaguely resembles art.

I was a bit surprised by one thing though, and that is how little the use of the CCSpriteBatchNode contributed to the framerate in this particular case. I added all the bullets to a CCSpriteBatchNode and found only a 15% increase in performance, it went up from 45 fps to a little over 50 with all those bullets flying. I sort of expected a bigger impact from previous experiences.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[apress](http://www.learn-cocos2d.com/tag/apress/)•

[art](http://www.learn-cocos2d.com/tag/art/)•

[Atlas](http://www.learn-cocos2d.com/tag/atlas/)•

[Batching](http://www.learn-cocos2d.com/tag/batching/)•

[book](http://www.learn-cocos2d.com/tag/book/)•

[category](http://www.learn-cocos2d.com/tag/category/)•

[CCAnimation](http://www.learn-cocos2d.com/tag/ccanimation/)•

[CCParallaxLayer](http://www.learn-cocos2d.com/tag/ccparallaxlayer/)•

[CCSprite](http://www.learn-cocos2d.com/tag/ccsprite/)•

[CCSpriteBatchNode](http://www.learn-cocos2d.com/tag/ccspritebatchnode/)•

[Chapter](http://www.learn-cocos2d.com/tag/chapter/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[collision tests](http://www.learn-cocos2d.com/tag/collision-tests/)•

[Doodle](http://www.learn-cocos2d.com/tag/doodle/)•

[framerate](http://www.learn-cocos2d.com/tag/framerate/)•

[memory management](http://www.learn-cocos2d.com/tag/memory-management/)•

[Objective-C](http://www.learn-cocos2d.com/tag/objective-c/)•

[Parallax](http://www.learn-cocos2d.com/tag/parallax/)•

[Performance](http://www.learn-cocos2d.com/tag/performance/)•

[Scrolling](http://www.learn-cocos2d.com/tag/scrolling/)•

[SneakyInput](http://www.learn-cocos2d.com/tag/sneakyinput/)•

[sprite sheets](http://www.learn-cocos2d.com/tag/sprite-sheets/)•

[texture memory](http://www.learn-cocos2d.com/tag/texture-memory/)•

[Zwoptex](http://www.learn-cocos2d.com/tag/zwoptex/)

I too was looking for a good solution to repeating layers when using parallax features in Cocos2d. Somewhere on the forums, I saw this posted when creating the background:

CCSprite *background = [CCSprite spriteWithFile:@”background1.png” rect:CGRectMake(0, 0, screen.width * 1000, 320)];

ccTexParams params = {GL_LINEAR, GL_REPEAT, GL_REPEAT};

[background.texture setTexParameters:¶ms];

background.anchorPoint = ccp(0, 0);

You still have to pass in a width, so it doesn’t truly repeat forever, but you can set it to something you know will be bigger than whatever the level is.

Yup, I know the GL_REPEAT trick. It’s neat but eventually, for an endless drawing background, you’d have to reset the position of the background. The CCParallaxNode strangely does not support changing the position of individual child nodes, so its use is limited to fixed-size scrolling areas.

I have a solution in mind and will add that to the book.

When will these chapters be added to APress? Thanks!

That’s up to Apress and depends on their workload. Sometimes it takes a few days, sometimes a couple more to edit my first draft chapters and make them available online.

In the book you mention that the Update loop can be faster over actions. Is this also true for animations? I have a ton of sprites that have a short 10 frame animations but I want to add tons of them. I was hoping to ++ something like curFrame.

It’s a matter of how many and how frequently CCAction are created to animate. If you create new actions basically every frame then manually managing the animation state will definitely be faster. But it’ll also be more code. I’d say use actions until you find that they’re slowing the app down.