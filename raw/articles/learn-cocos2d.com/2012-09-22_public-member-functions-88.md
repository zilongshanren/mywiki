---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_texture2_d/
published: '2012-09-22'
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

`#import <CCTexture2D.h>`


| (id) | -
|

[CCTexture2D](http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_texture2_d/) class. This class allows to easily create OpenGL 2D textures from images, text or raw data. The created [CCTexture2D](http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_texture2_d/) object will always have power-of-two dimensions. Depending on how you create the [CCTexture2D](http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_texture2_d/) object, the actual image area of the texture might be smaller than the texture dimensions i.e. "contentSize" != (pixelsWide, pixelsHigh) and (maxS, maxT) != (1.0, 1.0). Be aware that the content of the generated textures will be upside-down!

returns the bits-per-pixel of the in-memory OpenGL texture

Helper functions that returns bits per pixels for a given format.

Generates mipmap images for the texture. It only works if the texture size is POT (power of 2).

Initializes a texture from a CGImage object

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

Intializes with a texture2d with data

Initializes a texture from a PVR file.

Supported PVR formats:

By default PVR images are treated as if they alpha channel is NOT premultiplied. You can override this behavior with this class method:

IMPORTANT: This method is only defined on iOS. It is not supported on the Mac version.

| - (id) initWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

Initializes a texture from a string with dimensions, alignment, font name and font size

| - (id) initWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

Initializes a texture from a string with dimensions, alignment, line break mode, font name and font size Supported lineBreakModes:

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|

Initializes a texture from a string with font name and font size

treats (or not) PVR files as if they have alpha premultiplied. Since it is impossible to know at runtime if the PVR images have the alpha channel premultiplied, it is possible load them as if they have (or not) the alpha channel premultiplied.

By default it is disabled.

sets alias texture parameters:

sets antialias texture parameters:

sets the default pixel format for CGImages that contains alpha channel. If the CGImage contains alpha channel, then the options are:

How does it work ?

This parameter is not valid for PVR / PVR.CCZ images.

sets the min filter, mag filter, wrap s and wrap t texture parameters. If the texture size is NPOT (non power of 2), then in can only use GL_CLAMP_TO_EDGE in GL_TEXTURE_WRAP_{S,T}.

whether or not the texture has their Alpha premultiplied

Returns the resolution type of the texture. Is it a RetinaDisplay texture, an iPad texture or an standard texture ? Only valid on iOS. Not valid on OS X.

Should be a readonly property. It is readwrite as a hack.

shader program used by drawAtPoint and drawInRect