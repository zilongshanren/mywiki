---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3TextureUnit.h>`


| void |
|

[CC3TextureUnit](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/) is used by [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/) to configure the GL texture unit to which the texture is being applied.

Notably, the texture unit defines how the texture is to be combined with textures from other texture units in a multi-texture layout.

With multi-texturing, several textures can be overlaid and combined in interesting ways onto a single material. Each texture is processed by a GL texture unit, and is combined with the textures already processed by other texture units. The source and type of combining operation can be individually configured by subclasses of this class. Support for bump-mapping as one of these combining configurations is explicitly provided by the [CC3BumpMapTextureUnit](http://www.learn-cocos2d.com/) subclass.

[CC3TextureUnit](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/) is the default abstract parent class, and configures the texture to combine with other textures using the default GL_MODULATE combiner function, which is the same default functionality provided by a [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/) that does not contain any texture unit instance. As a result, there is never any need to use a concrete instance of this class, since assigning an instance of this class to a texture is the same as leaving the texture with no texture unit configuration at all.

Subclasses will modify this default capability by providing additional customization capabilities.

Automatically invoked from [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/) when no texture unit configuration is provided in that texture.

In the GL engine, sets the combining function to the default value of GL_MODULATE, and the texture constant color to the default value of kCCC4FBlackTransparent.

| void CC3TextureUnit::bindTo:withVisitor: | ( |
|

` [virtual]`

Template method that binds the configuration of this texture unit to the specified GL texture unit.

This implementation simply sets the combining function to the default value of GL_MODULATE, and sets the texture constant color to that of the constantColor property. This is the same functionality provided by the unbindFrom: method when no texture unit configuration is present. Subclasses will override to provide more interesting combining techniques.

The visitor provides additional configuration information that can be used by subclass overrides of this method.

| id CC3TextureUnit::textureUnit | ( | ) | ` [static, virtual]` |

Allocates and initializes an autoreleased instance.

ccColor3B CC3TextureUnit::color` [read, write, assign]` |

Implementation of the CCRGBAProtocol color property.

Querying this property returns the RGB components of the constantColor property, converted from the floating point range (0 to 1), to the byte range (0 to 255).

When setting this property, the RGB values are each converted to a floating point number between 0 and 1, and are set into the constantColor property. The alpha component of constantColor remains unchanged.

ccColor4F CC3TextureUnit::constantColor` [read, write, assign]` |

The constant color of the texture unit.

This will be used by the combiner when the value of one of the source properties of a subclass is set to GL_CONSTANT. This is often the case for bump-mapping configurations.

Although this property can be set directly, it is rare to do so. Usually, this property is set indirectly via the lightDirection property, which converts the XYZ coordinates of a lighting direction vector into the RGB components of this property.

This property is not used by this parent class implementation, but is provided for common access by subclasses.

The initial value of this property is kCCC4FBlackTransparent.

BOOL CC3TextureUnit::isBumpMap` [read, assign]` |

Returns whether this texture unit is configured as a bump-map.

This implementation always returns NO. Subclasses that support bump-mapping will override this default implementation.

Implemented in [CC3BumpMapTextureUnit](http://www.learn-cocos2d.com/#a1dabe37724632ce7ea82670f12e613a7), and [CC3ConfigurableTextureUnit](http://www.learn-cocos2d.com/#a9d2326f6b783cd6ef587efffc05fbb6c).

The direction, in local tangent coordinates, of the light source that is to interact with subclasses that are configured as bump-maps (aka normal maps).

Bump-maps are textures that store a normal vector (XYZ coordinates) in the RGB components of each texture pixel, instead of color information. These per-pixel normals interact with the value of this lightDirection property (through a dot-product), to determine the luminance of the pixel.

Setting this property changes the value of the constantColor property. The lightDirection vector is normalized and shifted from the range of +/- 1.0 to the range 0.0-1.0. Then each XYZ component in the vector is mapped to the RGB components of the constantColor using the rgbNormalMap property.

Reading this value reads the value from the constantColor property. The RGB components of the color are mapped to the XYZ components of the direction vector using the rgbNormalMap property, and then shifted from the color component range 0.0-1.0 to the directional vector range +/- 1.0.

The value of this property must be in the tangent-space coordinates associated with the texture UV space, in practice, this property is typically not set directly. Instead, you can use the globalLightLocation property of the mesh node that is making use of this texture and texture unit.

GLubyte CC3TextureUnit::opacity` [read, write, assign]` |

Implementation of the CCRGBAProtocol opacity property.

Querying this property returns the alpha component of the constantColor property, converted from the floating point range (0 to 1), to the byte range (0 to 255).

When setting this property, the value is converted to a floating point number between 0 and 1, and is set into the constantColor property. The RGB components of constantColor remain unchanged.

When a subclass is configured as a bump-map, this property indicates how the XYZ coordinates of each per-pixel normal are stored in the RGB values of each pixel.

The texture has three slots (R, G & B) in which to store three normal coordinate components (X, Y & Z). This can be done in any of six ways, as indicated by the values of the CC3DOT3RGB enumeration.

The initial value of this property is kCC3DOT3RGB_XYZ, indicating that the X, Y & Z components of the bump-map normals will be stored in the R, G & B coordinates of the texture pixels, respectively.