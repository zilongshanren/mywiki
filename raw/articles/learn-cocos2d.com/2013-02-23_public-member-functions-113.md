---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_file_utils/
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

`#import <CCFileUtils.h>`


| (void) | -
|

Helper class to handle file operations

Calling this method will populate the searchResolutionsOrder property depending on the current device.

Returns the fullpath for a given filename.

First it will try to get a new filename from the "filenameLookup" dictionary. If a new filename can't be found on the dictionary, it will use the original filename. Then it will try obtain the full path of the filename using the [CCFileUtils](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_file_utils/) search rules: resolutions, and search paths

If in iPad mode, and an iPad file is found, it will return that path. If in iPhoneRetinaDisplay mode, and a RetinaDisplay file is found, it will return that path. But if it is not found, it will try load an iPhone Non-RetinaDisplay file.

If the filename can't be found on the file system, it will return nil.

This method was added to simplify multiplatform support. Whether you are using cocos2d-js or any cross-compilation toolchain like StellaSDK or Apportable, you might need to load differerent resources for a given file in the different platforms.

Examples:

In iPad mode: "image.png" -> "image.pvr" -> "/full/path/image-ipad.pvr" (in case the -ipad file exists) In Android: "image.png" -> "image.png" -> "/full/path/image.png"

| - (NSString*)
|

Returns the fullpath for a given filename.

First it will try to get a new filename from the "filenameLookup" dictionary. If a new filename can't be found on the dictionary, it will use the original filename. Then it will try obtain the full path of the filename using the [CCFileUtils](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_file_utils/) search rules: resolutions, and search paths

If in iPad mode, and an iPad file is found, it will return that path. If in iPhoneRetinaDisplay mode, and a RetinaDisplay file is found, it will return that path. But if it is not found, it will try load an iPhone Non-RetinaDisplay file.

If the filename can't be found on the file system, it will return nil.

This method was added to simplify multiplatform support. Whether you are using cocos2d-js or any cross-compilation toolchain like StellaSDK or Apportable, you might need to load differerent resources for a given file in the different platforms.

Examples:

In iPad mode: "image.png" -> "image.pvr" -> "/full/path/image-ipad.pvr" (in case the -ipad file exists) In Android: "image.png" -> "image.png" -> "/full/path/image.png"

Returns the fullpath for a given filename, without taking into account device resolution.

It will try to get a new filename from the "filenameLookup" dictionary. If a new filename can't be found on the dictionary, it will use the original filename.

Once it gets the filename, it will try to get the fullpath for the filename, using the "searchPath", but it won't use any resolution search rules. If the file can't be found, it will return nil.

Useful for loading music files, shaders, "data" and other files that are not related to the screen resolution of the device.

This method was added to simplify multiplatform support. Whether you are using cocos2d-js or any cross-compilation toolchain like StellaSDK or Apportable, you might need to load differerent resources for a given file in the different platforms.

Examples:

On iOS: "sound.wav" -> "sound.caf" -> "/full/path/sound.caf" (in case the key dictionary says that "sound.wav" should be converted to "sound.caf") On Android: "sound.wav" -> "sound.wav" -> "/full/path/sound.caf" (in case the key dictionary says that "sound.wav" should be converted to "sound.caf")

Returns the fullpath of an filename.

If in iPhoneRetinaDisplay mode, and a RetinaDisplay file is found, it will return that path. If in iPad mode, and an iPad file is found, it will return that path.

If the filename can't be found, it will return "relPath" instead of nil.

Examples:

In iPad mode: "image.png" -> "/full/path/image-ipad.png" (in case the -ipad file exists) In iPhone RetinaDisplay mode: "image.png" -> "/full/path/image-hd.png" (in case the -hd file exists) In iPad RetinaDisplay mode: "image.png" -> "/full/path/image-ipadhd.png" (in case the -ipadhd file exists)

| - (NSString*)
|

Returns the fullpath of an filename. It will try to get the correct file for the current screen resolution. Useful for loading images and other assets that are related for the screen resolution.

If in iPad mode, and an iPad file is found, it will return that path. If in iPhoneRetinaDisplay mode, and a RetinaDisplay file is found, it will return that path. But if it is not found, it will try load an iPhone Non-RetinaDisplay file.

If the filename can't be found, it will return "relPath" instead of nil.

Examples:

In iPad mode: "image.png" -> "/full/path/image-ipad.png" (in case the -ipad file exists) In iPhone RetinaDisplay mode: "image.png" -> "/full/path/image-hd.png" (in case the -hd file exists) In iPad RetinaDisplay mode: "image.png" -> "/full/path/image-ipadhd.png" (in case the -ipadhd file exists)

Returns the fullpath of an filename without taking into account the screen resolution suffixes or directories.

It will use the "searchPath" though. If the file can't be found, it will return nil.

Useful for loading music files, shaders, "data" and other files that are not related to the screen resolution of the device.

Returns whether or not a given filename exists with the iPad suffix. Only available on iOS. Not supported on OS X.

Returns whether or not a given filename exists with the iPad RetinaDisplay suffix. Only available on iOS. Not supported on OS X.

Returns whether or not a given path exists with the iPhone RetinaDisplay suffix. Only available on iOS. Not supported on OS X.

Purge cached entries. Will be called automatically by the Director when a memory warning is received

removes the suffix from a path On iPhone RetinaDisplay it will remove the -hd suffix On iPad it will remove the -ipad suffix On iPad RetinaDisplay it will remove the -ipadhd suffix

Sets the iPad Retina Display suffixes to load resources. By default it is "-ipadhd", "-ipad", "-hd", "", in that order. Only valid on iOS. Not valid for OS X.

The iPad suffixes to load resources. By default it is "-ipad", "-hd", "", in that order. Only valid on iOS. Not valid for OS X.

The iPhone RetinaDisplay suffixes to load resources. By default it is "-hd" and "" in that order. Only valid on iOS. Not valid for OS X.

Dictionary that contians the search directories for the different devices. Default values:

If "search in directories" is enabled (disabled by default), it will try to get the resources from the directories according to the order of "searchResolutionsOrder" array.

Whether of not the fallback suffixes is enabled. When enabled it will try to search for the following suffixes in the following order until one is found: On iPad HD : iPad HD, iPad, iPhone HD, Resources without resolution On iPad : iPad, iPhone HD, Resources without resolution On iPhone HD: iPhone HD, Resources without resolution On Mac HD : Mac HD, Mac, Resources without resolution On Mac : Mac, Resources without resolution

By default this functionality is off;

Dictionary used to lookup filenames based on a key. It is used internally by the following methods:

-(NSString*) [fullPathForFilename:](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_file_utils/#af562999bf32f0c4d6257f70e97ea20d1)key resolutionType:(ccResolutionType*)resolutionType; -(NSString*) [fullPathForFilenameIgnoringResolutions:](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_file_utils/#af4b9f181ccb6e2e7789b62562af97f98)key;

It determines how the "resolution resources" are to be searched. Possible values:

Default: kCCFileUtilsSearchSuffix

Array of search paths. You can use this array to modify the search path of the resources. If you want to use "themes" or search resources in the "cache", you can do it easily by adding new entries in this array.

By default it is an array with only the "" (empty string) element.

Array that contains the search order of the resources based for the device. By default it will try to load resources in the following order until one is found:

If the property "enableiPhoneResourcesOniPad" is enabled, it will also search for iPhone resources if you are in an iPad.

Dictionary that contians the suffix for the different devices. Default values:

If "search with suffixes" is enabled (enabled by default), it will try to get the resources by appending the suffixes according to the order of "searchResolutionsOrder" array.