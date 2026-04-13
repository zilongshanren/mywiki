---
title: Protected Attributes
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/structt_c_c_particle/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCParticleSystem.h>`



[List of all members.](/)

Protected Attributes
|
CGPoint | **pos** |
CGPoint | **startPos** |
[ccColor4F](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/structcc_color4_f/) | **color** |
[ccColor4F](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/structcc_color4_f/) | **deltaColor** |
float | **size** |
float | **deltaSize** |
float | **rotation** |
float | **deltaRotation** |
[ccTime](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/cc_types_8h/#a567bc32a0587702a30aa4e1dd7bedd33) | **timeToLive** |
NSUInteger | **atlasIndex** |
union { |
| struct { |
CGPoint **dir** |
float **radialAccel** |
float **tangentialAccel** |
} **A** |
| struct { |
float **angle** |
float **degreesPerSecond** |
float **radius** |
float **deltaRadius** |
} **B** |
| } | **mode** |


## Detailed Description

Structure that contains the values of each particle


The documentation for this struct was generated from the following file: