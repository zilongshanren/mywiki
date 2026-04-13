---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3Texture.h>`


| void |
|

Each instance of [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/) wraps a cocos2d CCTexture2D instance, and manages applying that texture to the GL engine.

In most cases, a material will hold a single instance of [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/) in the texture property to provide a simple single-texture surface. This is the most common application of textures to a material.

For more sophisticated surfaces, materials also support multi-texturing, where more than one instance of [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/) is added to the material. With multi-texturing, several textures can be combined in flexible, customized fashion, permitting sophisticated surface effects.

With OpenGL, multi-texturing is processed by a chain of texture units. The material's first texture is processed by the first texture unit (texture unit zero), and subsequent textures held in the material are processed by subsequent texture units, in the order in which the textures were added to the material.

Each texture unit combines its texture with the output of the previous texture unit in the chain. Combining textures is quite flexible under OpenGL, and there are many ways that each texture can be combined with the output of the previous texture unit. The way that a particular texture combines with the previous textures is defined by an instance of [CC3TextureUnit](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/), held in the textureUnit property of each texture that was added to the material.

For example, to configure a material for bump-mapping, add a texture that contains a normal vector at each pixel instead of a color, and set the textureUnit property of the texture to a [CC3BumpMapTextureUnit](http://www.learn-cocos2d.com/). Then add another texture, containing the image that will be visible, to the material. The material will combine these two textures, as specified by the [CC3TextureUnit](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/) held by the second texture.

If the texture property is not nil, draws the texture to the GL engine as follows:

| id CC3Texture::initFromFile: | ( | NSString * | aFilePath | ) | ` [virtual]` |

Initializes this unnamed instance with an automatically generated unique tag value.

The tag value will be generated automatically via the method nextTag. The texture file from the specified path will be loaded into the texture property.

| id CC3Texture::initWithName:fromFile: | ( | NSString * | aName, |
| [fromFile] NSString * | aFilePath |
||
| ) | ` [virtual]` |

Initializes this instance with the specified name and an automatically generated unique tag value.

The tag value will be generated automatically via the method nextTag. The texture file from the specified path will be loaded into the texture property.

| id CC3Texture::initWithTag:fromFile: | ( | GLuint | aTag, |
| [fromFile] NSString * | aFilePath |
||
| ) | ` [virtual]` |

Initializes this unnamed instance with the specified tag.

The texture file from the specified path will be loaded into the texture property.

| id CC3Texture::initWithTag:withName:fromFile: | ( | GLuint | aTag, |
| [withName] NSString * | aName, |
||
| [fromFile] NSString * | aFilePath |
||
| ) | ` [virtual]` |

Initializes this instance with the specified tag and name.

The texture file from the specified path will be loaded into the texture property.

| BOOL CC3Texture::loadTextureFile: | ( | NSString * | aFilePath | ) | ` [virtual]` |

Loads the specified texture file into the texture property, and returns whether the loading was successful.

| id CC3Texture::textureFromFile: | ( | NSString * | aFilePath | ) | ` [static, virtual]` |

Allocates and initializes an autoreleased unnamed instance with an automatically generated unique tag value.

The tag value is generated using a call to nextTag. The texture file from the specified path will be loaded into the texture property.

| id CC3Texture::textureWithName:fromFile: | ( | NSString * | aName, |
| [fromFile] NSString * | aFilePath |
||
| ) | ` [static, virtual]` |

Allocates and initializes an autoreleased instance with the specified name and an automatically generated unique tag value.

The tag value is generated using a call to nextTag. The texture file from the specified path will be loaded into the texture property.

| id CC3Texture::textureWithTag:fromFile: | ( | GLuint | aTag, |
| [fromFile] NSString * | aFilePath |
||
| ) | ` [static, virtual]` |

Allocates and initializes an unnamed autoreleased instance with the specified tag.

The texture file from the specified path will be loaded into the texture property.

| id CC3Texture::textureWithTag:withName:fromFile: | ( | GLuint | aTag, |
| [withName] NSString * | aName, |
||
| [fromFile] NSString * | aFilePath |
||
| ) | ` [static, virtual]` |

Allocates and initializes an autoreleased instance with the specified tag and name.

The texture file from the specified path will be loaded into the texture property.

| void CC3Texture::unbind | ( | ) | ` [static, virtual]` |

Disables all texture units in the GL engine.

| void CC3Texture::unbind: | ( | GLuint | texUnit | ) | ` [static, virtual]` |

Disables the specified texture unit in the GL engine.

The texture unit value should be a number between zero and the maximum number of texture units, which can be read from [[CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) engine].platform.maxTextureUnits.value.

| void CC3Texture::unbindRemainingFrom: | ( | GLuint | textureUnit | ) | ` [static, virtual]` |

Disables all texture units between the specified texture unit index and the number of texture units that are in use in this application.

This method is automatically invoked by the material to disable all texture units that are not used by the texture or textures contained within the material.

BOOL CC3Texture::hasPremultipliedAlpha` [read, assign]` |

Indicates whether the RGB components of each pixel of the encapsulated texture have had the corresponding alpha component applied already.

Returns YES if this instance contains a CCTexture2D instance, and that texture instance indicates that it contains pre-mulitiplied alpha.

BOOL CC3Texture::isBumpMap` [read, assign]` |

Returns whether this texture contains a texture unit that is configured as a bump-map.

Returns YES only if the textureUnit property is not nil, and the same property on that texture unit is set to YES. Otherwise, this property returns NO.

The direction, in local tangent coordinates, of the light source that is to interact with this texture if the texture unit has been configured as a bump-map.

Bump-maps are textures that store a normal vector (XYZ coordinates) in the RGB components of each texture pixel, instead of color information. These per-pixel normals interact with the value of this lightDirection property (through a dot-product), to determine the luminance of the pixel.

Setting this property sets the equivalent property in the texture unit.

Reading this value returns the value of the equivalent property in the texture unit, or returns kCC3VectorZero if this texture has no textureUnit.

The value of this property must be in the tangent-space coordinates associated with the texture UV space, in practice, this property is typically not set directly. Instead, you can use the globalLightLocation property of the mesh node that is making use of this texture.

ccTex2F CC3Texture::mapSize` [read, assign]` |

Returns the proportional size of the usable image in the contained CCTexture2D, relative to its physical size.

The physical size of most textures is some power-of-two (POT), whereas the usable image size is the actual portion of it that contains the image. The value returned by this method contains two fractional floats (u & v), each between zero and one, representing the proportional size of the usable image

As an example, an image whose dimensions are actually 320 x 480 pixels will result in a texture that is 512 x 512 pixels, and the mapSize returned by this method will be {0.625, 0.9375}, calculated from {320/512, 480/512}.

CCTexture2D * CC3Texture::texture` [read, write, retain]` |

The 2D texture being managed by this instance.

ccTexParams CC3Texture::textureParameters` [read, write, assign]` |

A set of texture parameters used to optimize the display of the contained texture in the GL engine.

These setting are passed to the underlying CCTexture2D instance.

The initial value of these parameters are set to kCC3DefaultTextureParameters, which defines:

The texture environment settings that are applied to the texture unit that draws this texture.

The texture unit is optional, and this propety may be left as nil to provide standard single texture rendering. The default value of this property is nil.

The texture unit can be used to configure how the texture will be combined with other textures when using multi-texturing. When the material supports multiple textures, each texture should contain a texture unit that describes how the GL engine should combine that texture with the textures that have already been applied.

Different subclasses of [CC3TextureUnit](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture_unit/) provide different customizations for combining textures. The [CC3BumpMapTextureUnit](http://www.learn-cocos2d.com/) provides easy settings for DOT3 bump-mapping, and [CC3ConfigurableTextureUnit](http://www.learn-cocos2d.com/) provides complete flexibility in setting texture environment settings.