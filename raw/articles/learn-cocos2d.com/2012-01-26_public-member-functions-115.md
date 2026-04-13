---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_b_m_font/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCLabelBMFont.h>`


| id |
|

[CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_b_m_font/) is a subclass of [CCSpriteBatchNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite_batch_node/)

Features:

Limitations:

[CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_b_m_font/) implements the protocol [CCLabelProtocol](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/protocol_c_c_label_protocol-p/), like CCLabel and [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_atlas/). [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_b_m_font/) has the flexibility of CCLabel, the speed of [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_atlas/) and all the features of [CCSprite](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_sprite/). If in doubt, use [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_b_m_font/) instead of [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_atlas/) / CCLabel.

Supported editors:

| void CCLabelBMFont::createFontChars | ( | ) | ` [virtual]` |

updates the font chars based on the string to render

| id CCLabelBMFont::initWithString:fntFile: | ( | NSString * | string, |
| [fntFile] NSString * | fntFile |
||
| ) | ` [virtual]` |

init a BMFont label with an initial string and the FNT file

| id CCLabelBMFont::labelWithString:fntFile: | ( | NSString * | string, |
| [fntFile] NSString * | fntFile |
||
| ) | ` [static, virtual]` |

creates a BMFont label with an initial string and the FNT file

| void CCLabelBMFont::purgeCachedData | ( | ) | ` [static, virtual]` |

Purges the cached data. Removes from memory the cached configurations and the atlas name dictionary.