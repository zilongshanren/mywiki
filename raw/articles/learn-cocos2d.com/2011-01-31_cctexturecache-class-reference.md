---
title: CCTextureCache Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture_cache/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCTextureCache.h](http://www.learn-cocos2d.com/)"

| (
|

Singleton that handles the loading of textures Once the texture is loaded, the next time it will return a reference of the previously loaded texture reducing GPU & CPU memory

Returns a Texture2D object given an CGImageRef image If the image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) object and it will return it. Otherwise it will return a reference of a previously loaded image The "key" parameter will be used as the "key" for the cache. If "key" is nil, then a new texture will be created each time.

Returns a Texture2D object given an file image If the file image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) object and it will return it. It will use the filename as a key. Otherwise it will return a reference of a previosly loaded image. Supported image extensions: .png, .bmp, .tiff, .jpeg, .pvr, .gif

| - (void) addImageAsync: | (NSString *) | filename |
||
| target: | (id) | target |
||
| selector: | (SEL) | selector | ||

Returns a Texture2D object given a file image If the file image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) object and it will return it. Otherwise it will load a texture in a new thread, and when the image is loaded, the callback will be called with the Texture2D as a parameter. The callback will be called from the main thread, so it is safe to create any cocos2d object from the callback. Supported image extensions: .png, .bmp, .tiff, .jpeg, .pvr, .gif

Returns a Texture2D object given an PVR filename. If the file image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) object and it will return it. Otherwise it will return a reference of a previosly loaded image

| - (
|

Returns a Texture2D object given an PVRTC RAW filename If the file image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture2_d/) object and it will return it. Otherwise it will return a reference of a previosly loaded image

It can only load square images: width == height, and it must be a power of 2 (128,256,512...) bpp can only be 2 or 4. 2 means more compression but lower quality. hasAlpha: whether or not the image contains alpha channel

IMPORTANT: This method is only defined on iOS. It is not supported on the Mac version.

| + (void) purgeSharedTextureCache |

purges the cache. It releases the retained instance.

| - (void) removeAllTextures |

Purges the dictionary of loaded textures. Call this method if you receive the "Memory Warning" In the short term: it will free some resources preventing your app from being killed In the medium term: it will allocate more resources In the long term: it will be the same

| - (void) removeTextureForKey: | (NSString *) | textureKeyName |

Deletes a texture from the cache given a its key name

| - (void) removeUnusedTextures |

Removes unused textures Textures that have a retain count of 1 will be deleted It is convinient to call this method after when starting a new Scene

Returns an already created texture. Returns nil if the texture doesn't exist.