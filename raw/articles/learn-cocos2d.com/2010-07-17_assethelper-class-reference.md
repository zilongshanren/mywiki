---
title: AssetHelper Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_asset_helper/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Makes loading device-dependant resoures (assets) easier.
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[AssetHelper.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_asset_helper_8h_source/)>

| (NSString *) | +
|

Makes loading device-dependant resoures (assets) easier.

By default it simply assumes all iPad resources to be suffixed by "-ipad" before the filename extension. On iPhone/iPod Touch it will simply return the given filename, so the overhead is minimal while the iPad has enough power to cope with modifying a resource strings on the fly.

| + (NSString *) getDeviceSpecificFileNameFor: | (NSString*) | fileName |

Takes a string that is a filename (with or without path component) and returns the correct filename depending on the current device.

On iPhone/iPod Touch it will simply return fileName. On iPad it will append "-ipad" to the filename and before the suffix and return that. By naming all corresponding iPad assets with the "-ipad" suffix and using this function you can avoid a lot of ifdef and load different resource files with the same code.