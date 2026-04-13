---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_slider/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone-extensions
0.2
Cocos2D Extensions API Reference (iOS version) for www.kobold2d.com developers
|

| (id) | -
|

for Cocos2D. Designed with SFX/Music level options in mind.

| - (id) initWithBackgroundFile: | (NSString *) | bgFile |
|
| thumbFile: | (NSString *) | thumbFile |
|

Easy init - filenames instead of CCSprite & CCMenuItem. Uses designated init inside.

| thumbFile | Filename, that is used to create normal & selected images for thumbMenuItem. Selected sprite is darker than normal sprite. |
| bgFile | Filename for background CCSprite. |

| - (id) initWithBackgroundSprite: | (CCSprite *) | bgSprite |
|
| thumbMenuItem: | (CCMenuItem *) | aThumb |
|

Designated init.

| bgSprite | CCSprite, that is used as a background. It's bounding box is used to determine max & min x position for a thumb menu item. |
| aThumb | MenuItem that is used as a thumb. Used without CCMenu, so CCMenuItem::activate doesn't get called. |

| + (id) sliderWithBackgroundFile: | (NSString *) | bgFile |
|
| thumbFile: | (NSString *) | thumbFile |
|

| + (id) sliderWithBackgroundSprite: | (CCSprite *) | bgSprite |
|
| thumbMenuItem: | (CCMenuItem *) | aThumb |
|

Creates slider with given bg sprite and menu item as a thumb.