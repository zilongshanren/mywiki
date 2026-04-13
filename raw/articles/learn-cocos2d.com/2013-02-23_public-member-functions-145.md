---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_motion_streak/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCMotionStreak.h>`


| (id) | -
|

MotionStreak. Creates a trailing path.

| - (id) initWithFade: | (float) | fade |
|
| minSeg: | (float) | minSeg |
|
| width: | (float) | stroke |
|
| color: | (
|

initializes a motion streak with fade in seconds, minimum segments, stroke's width, color and texture

| - (id) initWithFade: | (float) | fade |
|
| minSeg: | (float) | minSeg |
|
| width: | (float) | stroke |
|
| color: | (
|

initializes a motion streak with fade in seconds, minimum segments, stroke's width, color and texture filename

| + (id) streakWithFade: | (float) | fade |
|
| minSeg: | (float) | minSeg |
|
| width: | (float) | stroke |
|
| color: | (
|

creates and initializes a motion streak with fade in seconds, minimum segments, stroke's width, color, texture

| + (id) streakWithFade: | (float) | fade |
|
| minSeg: | (float) | minSeg |
|
| width: | (float) | stroke |
|
| color: | (
|

creates and initializes a motion streak with fade in seconds, minimum segments, stroke's width, color, texture filename

When fast mode is enabled, new points are added faster but with lower precision