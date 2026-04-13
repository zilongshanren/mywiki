---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_block_allocator/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Box2D
2.2
Box2D API Reference for www.kobold2d.com developers
|

`#include <b2BlockAllocator.h>`


| void * |
|

This is a small object allocator used for allocating small objects that persist for more than one time step. See: [http://www.codeproject.com/useritems/Small_Block_Allocator.asp](http://www.codeproject.com/useritems/Small_Block_Allocator.asp)

Allocate memory. This will use b2Alloc if the size is larger than b2_maxBlockSize.

Free memory. This will use b2Free if the size is larger than b2_maxBlockSize.