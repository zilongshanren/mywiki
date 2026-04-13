---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/
published: '2011-09-27'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3MeshNode.h>`


| void |
|

A [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) that draws a 3D mesh.

This class forms the base of all visible 3D mesh models in the 3D world.

[CC3MeshNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) is a type of [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/), and will often participate in a structural node assembly. An instance can be the child of another node, and the mesh node itself can have child nodes.

CC3MeshNodes encapsulate a [CC3Mesh](http://www.learn-cocos2d.com/) instance, and can also encapsulate either a [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/) instance, or a pure color. The [CC3Mesh](http://www.learn-cocos2d.com/) instance contains the mesh vertex data. The [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/) instance describes the material and texture properties covering the mesh, which are affected by lighting conditions. Alternately, instead of a material, the mesh may be colored by a single pure color via the pureColor property.

When this node is drawn, it delegates to the mesh instance to render the mesh vertices. If a material is defined, before drawing the mesh, it delegates to the material to configure the covering of the mesh. If no material is defined, the node establishes its pure color before rendering the mesh. The pure color is only used if the node has no material attached. And the pure color may in turn be overridden by the mesh data if vertex coloring is in use.

Each [CC3MeshNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) can have only one material or pure color. For large, complicated meshes that are covered by more than one material, or colored with more than one color, the mesh must be broken into smaller meshes, each of which are covered by a single material or color. These smaller sub-meshes are sometimes referred to as "vertex groups". Each such sub-mesh is then wrapped in its own [CC3MeshNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) instance, along with the material that covers that sub-mesh.

These [CC3MeshNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) instances can then be added as child nodes to a single parent [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) instance. This parent [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) can then be moved, rotated and scaled, and all of its child nodes will transform in sync. The assembly will behave and be seen as a single object.

When the mesh is set in the mesh property, the [CC3MeshNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) instance creates and builds a [CC3NodeBoundingVolume](http://www.learn-cocos2d.com/) instance from the mesh data, and sets it into its boundingVolume property.

When a copy is made of a [CC3MeshNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) instance using the copy method, a copy is made of the material, but the mesh is simply assigned by reference, and is not copied. The result is that the the new and original nodes will have different materials, but will share the same mesh. This design avoids creating multiple copies of volumnious and static mesh data when creating copies of nodes.

Normally, the front faces of a mesh are displayed, and the back faces are culled and not displayed. You can change this behaviour if you need to be changing the values of the shouldCullFrontFaces and shouldCullBackFaces properties. An example might be if you wanted to show the back-side of a planar sign, or if you wanted to show the inside faces of a skybox.

However, be aware that culling is a significant performance-improving technique. You should avoid disabling backface culling except where specifically needed for visual effect. And when you do, if you only need the back faces, turn on front face culling for that mesh by setting the shouldCullFrontFaces property to YES.

| void CC3MeshNode::alignInvertedTextures | ( | ) | ` [virtual]` |

Aligns the texture coordinates of the mesh with the textures held in the material.

The texture coordinates are aligned assuming that the texture is inverted in the Y-direction. Certain texture formats are inverted during loading, and this method can be used to compensate.

This method can be useful when the width and height of the textures in the material are not a power-of-two. Under iOS, when loading a texture that is not a power-of-two, the texture will be converted to a size whose width and height are a power-of-two. The result is a texture that can have empty space on the top and right sides. If the texture coordinates of the mesh do not take this into consideration, the result will be that only the lower left of the mesh will be covered by the texture.

When this occurs, invoking this method will adjust the texture coordinates of the mesh to map to the original width and height of the texturesa.

If the mesh is using multi-texturing, this method will adjust the texture coordinates array for each texture unit, using the corresponding texture for that texture unit in the specified material.

Care should be taken when using this method, as it changes the actual vertex data. This method should only be invoked once on any mesh, and it may cause mapping conflicts if the same mesh is shared by other CC3MeshNodes that use different textures.

This method will also invoke the superclass behaviour to invoke the same method on each child node.

To adjust the texture coordinates of only a single mesh, without adjusting the texture coordinates of any descendant nodes, invoke the alignWithInvertedTexturesIn: method of the [CC3Mesh](http://www.learn-cocos2d.com/) held in this mesh node. To adjust the texture coordinates of only a single texture coordinates array within the mesh, invoke the alignWithInvertedTexture: method on the appropriate instance of [CC3VertexTextureCoordinates](http://www.learn-cocos2d.com/).

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a5b69b89f01d7c98c0303f1e03d976558).

| void CC3MeshNode::alignTextures | ( | ) | ` [virtual]` |

Aligns the texture coordinates of the mesh with the textures held in the material.

This method can be useful when the width and height of the textures in the material are not a power-of-two. Under iOS, when loading a texture that is not a power-of-two, the texture will be converted to a size whose width and height are a power-of-two. The result is a texture that can have empty space on the top and right sides. If the texture coordinates of the mesh do not take this into consideration, the result will be that only the lower left of the mesh will be covered by the texture.

When this occurs, invoking this method will adjust the texture coordinates of the mesh to map to the original width and height of the textures.

If the mesh is using multi-texturing, this method will adjust the texture coordinates array for each texture unit, using the corresponding texture for that texture unit in the specified material.

Care should be taken when using this method, as it changes the actual vertex data. This method should only be invoked once on any mesh, and it may cause mapping conflicts if the same mesh is shared by other CC3MeshNodes that use different textures.

This method will also invoke the superclass behaviour to invoke the same method on each child node.

To adjust the texture coordinates of only a single mesh, without adjusting the texture coordinates of any descendant nodes, invoke the alignWithTexturesIn: method of the [CC3Mesh](http://www.learn-cocos2d.com/) held in this mesh node. To adjust the texture coordinates of only a single texture coordinates array within the mesh, invoke the alignWithTexture: method on the appropriate instance of [CC3VertexTextureCoordinates](http://www.learn-cocos2d.com/).

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a6ba26fe792bf02227f68e7e22d3a56cb).

Draws the local content of this mesh node by following these steps:

This method is called automatically from the transformAndDrawWithVisitor: method of this node. Usually, the application never needs to invoke this method directly.

| void CC3MeshNode::populateAsCenteredRectangleWithSize: | ( | CGSize | rectSize | ) | ` [virtual]` |

Populates this instance as a simple rectangular mesh of the specified size, centered at the origin, and laid out on the X-Y plane.

The rectangular mesh contains only one face with two triangles. The result is the same as invoking populateAsCenteredRectangleWithSize:andTessellation: with the facesPerSide argument set to {1,1}.

You can add a material or pureColor as desired to establish how the look of the rectangle.

As this node is translated, rotate and scaled, the rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, signs, etc.

| void CC3MeshNode::populateAsCenteredRectangleWithSize:andTessellation: | ( | CGSize | rectSize, |
| [andTessellation] ccGridSize | facesPerSide |
||
| ) | ` [virtual]` |

Populates this instance as a simple rectangular mesh of the specified size, centered at the origin, and laid out on the X-Y plane.

The large rectangle can be broken down into many smaller faces. Building a rectanglular surface from more than one face can dramatically improve realism when the surface is illuminated with specular lighting or a tightly focused spotlight, because increasing the face count increases the number of vertices that interact with the specular or spot lighting.

The facesPerSide argument indicates how to break this large rectangle into multiple faces. The X & Y elements of the facesPerSide argument indicate how each axis if the rectangle should be divided into faces. The total number of faces in the rectangle will therefore be the multiplicative product of the X & Y elements of the facesPerSide argument.

For example, a value of {5,5} for the facesPerSide argument will result in the rectangle being divided into 25 faces, arranged into a 5x5 grid.

You can add a material or pureColor as desired to establish how the look of the rectangle.

As this node is translated, rotate and scaled, the rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, signs, etc.

| void CC3MeshNode::populateAsCenteredRectangleWithSize:andTessellation:withTexture:invertTexture: | ( | CGSize | rectSize, |
| [andTessellation] ccGridSize | facesPerSide, |
||
| [withTexture]
|

` [virtual]`

Populates this instance as a simple textured rectangular mesh of the specified size, centered at the origin, and laid out on the X-Y plane.

The large rectangle can be broken down into many smaller faces. Building a rectanglular surface from more than one face can dramatically improve realism when the surface is illuminated with specular lighting or a tightly focused spotlight, because increasing the face count increases the number of vertices that interact with the specular or spot lighting.

The facesPerSide argument indicates how to break this large rectangle into multiple faces. The X & Y elements of the facesPerSide argument indicate how each axis if the rectangle should be divided into faces. The total number of faces in the rectangle will therefore be the multiplicative product of the X & Y elements of the facesPerSide argument.

For example, a value of {5,5} for the facesPerSide argument will result in the rectangle being divided into 25 faces, arranged into a 5x5 grid.

The shouldInvert flag indicates whether the texture should be inverted when laid out on the mesh. Some textures appear inverted after loading under iOS. This flag can be used to compensate for that by reinverting the texture to the correct orientation.

As this node is translated, rotate and scaled, the textured rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, etc.

| void CC3MeshNode::populateAsCenteredRectangleWithSize:withTexture:invertTexture: | ( | CGSize | rectSize, |
| [withTexture]
|

` [virtual]`

Populates this instance as a simple textured rectangular mesh of the specified size, centered at the origin, and laid out on the X-Y plane.

The rectangular mesh contains only one face with two triangles. The result is the same as invoking populateAsCenteredRectangleWithSize:andTessellation:withTexture:invertTexture: with the facesPerSide argument set to {1,1}.

The shouldInvert flag indicates whether the texture should be inverted when laid out on the mesh. Some textures appear inverted after loading under iOS. This flag can be used to compensate for that by reinverting the texture to the correct orientation.

As this node is translated, rotate and scaled, the textured rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, etc.

| void CC3MeshNode::populateAsLineStripWith:vertices:andRetain: | ( | GLshort | vertexCount, |
| [vertices]
|

` [virtual]`

Populates this instance as a line strip with the specified number of vertex points.

The data for the points that define the end-points of the lines are contained within the specified vertices array. The vertices array must contain at least vertexCount elements.

The lines are specified and rendered as a strip, where each line is connected to the previous and following lines. Each line starts at the point where the previous line ended, and that point is defined only once in the vertices array. Therefore, the number of lines drawn is equal to one less than the specified vertexCount.

The shouldRetainVertices flag indicates whether the data in the vertices array should be retained by this instance. If this flag is set to YES, the data in the vertices array will be copied to an internal array that is managed by this instance. If this flag is set to NO, the data is not copied internally and, instead, a reference to the vertices data is established. In this case, it is up to you to manage the lifespan of the data contained in the vertices array.

If you are defining the vertices data dynamically in another method, you may want to set this flag to YES to have this instance copy and manage the data. If the vertices array is a static array, you can set this flag to NO.

You can add a material or pureColor as desired to establish the color of the lines. If a material is used, the appearance of the lines will be affected by the lighting conditions. If a pureColor is used, the appearance of the lines will not be affected by the lighting conditions, and the wire-frame box will always appear in the same pure, solid color, regardless of the lighting sources.

As this node is translated, rotate and scaled, the line strip will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful, shape.

| void CC3MeshNode::populateAsRectangleWithSize:andPivot: | ( | CGSize | rectSize, |
| [andPivot] CGPoint | pivot |
||
| ) | ` [virtual]` |

Populates this instance as a simple rectangular mesh of the specified size, with the specified pivot point at the origin, and laid out on the X-Y plane.

The rectangular mesh contains only one face with two triangles. The result is the same as invoking populateAsRectangleWithSize:andPivot:andTessellation: with the facesPerSide argument set to {1,1}.

You can add a material or pureColor as desired to establish how the look of the rectangle.

The pivot point can be any point within the rectangle's size. For example, if the pivot point is {0, 0}, the rectangle will be laid out so that the bottom-left corner is at the origin. Or, if the pivot point is in the center of the rectangle's size, the rectangle will be laid out centered on the origin, as in the populateAsCenteredRectangleWithSize method.

As this node is translated, rotate and scaled, the rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, signs, etc.

| void CC3MeshNode::populateAsRectangleWithSize:andPivot:andTessellation: | ( | CGSize | rectSize, |
| [andPivot] CGPoint | pivot, |
||
| [andTessellation] ccGridSize | facesPerSide |
||
| ) | ` [virtual]` |

Populates this instance as a simple rectangular mesh of the specified size, with the specified pivot point at the origin, and laid out on the X-Y plane.

The large rectangle can be broken down into many smaller faces. Building a rectanglular surface from more than one face can dramatically improve realism when the surface is illuminated with specular lighting or a tightly focused spotlight, because increasing the face count increases the number of vertices that interact with the specular or spot lighting.

The facesPerSide argument indicates how to break this large rectangle into multiple faces. The X & Y elements of the facesPerSide argument indicate how each axis if the rectangle should be divided into faces. The total number of faces in the rectangle will therefore be the multiplicative product of the X & Y elements of the facesPerSide argument.

For example, a value of {5,5} for the facesPerSide argument will result in the rectangle being divided into 25 faces, arranged into a 5x5 grid.

You can add a material or pureColor as desired to establish how the look of the rectangle.

The pivot point can be any point within the rectangle's size. For example, if the pivot point is {0, 0}, the rectangle will be laid out so that the bottom-left corner is at the origin. Or, if the pivot point is in the center of the rectangle's size, the rectangle will be laid out centered on the origin, as in the populateAsCenteredRectangleWithSize method.

As this node is translated, rotate and scaled, the rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, signs, etc.

| void CC3MeshNode::populateAsRectangleWithSize:andPivot:andTessellation:withTexture:invertTexture: | ( | CGSize | rectSize, |
| [andPivot] CGPoint | pivot, |
||
| [andTessellation] ccGridSize | facesPerSide, |
||
| [withTexture]
|

` [virtual]`

Populates this instance as a simple textured rectangular mesh of the specified size, with the specified pivot point at the origin, and laid out on the X-Y plane.

The large rectangle can be broken down into many smaller faces. Building a rectanglular surface from more than one face can dramatically improve realism when the surface is illuminated with specular lighting or a tightly focused spotlight, because increasing the face count increases the number of vertices that interact with the specular or spot lighting.

The facesPerSide argument indicates how to break this large rectangle into multiple faces. The X & Y elements of the facesPerSide argument indicate how each axis if the rectangle should be divided into faces. The total number of faces in the rectangle will therefore be the multiplicative product of the X & Y elements of the facesPerSide argument.

For example, a value of {5,5} for the facesPerSide argument will result in the rectangle being divided into 25 faces, arranged into a 5x5 grid.

The pivot point can be any point within the rectangle's size. For example, if the pivot point is {0, 0}, the rectangle will be laid out so that the bottom-left corner is at the origin. Or, if the pivot point is in the center of the rectangle's size, the rectangle will be laid out centered on the origin, as in the populateAsCenteredRectangleWithSize:withTexture: method.

The shouldInvert flag indicates whether the texture should be inverted when laid out on the mesh. Some textures appear inverted after loading under iOS. This flag can be used to compensate for that by reinverting the texture to the correct orientation.

As this node is translated, rotate and scaled, the textured rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, etc.

| void CC3MeshNode::populateAsRectangleWithSize:andPivot:withTexture:invertTexture: | ( | CGSize | rectSize, |
| [andPivot] CGPoint | pivot, |
||
| [withTexture]
|

` [virtual]`

Populates this instance as a simple textured rectangular mesh of the specified size, with the specified pivot point at the origin, and laid out on the X-Y plane.

The rectangular mesh contains only one face with two triangles. The result is the same as invoking populateAsRectangleWithSize:andPivot:andTessellation:withTexture:invertTexture: with the facesPerSide argument set to {1,1}.

The pivot point can be any point within the rectangle's size. For example, if the pivot point is {0, 0}, the rectangle will be laid out so that the bottom-left corner is at the origin. Or, if the pivot point is in the center of the rectangle's size, the rectangle will be laid out centered on the origin, as in the populateAsCenteredRectangleWithSize:withTexture: method.

The shouldInvert flag indicates whether the texture should be inverted when laid out on the mesh. Some textures appear inverted after loading under iOS. This flag can be used to compensate for that by reinverting the texture to the correct orientation.

As this node is translated, rotate and scaled, the textured rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create walls, floors, etc.

Populates this instance as a simple rectangular box mesh from the specified bounding box, which contains two of the diagonal corners.

You can add a material or pureColor as desired to establish how the look of the box.

To add a texture, add a material to this node, then add a [CC3Texture](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_texture/) instance to that material. You must also add an instance of [CC3VertexTextureCoordinates](http://www.learn-cocos2d.com/) to the mesh model of this node, and populate it with the texture coordinate mapping data.

The mesh uses interleaved data, so when populating the texture coordinate data, set the elements property of the [CC3VertexTextureCoordinates](http://www.learn-cocos2d.com/) instance to the same as the elements property of the [CC3VertexLocations](http://www.learn-cocos2d.com/) instance from the vertexLocations property of the mesh. Then insert the texture coordinate data into that interleaved vertex data. Each element of that interleaved elements array is a [CC3TexturedVertex](http://www.learn-cocos2d.com/) structure, which contains the combined location, normal, and texture coordinate data for a single vertex. For more on how to do this, see the implementation of this method and take note of how this is done with the normal data.

As this node is translated, rotate and scaled, the rectangle will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful shape, which can be used to create simple structures in your 3D world.

Populates this instance as a wire-frame box with the specified dimensions.

You can add a material or pureColor as desired to establish the color of the lines of the wire-frame. If a material is used, the appearance of the lines will be affected by the lighting conditions. If a pureColor is used, the appearance of the lines will not be affected by the lighting conditions, and the wire-frame box will always appear in the same pure, solid color, regardless of the lighting sources.

As this node is translated, rotate and scaled, the wire-frame box will be re-oriented in 3D space.

This is a convenience method for creating a simple, but useful, shape.

| void CC3MeshNode::setTextureRectangle:forTextureUnit: | ( | CGRect | aRect, |
| [forTextureUnit] GLuint | texUnit |
||
| ) | ` [virtual]` |

Sets the textureRectangle property from the texture coordinates that are mapping the specified texture unit index.

See the notes for the textureRectangle property of this class for an explanation of the use of this property.

| void CC3MeshNode::setVertexColor4B:at: | ( | ccColor4B | aColor, |
| [at] GLsizei | index |
||
| ) | ` [virtual]` |

Sets the color element at the specified index in the vertex data to the specified value.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| void CC3MeshNode::setVertexColor4F:at: | ( | ccColor4F | aColor, |
| [at] GLsizei | index |
||
| ) | ` [virtual]` |

Sets the color element at the specified index in the vertex data to the specified value.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| void CC3MeshNode::setVertexIndex:at: | ( | GLushort | vertexIndex, |
| [at] GLsizei | index |
||
| ) | ` [virtual]` |

Sets the index element at the specified index in the vertex data to the specified value.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

Sets the location element at the specified index in the vertex data to the specified value.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

Sets the normal element at the specified index in the vertex data to the specified value.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| void CC3MeshNode::setVertexTexCoord2F:at: | ( | ccTex2F | aTex2F, |
| [at] GLsizei | index |
||
| ) | ` [virtual]` |

Sets the texture coordinate element at the specified index in the vertex data, at the commonly used texture unit zero, to the specified texture coordinate value.

This is a convenience method that delegates to the setVertexTexCoord2F:at:forTextureUnit: method, passing in zero for the texture unit index.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| void CC3MeshNode::setVertexTexCoord2F:at:forTextureUnit: | ( | ccTex2F | aTex2F, |
| [at] GLsizei | index, |
||
| [forTextureUnit] GLuint | texUnit |
||
| ) | ` [virtual]` |

Sets the texture coordinate element at the specified index in the vertex data, at the specified texture unit index, to the specified texture coordinate value.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| CGRect CC3MeshNode::textureRectangleForTextureUnit: | ( | GLuint | texUnit | ) | ` [virtual]` |

Returns the textureRectangle property from the texture coordinates that are mapping the specified texture unit index.

See the notes for the textureRectangle property of this class for an explanation of the use of this property.

| ccColor4B CC3MeshNode::vertexColor4BAt: | ( | GLsizei | index | ) | ` [virtual]` |

Returns the color element at the specified index from the vertex data.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| ccColor4F CC3MeshNode::vertexColor4FAt: | ( | GLsizei | index | ) | ` [virtual]` |

Returns the color element at the specified index from the vertex data.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| GLushort CC3MeshNode::vertexIndexAt: | ( | GLsizei | index | ) | ` [virtual]` |

Returns the index element at the specified index from the vertex data.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

Returns the location element at the specified index from the vertex data.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

Returns the normal element at the specified index from the vertex data.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| ccTex2F CC3MeshNode::vertexTexCoord2FAt: | ( | GLsizei | index | ) | ` [virtual]` |

Returns the texture coordinate element at the specified index from the vertex data at the commonly used texture unit zero.

This is a convenience method that delegates to the vertexTexCoord2FAt:forTextureUnit: method, passing in zero for the texture unit index.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

| ccTex2F CC3MeshNode::vertexTexCoord2FAt:forTextureUnit: | ( | GLsizei | index, |
| [forTextureUnit] GLuint | texUnit |
||
| ) | ` [virtual]` |

Returns the texture coordinate element at the specified index from the vertex data at the specified texture unit index.

The index refers to elements, not bytes. The implementation takes into consideration the elementStride and elementOffset properties to access the correct element.

If the releaseRedundantData method has been invoked and the underlying vertex data has been released, this method will raise an assertion exception.

ccColor4F CC3MeshNode::ambientColor` [read, write, assign]` |

The ambient color of the material of this mesh node.

Material color is initially set to kCC3DefaultMaterialColorAmbient. If this instance has no material, this property will return kCCC4FBlackTransparent.

The value of this property is also affected by changes to the color and opacity properties. See the notes for those properties for more information.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a87fc1dcd7533a6d9f29564116ab7d3fe).

ccColor3B CC3MeshNode::color` [read, write, assign]` |

Implementation of the CCRGBAProtocol color property.

Querying this property returns the RGB components of the material's diffuseColor property, or of this node's pureColor property if this node has no material. In either case, the RGB values are converted from the floating point range (0 to 1), to the byte range (0 to 255).

When setting this property, the RGB values are each converted to a floating point number between 0 and 1, and are set into both the ambientColor and diffuseColor properties of this node's material, and the pureColor property of this node. The alpha of each of those properties remains unchanged.

Setting this property also sets the same property on all descendant nodes.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a03aece3103f5751908dfda571a5a4145).

ccColor4F CC3MeshNode::diffuseColor` [read, write, assign]` |

The diffuse color of the material of this mesh node.

Material color is initially set to kCC3DefaultMaterialColorDiffuse. If this instance has no material, this property will return kCCC4FBlackTransparent.

The value of this property is also affected by changes to the color and opacity properties. See the notes for those properties for more information.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a0bb07b8079bf75af208434b5360cc58b).

ccColor4F CC3MeshNode::emissionColor` [read, write, assign]` |

The emission color of the material of this mesh node.

Material color is initially set to kCC3DefaultMaterialColorEmission. If this instance has no material, this property will return kCCC4FBlackTransparent.

The value of this property is also affected by changes to the opacity property. See the notes for the opacity property for more information.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a821370544c7d36e7cbb742988b936102).

When this mesh node is textured with a DOT3 bump-map (normal map), this property indicates the location, in the global coordinate system, of the light that is illuminating the node.

This global light location is tranformed from a loction in the global coordinate system to a direction in the local coordinate system of this node. This local direction is then applied to the texture of this node, where it interacts with the normals stored in the bump-map texture to determine surface illumination.

This property only needs to be set, and will only have effect when set, when one of the textures of this node is configured as a bump-map. Set the value of this property to the globalLocation of the light source. Bump-map textures may interact with only one light source.

When setting this property, this implementation also sets the same property in all child nodes. When reading this property, this implementation returns a value if this node contains a texture configured for bump-mapping, or the value of the same property from the first descendant node that is a [CC3MeshNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_mesh_node/) and that contains a texture configured for bump-mapping. Otherwise, this implementation returns kCC3VectorZero.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a2fdfd0ca5824487179b86d45b868c78b).

BOOL CC3MeshNode::isOpaque` [read, write, assign]` |

Indicates whether the material of this mesh node is opaque.

If this node has a material, returns the value of the same property on the material. If this node has no material, return YES if the alpha component of the pureColor property is 1.0, otherwise returns NO.

Setting this property sets the same property in the material and in all descendants, and sets the alpha component of the pureColor property to 1.0.

See the notes for this property on [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/) for more information on how this property interacts with the other material properties.

Setting this property should be thought of as a convenient way to switch between the two most common types of blending combinations. For finer control of blending, set specific blending properties on the [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/) instance directly, and avoid making changes to this property.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#ac178e6f33f03b599753ac1692bcf3dce).

The mesh that holds the vertex data for this mesh node.

When this property is set, if this node has a boundingVolume, it is forced to rebuild itself, otherwise, if this node does not have a boundingVolume, a default bounding volume is created from the mesh.

GLubyte CC3MeshNode::opacity` [read, write, assign]` |

Implementation of the CCRGBAProtocol opacity property.

Querying this property returns the alpha component of the material's diffuseColor property, or of this node's pureColor property if this node has no material. In either case, the RGB values are converted from the floating point range (0 to 1), to the byte range (0 to 255).

When setting this property, the value is converted to a floating point number between 0 and 1, and is set into all of the ambientColor, diffuseColor, specularColor, and emissionColor properties of this node's material, and the pureColor property of this node The RGB components of each of those properties remains unchanged.

Setting this property also sets the same property on all descendant nodes.

See the notes for this property on [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/) for more information on how this property interacts with the other material properties.

Setting this property should be thought of as a convenient way to switch between the two most common types of blending combinations. For finer control of blending, set specific blending properties on the [CC3Material](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_material/) instance directly, and avoid making changes to this property.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a7c97161a1d0bd50fb265bd390fab9247).

ccColor4F CC3MeshNode::pureColor` [read, write, assign]` |

The pure, solid color used to paint the mesh if no material is established for this node.

This color is not not be affected by the lighting conditions. The mesh will always appear in the same pure, solid color, regardless of the lighting sources.

BOOL CC3MeshNode::shouldCullBackFaces` [read, write, assign]` |

Indicates whether the back faces of the mesh should be culled.

The initial value is YES, indicating that back faces will not be displayed. You can set this property to NO if you have reason to display the back faces of the mesh (for instance, if you have a rectangular plane and you want to show both sides of it).

Since the normal of the face points out the front face, back faces interact with light the same way the front faces do, and will appear luminated by light that falls on the front face, much like a stained-glass window. This may not be the affect that you are after, and for some lighting conditions, instead of disabling back face culling, you might consider creating a second textured front face, placed back-to-back with the original front face.

Be aware that culling improves performance, so this property should be set to NO only when specifically needed for visual effect, and only on the meshes that need it.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a0a02ef76817887e925c9dc04c0e9826e).

BOOL CC3MeshNode::shouldCullFrontFaces` [read, write, assign]` |

Indicates whether the front faces of the mesh should be culled.

The initial value is NO. Normally, you should leave this property with the initial value, unless you have a specific need not to display the front faces.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a890865bb4d5cf77011e4e3de7f3d1e17).

BOOL CC3MeshNode::shouldUseLighting` [read, write, assign]` |

If this value is set to YES, current lighting conditions will be taken into consideration when drawing colors and textures, and the material ambientColor, diffuseColor, specularColor, emissionColor, and shininess properties will have effect.

If this value is set to NO, lighting conditions will be ignored when drawing colors and textures, and the material emissionColor will be applied to the mesh surface without regard to lighting. Blending will still occur, but the other material aspects, including ambientColor, diffuseColor, specularColor, and shininess will be ignored. This is useful for a cartoon effect, where you want a pure color, or the natural colors of the texture, to be included in blending calculations, without having to arrange lighting, or if you want those colors to be displayed in their natural values despite current lighting conditions.

Setting the value of this property sets the same property in the contained material. Reading the value of this property returns the value of the same property in the contained material.

The initial value of this property is YES.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a3cbea6e6582b701b52b7a64d37ce6aa6).

ccColor4F CC3MeshNode::specularColor` [read, write, assign]` |

The specular color of the material of this mesh node.

Material color is initially set to kCC3DefaultMaterialColorSpecular. If this instance has no material, this property will return kCCC4FBlackTransparent.

The value of this property is also affected by changes to the opacity property. See the notes for the opacity property for more information.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a12ec9c3ae66471ffdc3eec5612cf4b4e).

CGRect CC3MeshNode::textureRectangle` [read, write, assign]` |

Defines the rectangular area of the textures, for all texture units, that should be mapped to the mesh used by this node.

This property facilitates the use of sprite-sheets, where the mesh is covered by a small fraction of a larger texture. This technique has many uses, including animating a texture onto a mesh, where each section of the full texture is really a different frame of a texture animation, or simply loading one larger texture and using parts of it to texture many different meshes.

The dimensions of this rectangle are taken as fractional portions of the full area of the texture. Therefore, a rectangle with zero origin, and unit size ((0.0, 0.0), (1.0, 1.0)) indicates that the mesh should be covered with the complete texture.

A rectangle of smaller size, and/or a non-zero origin, indicates that the mesh should be covered by a fractional area of the texture. For example, a rectangular value for this property with origin at (0.5, 0.5), and size of (0.5, 0.5) indicates that only the top-right quarter of the texture will be used to cover this mesh.

The bounds of the texture rectangle must fit within a unit rectangle. Both the bottom-left and top-right corners must lie between zero and one in both the X and Y directions.

The dimensions of the rectangle in this property are independent of adjustments made by the alignTextures and alignInvertedTextures methods. A unit rectangle value for this property will automatically take into consideration the adjustment made to the mesh by those methods, and will display only the part of the texture defined by them. Rectangular values for this property that are smaller than the unit rectangle will be relative to the displayable area defined by alignTextures and alignInvertedTextures.

As an example, if the alignWithTexturesIn: method was used to limit the mesh to using only 80% of the texture (perhaps when using a non-POT texture), and this property was set to a rectangle with origin at (0.5, 0.0) and size (0.5, 0.5), the mesh will be covered by the bottom-right quarter of the usable 80% of the overall texture.

This property affects all texture units used by this mesh, to query or change this property for a single texture unit only, use the textureRectangleForTextureUnit: and setTextureRectangle:forTextureUnit: methods.

The initial value of this property is a rectangle with origin at zero, and unit size, indicating that the mesh will be covered with the complete usable area of the texture.