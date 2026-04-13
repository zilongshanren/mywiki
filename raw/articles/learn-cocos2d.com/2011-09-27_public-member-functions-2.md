---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_drawing_visitor/
published: '2011-09-27'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3NodeVisitor.h>`


| void |
|

[CC3NodeDrawingVisitor](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_drawing_visitor/) is a [CC3NodeVisitor](http://www.learn-cocos2d.com/) that is passed to a node when it is visited during drawing operations.

This visitor extracts the camera's frustum from the encapsulated world, so that only nodes that are within the camera's field of view will be visited. Nodes outside the frustum will be culled and not drawn.

Draws the local content of the specified node.

Invoked by the node itself when the node's local content is to be drawn.

This implementation double-dispatches back to the node's drawLocalContentWithVisitor: method to perform the drawing. Subclass may override to enhance or modify this behaviour.

The frustum used to determine if a node is within the camera's view.

This is extracted from the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), set in the property by the open method, and cleared by the close method. It is therefore only available during a visitation run. Since the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) may contain multiple cameras, this ensures that the frustum of the current activeCamera is used.

BOOL CC3NodeDrawingVisitor::shouldDecorateNode` [read, write, assign]` |

Indicates whether nodes should decorate themselves with their configured material, textures, or color arrays.

In most cases, nodes should be drawn decorated. However, specialized visitors may turn off normal decoration drawing in order to do specialized coloring instead.

The default initial value is YES.

GLuint CC3NodeDrawingVisitor::textureUnit` [read, write, assign]` |

The current texture unit being drawn.

This value is set during drawing when the visitor is passed to the texture coordinates array.

GLuint CC3NodeDrawingVisitor::textureUnitCount` [read, write, assign]` |

The number of texture units being drawn.

This value is set by the texture contained in the node's material, and is then consumed by the mesh when binding texture coordinates.