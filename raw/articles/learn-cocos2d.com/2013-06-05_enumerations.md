---
title: Enumerations
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/cc_g_l_state_cache_8h/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.koboldtouch.com developers
|

| enum | { kCCVertexAttribFlag_None = 0,
kCCVertexAttribFlag_Position = 1 << 0,
kCCVertexAttribFlag_Color = 1 << 1,
kCCVertexAttribFlag_TexCoords = 1 << 2,
kCCVertexAttribFlag_PosColorTex = (kCCVertexAttribFlag_Position | kCCVertexAttribFlag_Color | kCCVertexAttribFlag_TexCoords)
} |
| enum |
CC_GL_ALL = 0
} |

| void |
|

| anonymous enum |

vertex attrib flags

| void ccGLBindTexture | ( | GLenum | target, |
| GLuint | textureId |
||
| ) |

If the texture is not already bound to texture unit 0 and if target is GL_TEXTURE_2D, it binds it. If CC_ENABLE_GL_STATE_CACHE is disabled or if target != GL_TEXTURE_2D it will call glBindTexture() directly.

| void ccGLBindTexture2D | ( | GLuint | textureId) |

If the texture is not already bound to texture unit 0, it binds it. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glBindTexture() directly.

| void ccGLBindTexture2DN | ( | GLuint | textureUnit, |
| GLuint | textureId |
||
| ) |

If the texture is not already bound to a given unit, it binds it. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glBindTexture() directly.

| void ccGLBindVAO | ( | GLuint | vaoId) |

If the vertex array is not already bound, it binds it. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glBindVertexArray() directly.

| void ccGLBlendFunc | ( | GLenum | sfactor, |
| GLenum | dfactor |
||
| ) |

Uses a blending function in case it not already used. If CC_ENABLE_GL_STATE_CACHE is disabled, it will the glBlendFunc() directly.

| void ccGLBlendResetToCache | ( | void | ) |

Resets the blending mode back to the cached state in case you used glBlendFuncSeparate() or glBlendEquation(). If CC_ENABLE_GL_STATE_CACHE is disabled, it will just set the default blending mode using GL_FUNC_ADD.

| void ccGLDeleteProgram | ( | GLuint | program) |

Deletes the GL program. If it is the one that is being used, it invalidates it. If CC_ENABLE_GL_STATE_CACHE is disabled, it will the glDeleteProgram() directly.

| void ccGLDeleteTexture | ( | GLuint | textureId) |

It will delete a given texture. If the texture was bound, it will invalidate the cached for texture unit 0. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glDeleteTextures() directly.

| void ccGLDeleteTextureN | ( | GLuint | textureUnit, |
| GLuint | textureId |
||
| ) |

It will delete a given texture. If the texture was bound, it will invalidate the cached for the given texture unit. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glDeleteTextures() directly.

It will enable / disable the server side GL states. If CC_ENABLE_GL_STATE_CACHE is disabled, it will call glEnable() directly.

| void ccGLEnableVertexAttribs | ( | unsigned int | flags) |

Will enable the vertex attribs that are passed as flags. Possible flags:

kCCVertexAttribFlag_Position kCCVertexAttribFlag_Color kCCVertexAttribFlag_TexCoords

These flags can be ORed. The flags that are not present, will be disabled.

| void ccGLInvalidateStateCache | ( | void | ) |

Invalidates the GL state cache. If CC_ENABLE_GL_STATE_CACHE it will reset the GL state cache.

| void ccGLUseProgram | ( | GLuint | program) |

Uses the GL program in case program is different than the current one. If CC_ENABLE_GL_STATE_CACHE is disabled, it will the glUseProgram() directly.

| void ccSetProjectionMatrixDirty | ( | void | ) |

sets the projection matrix as dirty