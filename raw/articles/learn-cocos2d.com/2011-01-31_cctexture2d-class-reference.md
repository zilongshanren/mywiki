---
title: CCTexture2D Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCTexture2D.h](http://www.learn-cocos2d.com/)"

| (CGSize) | -
|

[CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) class. This class allows to easily create OpenGL 2D textures from images, text or raw data. The created [CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) object will always have power-of-two dimensions. Depending on how you create the [CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) object, the actual image area of the texture might be smaller than the texture dimensions i.e. "contentSize" != (pixelsWide, pixelsHigh) and (maxS, maxT) != (1.0, 1.0). Be aware that the content of the generated textures will be upside-down!

| - (CGSize) contentSize |

returns the content size of the texture in points

| + (CCTexture2DPixelFormat) defaultAlphaPixelFormat |

returns the alpha pixel format

| - (void) drawAtPoint: | (CGPoint) | point |

draws a texture at a given point

| - (void) drawInRect: | (CGRect) | rect |

draws a texture inside a rect

| - (void) generateMipmap |

Generates mipmap images for the texture. It only works if the texture size is POT (power of 2).

| - (id) initWithData: | (const void *) | data |
||
| pixelFormat: | (CCTexture2DPixelFormat) | pixelFormat |
||
| pixelsWide: | (NSUInteger) | width |
||
| pixelsHigh: | (NSUInteger) | height |
||
| contentSize: | (CGSize) | size | ||

Intializes with a texture2d with data

| - (id) initWithImage: | (UIImage *) | uiImage |

Initializes a texture from a UIImage object

| - (id) initWithPVRFile: | (NSString *) | file |

Initializes a texture from a PVR file.

Supported PVR formats:

By default PVR images are treated as if they alpha channel is NOT premultiplied. You can override this behavior with this class method:

IMPORTANT: This method is only defined on iOS. It is not supported on the Mac version.

| - (id) initWithPVRTCData: | (const void *) | data |
||
| level: | (int) | level |
||
| bpp: | (int) | bpp |
||
| hasAlpha: | (BOOL) | hasAlpha |
||
| length: | (int) | length | ||

Initializes a texture from a PVR Texture Compressed (PVRTC) buffer

IMPORTANT: This method is only defined on iOS. It is not supported on the Mac version.

| - (id) initWithString: | (NSString *) | string |
||
| dimensions: | (CGSize) | dimensions |
||
| alignment: | (CCTextAlignment) | alignment |
||
| fontName: | (NSString *) | name |
||
| fontSize: | (CGFloat) | size | ||

Initializes a texture from a string with dimensions, alignment, font name and font size

| - (id) initWithString: | (NSString *) | string |
||
| fontName: | (NSString *) | name |
||
| fontSize: | (CGFloat) | size | ||

Initializes a texture from a string with font name and font size

| + (void) PVRImagesHavePremultipliedAlpha: | (BOOL) | haveAlphaPremultiplied |

treats (or not) PVR files as if they have alpha premultiplied. Since it is impossible to know at runtime if the PVR images have the alpha channel premultiplied, it is possible load them as if they have (or not) the alpha channel premultiplied.

By default it is disabled.

| - (void) releaseData: | (void *) | data |

These functions are needed to create mutable textures

| - (void) setAliasTexParameters |

sets alias texture parameters:

| - (void) setAntiAliasTexParameters |

sets antialias texture parameters:

| + (void) setDefaultAlphaPixelFormat: | (CCTexture2DPixelFormat) | format |

sets the default pixel format for UIImages that contains alpha channel. If the UIImage contains alpha channel, then the options are:

How does it work ?

This parameter is not valid for PVR images.

sets the min filter, mag filter, wrap s and wrap t texture parameters. If the texture size is NPOT (non power of 2), then in can only use GL_CLAMP_TO_EDGE in GL_TEXTURE_WRAP_{S,T}.

- (CGSize) contentSizeInPixels` [read, assign]` |

returns content size of the texture in pixels

- (BOOL) hasPremultipliedAlpha` [read, assign]` |

whether or not the texture has their Alpha premultiplied

- (GLfloat) maxS` [read, write, assign]` |

texture max S

- (GLfloat) maxT` [read, write, assign]` |

texture max T

- (GLuint) name` [read, assign]` |

texture name

- (CCTexture2DPixelFormat) pixelFormat` [read, assign]` |

pixel format of the texture

- (NSUInteger) pixelsHigh` [read, assign]` |

hight in pixels

- (NSUInteger) pixelsWide` [read, assign]` |

width in pixels