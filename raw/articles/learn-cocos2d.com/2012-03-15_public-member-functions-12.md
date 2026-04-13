---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_c_c_sprite_07_kobold_extensions_08/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCSpriteExtensions.h>`


| void |
|

extends CCSprite

| void CCSprite(KoboldExtensions)::playAnimAndRemoveWithFormat:numFrames:firstIndex:delay:animateTag: | ( | NSString * | format, |
| [numFrames] int | numFrames, |
||
| [firstIndex] int | firstIndex, |
||
| [delay] float | delay, |
||
| [animateTag] int | animateTag |
||
| ) | ` [virtual]` |

Plays an anim once with the given file format (eg "playeranimi.png") with the given number of frames and a starting index. The animateTag parameter is the tag given to the action playing the animation, so that you can stop it by tag. When the anim has cycled through all frames, the node running the animation will be removed from its parent. Useful for one-off animations, like an explosion, smoke-puff, blood splat, etc.

| void CCSprite(KoboldExtensions)::playAnimAndRemoveWithFormat:numFrames:firstIndex:delay:animateTag:restoreOriginalFrame: | ( | NSString * | format, |
| [numFrames] int | numFrames, |
||
| [firstIndex] int | firstIndex, |
||
| [delay] float | delay, |
||
| [animateTag] int | animateTag, |
||
| [restoreOriginalFrame] BOOL | restoreOriginalFrame |
||
| ) | ` [virtual]` |

Variant that allows to set the restoreOriginalFrame property.

| void CCSprite(KoboldExtensions)::playAnimLoopedWithFormat:numFrames:firstIndex:delay:animateTag: | ( | NSString * | format, |
| [numFrames] int | numFrames, |
||
| [firstIndex] int | firstIndex, |
||
| [delay] float | delay, |
||
| [animateTag] int | animateTag |
||
| ) | ` [virtual]` |

Plays an anim looped with the given file format (eg "playeranimi.png") with the given number of frames and a starting index. The animateTag parameter is the tag given to the action playing the animation, so that you can stop it by tag.

| void CCSprite(KoboldExtensions)::playAnimLoopedWithFormat:numFrames:firstIndex:delay:animateTag:restoreOriginalFrame: | ( | NSString * | format, |
| [numFrames] int | numFrames, |
||
| [firstIndex] int | firstIndex, |
||
| [delay] float | delay, |
||
| [animateTag] int | animateTag, |
||
| [restoreOriginalFrame] BOOL | restoreOriginalFrame |
||
| ) | ` [virtual]` |

Variant that allows to set the restoreOriginalFrame property.

| void CCSprite(KoboldExtensions)::playAnimWithFormat:numFrames:firstIndex:delay:animateTag: | ( | NSString * | format, |
| [numFrames] int | numFrames, |
||
| [firstIndex] int | firstIndex, |
||
| [delay] float | delay, |
||
| [animateTag] int | animateTag |
||
| ) | ` [virtual]` |

Plays an anim once with the given file format (eg "playeranimi.png") with the given number of frames and a starting index. The animateTag parameter is the tag given to the action playing the animation, so that you can stop it by tag.

| void CCSprite(KoboldExtensions)::playAnimWithFormat:numFrames:firstIndex:delay:animateTag:restoreOriginalFrame: | ( | NSString * | format, |
| [numFrames] int | numFrames, |
||
| [firstIndex] int | firstIndex, |
||
| [delay] float | delay, |
||
| [animateTag] int | animateTag, |
||
| [restoreOriginalFrame] BOOL | restoreOriginalFrame |
||
| ) | ` [virtual]` |

Variant that allows to set the restoreOriginalFrame property.

| id CCSprite(KoboldExtensions)::spriteWithRenderTexture: | ( | CCRenderTexture * | rtx | ) | ` [static, virtual]` |

Creates an autoreleased sprite from a CCRenderTexture

| id CCSprite(KoboldExtensions)::spriteWithSpriteFrameNameOrFile: | ( | NSString * | nameOrFile | ) | ` [static, virtual]` |

First, checks if the string can be found in the spriteFrameCache, if not it will try to load the string assuming its a file name.