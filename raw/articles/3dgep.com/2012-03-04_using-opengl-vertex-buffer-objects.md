---
title: Using OpenGL Vertex Buffer Objects
url: https://www.3dgep.com/using-opengl-vertex-buffer-objects/
author: Jeremiah
published: '2012-03-04'
source_blog: 3D Game Engine Programming
source_site: https://www.3dgep.com/
category: graphics
fetched: '2026-04-13'
---

**ARB_vertex_buffer_object**extension to efficiently render geometry in OpenGL.

If you are not sure how to use extensions in OpenGL, you can refer to my previous article titled

[OpenGL Extensions](https://www.3dgep.com/?p=2415). If you have never programmed an OpenGL application before, you can refer to my previous article titled

[Introduction to OpenGL](https://www.3dgep.com/?p=636).


When OpenGL was first conceived there was no concept of storing data directly on the hardware that performed the graphics rendering. Initially, everything was rendered using immediate mode rendering (for an explanation on different methods for rendering primitives, refer to my previous article titled [Rendering Primitives](https://www.3dgep.com/?p=2365)). Vertex arrays were introduced into the core specification in OpenGL 1.1 in 1992. Although vertex arrays were far more efficient than immediate mode rendering, they still required the client application to pass geometry information to the renderer ever frame. In 2003 the OpenGL 1.5 specification was introduced which added the **ARB_vertex_buffer_object** extension into the core specification. Vertex Buffer Objects (VBO) allow you to store the geometry information directly on the GPU. This is far more efficient than passing the data to the GPU every frame. In this article, I will show how you can use VBOs in your own applications to improve rendering performance.

It is also interesting to note that if you plan on using the forward-compatible contexts introduced in OpenGL 3.0, then VBOs are the only way to send geometry to the GPU.

Before we can use VBO’s in our own programs then we must ensure the current OpenGL context has support for them. I will use [GLEW](http://glew.sourceforge.net/) for extension support. For an in-depth discussion on extensions, refer to my previous article titled [OpenGL Extensions](https://www.3dgep.com/?p=2415).

The first step is to initialize GLEW in our application. This can only be done after the OpenGL context has been created as GLEW will not automatically create a context for us, it will only use the currently active OpenGL context. If you are using GLUT or freeGLUT, this only happens after a render window has been created using the **glutCreateWindow** function.

|
1
2
3
4
5
6
|
// Init GLEW
if ( glewInit() != GLEW_OK )
{
std::cerr << "Failed to initialize GLEW." << std::endl;
exit(-1);
}
|

After GLEW has been successfully initialized, we can use it to check for support of the VBO extension.

|
1
2
3
4
5
|
if ( !glewIsSupported("GL_VERSION_1_5") && !glewIsSupported( "GL_ARB_vertex_buffer_object" ) )
{
std::cerr << "ARB_vertex_buffer_object not supported!" << std::endl;
exit(-2);
}
|

If neither OpenGL 1.5 nor the **ARB_vertex_buffer_object** extension are supported then we can’t use VBOs to render our geometry, so we just exit the application with some random error code. If either of these statements returns true then we can use the VBO extension in our application.

To create VBO’s we first need to define the data that will be used to populate our buffers. In this demo, I will render a simple cube object. Each vertex of the cube will be rendered with a different color. As a result, we should see a nice smooth-shaded cube rotating on our screen.

For our geometry, we’ll use interleaved arrays with the following vertex definition:

|
1
2
3
4
5
|
struct VertexXYZColor
{
float3 m_Pos;
float3 m_Color;
};
|

The **float3** type is simply a 3-component floating-point struct type.

We’ll define the geometry that will be used to render the cube:

|
1
2
3
4
5
6
7
8
9
10
11
|
// Define the 8 vertices of a unit cube
VertexXYZColor g_Vertices[8] = {
{ float3( 1, 1, 1 ), float3( 1, 1, 1 ) }, // 0
{ float3( -1, 1, 1 ), float3( 0, 1, 1 ) }, // 1
{ float3( -1, -1, 1 ), float3( 0, 0, 1 ) }, // 2
{ float3( 1, -1, 1 ), float3( 1, 0, 1 ) }, // 3
{ float3( 1, -1, -1 ), float3( 1, 0, 0 ) }, // 4
{ float3( -1, -1, -1 ), float3( 0, 0, 0 ) }, // 5
{ float3( -1, 1, -1 ), float3( 0, 1, 0 ) }, // 6
{ float3( 1, 1, -1 ), float3( 1, 1, 0 ) }, // 7
};
|

The vertex buffer defines the position of each vertex in object space as well color for each unique vertex. This is an interleaved buffer but it is entirely possible to define a different buffer for the vertex positions and each vertex attribute (like color, normal, texture coordinates). It is generally a good idea to use as few buffers as possible as binding each buffer can have a slight performance impact.

This vertex array only defines the 8 unique vertices for the cube but in order to render a cube object in OpenGL, we need to define the triangles that make up the faces of the cube. For that, we’ll use an index buffer which defines the order in which the vertices should be rendered.

|
1
2
3
4
5
6
7
8
9
|
// Define the vertex indices for the cube.
GLuint g_Indices[24] = {
0, 1, 2, 3, // Front face
7, 4, 5, 6, // Back face
6, 5, 2, 1, // Left face
7, 0, 3, 4, // Right face
7, 6, 1, 0, // Top face
3, 2, 5, 4, // Bottom face
};
|

We also need to define variables that will be used to store the unique object ID’s that will be used to refer to our two buffers.

|
1
2
|
GLuint g_uiVerticesVBO = 0;
GLuint g_uiIndicesVBO = 0;
|

Just like OpenGL texture objects, we must first define buffer object ID’s using the **glGenBuffersARB** function.

|
1
2
3
|
// Create VBO's
glGenBuffersARB( 1, &g_uiVerticesVBO );
glGenBuffersARB( 1, &g_uiIndicesVBO );
|

With our unique VBO ID’s, we can then fill the buffer data with the vertex array and index array using the **glBufferDataARB** function.

|
1
2
3
4
5
6
7
8
9
|
// Copy the vertex data to the VBO
glBindBufferARB( GL_ARRAY_BUFFER_ARB, g_uiVerticesVBO );
glBufferDataARB( GL_ARRAY_BUFFER_ARB, sizeof(g_Vertices), g_Vertices, GL_STATIC_DRAW_ARB );
glBindBufferARB( GL_ARRAY_BUFFER_ARB, 0 );
// Copy the index data to the VBO
glBindBufferARB( GL_ELEMENT_ARRAY_BUFFER_ARB, g_uiIndicesVBO );
glBufferDataARB( GL_ELEMENT_ARRAY_BUFFER_ARB, sizeof(g_Indices), g_Indices, GL_STATIC_DRAW_ARB );
glBindBufferARB( GL_ELEMENT_ARRAY_BUFFER_ARB, 0 );
|

The **ARB_vertex_buffer_object** extension defines the following targets to bind buffers to using the **glBindBufferARB** method:

-
**GL_ARRAY_BUFFER_ARB**: Used to refer to vertex array data such as vertex position, vertex color, vertex normal, texture coordinates, or any other data associated with vertex attribute information. -
**GL_ELEMENT_ARRAY_BUFFER_ARB**: Array index data. This target is applied when drawing primitives with indexed element methods such as**glDrawElements**or**glDrawRangeElements**.

The **glBufferDataARB** method is used to copy the vertex data from system memory to the high-performance GPU memory.

This method has the following signature:

|
1 |
void glBufferData( GLenum target, GLsizeiptr size, const GLvoid * data, GLenum usage );
|

Where,

-
**GLenum target**: The target buffer object that has previously been bound using the**glBindBufferARB**method. This can be either**GL_ARRAY_BUFFER_ARB**, or**GL_ELEMENT_ARRAY_BUFFER_ARB**. -
**GLsizeiptr size**: Specify the size in bytes to allocate for the buffer. -
**const GLvoid * data**: A pointer to the data in system memory that will be copied to the data store during initialization. This value can be**NULL**in which case the memory for the VBO will be allocated but not initialized. -
**GLenum usage**: Specify the usage pattern for the data store. This value can be:-
**GL_STREAM_DRAW_ARB**: Specifies that the contents of the buffer will be modified once by the application and used as the source for OpenGL render calls once per frame. -
**GL_STREAM_READ_ARB**: Specifies that the data store contents will modified by reading data from the OpenGL library once per frame and queried once per frame by the application. -
**GL_STREAM_COPY_ARB**: Specifies that the data store contents will be both modified by reading data form the OpenGL library and rendered once per frame. -
**GL_STATIC_DRAW_ARB**: Specifies that the data store contents will be modified once by the application and drawn many times. -
**GL_STATIC_READ_ARB**: Specifies that the contents of the buffer will be modified once by reading data from the OpenGL libarary and queried many times. -
**GL_STATIC_COPY_ARB**: Specifies that the contents of the buffer will be modified once by reading data from the OpenGL library and used many times as the source for OpenGL render commands. -
**GL_DYNAMIC_DRAW_ARB**: Specifies that the contents will be modified many times by the application and used many times as the source for OpenGL render calls. -
**GL_DYNAMIC_READ_ARB**: Specifies that the contents will be modified many times by reading data from the OpenGL library and queried many times by the application. -
**GL_DYNAMIC_COPY_ARB**: Specifies that the contents will be modified many times by reading data from the OpenGL library and used many times as the source for OpenGL render calls.

-

Rendering with vertex buffer objects is very similar to rendering with vertex arrays. Using vertex arrays, we enable the client states for the vertex position and vertex attributes, specify the pointers to the data using the **gl*Pointer** family of functions, and render the data with **glDrawArrays**, **glDrawElements**, or **glDrawRangeElements**. Using vertex buffer objects requires an additional step of binding the vertex buffer object to the **GL_ARRAY_BUFFER_ARB** target before you specify the pointer offsets with **gl*Pointer** family of functions.

First, we need to enable the client states for the vertex attributes we want to supply to the rendering pipeline. We need to enable these client states even if we are not using client-side vertex arrays because this function are still used to “enable” these elements in the rendering pipeline.

|
1
2
3
4
|
// We need to enable the client stats for the vertex attributes we want
// to render even if we are not using client-side vertex arrays.
glEnableClientState(GL_VERTEX_ARRAY);
glEnableClientState(GL_COLOR_ARRAY);
|

We need to bind the VBO’s to the **GL_ARRAY_BUFFER_ARB** before we can define the pointer to the buffer data.

|
1
2
3
4
|
// Bind the vertices's VBO
glBindBufferARB( GL_ARRAY_BUFFER_ARB, g_uiVerticesVBO );
glVertexPointer( 3, GL_FLOAT, sizeof(VertexXYZColor), MEMBER_OFFSET(VertexXYZColor,m_Pos) );
glColorPointer( 3, GL_FLOAT, sizeof(VertexXYZColor), MEMBER_OFFSET(VertexXYZColor,m_Color) );
|

On line 826, the vertices VBO is bound to the **GL_ARRAY_BUFFER_ARB** target.

On line 827, we use the **glVertexPointer** function to define the offset in the VBO to the vertex position data. This is similar to the way we define the pointer address of the vertex data when using vertex arrays but instead of a pointer address, this function now expects an offset in bytes to the first position vertex in the vertex buffer.

We’ll use the MEMBER_OFFSET macro to get the offset in bytes to a specific member of a struct. This macro has the following definition:

|
1 |
#define MEMBER_OFFSET(s,m) ((char *)NULL + (offsetof(s,m))) |

This macro uses the [offsetof](http://www.cplusplus.com/reference/clibrary/cstddef/offsetof/) macro defined in the “stddef.h” header file. The **offsetof** macro will return the offset in bytes to the member (m) in the struct (s). The **MEMBER_OFFSET** macro will convert the **size_t** value returned by this macro to a pointer type that the **glVertexPointer** method accepts.

On line 828, we do the same, but this time for the color attribute.

If we were using packed arrays instead of interleaved arrays, we would need to bind each individual vertex buffer object to the **GL_ARRAY_BUFFER_ARB** target before using the **gl*Pointer** function to define the offset in the bound buffer.

We also need to bind the index buffer to the **GL_ELEMENT_ARRAY_BUFFER_ARB** target before we can draw the elements using the **glDrawElements** method.

|
1
2
3
|
// Bind the indices's VBO
glBindBufferARB( GL_ELEMENT_ARRAY_BUFFER_ARB, g_uiIndicesVBO );
glDrawElements( GL_QUADS, 24, GL_UNSIGNED_INT, BUFFER_OFFSET( 0 ) );
|

In this case, we use the **BUFFER_OFFSET** macro which is a simpler version of the **MEMBER_OFFSET** macro.

The **BUFFER_OFFSET** macro has the following definition:

|
1 |
#define BUFFER_OFFSET(i) ((char *)NULL + (i)) |

This macro just casts the integer buffer offset value to a pointer type that is accepted by the **glDrawElements** method.

When we’re done drawing, don’t forget to set the OpenGL states back to normal.

|
1
2
3
4
5
6
7
|
// Unbind buffers so client-side vertex arrays still work.
glBindBufferARB( GL_ELEMENT_ARRAY_BUFFER_ARB, 0 );
glBindBufferARB( GL_ARRAY_BUFFER_ARB, 0 );
// Disable the client side arrays again.
glDisableClientState(GL_VERTEX_ARRAY);
glDisableClientState(GL_COLOR_ARRAY);
|

If everything is correct, we should see something similar to what is shown below. You can use your mouse to rotate the cube (unless you see the YouTube video which happens if your browser doesn’t support WebGL).



Vertex Buffer Objects

At some point, you may want to modify the contents of the VBO. This is required if you want to create a particle effect or perform CPU skinning on animated characters.

If you are updating the entire VBO, the best way to update the VBO is just to call **glBufferDataARB** again, just as if you were populating the data the first time. Using this method requires that you keep a copy of your vertex data in system memory so that you can change the vertex data on the CPU then upload it again to the VBO.

You can also map the VBO data to a pointer in system memory, modify the data and unmap the buffer again. To do this, we’ll use the **glMapBufferARB** method to retrieve a pointer to the VBO data.

The **glMapBufferARB** has the following signature:

|
1 |
void * glMapBufferARB(GLenum target, GLenum access);
|

Where

-
**GLenum target**: Specifies the target buffer object to map. There must be a valid buffer bound to either the**GL_ARRAY_BUFFER_ARB**target or**GL_ELEMENT_ARRAY_BUFFER_ARB**target using the**glBindBufferARB**

method, otherwise**glMapBufferARB**will return a**NULL**pointer. -
**GLenum access**: Specifies the access policy. This value must be one of the symbolic constants:-
**GL_READ_ONLY_ARB**: You will only be reading from the buffer object. -
**GL_WRITE_ONLY_ARB**: You will only be modifying the buffer. -
**GL_READ_WRITE_ARB**: You want to both read and write the buffer contents.

-

Acquiring a mapped pointer to a VBO could possibly cause a stall to occur if the rendering thread is still using the VBO to render the geometry causing your program to perform worse than expected. To avoid a thread stall, you can discard the current contents of the VBO by using the **glBufferDataARB** and passing **NULL** for the **data** parameter. This let’s the driver know that you don’t care about the contents of the VBO and basically discards the VBO contents and allocates space on the GPU for new data. Then when you map the VBO, the thread won’t stall. Obviously, you only want to do this if you intend to write new data to the vbo only. If you need to read the contents of the VBO, obviously you don’t want to discard the VBO contents.

You might be wondering why you just don’t use **glBufferDataARB** to overwrite the contents of the VBO instead of mapping a pointer to it? Mapping a pointer to the vertex buffer object to modify the contents is useful if system memory is scarce and you don’t want to keep duplicate data after you’ve uploaded the data to the GPU. Usually you can discard the system memory after the data has been uploaded to the GPU but then you must map the buffer before you can make changes to it.

After you are finished modifying the contents of the VBO, you should not forget to unmap it again using the **glUnmapBufferARB** method. This method accepts as it’s only argument the target buffer that was mapped with **glMapBufferARB**. You will most likely generate an error if you try to render the contents of a mapped buffer.

When we are finished with the VBOs, we should not forget to delete them. Buffer objects can be deleted with the **glDeleteBuffersARB** method.

|
1
2
3
4
5
6
7
8
9
10
|
if ( g_uiIndicesVBO != 0 )
{
glDeleteBuffersARB( 1, &g_uiIndicesVBO );
g_uiIndicesVBO = 0;
}
if ( g_uiVerticesVBO != 0 )
{
glDeleteBuffersARB( 1, &g_uiVerticesVBO );
g_uiVerticesVBO = 0;
}
|

In this article, I’ve shown how you can use the **ARB_vertex_buffer_object** extension to facilitate efficient rendering of your geometry.

I’ve shown how you can check for the **ARB_vertex_buffer_object** extension support so that you know for sure you can use the features described in the extension specification.

I showed you how to create vertex buffer objects and populate the VBO with data. I’ve also shown how you can use the VBO to render the geometry to the screen.

I’ve also described how to manipulate the contents of the VBO using the **glMapBufferARB** methods.

I’ve also showed the **glDeleteBuffersARB** method which is used to release the resources used by the VBO.

|
Benstead, Luke with Astle, D. and Hawkins, K. (2009).
|

Hello,

nice tutorial. Where can I get the code? I am having some trouble making it work.

Thanks!

Michael,

There is no code sample for this demo. The source code in the article should be sufficient to get VBO’s working.

What in particular are you having trouble with?

Hello,

I may bea bit doofy and unobservant, but where is the link to the main.cpp you refer to through this article?

Thanks all the same, it’s quite useful.

Cameron,

There is no source code sample for this demo. All the source code is in the article. Is there something in particular you are having issues with?

Thanks for this!

Just in case it helps anyone else, I found that unless the other arrays which are not being used are explicitly disabled, the program would crash on the glDrawElements/glDrawArrays call. This seems to be an nVidia thing. So in the case above where only vertex and color are being used, you would want to have this somewhere before the actual draw call:

glDisableClientState(GL_NORMAL_ARRAY);

glDisableClientState(GL_INDEX_ARRAY);

glDisableClientState(GL_TEXTURE_COORD_ARRAY);

glDisableClientState(GL_EDGE_FLAG_ARRAY);

Okay. I haven’t seen this myself, but thanks for the tip!