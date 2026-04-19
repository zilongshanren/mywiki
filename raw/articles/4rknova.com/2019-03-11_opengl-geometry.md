---
title: OpenGL Geometry
url: https://www.4rknova.com/blog/2019/03/11/opengl-geometry
author: Nikolaos Papadopoulos
published: '2019-03-11'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

This blog post presents the evolution of the OpenGL API in terms of defining and submitting geometric attributes to the GPU. Please note that the different methods are not presented in full detail. Only relevant function parameters are explained and specialized functionality such as instancing is not included here so as to keep this post focused on beginner level concepts. Please see the references section for further reading resources.

# Immediate Mode

At the begining, the OpenGL specification defined a Fixed Function Pipeline. In this paradigm, vertex attributes are submitted to the server (i.e. GPU) using explicit API calls, with only a single property being transfered at each call. An OpenGL program would use the following API to upload geometry to GPU memory:

```
glBegin(GL_TRIANGLES);
glColor3f(1.0f, 0.0f, 0.0f); glVertex2f( 0.5f, 1.0f);
glColor3f(0.0f, 1.0f, 0.0f); glVertex2f( 0.5f,-0.5f);
glColor3f(0.0f, 0.0f, 1.0f); glVertex2f(-0.5f,-0.5f);
glEnd();
```


The Fixed Function Pipeline API also includes the following:

- Attribute uploading within glBegin / glEnd blocks.

i.e.*glVertex[*], glNormal[*], glColor[*]* - Matrix stack manipulation.

i.e.*glMatrixMode, glLoadIdentity, glRotatef, glTranslatef, glScalef* - Auxiliary state management for fixed pipeline functionality.

i.e.*glLight*, glLightModel, glMaterial*, etc

The obvious drawback of immediate mode is that it tends to create significant bottlenecks across the pipeline. The cost paid due to the frequency and granularity of transactions between client and server (i.e. CPU and GPU) results in CPU-bound performance. This is especially evident in modern real time applications, where geometric complexity is typically high and efficient bus utilization becomes a crucial optimization factor.

It’s important to note that at the OpenGL 1.0 era, real-time graphics applications were quite simplistic in comparison. The scope of 3D rendering was limited to simple shapes. Geometric complexity of even the most elaborate virtual scenes was crude and did not incorporate any small scale detail. Subsequently, bandwidth requirements were, for the most part, relatively low. The architecture, performance and complexity of CPUs as well as the first graphics accelerators of the time aimed to satisfy a simpler set of requirements.

This API was officially deprecated with the release of OpenGL 3.0 in 2008 and is nowadays referred to as *Legacy Mode*. Irrespectively, some implementations still provide support for it through the *GL_ARB_compatibility* extension.

# Display Lists (Retained mode)

Display lists were part of the OpenGL 1.0 specification. The main motivation behind display lists follows the observation that vertex attributes for static geometry need not be reuploaded to the server in every frame update. The block of commands could instead be *compiled* once and stored in server memory (i.e. on GPU memory) for later execution. Display lists can also bundle other fixed pipeline API calls. (eg. matrix stack manipulation calls).

The major drawback is that once a display list is compiled, it can no longer be modified. The relevant part of the API is straightforward:

```
// Create one display list once at initialization
GLuint index = glGenLists(1);
// Compile the display list
glNewList(index, GL_COMPILE);
glScalef(2.0f,2.0f,2.0f);
glBegin(GL_TRIANGLES);
glVertex3fv(v0);
glVertex3fv(v1);
glVertex3fv(v2);
glEnd();
glEndList();
[...]
// Draw the display list at each update
glCallList(index);
[...]
// Delete the list if it is not used any more
glDeleteLists(index, 1);
[...]
```


It is also possible to invoke multiple display lists with a single call.

```
GLuint index = glGenLists(10); // create 10 display lists
[...]
// Store the offsets in an array.
lists[0]=0;
lists[1]=2;
lists[2]=4;
// Set base address
glListBase(index);
// Draw lists with a single call
glCallLists(3, GL_UNSIGNED_BYTE, lists);
```


This API was officially deprecated with the release of OpenGL 3.1 in 2009.

# Vertex Arrays

Vertex arrays were introduced in OpenGL 1.1 through the *EXT_vertex_array* extension. They extend the immediate mode paradigm, to improve usability and performance. They reduce the number of API calls and eliminate the duplication of data for vertices shared across different primitives (eg. along the edges of a cube). The geometry parameters are packed in simple arrays. There is an option to use indexing in order to reuse common vertex data.

```
// Data for cube geometry
GLfloat vertices[] = {
...
}; // 8 vertex coords
GLubyte indices[] = {
0,1,2, 2,3,0,
0,3,4, 4,5,0,
0,5,6, 6,1,0,
1,6,7, 7,2,1,
7,4,3, 3,2,7,
4,7,6, 6,5,4
}; // 36 indices
```


The new API provides functions to activate and deactivate 6 different types of arrays. Six additional functions are used to specify the memory addresses of the respective data arrays stored in client memory.

| API | Use |
|---|---|
| glEnableClientState(…) | Enable an array type |
| glDisableClientState(…) | Disable an array type |
| glVertexPointer(…) | Set the pointer to vertex coords array |
| glNormalPointer(…) | Set the pointer to normals array |
| glColorPointer(…) | Set the pointer to color array |
| glIndexPointer(…) | Set the pointer to indexed color array |
| glTexCoordPointer(…) | Set the pointer to texture cords array |
| glEdgeFlagPointer(…) | Set the pointer to edge flag array |

A minimal example that uses the API is shown below. Notice that the API call used is *glDrawArrays(…)*. This function does not utilize the indices array and therefore the vertex data in the vertices array might be duplicated.

```
// Activate and specify pointer to vertex array
glEnableClientState(GL_VERTEX_ARRAY);
glVertexPointer(3, GL_FLOAT, 0, vertices);
// Draw a cube
// This replaces the 36 glVertex calls used in immediate mode
// to upload all vertex coords with a single call.
// Note that no indexing is used here and we are feeding a raw
// list of possibly duplicated vertex data.
glDrawArrays(GL_TRIANGLES, 0, 36);
// Deactivate vertex arrays after drawing
glDisableClientState(GL_VERTEX_ARRAY);
```


A different API function is provided for use cases where an indexing array is available.

```
// Activate and specify pointer to vertex array
glEnableClientState(GL_VERTEX_ARRAY);
glVertexPointer(3, GL_FLOAT, 0, vertices);
// Draw a cube
// This call uses indexing to reduce data redundancy
glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_BYTE, indices);
// Deactivate vertex arrays after drawing
glDisableClientState(GL_VERTEX_ARRAY);
```


Finally, in OpenGL 1.2 a third API function is introduced to allow prefetching a subset of the vertex data and increase performance. This could be used to pack multiple objects in the same buffer.

```
// draw second half
// range is 7 - 1 + 1 = 7 vertices used, 18 indices (idx)
glDrawRangeElements(GL_TRIANGLES, 1, 7, 18, GL_UNSIGNED_BYTE, idx+18);
```


It’s important to highlight that the geometry data is copied to the server in every render call.

# Vertex Buffer Objects (VBO)

As described above, vertex arrays store geometric data in client memory space. This proves to be inefficient in most use cases as the attributes will have to be perpetually copied to server (GPU) memory with every draw call. Buffer objects were introduced in OpenGL 1.5 in late 2003 to provide a mechanism to allocate and initialize, and render data in an optimized way.

The *GL_ARB_vertex_buffer_object* extension aims to combine the benefits of vertex arrays and the display lists. VBOs store vertex attributes in high-performance memory blocks that are managed and optimized by the server side. Relevant API functions are introduced to allocate, access and modify these memory blocks in a workflow similar to vertex arrays.

A buffer object is created by calling *glGenBuffers(…)*. It’s then bound as the current buffer object target with *glBindBuffer(…)* where a target is specified to be either *GL_ELEMENT_ARRAY_BUFFER* or *GL_ARRAY_BUFFER* depending on whether the buffer will store index data or regular attributes. The target parameter is used as a hint for the memory allocator to try and optimize the performance of the buffer by selection the appropriate location to allocate memory from (system memory, AGP, video memory). Finally *glBufferData(…)* allocates the memory block and copies the data if a non-NULL pointer is provided. It’s important to remember that the OpenGL framework operates as a state machine and the operation of binding a buffer before manipulating its contents corellates with that design.

Below is an example of how the API would be used to create a buffer object containing vertices (VBO).

```
// Generate a new VBO and get the associated ID
glGenBuffers(1, &vboId);
// Bind the VBO ID
glBindBuffer(GL_ARRAY_BUFFER, vboId);
// Upload data.
// The vertices array can be safely deleted after this call.
glBufferData(GL_ARRAY_BUFFER, dataSize, vertices, GL_STATIC_DRAW);
```


If a subset of the data in a buffer needs to be updated at a later stage, the *glBufferSubData(..,)* can facilitate that. The respective buffer needs to be bound before updating. Buffers that are no longer in use can be discarded, to release their allocated memory using the *glDeleteBuffers(…)* function.

For indexed data, an additional buffer needs to be created, which will contain the indices and is called an Index Buffer Object (IBO).

VBOs extend the existing vertex array mechanism and as such, the rendering interface is similar. The main point of divergence is that the pointer to the vertex array data is an offset into a bound buffer object instead of a raw memory address.

```
// Bind the VBOs for vertex and index arrays
glBindBuffer(GL_ARRAY_BUFFER, vbo);
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);
glEnableClientState(GL_VERTEX_ARRAY); // vertex position array
glEnableClientState(GL_NORMAL_ARRAY); // vertex normal array
glEnableClientState(GL_TEXTURE_COORD_ARRAY);// texture coords array
// do same as in vertex array except for pointer
glVertexPointer(3, GL_FLOAT, stride, offset1);
glNormalPointer(GL_FLOAT, stride, offset2);
glTexCoordPointer(2, GL_FLOAT, stride, offset3);
// draw 6 faces using offset of index array
glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_BYTE, nullptr);
glDisableClientState(GL_VERTEX_ARRAY);
glDisableClientState(GL_NORMAL_ARRAY);
glDisableClientState(GL_TEXTURE_COORD_ARRAY);
// bind with 0, so, switch back to normal pointer operation
glBindBuffer(GL_ARRAY_BUFFER, 0);
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
```


Note that only one array buffer and one element array buffer may be bound at a time, meaning that vertex attributes may not be stored in separate buffer objects and can only be interleaved within the same array. If no index data is used,

OpenGL 2.0 specification adds the *glVertexAttribPointer()*, *glEnableVertexAttribArray()* and *glDisableVertexAttribArray()* functions to allow for generic vertex attributes.

# Vertex Array Objects (VAO)

VAOs were introduced in OpenGL 3.0 in 2008. A VAO is an OpenGL Object that stores all of the state needed to supply vertex data as well as the VBOs that contain the vertex attribute arrays, further reducing the number of API calls require to draw.

At the initialization stage for each unit of geometry a Vertex Array Object (VAO) is created. A VAO can contain either a single VBO interleaved attributes (eg. position, normal, uv, etc) or a separate VBO per attribute. To draw the geometry all that is needed is binding the VAO and issuing a single draw call.

```
size_t k = sizeof(GLfloat);
// Create the Vertex Array Object (VAO) and bind it
GLuint vao = 0;
glGenVertexArrays(1, &vao);
glBindVertexArray(vao);
// Create a Vertex Buffer Object (VBO) for attribute 0 and bind it.
// This VBO will store vertex coordinates.
GLuint vertexbuffer = 0;
glEnableVertexAttribArray(0);
glGenBuffers(1, &vertexbuffer);
glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
// Copy attributes and set descriptors
glBufferData(GL_ARRAY_BUFFER, k * vert.size(), vert.data(),
GL_STATIC_DRAW);
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);
// Do the same process for the next attribute.
// This VBO will store normals.
GLuint normalbuffer = 0;
glEnableVertexAttribArray(1);
glGenBuffers(1, &normalbuffer);
glBindBuffer(GL_ARRAY_BUFFER, normalbuffer);
glBufferData(GL_ARRAY_BUFFER, k * norm.size(), norm.data(),
GL_STATIC_DRAW);
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);
[...]
// draw the geometry
glDrawArrays(GL_TRIANGLES, 0, vertices.size());
```


The example above renders non-indexed data. To use indices, an IBO is required. The process and API calls involved are the same as in the case of plain VBOs. Some additional functions are available to allow for more complex operations (eg automatically re-adjusting the values in concatenated index buffers via *glDrawElementsBaseVertex(…)*), however that functionality is beyond the scope of this article. More information on those functions can be found in the references section below.