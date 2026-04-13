---
title: Row-major vs. column-major and GL ES
url: https://fgiesen.wordpress.com/2011/05/04/row-major-vs-column-major-and-gl-es/
published: '2011-05-04'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Row-major vs. column-major and GL ES

There’s two major (no pun intended) ways to store 2D arrays: Row-major and Column-major. Row-major is the default layout in C, Pascal and most other programming languages; column-major is the default in FORTRAN and some numeric math-centric languages (mainly Matlab and R) – presumably because they started out as a kind of frontend for FORTRAN code.

Confusingly, the same terminology is also used by some people to denote whether you’re treating vectors as column vectors or row vectors by default. If you treat them as column vectors, you typically multiply a vector with a matrix from the left, i.e. the result of transforming a vector v by a matrix M is written . Transforming a vector by M then N is written as

, which I thought was backwards and confusing when I first saw it, but it has the big advantage of being consistent with the way we usually write function evaluation and composition:

(treating a matrix and its associated linear map given the standard basis as the same thing here). This is why most Maths and Physics texts generally treat vectors as column vectors (unless specified otherwise). The “row-major” convention defaults to row vectors, which means you end up with reverse order:

. This matches “reading order” (take v, transform by M, transform by N) but now you need to reverse the order when you look at the associated linear maps; this is generally more trouble than it’s worth.


Historically, IRIS GL used the row-vector convention, then OpenGL (which was based on IRIS GL) switched to column vectors in its specification (to make it match up better with standard mathematical practice) but at the same time switched storage layout from row-major to column-major to make sure that existing IRIS GL code didn’t break. That’s a somewhat unfortunate legacy, since C defaults to row-major storage, so you would normally expect a C library to use that too. ES got rid of a lot of other historical ballast, so this would’ve been a good place to change it.

Anyway, a priori, there’s no huge reason to strongly prefer one storage layout over the other. However in some cases, external constraints tilt the balance. I recently bitched a bit about OpenGL ES favoring column-major order, because it happens to be such a case, and column-major is the wrong choice. Don’t get me wrong, it’s by no means a big deal anyway, but it makes things less orthogonal than they need to be, which annoys me.

GLSL and HLSL have vec4/float4 as their basic native vector data type, and shader constants are usually passed in groups of 4 floats (as of D3D10+ HW this is a bit more freeform, but the alignment/packing rules are still float4-centric). In a row-major layout, a 4×4 matrix gets stored as

struct mat4_row_major { vec4 row0; vec4 row1; vec4 row2; vec4 row3; };

and multiplying a matrix with a 4-vector gets computed as

// This implements o = M*v o.x = dot(M.row0, v); o.y = dot(M.row1, v); o.z = dot(M.row2, v); o.w = dot(M.row3, v);

whereas for column-major storage layout you get

struct mat4_col_major { vec4 col0; vec4 col1; vec4 col2; vec4 col3; }; // M*v expands to... o = M.col0 * v.x; o += M.col1 * v.y; o += M.col2 * v.z; o += M.col3 * v.w;

so column-major uses muls/multiply-adds whereas row-major storage ends up using dot products. Same difference, so far – generally, shaders take the exact same time for both variants. But there’s an important special case: affine transforms, i.e. ones for which the last row of the matrix is “0 0 0 1”. Generally almost all of the transforms you’ll use in a game/rendering engine, except for the final projection transform, are of this form. More concretely, all of the transforms you’ll normally use for character skinning are affine, and if you do skinning in a shader you’ll use a lot of them, so their size matters. With the row-major layout you can just drop the last row and do this:

// M*v, where M is affine with last row not stored o.x = dot(M.row0, v); o.y = dot(M.row1, v); o.z = dot(M.row2, v); o.w = v.w; // often v.w==1 so this simplifies further

while with the column-major layout, you get to drop the last entry of every column vector, but that saves neither memory nor shader instructions. (As an aside, GL ES doesn’t support non-square matrix types directly; if you want to use a non-square matrix, you have to use an array/struct of vecs instead – another annoyance)

Furthermore, I generally prefer (for rendering code anyway) to store matrices in the format that I’m gonna send to the hardware or graphics API. On GL ES, that means I have to do one of three things:

- Use 4×4 matrices everywhere and live with 25% unnecessary extra arithmetic and memory transfers,
- Have my 3×4 matrix manipulation use row-major layout while 4×4 uses column-major,
- Avoid the GL ES builtin mat4 type and use a vec4[4] (or a corresponding struct) instead.

Now, options 2 and 3 are perfectly workable, but they’re ugly, and it annoys me that an API that breaks compatibility with the original OpenGL in about 50 different ways anyway didn’t clean up this historical artifact.

Nice article about an issue that has bothered me in the past, too. For reference, here’s a web page that archived the original Usenet discussion when OpenGL switched to column vectors:

http://steve.hollasch.net/cgindex/math/matrix/column-vec.html

I suspected mul/mad vs dot would be showing its head somewhere.

Thanks for explaining what you meant in more than 48 chars :-)

All the APIs I’m aware of historically use the same host memory layout (including IrisGL and DX). Iris GL and DX are explained as row major storage with v.M operations, whereas OpenGL is described as column major storage with M.v. In all cases, the host memory storage is really vector-major (nomenclature that I much prefered to row vs column major on fixed function).

Really, they were all doing the same thing until we started writing shaders. That’s when things started to go amiss. Now, row/column major nomenclature makes somewhat more sense, as the final matrix is visible in the shaders.

If you look at http://msdn.microsoft.com/en-us/library/ee416406%28v=vs.85%29.aspx, on hlsl, they’re still doing v.M (with row-major matrices, so mul/mad if the memory directly maps to constant registers). In the same way, gl_ModelViewProjection requires a M.v (with col-major matrices, still mul/mad).

But, as GL and DX started to use shaders (heavily influenced by Cg), people have been starting to write them in ways they could share. At that point, people started writing hlsl shaders with a M.v, requiring a transpose on the host, or change the math to generate the transposed matrix directly. Worth noting, the same *lsl code generates different low-level instructions on GL vs DX (if the GL runtime does not transpose by default, which it also could).

That’s part of why I’m not sure I understand your rant. With programmable shaders, you get to pick which side you do matrix-vector multiplications. Which means you can start doing them in a way that does not match the historical fixed function, and do dot4 for matrix multiplies accordingly. Just generate the matrices the other way around in the first place ?

Memory layout and matrix/vector product order: For some reason a lot of early computer graphics work used the v.M-style notation (e.g. the original Foley-van Dam did it that way), which is where IrisGL and Windows GDI got it from (yes, GDI has matrices). Then OpenGL had to be compatible with IrisGL so they stuck with that memory layout, and D3D decided to be compatible with GDI which gave them the matrix memory layout and the pixel-center convention they keep until DX10, when they switched it to be the same as GL. Point being, this is all for the sake of compatibility with previous APIs, not sanity, and as explained in the article, there’s good reason to stick with the same notation that everyone outside of computer graphics uses.

But notational issues aren’t the reason to prefer one over the other; the reason (given in the post!) is that affine transforms (which can be compactly stored as 3×4 matrices by implicitly taking the last row to be “0 0 0 1”) turn out to be very important in practice whereas 4×3 matrices aren’t. Combined with the fact that constant buffer storage is based around float4 packing, that means that storing it as 3x float4 has no wasted space whereas 4x float3 has 25% wasted space (and more data to move around). This isn’t about the way you write your matrix-vector products, or which storage order you generally prefer; storing affine transforms like that has clear-cut technical advantages in this particular case (which happens to be very relevant to e.g. skinning). How that fits into your theoretical/notational framework is a separate issue that I’m not talking about at all.

Anyway, so your hands are tied on this particular layout if you don’t want to waste space – and esp. with skinning and small number of constant registers, this directly translates into more memory transfers, smaller batches and more CPU/GPU work! But you do get to pick your layout for 4×4 matrices (where both representations are equally efficient). And my point is that with M.v product order and row-major storage, 3×4 and 4×4 happen to have compatible memory layouts (the same goes for v.M product order with column-major storage; here affine transforms are 4×3 matrices which again works out nicely). And GL ES has picked M.v+col-major storage, which means you need to store+transfer 3×4 in transposed layout if you don’t want to waste space, which sucks. Of course you can always store 4x4s as row-major and write the product as v.M in the shader – or explicitly do the transform elsewhere.

But all of this sucks. You want to use uniform notation in all your shaders to prevent confusion, you want uniform storage layouts for all your matrix types (again to prevent confusion), and you don’t want to transpose data all the time: having a transpose you need to add in some cases is like having a codebase that mixes left-handed and right-handed coordinate systems. Sure the two are just related by a similarity transform which is trivial in theory, but in practice people tend to forget it or do it in the wrong place and then the fun starts.

With M.v+row-major (or v.M+col-major), you get to have your cake and eat it too in this regard. It also happens to have the storage layout that C programmers would expect. And GL ES kills all of the builtin “build matrix” GL functions so every GL->GL ES port needs to go over all code that handles matrices anyway.

The programmable pipeline of D3D8+ (and D3D10+ in general) sidesteps this issue completely by not having any preference one way or the other, and no API functions that directly take matrices. The D3DX matrix functions and some of the samples still assume “D3D classic” v.M+row-major, but neither are part of the actual D3D API.

setting the notational issue aside, I do want to react to “GL ES has picked M.v+col-major”. GL ES 2.0 has picked col-major. You picked M.v (in your shader code!).

That was my point. If you do v.M, and compute M accordingly, you get back your 4×3 savings (that I did mention as “dot4 matrix multiplies”. I did get the point about the saving. I’ve coded it in the past).

But yeah, if you want to write M.v, and still keep the 4×3 saving, GLES 2.0 did not get the right default. Then again, the other default would kill the m[2] performance (unless you start modifying the glsl es spec as well, so that m[2] is not the 3rd column as it is right now). That’s a nasty can of worms too.

Does the row -vs column issue make any difference for 4×4 by 4×4 matrix multiplies? Most pre SSE4.1 (dpps) examples I’ve seen seem to assume column major format and perform 4 matrix x vector (each a 4x mul-add) multiplies.

Would this change if all your matrices where row major?

Matrix multiplication C=A*B of A=(a_ij), B=(b_ij), C=(c_ij) is

If you store in column-major, you want to factor this as

where c_X0, c_X1 etc. are the column vectors of C – i.e. the columns of C are computed as linear combinations of the columns of a, weighted by the elements of b. If you store in row-major, you instead prefer

which computes the rows of C as linear combinations of the rows of B, weighted by the elements of a. Either way works fine, has the exact same operation count, and doesn’t require any dot-product instructions. Does that answer your question?

I get it – so the same “multiply-add” sequence works if A,B are column major or row major Mat4 inputs – with the output C being in the same “format”. This is because we’re either processing rows or columns with the same SIMD goodness….

Not quite the same – the roles of A and B are reversed between the two methods – but yeah.

Oh sure – we’d post-multiply were we’d pre-multiply and vice-versa. Now all we need is a the proper fmadd in AVX 2: http://en.wikipedia.org/wiki/FMA_instruction_set

Thanks!

Dot product for 4×4 matrix-vector mul is slower on simd architecture.

Amd radeon cards have simd units

Also introduces consistency between your vector object data store and matrix.

That’s just one reason.

Feel free to look at the publically documented shader ISAs for AMD GCN or the older TeraScale (VLIW4/5) architectures, or at disassembled shader binary code. :)

GCN instructions are “scalar” (but across 64 vertices, fragments, …) so it’s all multiply-adds no matter what and the only thing that changes between the two layouts is the addresses the vaues get loaded from. TeraScale has X/Y/Z/W (X/Y/Z/W/T for VLIW5) *pipes* with various banking restrictions on register file and constant buffer access, but each of the 4 (5) pipes gets a separate instruction each cycle (although some of them internally forward between the pipes, including the dot product instructions that exist in that architecture). Either way, both MUL/MAD style matrix*vector multiplies and dot product-style variants have the exact same throughput on TeraScale.