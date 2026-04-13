---
title: CCMotionStreak Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_motion_streak/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCMotionStreak.h](http://www.learn-cocos2d.com/)"

Inherits [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/), and [CCTextureProtocol-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_texture_protocol-p/).

| (id) | -
|

[CCMotionStreak](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_motion_streak/) manages a Ribbon based on it's motion in absolute space. You construct it with a fadeTime, minimum segment size, texture path, texture length and color. The fadeTime controls how long it takes each vertex in the streak to fade out, the minimum segment size it how many pixels the streak will move before adding a new ribbon segement, and the texture length is the how many pixels the texture is stretched across. The texture is vertically aligned along the streak segemnts.

Limitations: [CCMotionStreak](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_motion_streak/), by default, will use the GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA blending function. This blending function might not be the correct one for certain textures. But you can change it by using: [obj setBlendFunc: (ccBlendfunc) {new_src_blend_func, new_dst_blend_func}];

| - (id) initWithFade: | (float) | fade |
||
| minSeg: | (float) | seg |
||
| image: | (NSString *) | path |
||
| width: | (float) | width |
||
| length: | (float) | length |
||
| color: | (
|

initializes a MotionStreak. The file will be loaded using the TextureMgr.

| + (id) streakWithFade: | (float) | fade |
||
| minSeg: | (float) | seg |
||
| image: | (NSString *) | path |
||
| width: | (float) | width |
||
| length: | (float) | length |
||
| color: | (
|

creates the a MotionStreak. The image will be loaded using the TextureMgr.