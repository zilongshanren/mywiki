---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_label_t_t_f/
published: '2012-07-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-mac
2.0
Improved Cocos2D API Reference (Mac OS X version) for www.kobold2d.com developers
|

`#import <CCLabelTTF.h>`


CCLabel is a subclass of CCTextureNode that knows how to render text labels

All features from CCTextureNode are valid in CCLabel

CCLabel objects are slow. Consider using [CCLabelAtlas](http://www.learn-cocos2d.com/) or [CCLabelBMFont](http://www.learn-cocos2d.com/) instead.

| - (id) initWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

initializes the [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_label_t_t_f/) with a font name, horizonal alignment, dimension in points, and font size in points. Default verticalAlignment: kCCVerticalTextAlignmentTop Default lineBreakMode: CCLineBreakModeWordWrap

| - (id) initWithString: | (NSString *) | str |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

initializes the [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_label_t_t_f/) with a font name, horizontal alignment, dimension in points, line break mode and font size in points. Default verticalAlignment: kCCVerticalTextAlignmentTop

Supported lineBreakModes:

| - (id) initWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

| - (id) initWithString: | (NSString *) | str |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

initializes the [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_label_t_t_f/) with a font name, horizontal alignment, vertical aligment, dimension in points, line break mode and font size in points. Supported lineBreakModes:

| - (id) initWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|

| + (id) labelWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_label_t_t_f/) from a fontname, horizontal alignment, dimension in points, and font size in points. Supported lineBreakModes:

| + (id) labelWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_label_t_t_f/) from a fontname, horizontal alignment, dimension in points, line break mode, and font size in points. Supported lineBreakModes:

| + (id) labelWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a CCLabel from a fontname, alignment, dimension in points and font size in points

| + (id) labelWithString: | (NSString *) | string |
|
| dimensions: | (CGSize) | dimensions |
|
| hAlignment: | (
|

creates a [CCLabelTTF](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone-mac/html/interface_c_c_label_t_t_f/) from a fontname, horizontal aligment, vertical alignment, dimension in points, line break mode, and font size in points. Supported lineBreakModes:

| + (id) labelWithString: | (NSString *) | string |
|
| fontName: | (NSString *) | name |
|
| fontSize: | (CGFloat) | size |
|

changes the string to render

Reimplemented from [<CCLabelProtocol>](http://www.learn-cocos2d.com/#a319778fa4130a457caaf5c5d08e7f420).

The vertical alignment of the label