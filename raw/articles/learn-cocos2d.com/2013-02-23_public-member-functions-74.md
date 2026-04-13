---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_camera/
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

`#import <CCCamera.h>`


| (void) | -
|

A [CCCamera](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_camera/) is used in every [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/). Useful to look at the object from different views. The OpenGL gluLookAt() function is used to locate the camera.

If the object is transformed by any of the scale, rotation or position attributes, then they will override the camera.

IMPORTANT: Either your use the camera or the rotation/scale/position properties. You can't use both. World coordinates won't work if you use the camera.

Limitations:

| - (void) centerX: | (float *) | x |
|
| centerY: | (float *) | y |
|
| centerZ: | (float *) | z |
|

get the center vector values in points

| - (void) eyeX: | (float *) | x |
|
| eyeY: | (float *) | y |
|
| eyeZ: | (float *) | z |
|

get the eye vector values in points

| - (void) setCenterX: | (float) | x |
|
| centerY: | (float) | y |
|
| centerZ: | (float) | z |
|

sets the center values in points

| - (void) setEyeX: | (float) | x |
|
| eyeY: | (float) | y |
|
| eyeZ: | (float) | z |
|

sets the eye values in points

| - (void) setUpX: | (float) | x |
|
| upY: | (float) | y |
|
| upZ: | (float) | z |
|

sets the up values

| - (void) upX: | (float *) | x |
|
| upY: | (float *) | y |
|
| upZ: | (float *) | z |
|

get the up vector values