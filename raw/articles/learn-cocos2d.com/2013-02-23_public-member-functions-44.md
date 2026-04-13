---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_texture_cache/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCTextureCache.h>`


| (
|

Singleton that handles the loading of textures Once the texture is loaded, the next time it will return a reference of the previously loaded texture reducing GPU & CPU memory

Returns a Texture2D object given an CGImageRef image If the image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_texture2_d/) object and it will return it. Otherwise it will return a reference of a previously loaded image The "key" parameter will be used as the "key" for the cache. If "key" is nil, then a new texture will be created each time.

Returns a Texture2D object given an file image If the file image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_texture2_d/) object and it will return it. It will use the filename as a key. Otherwise it will return a reference of a previously loaded image. Supported image extensions: .png, .bmp, .tiff, .jpeg, .pvr, .gif

| - (void) addImageAsync: | (NSString *) | filename |
|
| target: | (id) | target |
|
| selector: | (SEL) | selector |
|

Asynchronously, load a texture2d from a file. If the file image was previously loaded, it will use it. Otherwise it will load a texture in a new thread, and when the image is loaded, the callback will be called with the Texture2D as a parameter. The callback will be called in the cocos2d thread, so it is safe to create any cocos2d object from the callback. Supported image extensions: .png, .bmp, .tiff, .jpeg, .pvr, .gif

Asynchronously, load a texture2d from a file. If the file image was previously loaded, it will use it. Otherwise it will load a texture in a new thread, and when the image is loaded, the block will be called. The callback will be called in the cocos2d thread, so it is safe to create any cocos2d object from the callback. Supported image extensions: .png, .bmp, .tiff, .jpeg, .pvr, .gif

Returns a Texture2D object given an PVR filename. If the file image was not previously loaded, it will create a new [CCTexture2D](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_texture2_d/) object and it will return it. Otherwise it will return a reference of a previously loaded image

Purges the dictionary of loaded textures. Call this method if you receive the "Memory Warning" In the short term: it will free some resources preventing your app from being killed In the medium term: it will allocate more resources In the long term: it will be the same

Deletes a texture from the cache given a its key name

Removes unused textures Textures that have a retain count of 1 will be deleted It is convenient to call this method after when starting a new Scene

Returns an already created texture. Returns nil if the texture doesn't exist.