---
title: Enumerations
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/cc_g_l_state_cache_8h/
published: '2012-07-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.0
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

| enum | { kCCVertexAttribFlag_None = 0,
kCCVertexAttribFlag_Position = 1 << 0,
kCCVertexAttribFlag_Color = 1 << 1,
kCCVertexAttribFlag_TexCoords = 1 << 2,
kCCVertexAttribFlag_PosColorTex = ( kCCVertexAttribFlag_Position | kCCVertexAttribFlag_Color | kCCVertexAttribFlag_TexCoords )
} |
| enum |
CC_GL_BLEND = 1 << 3,
CC_GL_ALL = ( CC_GL_BLEND )
} |

| anonymous enum |

vertex attrib flags

If the active texture is not textureEnum, then it will active it. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glActiveTexture() directly.

If the texture is not already bound, it binds it. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glBindTexture() directly.

Uses a blending function in case it not already used. If CC_ENABLE_GL_STATE_CACHE is disabled, it will the glBlendFunc() directly.

Deletes the GL program. If it is the one that is being used, it invalidates it. If CC_ENABLE_GL_STATE_CACHE is disabled, it will the glDeleteProgram() directly.

It will delete a given texture. If the texture was bound, it will invalidate the cached. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glDeleteTextures() directly.

It will enable / disable the server side GL states. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glEnable() directly.

Will enable the vertex attribs that are passed as flags. Possible flags:

kCCVertexAttribFlag_Position kCCVertexAttribFlag_Color kCCVertexAttribFlag_TexCoords

These flags can be ORed. The flags that are not present, will be disabled.

Returns the active texture. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glGetIntegerv(GL_ACTIVE_TEXTURE);

Invalidates the GL state cache. If CC_ENABLE_GL_STATE_CACHE it will reset the GL state cache.

Uses the GL program in case program is different than the current one. If CC_ENABLE_GL_STATE_CACHE is disabled, it will the glUseProgram() directly.