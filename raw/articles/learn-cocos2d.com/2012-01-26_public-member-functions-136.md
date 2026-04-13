---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCTexture2D.h>`


| id |
|

[CCTexture2D](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) class. This class allows to easily create OpenGL 2D textures from images, text or raw data. The created [CCTexture2D](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) object will always have power-of-two dimensions. Depending on how you create the [CCTexture2D](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_texture2_d/) object, the actual image area of the texture might be smaller than the texture dimensions i.e. "contentSize" != (pixelsWide, pixelsHigh) and (maxS, maxT) != (1.0, 1.0). Be aware that the content of the generated textures will be upside-down!

returns the bits-per-pixel of the in-memory OpenGL texture

| CGSize CCTexture2D::contentSize | ( | ) | ` [virtual]` |

returns the content size of the texture in points

returns the alpha pixel format

Generates mipmap images for the texture. It only works if the texture size is POT (power of 2).

| id CCTexture2D::initWithData:pixelFormat:pixelsWide:pixelsHigh:contentSize: | ( | const void * | data, |
| [pixelFormat] CCTexture2DPixelFormat | pixelFormat, |
||
| [pixelsWide] NSUInteger | width, |
||
| [pixelsHigh] NSUInteger | height, |
||
| [contentSize] CGSize | size |
||
| ) | ` [virtual]` |

Intializes with a texture2d with data

Initializes a texture from a UIImage object

Initializes a texture from a PVR file.

Supported PVR formats:

By default PVR images are treated as if they alpha channel is NOT premultiplied. You can override this behavior with this class method:

IMPORTANT: This method is only defined on iOS. It is not supported on the Mac version.

| id
|

` [virtual]`

Initializes a texture from a PVR Texture Compressed (PVRTC) buffer

IMPORTANT: This method is only defined on iOS. It is not supported on the Mac version.

| id
|

` [virtual]`

Initializes a texture from a string with dimensions, alignment, font name and font size

| id
|

` [virtual]`

Initializes a texture from a string with dimensions, alignment, line break mode, font name and font size Supported lineBreakModes:

| id
|

` [virtual]`

Initializes a texture from a string with font name and font size

| void
|

` [static, virtual]`

treats (or not) PVR files as if they have alpha premultiplied. Since it is impossible to know at runtime if the PVR images have the alpha channel premultiplied, it is possible load them as if they have (or not) the alpha channel premultiplied.

By default it is disabled.

| void CCTexture2D::releaseData: | ( | void * | data | ) | ` [virtual]` |

These functions are needed to create mutable textures

sets alias texture parameters:

sets antialias texture parameters:

| void
|

` [static, virtual]`

sets the default pixel format for UIImages that contains alpha channel. If the UIImage contains alpha channel, then the options are:

How does it work ?

This parameter is not valid for PVR images.

sets the min filter, mag filter, wrap s and wrap t texture parameters. If the texture size is NPOT (non power of 2), then in can only use GL_CLAMP_TO_EDGE in GL_TEXTURE_WRAP_{S,T}.

CGSize CCTexture2D::contentSizeInPixels` [read, assign]` |

returns content size of the texture in pixels

BOOL CCTexture2D::hasPremultipliedAlpha` [read, assign]` |

whether or not the texture has their Alpha premultiplied

GLfloat CCTexture2D::maxS` [read, write, assign]` |

texture max S

GLfloat CCTexture2D::maxT` [read, write, assign]` |

texture max T

GLuint CCTexture2D::name` [read, assign]` |

texture name

CCTexture2DPixelFormat CCTexture2D::pixelFormat` [read, assign]` |

pixel format of the texture

NSUInteger CCTexture2D::pixelsHigh` [read, assign]` |

hight in pixels

NSUInteger CCTexture2D::pixelsWide` [read, assign]` |

width in pixels