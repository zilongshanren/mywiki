---
title: <CCTextureProtocol> Protocol Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_texture_protocol-p/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCProtocols.h](http://www.learn-cocos2d.com/)"

Inherits [CCBlendProtocol-p](http://www.learn-cocos2d.com/).

Inherited by [CCAtlasNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_atlas_node/), [CCMotionStreak](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_motion_streak/), [CCParticleSystem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_particle_system/), [CCRibbon](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_ribbon/), [CCSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite/), and [CCSpriteBatchNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/).

| (void) | -
|

[CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) objects that uses a Texture2D to render the images. The texture can have a blending function. If the texture has alpha premultiplied the default blending function is: src=GL_ONE dst= GL_ONE_MINUS_SRC_ALPHA else src=GL_SRC_ALPHA dst= GL_ONE_MINUS_SRC_ALPHA But you can change the blending funtion at any time.