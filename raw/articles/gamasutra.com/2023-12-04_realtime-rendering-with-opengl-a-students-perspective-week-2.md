---
title: Realtime Rendering With OpenGL – A Students Perspective (Week 2)
url: https://www.gamedeveloper.com/art/realtime-rendering-with-opengl-a-students-perspective-week-2-
author: Josh Church
published: '2023-12-04'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Realtime Rendering With OpenGL – A Students Perspective (Week 2)

This project was started for an independent study I was doing under Rush Swope at Indiana University Bloomington.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Week 2

Optimizing the engine and creating classes:

There were four main additions we made last week. The VAO, vertex array object. The VBO, vertex buffer object. The EBO, elements buffer object. The final addition was shaders. To build a larger engine we have to create classes for each of these different objects.

For the VAO, VBO, and EBO there are a lot of consistencies in the functions.

There is the Bind() function which is used to show glfw that we want to use this object.

There is the Unbind() function which is used to show glfw that we are done using this object.

Then finally there is the Delete() function which cleans up the object.

![VBO.png VBO.png](../../assets/8c063f17abcc05cb.png)

![VAO.png VAO.png](../../assets/15d8a050a470f5c5.png)


![EBO.png EBO.png](../../assets/542280b3c015b250.png)


The VAO, VBO, and EBO also all have constructors. The VBO constructor takes in all the vertices and stores them. The EBO constructor takes in the information about how those vertices will be used by taking in a list of indices. The VAO binds a VBO to itself so that it can transfer over the vertex information.

We also had to create a shader class. In this class I copied some code to read in the shader code we used last week. This allows us to store the shaders in a different file and make, giving us more freedom in the creation of new shaders in the future. The constructor for the shader class uses the previously mentioned function to read in specified shaders and turns them into a shader program, which can be referenced through the ID. The shader class also has an Activate() function, which tells glfw to use the shader program. Finally, it has a Delete() function which cleans up the shader program.

![Shader.png Shader.png](../../assets/b04ae67dae6ede1c.png)


Moving into 3D:

The first addition that had to be made when transitioning to 3D was the reference of another library. This library is called glm ([OpenGL Mathematics (g-truc.net)](https://glm.g-truc.net/0.9.9/index.html)). It allows for the use of matrix math on homogonous coordinates, taking a normal three coordinate system x, y, z and apply translations and rotations to those points. I had taken a linear algebra course before doing this project so I had some background knowledge about the use of matrix math when rendering.

After we have initialized the matrices, we apply translations and rotations to them. There is one specifically for the vertices, one for the camera view, and one for setting the FOV and clip planes for the camera view. We then apply those matrices to the vertex shader with the glGetUniformLocation() and glUniformMatrix4fv() functions.

The following gif is the original spinning pyramid, as you can see there are fractures in the pyramid, making it look glitchy.

![Week2OriginalPyramid.gif Week2OriginalPyramid.gif](../../assets/5e2cac9ab4018088.gif)


The reason for the fracturing in the pyramid is that we are now adding a layer of depth into the equation, we must enable the depth buffer for glfw. If you look below, you can see that after we enable the depth buffer and clear the bit every frame the fractures are gone.

![Week2DepthBuffer.gif Week2DepthBuffer.gif](../../assets/3d00212c30a9932d.gif)