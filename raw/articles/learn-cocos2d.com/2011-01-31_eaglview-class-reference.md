---
title: EAGLView Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`[EAGLView.h](/)"


[List of all members.](/)


## Detailed Description

[EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) Class. This class wraps the CAEAGLLayer from CoreAnimation into a convenient UIView subclass. The view content is basically an EAGL surface you render your OpenGL scene into. Note that setting the view non-opaque will only work if the EAGL surface has an alpha channel.


## Member Function Documentation

| - (id) initWithFrame: |
|
(CGRect) |
*frame* |
|
|

Initializes an [EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) with a frame and 0-bit depth buffer, and a RGB565 color buffer

| - (id) initWithFrame: |
|
(CGRect) |
*frame* |
| pixelFormat: |
|
(NSString *) |
*format* | |
|
|
| | |

Initializes an [EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) with a frame, a color buffer format, and 0-bit depth buffer

| - (id) initWithFrame: |
|
(CGRect) |
*frame* |
| pixelFormat: |
|
(NSString *) |
*format* |
| depthFormat: |
|
(GLuint) |
*depth* |
| preserveBackbuffer: |
|
(BOOL) |
*retained* |
| sharegroup: |
|
(EAGLSharegroup *) |
*sharegroup* |
| multiSampling: |
|
(BOOL) |
*sampling* |
| numberOfSamples: |
|
(unsigned int) |
*nSamples* | |
|
|
| | |

Initializes an [EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) with a frame, a color buffer format, a depth buffer format, a sharegroup and multisampling support

[EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) uses double-buffer. This method swaps the buffers

| + (id) viewWithFrame: |
|
(CGRect) |
*frame* |
|
|

creates an initializes an [EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) with a frame and 0-bit depth buffer, and a RGB565 color buffer.

| + (id) viewWithFrame: |
|
(CGRect) |
*frame* |
| pixelFormat: |
|
(NSString *) |
*format* | |
|
|
| | |

creates an initializes an [EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) with a frame, a color buffer format, and 0-bit depth buffer.

| + (id) viewWithFrame: |
|
(CGRect) |
*frame* |
| pixelFormat: |
|
(NSString *) |
*format* |
| depthFormat: |
|
(GLuint) |
*depth* | |
|
|
| | |

creates an initializes an [EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) with a frame, a color buffer format, and a depth buffer.

| + (id) viewWithFrame: |
|
(CGRect) |
*frame* |
| pixelFormat: |
|
(NSString *) |
*format* |
| depthFormat: |
|
(GLuint) |
*depth* |
| preserveBackbuffer: |
|
(BOOL) |
*retained* |
| sharegroup: |
|
(EAGLSharegroup *) |
*sharegroup* |
| multiSampling: |
|
(BOOL) |
*multisampling* |
| numberOfSamples: |
|
(unsigned int) |
*samples* | |
|
|
| | |

creates an initializes an [EAGLView](../../../unofficial-cocos2d-api-reference/html/interface_e_a_g_l_view/) with a frame, a color buffer format, a depth buffer format, a sharegroup, and multisamping


## Property Documentation

- (EAGLContext*) context` [read, assign]` |

- (GLuint) depthFormat` [read, assign]` |

depth format of the render buffer: 0, 16 or 24 bits

- (NSString*) pixelFormat` [read, assign]` |

pixel format: it could be RGBA8 (32-bit) or RGB565 (16-bit)

- (CGSize) surfaceSize` [read, assign]` |

returns surface size in pixels

- (id<EAGLTouchDelegate>) touchDelegate` [read, write, assign]` |


The documentation for this class was generated from the following file:

- /depot/cocosdocs/cocos2d-iphone-0.99.5/cocos2d/Platforms/iOS/
[EAGLView.h](/)