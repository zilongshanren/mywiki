---
title: 'cocos2d Book, Chapter 9: Particle Effects'
url: http://www.learn-cocos2d.com/2010/08/cocos2d-book-chapter-9-particle-effects/
author: Guyal Says
published: '2010-08-21'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 9 - Particle Effects

Those tiny specks which you can see on your touchscreen after a sneeze.

Not exactly. Of course I mean the cocos2d particle system and its built-in particle effects which will be the focus of this chapter. And no discussion of particles would be complete without describing the workflow revolving around the [Particle Designer](http://particledesigner.71squared.com/) tool.

### Summary of working on Chapter 8 - Shoot ’em Up

This certainly wasn’t the easiest chapter for me to write. I had very ambitious goals, maybe too ambitious for 27 pages. I did manage to sneak in quite a lot though, here’s a partial list:

- how to refactor existing code to make it work better with the new features
- how to pool bullets and enemies together for easier access and better performance
- how to not use too many subclasses, instead relying on type switches
- how to use cocos2d’s node hierarchy as a simple
[component system](http://www.learn-cocos2d.com/2010/06/prefer-composition-inheritance/)for writing reusable game logic components - how to implement basic movement, shooting and a healthbar as components
- how to detect collisions between bullets and enemies

The not so easy part was striking the right balance. Not going too technical. Not doing too much at once. Not dividing things into too many tiny pieces. But most of all I frequently encountered various bugs in the code, or just unexpected behavior of cocos2d which forced me to spend more time debugging and sometimes backtracking changes than I was prepared for.![2010-08-21_21.31.39](../../../wordpress/wp-content/uploads/2010-08-21_21.31.39-300x156.png)


After a long and hard work week, paired with physical exhaustion and an late-summer allergy burst, my concentration didn’t allow me to work at 100% capacity. In the end I did manage but it took longer than I had planned, I’m over a day late to submit this chapter. The next one will be easier though, and it has to be as I’m preparing for a short trip near the end of next week. I certainly am looking forward to a couple days off now. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[apress](http://www.learn-cocos2d.com/tag/apress/)•

[Chapter](http://www.learn-cocos2d.com/tag/chapter/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[collision](http://www.learn-cocos2d.com/tag/collision/)•

[collisions](http://www.learn-cocos2d.com/tag/collisions/)•

[component](http://www.learn-cocos2d.com/tag/component/)•

[component system](http://www.learn-cocos2d.com/tag/component-system/)•

[Components](http://www.learn-cocos2d.com/tag/components/)•

[composition](http://www.learn-cocos2d.com/tag/composition/)•

[Designer](http://www.learn-cocos2d.com/tag/designer/)•

[enemies](http://www.learn-cocos2d.com/tag/enemies/)•

[healthbar](http://www.learn-cocos2d.com/tag/healthbar/)•

[hierarchy](http://www.learn-cocos2d.com/tag/hierarchy/)•

[inheritance](http://www.learn-cocos2d.com/tag/inheritance/)•

[movement](http://www.learn-cocos2d.com/tag/movement/)•

[Particle](http://www.learn-cocos2d.com/tag/particle/)•

[particle effects](http://www.learn-cocos2d.com/tag/particle-effects/)•

[shooting](http://www.learn-cocos2d.com/tag/shooting/)

General comments - am up to chapter 4, finding it all very valuable. As in, its trivial to figure out how to put a CCSprite onscreen and move it, but I’ve learned a lot of the bits and pieces to make it all work well, like using mult instead of div, or the explanation of autorelease in Cocos. The upcoming chapter list looks promising, also. Already worth the money spent.

But I am looking forward to access to the source code, as I’m having a bit of trouble with taking the fragments of DoodleDrop code and making it live. There’s nothing quite like having a functional project to tinker with…

PS I appreciate a game dev book actually written by an experienced, professional game developer. It’s amazing (albeit rationally explicable) that the vast majority of the game dev books are written by people who’ve never shipped significant titles (AAA, or a strong string of indie work). And the exceptions are almost all article collections (Gems, ShaderX, etc), rather than a full length, deep dive like this.

Thank you! I’m still waiting on feedback from Apress if or when the source code will be available in Alpha form. Please be patient.

Easy read, learned a lot of things that were a bit blurry on cocos2d wiki page and also new things came to clarity that were a bit shady from my own trail and error sessions…. Waiting for the next chapters. Keep it up!

Essentials, page 9. -> “The keyword _cmd is shorthand for the current method.”

_cmd is a hidden parameter of type SEL (as self of type id) to method implementation and not a keyword.

Of course. I have the unfortunate habit of calling things like #define SOMETHING keywords too.

I too found the first 5 chapters very well written and I’ve had “ah-ha” moments throughout. If there’s anyway you can pester Apress to release more chapters - I’d like to keep reading… Thanks again

Greg

Would be very cool if you add something about the high-res textures! I’d like to know how i can get the best out of cocos2d on iphone4.

You sure know how to write understandable texts but your graphics is obviously not your area of expertise…..Lol

Love your stuff, waiting for the next chapters to arrive…

Great tutor Steffen

David