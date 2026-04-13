---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_texture2_d/
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

`#import <CCTexture2D.h>`


| (id) | -
|

| (void) | +
|

|

| CCTexture2DPixelFormat |
|

[CCTexture2D](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_texture2_d/) class. This class allows to easily create OpenGL 2D textures from images, text or raw data. The created [CCTexture2D](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_texture2_d/) object will always have power-of-two dimensions. Depending on how you create the [CCTexture2D](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_texture2_d/) object, the actual image area of the texture might be smaller than the texture dimensions i.e. "contentSize" != (pixelsWide, pixelsHigh) and (maxS, maxT) != (1.0, 1.0). Be aware that the content of the generated textures will be upside-down!

| - (NSUInteger) bitsPerPixelForFormat |

| + (NSUInteger) bitsPerPixelForFormat: | (CCTexture2DPixelFormat) | format |

| - (CGSize) contentSize |

returns the content size of the texture in points

| + (CCTexture2DPixelFormat) defaultAlphaPixelFormat |

| - (void) drawAtPoint: | (CGPoint) | point |

| - (void) drawInRect: | (CGRect) | rect |

| - (void) generateMipmap |

| - (id) initWithData: | (const void *) | data |
|
| pixelFormat: | (CCTexture2DPixelFormat) | pixelFormat |
|
| pixelsWide: | (NSUInteger) | width |
|
| pixelsHigh: | (NSUInteger) | height |
|
| contentSize: | (CGSize) | size |
|

Initializes with a texture2d with data

| - (id) initWithPVRFile: | (NSString *) | file |

Initializes a texture from a PVR file.

Supported PVR formats:

By default PVR images are treated as if they alpha channel is NOT premultiplied. You can override this behavior with this class method:

IMPORTANT: This method is only defined on iOS. It is not supported on the Mac version.

Provided by category [CCTexture2D(PVRSupport)](http://www.learn-cocos2d.com/#aad368c7ee5b5b81725772b8753a2aa51).

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

Initializes a texture from a string with dimensions, alignment, line break mode, font name and font size Supported lineBreakModes:

Provided by category [CCTexture2D(Text)](http://www.learn-cocos2d.com/#a65fea0340c96ad30c38ccb32af4c668d).

| + (void) PVRImagesHavePremultipliedAlpha: | (BOOL) | haveAlphaPremultiplied |

treats (or not) PVR files as if they have alpha premultiplied. Since it is impossible to know at runtime if the PVR images have the alpha channel premultiplied, it is possible load them as if they have (or not) the alpha channel premultiplied.

By default it is disabled.

Provided by category [CCTexture2D(PVRSupport)](http://www.learn-cocos2d.com/#a129338ae7dc5eccd0bc97b8af0a81b2a).

| - (void) releaseData: | (void *) | data |

These functions are needed to create mutable textures

| - (void) setAliasTexParameters |

sets alias texture parameters:

Provided by category [CCTexture2D(GLFilter)](http://www.learn-cocos2d.com/#a8dd7c5360b4d52d0ff83329292c0719e).

| - (void) setAntiAliasTexParameters |

sets antialias texture parameters:

Provided by category [CCTexture2D(GLFilter)](http://www.learn-cocos2d.com/#ae93d798c556a1550f1f553c33d2ab371).

| + (void) setDefaultAlphaPixelFormat: | (CCTexture2DPixelFormat) | format |

sets the default pixel format for CGImages that contains alpha channel. If the CGImage contains alpha channel, then the options are:

How does it work ?

This parameter is not valid for PVR / PVR.CCZ images.

Provided by category [CCTexture2D(PixelFormat)](http://www.learn-cocos2d.com/#add7db64ac4efbfb1570986c2f0f55ce6).

sets the min filter, mag filter, wrap s and wrap t texture parameters. If the texture size is NPOT (non power of 2), then in can only use GL_CLAMP_TO_EDGE in GL_TEXTURE_WRAP_{S,T}.

Provided by category [CCTexture2D(GLFilter)](http://www.learn-cocos2d.com/#a9cd0e19948c328609ec0c849a6cf0876).

| - (NSString*) stringForFormat |

|
readnonatomicassign |

returns content size of the texture in pixels

|
readnonatomicassign |

whether or not the texture has their Alpha premultiplied

|
readwritenonatomicassign |

texture max S

|
readwritenonatomicassign |

texture max T

|
readnonatomicassign |

texture name

|
readnonatomicassign |

pixel format of the texture

|
readnonatomicassign |

hight in pixels

|
readnonatomicassign |

width in pixels

Returns the resolution type of the texture. Is it a RetinaDisplay texture, an iPad texture, a Mac, a Mac RetinaDisplay or an standard texture ?

Should be a readonly property. It is readwrite as a hack.

shader program used by drawAtPoint and drawInRect