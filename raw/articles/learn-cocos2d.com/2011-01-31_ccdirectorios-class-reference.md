---
title: CCDirectorIOS Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCDirectorIOS.h](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/_c_c_director_i_o_s_8h_source/)"

Inherits [CCDirector](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director/).

Inherited by [CCDirectorDisplayLink](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_display_link/), [CCDirectorFast](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_fast/), [CCDirectorFastThreaded](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_fast_threaded/), and [CCDirectorTimer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_timer/).

| (BOOL) | -
|

[CCDirectorIOS](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/): Base class of iOS directors

| - (BOOL) attachInView: | (UIView *) | DEPRECATED_ATTRIBUTE |

| - (BOOL) attachInView: | (UIView *) | view |
||
| withFrame: | (CGRect) | DEPRECATED_ATTRIBUTE | ||

| - (BOOL) attachInWindow: | (UIWindow *) | DEPRECATED_ATTRIBUTE |

| - (BOOL) DEPRECATED_ATTRIBUTE |

detach the cocos2d view from the view/window

| - (void) setDepthBufferFormat: | (tDepthBufferFormat) | DEPRECATED_ATTRIBUTE |

Change depth buffer format of the render buffer. Call this class method before attaching it to a UIWindow/UIView Default depth buffer: 0 (none). Supported: kCCDepthBufferNone, kCCDepthBuffer16, and kCCDepthBuffer24

| - (void) setPixelFormat: | (tPixelFormat) | DEPRECATED_ATTRIBUTE |

Uses a new pixel format for the [EAGLView](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/). Call this class method before attaching it to a UIView Default pixel format: kRGB565. Supported pixel formats: kRGBA8 and kRGB565

- (tPixelFormat pixelFormat) DEPRECATED_ATTRIBUTE` [read, assign]` |

Pixel format used to create the context