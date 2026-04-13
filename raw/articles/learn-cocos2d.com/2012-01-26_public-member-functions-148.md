---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3Billboard.h>`


| void |
|

This [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) displays a 2D cocos2d CCNode as part of the 3D world.

The 2D node can be displayed in one of two ways, as determined by the value of the shouldDrawAs2DOverlay property:

CC3Billboards are useful for drawing a label, health-bar, speech-balloon, or some other 2D artifact in or on the 3D world, and have that 2D artifact move along with this node as it moves through the 3D world.

[CC3Billboard](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) is a type of [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), and can therefore participate in a structural node assembly. An instance can be the child of another node, and the [CC3Billboard](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) itself can have child nodes.

The size of the 2D node will be automatically scaled based on the distance between the 3D billboard node and the 3D camera to keep the 2D artifact at the correct perspective as this node moves toward or away from the camera.

The perspective sizing of the 2D node can be influenced by two properties: minimumBillboardScale and maximumBillboardScale, which can define a minimum and maximum limits to which the node will be sized, respectively, relative to a nominal size. This capability is useful when the 2D node is a label, health-bar, or speech-balloon, and it is desirable to keep the text at a readable size, regardless of how near or far the node moves in the 3D world, relative to the camera.

Since the scale of the 2D billboard is often automatically adjusted, you should be careful when setting the scale property of the 2D billboard. In particular, when the 2D node is embedded in the 3D world, (the shouldDrawAs2DOverlay property is set to the default NO), the scale property of the 2D node will be directly manipulated if the value of the shouldNormalizeScaleToDevice property on this [CC3Billboard](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) is set to YES, and any value you set for the 2D node scale property will be ignored.

As with all CC3Nodes, CC3Billboards support the protocol CCRGBAProtocol. When wrapping a 2D CCNode billboard that also supports CCRGBAProtocol, changes to the [CC3Billboard](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) color and opacity properties will change those same properties in the encapsulated 2D CCNode billboard. When reading the color and opacity properties of the [CC3Billboard](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/), the value returned will be that of the 2D CCNode.

A [CC3Billboard](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) can, and should, have a bounding volume, but the bounding volume must be an instance of a subclass of [CC3NodeBoundingArea](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_bounding_area/), which maps the 2D boundary of the 2D node into the 3D world, and when shouldDrawAs2DOverlay is YES, handles testing the 2D bounds of the 2D node against the bounds of the 2D drawing plane.

Invoked automatically by the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) to configure the 2D node relative to the location of the camera, including ensuring the correct perspective.

If the value of the shouldDrawAs2DOverlay property is NO, the 2D node is embedded in the 3D world. As such, the 2D node will naturally be drawn with the correct perspective projection, but invoking this method enforces the sizing restrictions specified in the minimumBillboardScale and maximumBillboardScale properties.

If the value of the shouldDrawAs2DOverlay property is YES, the 2D node is overlaid on the 3D world at a 2D position determined by projecting the location of the node onto the camera view. This position is cached in the projectedPosition property of this node.

In addition, with the shouldDrawAs2DOverlay property set to YES, since the 2D node is drawn over the whole 3D world, As such, the 2D node will not have natural perspective projection. To mimic perspetive sizing, this method scales the 2D node according to the distance between this node and the camera, relative to a scale of one at the unityScaleDistance, taking into consideration the sizing restrictions specified in the minimumBillboardScale and maximumBillboardScale properties.

This method is invoked automatically by [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/). Usually, the application never needs to invoke this method directly.

| GLfloat CC3Billboard::deviceScaleFactor | ( | ) | ` [static, virtual]` |

The scaling factor used to adjust the scale of the 2D overlay node so that it's size relative to the 3D artifacts appears consistent across all device screen resolutions, if the shouldNormalizeScaleToDevice property is set to YES.

The value returned depends on the device screen window size and is normalized to the original iPhone/iPod Touch screen size of 480 x 320. The value returned for an original iPhone or iPod Touch will be 1.0. The value returned for other devices depends on the screen resolution, and formally, on the screen height as measured in pixels. Devices with larger screen heights in pixels will return a value greater than 1.0. Devices with smaller screen heights in pixels will return a value less than 1.0

| BOOL CC3Billboard::doesIntersectBounds: | ( | CGRect | bounds | ) | ` [virtual]` |

Returns whether the local content of this node intersects the given bounding rectangle.

This check does not include checking children, only the local content.

If the value of the shouldDrawAs2DOverlay property is YES, this method is invoked during the drawing operations of each frame to determine whether this node should be culled from the visible nodes and not drawn. A return value of YES will cause the node to be drawn, a return value of NO will cause the node to be culled and not drawn.

Culling nodes that are not visible to the camera is an important performance enhancement. The node should strive to be as accurate as possible in returning whether it intersects the viewport. Incorrectly returning YES will cause wasted processing within the GL engine. Incorrectly returning NO will cause a node that should at least be partially visible to not be drawn.

In this implementation, if this node has a boundingVolume, this method delegates to it. Otherwise, it simply returns YES. Subclasses may override to change this standard behaviour.

The boundingVolume of a [CC3Billboard](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_billboard/) must be an instance of a subclass of [CC3NodeBoundingArea](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_bounding_area/).

| void CC3Billboard::draw2dWithinBounds: | ( | CGRect | bounds | ) | ` [virtual]` |

If the value of the shouldDrawAs2DOverlay property is YES, and the 2D node is within the given bounds, draws the 2D node at the projected 2D position calculated in the alignToCamera: method.

This method is invoked automatically by [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) at the end of each frame drawing cycle. Usually, the application never needs to invoke this method directly.

| id CC3Billboard::initWithBillboard: | ( | CCNode * | a2DNode | ) | ` [virtual]` |

Initializes this unnamed instance with an automatically generated unique tag value, and the specified 2D node to be drawn.

| id CC3Billboard::initWithName:withBillboard: | ( | NSString * | aName, |
| [withBillboard] CCNode * | a2DNode |
||
| ) | ` [virtual]` |

Initializes this instance with an automatically generated unique tag value, and the specified name and 2D node to be drawn.

| id CC3Billboard::initWithTag:withName:withBillboard: | ( | GLuint | aTag, |
| [withName] NSString * | aName, |
||
| [withBillboard] CCNode * | a2DNode |
||
| ) | ` [virtual]` |

Initializes this instance with the specified tag, name and 2D node to be drawn.

| id CC3Billboard::nodeWithBillboard: | ( | CCNode * | a2DNode | ) | ` [static, virtual]` |

Allocates and initializes an autoreleased unnamed instance with an automatically generated unique tag value, and the specified 2D node to be drawn.

| id CC3Billboard::nodeWithName:withBillboard: | ( | NSString * | aName, |
| [withBillboard] CCNode * | a2DNode |
||
| ) | ` [static, virtual]` |

Allocates and initializes an autoreleased instance with an automatically generated unique tag value, and the specified name and 2D node to be drawn.

| void CC3Billboard::resetBillboardBoundingRect | ( | ) | ` [virtual]` |

Resets the value of the billboardBoundingRect property so that it will be measured again from the 2D node the next time the billboardBoundingRect is accessed.

You can use this method after you change the 2D node is a way that changes its boundary, to force the bounding rectangle of the 2D node to be re-measured and re-cached. An example might be when you change the text of a 2D label, which will change the boundary of the label.

CCNode * CC3Billboard::billboard` [read, write, retain]` |

The 2D artifact that this node will display.

This can be any CCNode subclass.

CGRect CC3Billboard::billboardBoundingRect` [read, write, assign]` |

The rectangle, in pixels, bounding the 2D CCNode, in the local coordinate system of the 2D node.

This property is used by cocos3d when each frame is drawn, to test whether this node is within the field of view of the camera and should be drawn. It is accessed on each rendering frame. The value of this property is also used when picking nodes from touch events.

The value of this property can be set directly, or it can be measured automatically from the size of the 2D node when accesssed as follows:

The choice of how to use this property depends on the type of 2D node being held. If the value of the shouldDrawAs2DOverlay property is set to NO (the default), the 2D node is embedded in the 3D world, and the following applies:

If the shouldDrawAs2DOverlay property is set to YES, the 2D node will be drawn as a 2D overlay, and the value of this property will be measured from the 2D node each time this property is accessed. This is because the boundary of the 2D overlay node changes dynamically as either the node or the camera is moved.

The initial value of this property is CGRectNull. If this node contains a 2D node, the value returned will be measured from the 2D node the first time this property is accessed, and cached for future access. If this node does not contain a 2D node, this property will simply return the CGRectNull value.

CGPoint CC3Billboard::maximumBillboardScale` [read, write, assign]` |

The maximum scale to which the 2D node will be allowed to grow as it approaches the camera.

Setting this property to a non-zero value will stop the 2D node from growing too large as the 3D object approaches the camera. For example, you may want to keep a name label or speech-balloon at a readable text size, even if the character it is attached to is right in front of the camera.

The value of this property is relative to the unityScaleDistance. The 2D node will not grow to a size larger than its size at the unity distance multiplied by the value of this property. For example, if this property is set to 2.0, the 2D node will not grow to more than twice the size it appears when at the unityScaleDistance.

If this property is zero, no maximum will be applied. If this property is non-zero and is equal to the minimumBillboardScale, the 2D node will always be displayed at that single scale, regardless of how near or far this node is from the camera.

It is possible to specify different scales for each of the X and Y dimensions, if such behaviour makes sense.

CGPoint CC3Billboard::minimumBillboardScale` [read, write, assign]` |

The minimum scale to which the 2D node will be allowed to shrink as it moves away from the camera.

Setting this property to a non-zero value will stop the 2D node from shrinking away to nothing as the 3D object recedes far from the camera. For example, you may want to keep a name label or speech-balloon readable, even if the character it is attached to is far from the camera.

The value of this property is relative to the unityScaleDistance. The 2D node will not shrink to a size smaller than its size at the unity distance multiplied by the value of this property. For example, if this property is set to 0.5, the 2D node will not shrink to less than one-half the size it appears when at the unityScaleDistance.

If this property is zero, no minimum will be applied. If this property is non-zero and is equal to the maximumBillboardScale, the 2D node will always be displayed at that single scale, regardless of how near or far this node is from the camera.

It is possible to specify different scales for each of the X and Y dimensions, if such behaviour makes sense.

CGPoint CC3Billboard::offsetPosition` [read, write, assign]` |

An offset, measured in 2D display points, at which the 2D node should be positioned relative to the 2D projectedPosition of this node.

The initial value is {0, 0}. This property can be useful in helping to center or positionally justify the 2D artifact.

This property only has effect when the shouldDrawAs2DOverlay property is set to YES, indicating that the 2D node is being drawn as a 2D overlay to the 3D world.

BOOL CC3Billboard::shouldAlwaysMeasureBillboardBoundingRect` [read, write, assign]` |

Indicates whether the value of the billboardBoundingRect property should be measured from the 2D node each time the billboardBoundingRect property is accessed.

If the values of this property and the shouldMaximizeBillboardBoundingRect property are both set to NO, the boundary of the 2D node will only be measured the first time the billboardBoundingRect is accessed.

You can set this property to YES for dynamic 2D nodes whose boundary changes frequently or unpredicatably.

You should exercise caution in deciding to set this property to YES. The billboardBoundingRect property is accessed at least once per rendering frame during node culling, and the cost of re-measuring the boundary of some types of 2D nodes can be quite high. In particular, measuring the boundary of a particle system involves iterating though every particle vertex.

For 2D nodes whose boundary is expensive to measure, consider leaving this property set to NO, and either pre-calculating the maximum value of the billboardBoundingRect, and setting it explicitly, or using the resetBillboardBoundingRect method to measure the boundary of the 2D node only when necessary.

The initial value of this property is NO.

BOOL CC3Billboard::shouldDrawAs2DOverlay` [read, write, assign]` |

Indicates whether this instance should be drawn in 2D as an overlay on top of the 3D world, or embedded into the 3D world.

When set to NO, the 2D CCNode will be drawn at the Z-depth of this node, and will be occluded if other 3D nodes are between this node and the camera. And, like other 3D nodes, it can be rotated in 3D to face away from the camera, and can be selected by touch events.

When set to YES, the 2D CCNode will be drawn after the 3D world has completed drawing, and the GL engine has reverted to 2D rendering. The 2D node will ignore 3D depth testing, and will be drawn on top of all 3D nodes, even if there are other 3D nodes between this node and the camera. The CCNode will always appear to face directly towards the camera, and cannot be selected by touch events.

The initial value of this property is NO, indicating that the 2D node will be embedded into the 3D world.

In most cases, you will simply want to leave this property with the default NO value. However, there are some cases where you want the 2D node to truly be displayed on top of the whole 3D world. An example might be an identifier label or speech-balloon attached to a character in the game. You might want to display the label or speech-balloon even when the character is not visible becuase it is behind another object, or inside a building. You can attach this node to the character node and set the value of this property to YES. The label or speech- balloon will then move around as the character moves, but will remain visible even if the character moves behind another object in the scene.

BOOL CC3Billboard::shouldMaximizeBillboardBoundingRect` [read, write, assign]` |

If the value of this property is set to YES, the boundary of the 2D node will be measured each time the billboardBoundingRect property is accessed, and the resulting value will be accumulated in the billboardBoundingRect property so that the resulting value of the billboardBoundingRect property will be an ever-growing rectangle that covers all areas covered by the 2D node since initialization of this node, or since the resetBillboardBoundingRect method was last invoked.

If the values of this property and the shouldAlwaysMeasureBillboardBoundingRect property are both set to NO, the boundary of the 2D node will only be measured the first time the billboardBoundingRect is accessed.

This property can be useful when pre-computing an appropriate fixed boundary for a dynamic 2D node such as a particle system, and is often used at development time. The resulting accumulated boundary can then be explicitly set into the billboardBoundingRect property (with both this property and the shouldAlwaysMeasureBillboardBoundingRect property set to NO) so that the cost of measuring the 2D boundary is not incurred during each rendering frame at runtime.

If a truly dynamic boundary is required at runtime, there is no advantage to using this property instead of the shouldAlwaysMeasureBillboardBoundingRect property. The performance cost is the same, and the resulting boundary will be less accurate.

The initial value of this property is NO.

BOOL CC3Billboard::shouldNormalizeScaleToDevice` [read, write, assign]` |

Indicates whether the size of the 2D billboard node should be adjusted so that its size relative to the 3D artifacts appears to be the same across all devices.

The 3D camera frustum is consistent across all devices, making the view of the 3D scene consistent across all devices. The result is that on devices with larger screen resolutions, the 2D overlay node will be drawn across more pixels, and may appear visually larger.

If this property is set to YES, the scale of the 2D overlay node will be adjusted so that it appears to be the same size across all devices, relative to the 3D nodes.

If this property is set to NO, the 2D overlay node will be drawn in the same absolute pixel size across all devices, which may make it appear to be smaller or larger, relative to the 3D artifacts around it, on different devices.

This property has different effects, depending on the value of the shouldDrawAs2DOverlay property. If that property is set to YES, and the 2D node is being drawn as an overlay over the entire 3D scene, all 2D nodes will be adjusted.

However, if the shouldDrawAs2DOverlay property is set to NO, indicating that the 2D node is embedded in the 3D world, the 2D node will be scaled by the value of the billboardContentScaleFactor property of the 2D node. Most 2D nodes do not require scaling adjustment when being drawn embedded in the 3D world and will return 1.0 for this property. However, some 2D nodes, such as text labels and particle systems actively compensate for the screen resolution when drawing to a retina screen, and do need to be adjusted.

The initial value of this property is YES.

GLuint CC3Billboard::textureUnitIndex` [read, write, assign]` |

The index of the GL texture unit to use when drawing the 2D CCNode.

The initial value of this property is zero. cocos2d uses texture unit zero by default, and in most cases it is recommended that you use this initial value.

The value of this property must be between zero and one less than the maximum number of supported texture units. The maximum number of texture units is platform dependent, and can be read from [[CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) engine].platform.maxTextureUnits.value.

GLfloat CC3Billboard::unityScaleDistance` [read, write, assign]` |

The distance from the camera, in 3D space, at which the 2D artifact will be displayed at unity scale (its natural size).

This effect this property has depends on the value of the shouldDrawAs2DOverlay property.

If the value of the shouldDrawAs2DOverlay property is NO, the 2D node is embedded in the 3D world. As such, like all other nodes, the size of the 2D node automatically changes as this node moves closer to or farther away from the camera. As such, this property has no effect on the size of the 2D node, and is used only as a reference when calculating the effect of the minimumBillboardScale and maximumBillboardScale properties.

If the value of the shouldDrawAs2DOverlay property is YES, the 2D node is overlaid on the 3D world. As such, if this node is closer to the camera than the distance value of this property, the 2D artifact will be scaled up proportionally. If this node is farther from the camera than this distance, the 2D artifact will be scaled down proportionally.

If the value of this property is zero, the camera's near clip plane distance will be used as the unity scale distance.

The initial value of this property is zero.