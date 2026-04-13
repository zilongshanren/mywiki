---
title: b2DestructionListener Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_destruction_listener/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2WorldCallbacks.h](http://www.learn-cocos2d.com/box2d-api-reference/API/b2_world_callbacks_8h_source/)>

## Public Member Functions | |
| virtual |
|

Joints and fixtures are destroyed when their associated body is destroyed. Implement this listener so that you may nullify references to these joints and shapes.

| virtual b2DestructionListener::~b2DestructionListener | ( | ) | ` [inline, virtual]` |

Called when any fixture is about to be destroyed due to the destruction of its parent body.

Called when any joint is about to be destroyed due to the destruction of one of its attached bodies.