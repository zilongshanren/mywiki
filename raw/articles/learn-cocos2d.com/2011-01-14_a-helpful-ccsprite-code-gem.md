---
title: A helpful CCSprite code gem …
url: http://www.learn-cocos2d.com/2011/01/helpful-ccsprite-code-gem/
author: MorskoyZmey says
published: '2011-01-14'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I often start out with new code using dummy graphics. Until I figure out what exactly I need and what is going to work, I work with single image files added to the project’s resources. Creating a texture atlas is always the last step I do, once everything is settled. Creating and updating a Texture Atlas adds just a few extra steps but I always strive to avoid any unnecessary extra steps during a creative working period. Especially while experimenting. Any repetitive task hampers creativity.

But eventually, I will have to go in and change every CCSprite initialization code from spriteWithFile to spriteWithSpriteFrameName. Except, I don’t.

The following is a simple extension category for CCSprite that extends CCSprite with a spriteWithSpriteFrameNameOrFile initializer. It looks for the given file name in the CCSpriteFrameCache. If it exists as CCSpriteFrame, it uses that sprite frame and otherwise it reverts back to loading the sprite from file. Very easy, very helpful.

```
// CCSpriteExtensions.h
#import "cocos2d.h"
@interface CCSprite (Xtensions)
+(id) spriteWithSpriteFrameNameOrFile:(NSString*)nameOrFile;
@end
```


```
// CCSpriteExtensions.m
#import "CCSpriteExtensions.h"
@implementation CCSprite (Xtensions)
+(id) spriteWithSpriteFrameNameOrFile:(NSString*)nameOrFile
{
CCSpriteFrame* spriteFrame = [[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:nameOrFile];
if (spriteFrame)
{
return [CCSprite spriteWithSpriteFrame:spriteFrame];
}
return [CCSprite spriteWithFile:nameOrFile];
}
@end
```


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

It is realy easy and helpful

cocos2d dev team should add your function in official next release.

You should claim it on its forum

I wish it were that easy.

This is a gem. I approach it the same way. My designer sends me individual sprites and once I’m near the end of development, I switch over to spritesheets. This will be very useful.

Thanks!

[…] Gems: GameKitHelper, ClippingNode, Multiple Update Selectors, FrameOrFile, […]