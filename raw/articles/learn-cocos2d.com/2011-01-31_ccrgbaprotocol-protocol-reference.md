---
title: <CCRGBAProtocol> Protocol Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_r_g_b_a_protocol-p/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

CC RGBA protocol.
[More...](http://www.learn-cocos2d.com#_details)

`#import "`

[CCProtocols.h](http://www.learn-cocos2d.com/)"

Inherited by [CCAtlasNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_atlas_node/), [CCLabelBMFont](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_label_b_m_font/), [CCLayerColor](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer_color/), [CCMenu](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu/), [CCMenuItemLabel](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_label/), [CCMenuItemSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_sprite/), [CCMenuItemToggle](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item_toggle/), and [CCSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite/).

| (
|

CC RGBA protocol.

| - (BOOL) doesOpacityModifyRGB | ` [optional]` |

returns whether or not the opacity will be applied using glColor(R,G,B,opacity) or glColor(opacity, opacity, opacity, opacity);

| - (GLubyte) opacity |

returns the opacity

| - (void) setOpacity: | (GLubyte) | opacity |

sets the opacity.

| - (void) setOpacityModifyRGB: | (BOOL) | boolean |
` [optional]` |

sets the premultipliedAlphaOpacity property. If set to NO then opacity will be applied as: glColor(R,G,B,opacity); If set to YES then oapcity will be applied as: glColor(opacity, opacity, opacity, opacity ); Textures with premultiplied alpha will have this property by default on YES. Otherwise the default value is NO