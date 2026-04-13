---
title: Static Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_c_c_animation_07_kobold_extensions_08/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCAnimationExtensions.h>`


| id |
|

extends CCAnimation

| CCAnimation* CCAnimation(KoboldExtensions)::animationWithFiles:frameCount:delay: | ( | NSString * | name, |
| [frameCount] int | frameCount, |
||
| [delay] float | delay |
||
| ) | ` [static, virtual]` |

Creates a CCAnimation from individual files. The name is the base name of the files which must be suffixed with consecutive numbers. For example: ship0.png, ship1.png, ship2.png ... (name:"ship" frameCount:3)

| CCAnimation* CCAnimation(KoboldExtensions)::animationWithFrames:frameCount:delay: | ( | NSString * | frame, |
| [frameCount] int | frameCount, |
||
| [delay] float | delay |
||
| ) | ` [static, virtual]` |

Creates a CCAnimation from individual sprite frames. Assumes the sprite frames have already been loaded. The name is the base name of the files which must be suffixed with consecutive numbers. For example: ship0.png, ship1.png, ship2.png ... (name:"ship" frameCount:3)

| id CCAnimation(KoboldExtensions)::animationWithName:format:numFrames:firstIndex:delay: | ( | NSString * | name, |
| [format] NSString * | format, |
||
| [numFrames] int | numFrames, |
||
| [firstIndex] int | firstIndex, |
||
| [delay] float | delay |
||
| ) | ` [static, virtual]` |

Creates a CCAnimation with name, a format string for the consecutively numbered files (eg "frames_i.png"), the number of frames, the first index (from where to count numFrames), and delay between frames.