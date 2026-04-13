---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCLabelTTF.h>`


| id |
|

CCLabel is a subclass of CCTextureNode that knows how to render text labels

All features from CCTextureNode are valid in CCLabel

CCLabel objects are slow. Consider using [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_atlas/) or [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_label_b_m_font/) instead.

| id CCLabelTTF::initWithString:dimensions:alignment:fontName:fontSize: | ( | NSString * | string, |
| [dimensions] CGSize | dimensions, |
||
| [alignment] CCTextAlignment | alignment, |
||
| [fontName] NSString * | name, |
||
| [fontSize] CGFloat | size |
||
| ) | ` [virtual]` |

initializes the CCLabel with a font name, alignment, dimension in points and font size in points

| id CCLabelTTF::initWithString:dimensions:alignment:lineBreakMode:fontName:fontSize: | ( | NSString * | str, |
| [dimensions] CGSize | dimensions, |
||
| [alignment] CCTextAlignment | alignment, |
||
| [lineBreakMode] CCLineBreakMode | lineBreakMode, |
||
| [fontName] NSString * | name, |
||
| [fontSize] CGFloat | size |
||
| ) | ` [virtual]` |

initializes the CCLabel with a font name, alignment, dimension in points, line brea mode and font size in points. Supported lineBreakModes:

| id CCLabelTTF::initWithString:fontName:fontSize: | ( | NSString * | string, |
| [fontName] NSString * | name, |
||
| [fontSize] CGFloat | size |
||
| ) | ` [virtual]` |

initializes the CCLabel with a font name and font size in points

| id CCLabelTTF::labelWithString:dimensions:alignment:fontName:fontSize: | ( | NSString * | string, |
| [dimensions] CGSize | dimensions, |
||
| [alignment] CCTextAlignment | alignment, |
||
| [fontName] NSString * | name, |
||
| [fontSize] CGFloat | size |
||
| ) | ` [static, virtual]` |

creates a CCLabel from a fontname, alignment, dimension in points and font size in points

| id CCLabelTTF::labelWithString:dimensions:alignment:lineBreakMode:fontName:fontSize: | ( | NSString * | string, |
| [dimensions] CGSize | dimensions, |
||
| [alignment] CCTextAlignment | alignment, |
||
| [lineBreakMode] CCLineBreakMode | lineBreakMode, |
||
| [fontName] NSString * | name, |
||
| [fontSize] CGFloat | size |
||
| ) | ` [static, virtual]` |

creates a CCLabel from a fontname, alignment, dimension in points, line break mode, and font size in points. Supported lineBreakModes:

| id CCLabelTTF::labelWithString:fontName:fontSize: | ( | NSString * | string, |
| [fontName] NSString * | name, |
||
| [fontSize] CGFloat | size |
||
| ) | ` [static, virtual]` |

creates a CCLabel from a fontname and font size in points

| void CCLabelTTF::setString: | ( | NSString * | str | ) | ` [virtual]` |