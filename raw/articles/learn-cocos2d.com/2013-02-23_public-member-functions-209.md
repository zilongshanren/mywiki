---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_texture_p_v_r/
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

`#import <CCTexturePVR.h>`


| (id) | -
|

Object that loads PVR images.

Supported PVR formats:

Limitations: Pre-generated mipmaps, such as PVR textures with mipmap levels embedded in file, are only supported if all individual sprites are of *square* size. To use mipmaps with non-square textures, instead call [generateMipmap (CCTexture2D)](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_texture2_d/#a4b5fdc85363ee66f65d39a9e1f3489d0) on the sheet texture itself (and to save space, save the PVR sprite sheet without mip maps included).

whether or not the texture should use hasPremultipliedAlpha instead of global default

how many mipmaps the texture has. 1 means one level (level 0