---
title: 'Mini: The Matrix'
url: https://mini.gmshaders.com/p/matrix
author: Xor
published: '2023-11-18'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: The Matrix

### An introduction to matrices and matrix multiplication

Hi everyone,


In a previous tutorial, I’ve written about “vector spaces” like world space and screen space, and we used matrices to apply these transformations. You can read it here if you like (although not required for understanding today’s topic):


## GM Shaders Mini: Vector Spaces

Hi friends. Maybe you’ve heard terms like “view space”, “model space” or “screen space”, but you’re not sure what it all means exactly? This is what we’ll be exploring today. For our purposes, “spaces” can be thought of as coordinate systems, which can be rotated, translated, scaled and skewed. We’ll go over the most important vector spaces, what they’r…

Somehow, matrices can [rotate](https://mini.gmshaders.com/p/gm-shaders-mini-rotation-1364623), scale, skew vectors and vector spaces. So how do they actually work?

Let’s investigate!

# Vector of Vectors

First, let’s go over what we know. We have scalars which have one component value and vectors have multiple components (between 2 and 4 in shaders):

```
//Scalars with 1 component
float scalarA = 5.0;
float scalarB = -0.2;
int scalarC = 2;
//Vectors have 2 to 4 components
vec2 vectorA = vec2(1.0, 2.0);
vec3 vectorB = vec3(1.0, 2.0, 3.0);
ivec4 vectorC = ivec4(1.0, 2.0, 3.0, 4.0);
```


Matrices, like vectors, come in different sizes: mat2, mat3 and mat4. They can be thought of vec2x2, vec3x3 and vec4x4 respectively. So mat2 has 4 components, mat3 has 9 components and mat4 has 16 components.

```
//Matrices have 4 (2x2) to 16 (4x4) components
mat2 matrixA = mat2(1.0, 2.0, 3.0, 4.0);
//Any combination of vectors as long as it has at least 9 components
mat3 matrixB = mat3(vectorB.xx, vectorB.yyy, vectorB.zzzz);
//Since mat4 is a constructor, it works with ints to.
mat4 matrixC = mat4(vectorC, vectorC.yzwx, vectorC.zwxy, vectorC.wxyz);
```


If you think of matrices as a square grid, you’re actually filling them column by column, not row by row, so top-to-bottom then left-to-right. In “matrixA” here, 1.0 is the top-left cell, 2.0 is the bottom-left, 3.0 top-right and 4.0 in the bottom right. If you’re ever having issues with your matrices, make sure they are oriented correctly!

*Note: Newer versions of GLSL support rectangular matrices like mat2x3 (6 components) or mat4x2 (8 components), but GameMaker does not support it currently.*

You may or may not know about using brackets to access a particular component of a vector: `float z = vector[2];`


Matrices can also be accessed this way, but instead of returning a single component, it returns the whole column. `matrixA[0]`

would return `vec2(1.0, 2.0)`

and `matrixA[1][1]`

would return the second index of the second column, in this case 4.0. In fact, you can think of vectors as just single column vectors.

Matrices are sometimes used to store larger sets of data, like a Bayer matrix

Generally, textures are a much better choice, but sometimes a matrix is handy here and there. Some people use it for neural networks. But it’s more than just a larger constructor!

# Vector * Matrix

Matrices can be multiplied with vectors or other matrices of the same dimension (so no scalars). To understand matrix multiplication, let’s start with a simple example:

```
//Zero's matrix. Can you guess what this does?
vec2 vectorA = vec2(1, 2) * mat2(0,0, 0,0);
//It turns the vec2(0, 0) because it's multiplying all components by 0
//This is an identity matrix and has no effect on the multiplied vector/matrix
vec2 vectorB = vec2(1, 2) * mat2(1,0, 0,1);
//The matrix's first column (1, 0) tells us the resulting vector's x-component
//We're multiplying the x component by 1 plus the y component multiplied by 0
//The second column (0, 1) tells us there's 0 x + 1 y, returning the original y
//So this matrix has no effect on the vector
//Now let's look at generalized example
vec2 vectorC = vec2(x, y) * mat2(a,b, c,d);
//This returns vec2(x*a + y*b, x*c + y*d)
//One more example, this time in 3D
vec3 vectorD = vec3(0, 1, 2) * mat3(3,4,5, 6,7,8, 9,0,1);
//This returns vec3(0*3 + 1*4 + 2*5, 0*6 + 1*7 + 2*8, 0*9 + 1*0 + 2*1)
//Which computes to vec3(14, 23, 2)
```


This may seem confusing at first, but [there are many ways](https://twitter.com/XorDev/status/1724469281453179179/photo/1) to think of this to make it easier to understand and to remember. Matrices assign each component a unique weight independently for each output component. The first output component is the sum of the components of the vector times the first column of the matrix. Effectively, a dot product for each output component!

*Note: matrix * vector is not the same as vector * matrix. More on that later!*

# Bundle of Dot Products

It may be helpful to think of vector * matrix multiplication as a bundle of dot products.

Read this if you’re unfamiliar with dot products and their many uses:

In a sentence, dot products are like rulers for measuring length along any arbitrary axis and in any arbitrary units. So any you can do in a dot-product, you can do in matrix also.

If you’re pretty comfortable with dot products, they can make it easier to think about matrix multiplication:

```
//Example matrix and vector
mat2 matrixA = mat2(1,0, 0,1);
vec2 vectorA = vec2(1, 2);
//Alternative way to compute vec2 * mat2:
vec2 vecmatA = vec2(dot(vectorA, matrixA[0]),
dot(vectorA, matrixA[1]));
//How about a 3D example?
mat2 matrixB = mat3(3,4,5, 6,7,8, 9,0,1);
vec3 vectorB = vec3(0, 1, 2) * matrixB;
//Alternative way to compute vec3* mat3:
vec2 vecmatB = vec3(dot(vectorB, matrixB[0]),
dot(vectorB, matrixB[1]),
dot(vectorB, matrixB[2]));
```


This makes matrices useful in [color remapping](https://www.shadertoy.com/view/ttcyRS), [noise functions](https://www.shadertoy.com/view/DdBGDh) and many, many other places. So now let’s look at scaling.

# Scaling

`mat2(2)`

is a 2x scaling matrix, kinda like multiplying by `vec2(2)`

. When you give a matrix constructor only a single component, it fills in [0][0], [1][1] (plus [2][2] with mat3 and [3][3] with mat4). All the rest of the components are set to 0. For example: `mat3(3) == mat3(3,0,0, 0,3,0, 0,0,3)`


They can also be used to stretch space along each axis independently (but so can vectors):

`x * mat3(1,0,0, 0,2,0, 0,0,3) == x * vec3(1, 2, 3)`



But scaling is boring, what about rotation?

## Rotation

Rotation is a little more complicated, because you’re actually moving components from one axis to another. In 2D, it looks like this:

`mat2(cos(angle),-sin(angle), sin(angle),cos(angle))`


I've written about this in more detail here, if you want to know where this comes from:

What about 3D rotation? I’ll leave this for you to dissect if you’d like:

```
//Sourced from Twigl by h_doxas
//https://github.com/doxas/twigl/blob/master/src/shader_snippet/noise.glsl
mat3 rotate3D(float angle, vec3 axis)
{
vec3 a = normalize(axis);
float s = sin(angle);
float c = cos(angle);
float r = 1.0 - c;
return mat3(
a.x * a.x * r + c,
a.y * a.x * r + a.z * s,
a.z * a.x * r - a.y * s,
a.x * a.y * r - a.z * s,
a.y * a.y * r + c,
a.z * a.y * r + a.x * s,
a.x * a.z * r + a.y * s,
a.y * a.z * r - a.x * s,
a.z * a.z * r + c
);
}
```


## Translation

It may surprise you, but it’s actually impossible to shift/translate a vec2 using a mat2 or a vec3 with a mat3. This is why built-in matrices like `gm_matrices[MATRIX_VIEW]`

are actually mat4s. In order to translate a 3D vector, with a matrix, we have to make it a vec4, where the w component is always 1.0. Then, our matrix’s fourth column will be for our translation values. Since we know the w-component is 1.0, we can just set the xyz directly to the translation values we want. So we know how to scale, rotate and translate, but how can we combine them all together? Enter matrix * matrix multiplication.

## Skew/Shear

You can also use matrices for shearing. It could be as simple as `mat2(1,1, 0,1)`

, which means shifting the x one unit over for every y unit. Of course, you can do any amount of shear and negative values to flip the shear direction.

# Matrix * Matrix

When you multiply “matrixA” with “matrixB”, it’s effectively multiply matrixA with each column of matrixB. So with a mat2 it looks like:

`mat2(matrixA*matrixB[0], matrixA*matrixB[1]);`


And similarly with mat3:

`mat3(matrixA*matrixB[0], matrixA*matrixB[1], matrixA*matrixB[2]);`


If you deconstruct the matrix multiplication, you can see that matrixA * matrixB is not the same as matrixB * matrixA:

`mat2(a,b,c,d) * mat2(x,y,z,w) = mat2(x*a+y*b,x*c+y*d,z*a+w*b,z*c+w*d)`


`mat2(x,y,z,w) * mat2(a,b,c,d) = mat2(a*x+b*y,a*z+b*w,c*x+d*y,c*z+d*w)`


The diagonal components are the same (first and the last), but the middle two are flipped. With mat3, there are even more differences because cells flip from [x][y] to [y][x] based on the order of the multiplication!

This is why you have to be careful and intentional about the order of multiplication.

As a general rule, you should start with the transformation you want to be last:

`last * first`


This is why we do `projection * view * world * vec4(pos, 1.0) in that order`

. I hope that clears things up for you. It took me a long to figure this stuff out because I didn’t know of any tutorials to follow at the time.

# Conclusion

Matrices are a powerful when working with vectors because it gives you control of the weight of all the components. They can make rotation, stretching, skewing an easy process. They are often used in color space transformations, noise functions, and are used for GM’s camera system (all using mat4)! Having a grasp of how they work can make all of these situations easier to deal with.

I used matrices to compute the camera position from a view matrix:`vec3 cam = -mat3(view) * view[3].xyz;`


I used it to generate a pseudo-random vec2:

`fract(sin(p * mat2(0.129898, 0.81314, 0.78233, 0.15926)) * 43758.5453);`


I even used it to turn a square grid to a triangular grid:

`mat2(1.155, 0, 0.577, 1)`


I hope this tutorial makes the topic more approachable and adds yet another tool to your shader tool belt. If this sort of thing excites, subscribe for more like it!

# Extras

There are 3 common matrix functions that you may see across the web, but GM doesn’t support them natively. Thankfully, you can copy from these resources below:

: Allows you to effectively reverse a matrix operation, through multiplying by its inverse.[Inverse](https://github.com/glslify/glsl-inverse/blob/master/index.glsl): Flips your [x][y] columns to [y][x].[Transpose](https://github.com/glslify/glsl-transpose/blob/master/index.glsl): For computing the area/volume factor and whether a matrix flips/inverts the space. Here’s a great video on the topic![Determinant](../../assets/8d7aa596c1fb96d8.img)

That’s it for today! Thanks again for reading. Have a great weekend and I’ll talk with you soon!

— Xor

I'm currently studying matrix operations in shaders, and I might be mistaken because I'm still quite confused, but isn't the calculation shown in the “Matrix * Matrix” section incorrect?

Shouldn't it be:

mat2(a,b,c,d) * mat2(x,y,z,w) = mat2(x*a+y*c, x*b+y*d, z*a+w*c, z*b+w*d)

mat2(x,y,z,w) * mat2(a,b,c,d) = mat2(a*x+b*z, a*y+b*w, c*x+d*z, c*y+d*w)