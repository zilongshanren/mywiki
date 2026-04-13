---
title: Protected Attributes
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/structt_c_c_particle/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCParticleSystem.h>`



|
CGPoint | **pos** |
| |
CGPoint | **startPos** |
| |
[ccColor4F](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/structcc_color4_f/) | **color** |
| |
[ccColor4F](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/structcc_color4_f/) | **deltaColor** |
| |
float | **size** |
| |
float | **deltaSize** |
| |
float | **rotation** |
| |
float | **deltaRotation** |
| |
[ccTime](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/cc_types_8h/#a567bc32a0587702a30aa4e1dd7bedd33) | **timeToLive** |
| |
NSUInteger | **atlasIndex** |
| |
union { |
| struct { |
CGPoint **dir** |
| |
float **radialAccel** |
| |
float **tangentialAccel** |
| |
} **A** |
| |
| struct { |
float **angle** |
| |
float **degreesPerSecond** |
| |
float **radius** |
| |
float **deltaRadius** |
| |
} **B** |
| |
| } | **mode** |
| |

Structure that contains the values of each particle


The documentation for this struct was generated from the following file: