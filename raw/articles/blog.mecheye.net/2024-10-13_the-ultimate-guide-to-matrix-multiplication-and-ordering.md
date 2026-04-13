---
title: The Ultimate Guide to Matrix Multiplication and Ordering
url: https://blog.mecheye.net/2024/10/the-ultimate-guide-to-matrix-multiplication-and-ordering/
author: Jasper St Pierre
published: '2024-10-13'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

Matrix multiplication in graphics APIs is ridiculously confusing. People are often confused about the right order of multiplying their matrices, and about row-major, column-major, pre-multiplication, post-multiplication, row vectors and column vectors, and transposing.

I plan for this to be the last resource you’ll never need to check.

## Why do we use matrices?

If matrices are so confusing, why do we even use them in the first place? Our goal with using matrices in graphics is using them to transform objects in space, or to transform space itself.

If we imagine a cube with some X, Y, and Z coordinates, we can translate that cube along the X axis by 5 units by adding a constant 5:

```
x' = x + 5
```


If we wanted to scale the cube by 2, we can multiply by 2:

```
x' = 2x
```


These are both very simple forms of transformations. So why go more complicated and use matrices? Well, let’s introduce rotation. Scaling and translating happen along a single axis, while rotation happens within a plane. Rotating a point around the Y axis changes the point’s values on the X and Z axis.

That means that to transform a point in a way that lets us scale, rotate, and translate it in a generic way, we need a formula that looks something like this:

```
x' = 1x + 7y + 9z + 1
y' = 4x + 1y + 6z + 0
z' = 3x + 8y + 2z + 3
```


If we assume that all of our equations will always be of the form `Ax + By + Cz + D`

, then we can eliminate all of the “fluff” there and end up with a bag of 12 numbers:

As you might imagine, this “bag of numbers” is called a matrix.

## Combining Translations

One interesting fact that isn’t at all obvious is that transforms compose differently depending on the order. Let’s go back to our simple example of scaling and translation using simple equations:

```
x' = 2x // Scale x by 2
```


```
x' = x + 5 // Translate x by 5
```


If we want to combine the two, the answer changes depending on whether we scale *before* translating or scale *after* translating. Scaling before translating means that we substitute the scaling equation into the translation one:

```
x' = 2x + 5 // Scaling by 2, then translating by 5
```


While scaling after translating means that we substitute the translation equation into the scaling one:

```
x' = 2(x + 5) // Translating by 5, then scaling by 2
```


And we can further simplify that “translating, then scaling” equation by expanding terms to help see that this result is indeed very different.

```
x' = 2x + 10 // Translating by 5, then scaling by 2
```


As long as we reduce our formula to a standard polynomial expression like `Ax + B`

, we can take those coefficients and put them directly in a matrix. In fact, doing this “substitution and simplify” will give us the *exact same coefficients* as if we multiplied two matrices together.

**Matrix Fact #1**: The standard algorithm for matrix multiplication is nothing more than a “compressed” form of writing two systems of linear equations, substituting one into the other, and simplifying all the way down.

Matrix multiplication being non-commutative is just a representation of this fact, that the order that you substitute equations into each other matters.

If it helps clear things up, you can think of matrix multiplication as something more along the lines of function application, rather than the multiplication of two scalars. If we imagine “translate by 5” as being function `F`

and our “scale by 2” as some function `G`

, then as we’ve just shown, `F(G(x))`

is not the same thing as `G(F(x))`

.

With a full set of x, y, and z equations, you can still write it out, substitute, and simplify, however it quickly becomes tedious for even just a handful of equations:

```
x' = 1x + 7y + 9z + 1
y' = 4x + 1y + 6z + 0
z' = 3x + 8y + 2z + 3
x'' = 2x' + 1y' + 3z' + 10
y'' = 1x' + 9y' + 4z' + 12
z'' = 3x' + 9y' + 6z' + 3
x'' = 2(1x + 7y + 9z + 1) + 1(4x + 1y + 6z + 0) + 3(3x + 8y + 2z + 3) + 10
y'' = 1(1x + 7y + 9z + 1) + 9(4x + 1y + 6z + 0) + 4(3x + 8y + 2z + 3) + 12
z'' = 3(1x + 7y + 9z + 1) + 9(4x + 1y + 6z + 0) + 6(3x + 8y + 2z + 3) + 3
```


If you took this and simplified it *all* the way down, we’d end up with the *exact* same set of coefficients that we would have had we did matrix multiplication instead. But as you can imagine, as equations get more and more complex, and as we stack more and more transforms on top of each other, matrix multiplication is a lot easier than writing equations out and substituting.

If you were working with a set of transformations for an extended period of time, you would have invented matrices too!

## Matrix/Matrix Multiplication

Let’s cover the easy case first, from a mathematical perspective, before we start talking about code and memory layouts. It’s well-established that Matrix/Matrix multiplication is *not* commutative, that is, matrix A times matrix B does not result in the same thing as matrix B times matrix A. However, Matrix/Matrix multiplication has exactly one formula, and it’s fairly easy to remember: it’s always *Across times down*. What do I mean by that?

Let’s multiply two 4×4 matrices together. On the left is A, and on the right is B. To get the result at any individual slot in the result, we take elements going *across* on the left, multiply them together with elements going *down* on the right, and then add those all up. In other words, each element of the result is a dot product of a row from matrix A with a column from matrix B.

**Whether you’re using Vulkan or DirectX, GLSL or HLSL, row-major or column-major matrix math always respects this formula. Across times down.** If there’s one thing to remember from this post, it’s that. Everything else is a corollary of that simple fact.

**Matrix Fact #2**: All matrices are multiplied as *across times down* no matter what shading language or graphics API you use.

## What if the dimensions are different?

Let’s try to multiply a 2×4 matrix against a 4×3 matrix. Note that in standard mathematical lingo, a 2×4 matrix is a matrix with 2 rows and 4 columns.

**Matrix Fact #3**: the convention in mathematics is that an MxN matrix is made up of M rows and N columns.

Nonetheless, we can multiply a 2×4 matrix against a 4×3 matrix, resulting in a 2×3 matrix. *Across times down.*

However, if we try and multiply a 4×2 matrix against a 3×4 matrix, we run into an issue. We cannot do across times down without running off the end of one of the matrices.

This is an error. It is only possible to multiply matrices together if their “inner” dimensions match: when multiplying matrices **A** and **B**, the number of columns in **A** must match the number of rows in **B**.

## Matrix/Vector Multiplication

Let’s stretch the limit here. What happens when we try to multiply a 4×4 matrix against a 4×1 matrix?

*Across times down* works just fine! Shading languages like HLSL and GLSL both use this formula when multiplying a matrix against a vector — they turn the vector on its side, becoming a “column vector”, or a matrix of 4×1, so that they can multiply together.

What happens when we multiply a vector against a matrix? You might expect to be an error, as it would be illegal to multiply a 4×1 matrix against a 4×4 matrix. However, shading languages like HLSL and GLSL do something somewhat unexpected here. When multiplying a vector times a matrix, they will arrange the same exact matrix as a 1×4 “row vector” matrix!

Note that vectors by themselves don’t have an inherent direction, it’s only by “arranging” them into 1xN or Nx1 matrices that they grow into “column vectors” or “row vectors”.

**Matrix Fact #4**:

- Multiplying a matrix
**M**against a vector**v**is equivalent to multiplying**M**against a new Nx1 matrix made up of**v**. - Multiplying a vector
**v**against a matrix**M**is equivalent to multiplying a new 1xN matrix made up of**v**, against our matrix**M**. - An Nx1 matrix is called a “column vector” since it’s tall and skinny, while a 1xN matrix is called a “row vector” since it’s short and wide.

Multiplying a matrix by a vector or a vector by a matrix is sometimes called *pre-multiplication* or *post-multiplication*, but these are unclear phrases; sometimes *pre-multiplication* refers to the vector being on the left-hand side, and sometimes it refers to the matrix being on the left-hand side.

For clarity, whenever the vector is on the left-hand side of a matrix/vector multiplication, I prefer to call it “row-vector multiplication”, and whenever it’s on the right-hand side, I prefer to call it “column-vector multiplication”.

## Useful Identities

We can take any matrix and *transpose* it. This effectively swaps rows and columns; what was a row is now a column, and vice versa.

Swapping a matrix like this is helpful for all number of reasons, but an important fact you can remember is that multiplying a matrix **A** against a matrix **B** is equivalent to transposing the two matrices, and swapping the multiplication order, and transposing the result. Note that transposing them swaps their dimensions, so the transpose of an e.g. 3×4 matrix becomes a 4×3 matrix. Combined with the *across times down* rule, it should be easy to verify yourself that the calculations will be the same.

**Matrix Fact #5**: Given matrices **A** and **B**, `A * B`

is the same as `transpose(transpose(B) * transpose(A))`

.

Since vectors can become either row-vectors or column-vectors based on their usage, this means that they “automatically transpose” themselves in shading languages. So effectively, `A * v`

simplifies down to be the same as `v * transpose(A)`

, and `v * A`

can be written as `transpose(A) * v`

.

## Row-Major and Column-Major

So far we’ve only talked about things from the mathematical perspective. Let’s talk about the *computers* side of things. A 3×4 matrix consists of 12 numbers, which we’ve stored in an array. How can we unpack this flat array of numbers into a matrix? We have two options: row-major matrix packing, and column-major matrix packing.

Row-major matrix packing is probably what seems the most obvious to a programmer: we unpack each number first from left to right, then from top to bottom. One way to imagine this is that we’ve divided up the 12 numbers from our array into 3 “row vectors” stacked on top of each other. This is why it’s called “row-major”.

Conversely, column-major matrix packing runs first top to bottom, then from left to right. We can visualize this packing order as being equivalent to four consecutive “column vectors” packed left to right, giving us the name “column-major”. Note that both row-major and column-major matrix packing still gives us matrices with the same shape and dimensions, it only changes how the array of data is interpreted.

**Matrix Fact #6**: Row-major and column-major are *not* properties of matrices by themselves and do not affect matrix multiplication; that is *always across times down*. Row-major and column-major are simply about the memory storage order of a matrix when loading from buffers and storing back to buffers.

Shading languages can control the memory packing of matrices through different means.

In HLSL, there are two different ways to affect packing order of matrices:

- You can use the
[pack_matrix](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-appendix-pre-pragma-pack-matrix)pragma to affect packing. - You can use the
`/Zpc`

or`/Zpr`

[command line arguments](https://learn.microsoft.com/en-us/windows/win32/direct3dtools/dx-graphics-tools-fxc-syntax)to set the default matrix packing for the file.

In GLSL, you can use the `row_major`

and `column_major`

[layout options](https://www.khronos.org/opengl/wiki/Interface_Block_(GLSL)#Matrix_storage_order) on structures or individual field.

In both HLSL and GLSL, column-major packing is the default, if no other overrides here are specified.

Also note that since transposing a matrix swaps the rows and columns, it’s another way to handle the packing differences; this is what the `transpose`

parameter to the [ glUniformMatrixNxMv](https://registry.khronos.org/OpenGL-Refpages/gl4/html/glUniform.xhtml) functions do; calling

`glUniformMatrix3x4fv`

with the transpose parameter set to `false`

will treat your 12 numbers as 4 column-vectors, while with the transpose parameter set to `true`

it will treat your 12 numbers as 3 row-vectors.**Matrix Fact #7**: Transposing a matrix is effectively equivalent to changing its packing order (I’m being a bit wishy-washy here).

## Shading Language Differences

While GLSL and HLSL are both similar in how they work with matrices, there’s still some things we need to cover.

The first is matrix type naming. To declare a 3×4 matrix, one with 3 rows and 4 columns:

- In HLSL, the type is float3x4. HLSL chooses to name it as floatRxC, as is traditional.
- In GLSL, the type is mat4x3. GLSL unfortunately chooses to name it as matCxR which clashes with existing mathematical practice.

Next up is the syntax for matrix multiplication and element-wise multiplication, sometimes called the [Hadamard product](https://en.wikipedia.org/wiki/Hadamard_product_(matrices)). The Hadamard product only exists for two matrices of the same dimension, and is just the individual elements in each “slot” multiplied together.

- HLSL uses
`mul(A, B)`

for standard matrix multiplication, and`A * B`

for the Hadamard product. - GLSL uses
`A * B`

for standard matrix multiplication, andfor the Hadamard product.`matrixCompMult`


When constructing matrices inside a shader, HLSL and GLSL act differently.

- HLSL’s matrix constructor works by being supplied full row vectors at a time. For a 3×4 matrix, if you pass 12 numbers, it will first construct 3 row vectors out of each consecutive set of 4 numbers, and then stack them up on top of each other. You can also pass 3
`float4`

row vectors directly. This happens*regardless*of whatever`pack_matrix`

pragma is set, or any compile arguments. - GLSL’s matrix constructor works by being supplied full column vectors at a time. For a 3×4 matrix, if you pass 12 numbers, it will first construct 4 column vectors out of each consecutive set of 3 numbers, and then stack them up on top of each other. You can also pass 4
`vec3`

column vectors directly. This happens*regardless*of whether the matrix is tagged as`row_major`

or`column_major`

layout.

When indexing into matrices inside a shader, HLSL and GLSL act differently.

- In HLSL, indexing into a matrix with
`matrix[0][2]`

will return the value in the 0th row and 2nd column.`matrix[3]`

will return the 3rd row as a vector. As above, this happens independently of any pack settings and command line arguments. - In GLSL, indexing into a matrix with
`matrix[0][2]`

will return the value in the 0th column and 2nd row.`matrix[3]`

will return the 3rd column as a vector. As above, this happens independently of any layout settings on the matrix.

These three differences above, plus other more historical artifacts have led many to believe that HLSL (and DirectX) *are* row-major, while GLSL (and OpenGL) *are* column-major. While they have a preference for advanced cases of indexing and constructors, matrix multiplication works the *exact same* between HLSL and GLSL, and they support either mode for packing and unpacking.

**Matrix Fact #8**: There are some subtle differences that affect the behavior of matrix types between HLSL and GLSL, but they don’t change how multiplication works.

## Space Transformations and Associativity

Our goal with matrices in computer graphics is to transform objects between different spaces. If we have a point in *world space*, and we would like to have a version of that point in *view space*, we transform the point by what’s commonly called a *view matrix*. I’m going to use column-vector multiplication here for example’s sake:

```
vec3 view_space_P = view_matrix * world_space_P;
```


The matrix is in charge of taking our point and transforming it into a new space. In computer graphics, we often wrangle many spaces, and want to build large transformation chains. For instance, a common viewing transformation looks something like this:

```
vec3 clip_space_P = projection_matrix * view_matrix * model_matrix * model_space_P;
```


Here, we are chaining together a set of transformations to our point P: the model-matrix transforms from model-space to world-space, the view-matrix transforms from world-space to view-space, and the projection matrix transforms from view-space to clip-space.

(And for anyone following along, yes, putting a `vec3`

into a `projection_matrix`

is not what a standard transformation looks like. I simply didn’t wish to distract this discussion with homogeneous coordinates and `vec4`

for the purposes of this article.)

One interesting fact is that while matrix multiplication is not commutative, it *is* associative: that is, `(A * B) * C`

is the same as `A * (B * C)`

. That means that we can think of the transformation in two different, identical ways:

-
We transform our vector

`model_space_P`

by the`model_matrix`

to get a new vector in world-space, then transform*that*vector by the`view_matrix`

to get a new vector in view-space, then transform*that*vector by the`projection_matrix`

to get a new vector in clip-space. That is,`projection_matrix * (view_matrix * (model_matrix * model_space_P))`

-
We multiply the matrices together:

`projection_matrix * view_matrix`

results in a new matrix that transforms from world-space*directly*to clip-space, and`projection_matrix * view_matrix * model_matrix`

results in a new matrix that transforms from model-space*directly*to clip-space. That is,`((projection_matrix * view_matrix) * model_matrix) * P`


One interesting fact is that when multiplying matrices together, we never end up *growing* the size of the matrix: when multiplying two 4×4 matrices together, the end result is *always* a new 4×4 matrix. This means that no matter how many space transforms we end up wanting to do, whether we want to transform between 3 spaces or between 500 spaces, we can *always* collapse that space transformation into a single 4×4 matrix.

But note that this new matrix now depends on which order you’re intending to do the resulting multiplication! That is, a new matrix `M = projection_matrix * view_matrix * model_matrix`

*needs* to be used as `M * v`

. Your composition order needs to match your usage order.

**Matrix Fact #9**: Multiplying two matrices together builds a new matrix that combines the relevant space transformations. As long as you keep the order consistent, you can combine as many matrices as you want together.

## Matrix Multiplication Ordering in Practice

Enough theory. Let’s talk some practice. Like above, we have a standard transformation sequence, and we would like to transform a given position vector **P**. We now have two choices:

- Column-vector multiplication, where
**P**is on the right-hand side

```
vec3 clip_space_P = projection_matrix * view_matrix * model_matrix * model_space_P;
```


- Row-vector multiplication, where
**P**is on the left-hand side

```
vec3 clip_space_P = model_space_P * model_matrix * view_matrix * projection_matrix;
```


Now, remember that `A * v`

is the same as `v * transpose(A)`

, because v changes whether it is a row-vector or column-vector based on usage. This means that for these two to represent the same calculation, the matrices must be transposed between the top and bottom lines. And since swapping the packing order is roughly equivalent to transposing, that means that we can make the top and bottom lines work *by changing the packing order*.

This is where the *other* half of the confusion comes from; historical convention is that DirectX and HLSL codebases *tend* to use row-vector multiplication, while OpenGL and GLSL codebases *tend* to use column-vector multiplication. This is sometimes expressed online as “DirectX is row-major” and “OpenGL is column-major”, however, there is nothing inherent about this in the graphics APIs or shading languages, just set through years of inertia of sample code and existing codebases.

In practice, the combination of column-vector/row-vector multiplication, column-major/row-major packing, and the existence of `transpose`

means that you can often make two mistakes that cancel each other out, or just fiddle around with flipping multiplication order and inserting transposes until things work.

However, there are some ways to make your life easier. When dealing with matrices, try to consider the space your data starts in, and the space transformations you wish to make. The general rule is that when using column-vector multiplication with the vector on the right-hand side, we wish to have a series of space-from-space matrices where the starting space is on the right-hand side, and the resulting space is on the left-hand side. Some even prefer to [name their matrices this way](https://www.sebastiansylvan.com/post/matrix_naming_convention/).

With P on the right-hand side (column-vector multiplication), you want to phrase it as a chain of “A-from-B” transformations:

```
vec3 clip_space_P = clip_from_view_space * view_from_world_space * world_from_model_space * model_space_P;
```


And with P on the left-hand side (row-vector multiplication), you want to phrase it as a chain of “B-to-A” transformations:

```
vec3 clip_space_P = model_space_P * model_to_world_space * world_to_view_space * view_to_clip_space;
```


As long as you know your spaces, and pick a convention and *stick to it*, you should be good to go.

## Inverses

OK, we’ve figured out how to transform space one way, but what if we wanted to go backwards? What if we have a point in world-space, and we want it in model-space? That’s what an inverse matrix is for. If we have a matrix that takes us from model-space to world-space, its inverse will take us from world-space back to model-space.

When using an inverse matrix, you should still *multiply* in the same order, but the space transformations will be backwards.

```
vec3 world_space_P = world_from_model_space * model_space_P;
vec3 model_space_P = inverse(world_from_model_space) * world_space_P;
```


**Matrix Fact #10**: The inverse matrix applies the opposite space transform, but doesn’t change the multiplication order at all.

## Which one should I use?

Between column-vector and row-vector multiplication, and column-major and row-major packing, we find ourselves with four choices with no obvious preferences. At some level, this is a choice similar to spaces or tabs, or picking your favorite up vector. That said, my preference is *column-vector multiplication*, and *row-major packing*, and my rationale is the follows:

-
Column-vector multiplication, the convention with P being a column-vector on the right-hand side, is the more traditional convention that you will see spelled in papers from mathematics. I prefer it for this reason; if you only have space in your brain for one convention, I think it simplifies the load to only consider this. That said, given my experience working in the games industry, it is certainly the less standard convention here. Additionally, it maps more naturally to the function-application mental model: it’s easier to imagine

`A * B * C * v`

as`A(B(C(v)))`

. -
Row-major packing, I prefer because it allows you to pack affine transform matrices more efficiently; for our model and view matrices, the last row of our matrix will be (0, 0, 0, 1). By removing this, we can fit the remaining 3 rows into three float4’s, which are a natural thing for a GPU to pack. For instance, with GLSL’s (admittedly outdated) std140 packing mode, we save 16 bytes of storage packing a 3×4 matrix as row-major over packing a 3×4 matrix as column-major.


However, more than anything, please try to be consistent, and please document your conventions somewhere. Nothing makes a graphics programmer happier than having your matrix conventions consistently obeyed and clearly documented.

## Quick Reference Table

| HLSL | GLSL | Notes | |
|---|---|---|---|
| Multiplication Order | Across times down | Across times down | |
| Matrix Type Name | `floatRxC` |
`matCxR` |
|
| Matrix/Matrix Multiplication | `mul(A, B)` |
`A * B` |
|
| Matrix/Vector Multiplication | `mul(A, v)` |
`A * v` |
Treats `v` as a column vector. |
| Vector/Matrix Multiplication | `mul(v, A)` |
`v * A` |
Treats `v` as a row vector. |
| Hadamard Multiplication | `A * B` |
`matrixCompMult(A, B)` |
Only works for two matrices of the exact same size. |
| Default Matrix Packing | Column-Major Packing | Column-Major Packing | |
| Changing Matrix Packing | `#pragma pack_matrix` or the `/Zpc` command line argument |
`layout(row_major)` or `layout(column_major)` |
|
| Constructors | `float2x2(row0, row1)` |
`mat2x2(col0, col1)` |
The element-wise constructor acts like you took consecutive numbers and “bunched” them up into vectors, then called the vector constructor. |
| Indexing | `m[row_index][col_index]` |
`m[col_index][row_index]` |
This is sometimes called “column-major” or “row-major” but that is a misconception. Majority is just about the packing order, it does not change the indices. |

> Matrix Fact #4: Given matrices A and B, A * B is the same as transpose(B) * transpose(A).

It’s the transpose of transpose(B) * transpose(A), not?

Thank you for the catch. I was a little bit less than rigorous here, and have updated the post to correct my mistake.

This article is fantastic, thank you so much!

I was actually floating the idea of writing something similar, but with an additional twist: since changing either vector orientation or matrix storage order is effectively equivalent to first performing a transpose on the matrix, the four possible combinations of these properties actually collapse down into two. Either you match them (e.g. row vectors and row major storage) or you mismatch (e.g. column vectors and row major storage), or in other words either your axis and translation vectors inside the matrix are contiguous in memory or they are not.

I have not been able to fully explore this idea, so I don’t know whether it falls apart at some point, but so far it has helped me understand some cases (especially when in existing code different matrix definitions are just memcpy’d into each other and somehow work, following the match/mismatch model helps me analyze without having to consider 4 different cases). Just some food for thought if you’re interested.

Great post! I wrote one in a similar vein a couple of years ago to get all this out of my head too 😅 It doesn’t cover as much of the mathematical side of things but might be interesting for reference – https://tomhultonharrop.com/mathematics/matrix/2022/12/26/column-row-major.html

Hi Jasper,

Thanks for the article, this was a really good read and I learnt a few new things about GLSL!

If you are interested in fixing it, I found a typo in this blog as highlighted in this link:

https://blog.mecheye.net/2024/10/the-ultimate-guide-to-matrix-multiplication-and-ordering/#:~:text=from%20model%2Dspace%20back%20to%20world%2Dspace

It should be “world-space back to model-space”.

Thanks, Josh

Thanks, I’ve fixed it.