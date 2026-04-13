---
title: Learn Cocos2D Book Source Code Update
url: http://www.learn-cocos2d.com/2011/05/learn-cocos2d-book-source-code-update/
author: Cocos; Learn
published: '2011-05-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

The most frequent questions I get from readers of my [Learn Cocos2D book](http://www.learn-cocos2d.com/store/book-learn-cocos2d/):

- “Where can I download the source code?”
- “Why do I get compile errors in CCLabel?”
- “Is there an updated version of CCAnimationHelper?”

They all boil down to the fact that the book was written against cocos2d-iphone v0.99.5 with some projects using v0.99.4 and a few even had used v0.99.3.

Unfortunately this is also why some readers deducted one or more stars in their Amazon book reviews. Even more unfortunate because the changes that break the code were entirely cosmetic (renamed classes, function parameters removed or re-ordered, deprecated functions in favor of others). All changes required only fixing the lines using one of these outdated classes (CCLabel, CCLayerColor) or functions (bitmapFontAtlasWithString, frameWithTexture, …).

### Quick List of Changes

I kept track of the changes I made to the source code. This is what it boils down to:

**remove**: EAGLView viewWith… -> remove last parameter: preserveBackBuffer:NO**remove**: CCSpriteFrame: frameWithTexture -> remove last parameter: offset:CGPointZero**remove**: CCAnimation: animationWithName -> animationWithFrames & remove last parameter: frames**rename**: CCLabel -> CCLabelTTF**rename**: CCBitmapFontAtlas -> CCLabelBMFont**rename**: CCBitmapFontAtlas: bitmapFontAtlasWithString -> labelWithString**rename**: CCXxxxxTransition -> CCTransitionXxxxx**rename**: CCColorLayer -> CCLayerColor**rename**: CCQuadParticleSystem -> CCParticleSystemQuad**rename**: particle system: centerOfGravity -> sourcePosition**change**: particle system: use NSUInteger instead of int for initWithParticleCount

These are the changes affecting the book’s source code. There were some more changes in the cocos2d-iphone engine, for example some actions have been renamed as well.

### Good News: Updated Source Code for v1.0

I updated the book’s source code to use cocos2d-iphone v1.0.0 rc2. Once the v1.0 final is released I’ll make another update.

You can get the book’s source code from the [Learn Cocos2D Book product page](http://www.learn-cocos2d.com/store/book-learn-cocos2d/) (scroll to the bottom), or via this [direct download link](https://www.learn-cocos2d.com/files/Learn_iPhone_and_iPad_Cocos2D_Game_Development_Source_Code_cocos2d-1.0.zip). The download is about 100 MB and contains all the chapter’s source code plus some extra projects not mentioned in the book, and all of them (over 70!) are now using cocos2d-iphone v1.0.


Note:This code obviously differs slightly from the code described in the first edition of the Learn Cocos2D book, so you should get the[unmodified v0.99.x book source code]as well.

### Upgrading to Cocos2D v1.0

I also recently wrote a [tutorial outlining the steps to update an existing cocos2d-iphone v0.99.x project to v1.0](http://www.learn-cocos2d.com/2011/05/update-cocos2d-iphone-existing-project/) in case you have an existing project that you’d like to upgrade to the latest Cocos2D version.

### Learn Cocos2D: Second Edition

All these changes will be reflected in the [second edition of the Learn Cocos2D book](http://www.learn-cocos2d.com/2011/05/learn-cocos2d-book-2nd-edition-started/).

The second edition will be released summer 2011, likely around July to August. This is my estimate based on the fact that my work is scheduled to be completed on June 27th, and I’m working hard to keep that (tight) schedule.

Actually, make that **we** are working hard. The second edition of the Learn Cocos2D book will have contributions from a co-author. Someone who is well-known in the Cocos2D community! To be unveiled. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] completed the revisions on Chapter 1 through 5. The entire source code is now updated to use cocos2d-iphone v1.0.0 rc2. To make future code updates easier I also wrote a script that […]