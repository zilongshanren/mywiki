---
title: Detailed Description
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_menu_item_sprite_independent/
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

doesn't add normal, selected and disabled images as children. Instead of that its just retain them. So you can place images anyhow you want.

[CCMenuItemSpriteIndependent](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_menu_item_sprite_independent/) reimplements rect and convertToNodeSpace: methods delegating them to normalSprite. This allows you to position/scale/rotate only normal sprite and forget about positioning menuItem.