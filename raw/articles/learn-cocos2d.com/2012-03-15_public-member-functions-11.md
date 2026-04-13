---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_c_c_node_07_kobold_extensions_08/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCNodeExtensions.h>`


| BOOL |
|

extends CCNode

| BOOL CCNode(KoboldExtensions)::containsPoint: | ( | CGPoint | point | ) | ` [virtual]` |

Returns true if the point is contained in (is on) the node. Respects rotation and scaling of the node.

| BOOL CCNode(KoboldExtensions)::containsTouch: | ( | UITouch * | touch | ) | ` [virtual]` |

Returns true if the UITouch is contained in (is on) the node. Respects rotation and scaling of the node.

| BOOL CCNode(KoboldExtensions)::intersectsNode: | ( | CCNode * | other | ) | ` [virtual]` |

Returns true if the node's boundingBox intersects with the boundingBox of another node.

| id CCNode(KoboldExtensions)::nodeWithScene | ( | ) | ` [static, virtual]` |

Calls the node's "node" method to initialize it, then adds it to a CCScene object and returns that CCScene. Useful as a convenience method for creating a CCLayer instance wrapped in a scene, so that you can write:

[[CCDirector sharedDirector] replaceScene:[MyGameLayer nodeWithScene]];

| void CCNode(KoboldExtensions)::transferToNode: | ( | CCNode * | targetNode | ) | ` [virtual]` |

This transfers the node (self) from its current parent node to a different node (new parent). This can be used to transfer a node from one scene to a new scene, for example. The node must already have a parent (ie it must have been added with addChild).

CGPoint CCNode(KoboldExtensions)::boundingBoxCenter` [read, assign]` |

Returns the center position of the node's bounding box.