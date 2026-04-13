---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_grid_base/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCGrid.h>`




|
(id) | - **initWithSize:texture:flippedTexture:** |
| |
(id) | - **initWithSize:** |
| |
(void) | - **beforeDraw** |
| |
(void) | - **afterDraw:** |
| |
(void) | - **blit** |
| |
(void) | - **reuse** |
| |
(void) | - **calculateVertexPoints** |
| |

|
(id) | + **gridWithSize:texture:flippedTexture:** |
| |
(id) | + **gridWithSize:** |
| |

|
BOOL | **_active** |
| |
int | **_reuseGrid** |
| |
CGSize | **_gridSize** |
| |
[CCTexture2D](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_texture2_d/) * | **_texture** |
| |
CGPoint | **_step** |
| |
[CCGrabber](/) * | **_grabber** |
| |
BOOL | **_isTextureFlipped** |
| |
[CCGLProgram](../../../../../../api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_g_l_program/) * | **_shaderProgram** |
| |
ccDirectorProjection | **_directorProjection** |
| |

whether or not the grid is active

| - (BOOL) isTextureFlipped |
|
readwritenonatomicassign |

number of times that the grid will be reused


The documentation for this class was generated from the following file: