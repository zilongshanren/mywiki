---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/
published: '2013-01-09'
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

`#import <CCLabelTTF.h>`


| (id) | +
|

|

CCLabel is a subclass of CCTextureNode that knows how to render text labels

All features from CCTextureNode are valid in CCLabel

CCLabel objects are slow. Consider using [CCLabelAtlas](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_atlas/) or [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_b_m_font/) instead.

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

initializes the [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/) with a font name, horizontal alignment, dimension in points, and font size in points. Default verticalAlignment: kCCVerticalTextAlignmentTop Default lineBreakMode: CCLineBreakModeWordWrap

| - (id) initWithString: | (NSString *) | str |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

initializes the [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/) with a font name, horizontal alignment, dimension in points, line break mode and font size in points. Default verticalAlignment: kCCVerticalTextAlignmentTop

Supported lineBreakModes:

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

| - (id) initWithString: | (NSString *) | str |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

initializes the [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/) with a font name, horizontal alignment, vertical alignment, dimension in points, line break mode and font size in points. Supported lineBreakModes:

| + (id) labelWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|

| + (id) labelWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/) from a fontname, horizontal alignment, dimension in points, and font size in points. Supported lineBreakModes:

| + (id) labelWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/) from a fontname, horizontal alignment, dimension in points, line break mode, and font size in points. Supported lineBreakModes:

| + (id) labelWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a CCLabel from a fontname, alignment, dimension in points and font size in points

| + (id) labelWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_label_t_t_f/) from a fontname, horizontal alignment, vertical alignment, dimension in points, line break mode, and font size in points. Supported lineBreakModes:

| - (void) setString: | (NSString *) | str |

changes the string to render

Reimplemented from [<CCLabelProtocol>](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/protocol_c_c_label_protocol-p/#a319778fa4130a457caaf5c5d08e7f420).

|
readwritenonatomicassign |

Dimensions of the label in Points

|
readwritenonatomicretain |

Font name used in the label

|
readwritenonatomicassign |

Font size of the label

The vertical alignment of the label