---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_render_texture/
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

`#import <CCRenderTexture.h>`


| (id) | -
|

[CCRenderTexture](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_render_texture/) is a generic rendering target. To render things into it, simply construct a render target, call begin on it, call visit on any cocos2d scenes or objects to render them, and call end. For convenience, render texture adds a sprite as its display child with the results, so you can simply add the render texture to your scene and treat it like any other [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/). There are also functions for saving the render texture to disk in PNG or JPG format.

| - (void) beginWithClear: | (float) | r |
|
| g: | (float) | g |
|
| b: | (float) | b |
|
| a: | (float) | a |
|

starts rendering to the texture while clearing the texture first. This is more efficient then calling -clear first and then -begin

| - (void) beginWithClear: | (float) | r |
|
| g: | (float) | g |
|
| b: | (float) | b |
|
| a: | (float) | a |
|
| depth: | (float) | depthValue |
|

starts rendering to the texture while clearing the texture first. This is more efficient then calling -clear first and then -begin

| - (void) beginWithClear: | (float) | r |
|
| g: | (float) | g |
|
| b: | (float) | b |
|
| a: | (float) | a |
|
| depth: | (float) | depthValue |
|
| stencil: | (int) | stencilValue |
|

starts rendering to the texture while clearing the texture first. This is more efficient then calling -clear first and then -begin

| - (void) clear: | (float) | r |
|
| g: | (float) | g |
|
| b: | (float) | b |
|
| a: | (float) | a |
|

clears the texture with a color

| - (id) initWithWidth: | (int) | w |
|
| height: | (int) | h |
|
| pixelFormat: | (CCTexture2DPixelFormat) | format |
|

initializes a RenderTexture object with width and height in Points and a pixel format, only RGB and RGBA formats are valid

| - (id) initWithWidth: | (int) | w |
|
| height: | (int) | h |
|
| pixelFormat: | (CCTexture2DPixelFormat) | format |
|
| depthStencilFormat: | (GLuint) | depthStencilFormat |
|

initializes a RenderTexture object with width and height in Points and a pixel format( only RGB and RGBA formats are valid ) and depthStencil format

| + (id) renderTextureWithWidth: | (int) | w |
|
| height: | (int) | h |
|

creates a RenderTexture object with width and height in Points, pixel format is RGBA8888

| + (id) renderTextureWithWidth: | (int) | w |
|
| height: | (int) | h |
|
| pixelFormat: | (CCTexture2DPixelFormat) | format |
|

creates a RenderTexture object with width and height in Points and a pixel format, only RGB and RGBA formats are valid

| + (id) renderTextureWithWidth: | (int) | w |
|
| height: | (int) | h |
|
| pixelFormat: | (CCTexture2DPixelFormat) | format |
|
| depthStencilFormat: | (GLuint) | depthStencilFormat |
|

initializes a RenderTexture object with width and height in Points and a pixel format( only RGB and RGBA formats are valid ) and depthStencil format

saves the texture into a file using JPEG format. The file will be saved in the Documents folder. Returns YES if the operation is successful.

saves the texture into a file. The format could be JPG or PNG. The file will be saved in the Documents folder. Returns YES if the operation is successful.

When enabled, it will render its children into the texture automatically. Disabled by default for compatiblity reasons. Will be enabled in the future.

Clear color value. Valid only when "autoDraw" is YES.

Value for clearDepth. Valid only when autoDraw is YES.

Valid flags: GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_STENCIL_BUFFER_BIT. They can be OR'ed. Valid when "autoDraw is YES.

Value for clear Stencil. Valid only when autoDraw is YES

The [CCSprite](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite/) being used. The sprite, by default, will use the following blending function: GL_ONE, GL_ONE_MINUS_SRC_ALPHA. The blending function can be changed in runtime by calling: