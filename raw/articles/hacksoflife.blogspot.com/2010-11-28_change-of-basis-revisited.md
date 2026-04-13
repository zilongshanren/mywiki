---
title: Change of Basis, Revisited
url: http://hacksoflife.blogspot.com/2010/11/change-of-basis-revisited.html
author: Benjamin Supnik
published: '2010-11-28'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Transform Matrix As Basis Vectors

If we have a 3x3 matrix T of the form:

`[a d g]`

[b e h]

[c f i]


Then when we multiply a vector (x,y,z) by this matrix T, x gives us more or less of (a,b,c), y of (d,e,f) and z of (g,h,i). In other words, you can think of x, y, and z being orders for premade "amounts" of 3 vectors. In the old coordinate system, x gave us one unit of the 'x' axis, y one unit of the 'y' axis, and z one unit of the 'z' axis. So we can see (a,b,c) as the old coordinate system's "x" axis expressed in the new coordinate system, etc.This "change of basis" is essentially an arbitrary rotation about the origin - we are taking our model and changing where its axes are. Use the data with the old axes and you have the model rotated. So far everything we have done is with vectors, but you can think of a point cloud as a series of vectors from the origin to the data points.

Big Words

A lot of math for computer programmers is just learning what the mathematicians are talking about - math has a lot of vocabulary to describe ideas. Sometimes the words are harder than the ideas.

Our rotation matrix above is a set of orthonormal basis vectors. (We call the matrix an orthogonal matrix.) What does that mean? It means two things:

- Each basis vector is normal - that is, its length is 1.
- Each basis vector is orthogonal to all other basis vectors - that is, any two basis vectors are at right angles to each other.

- Our model isn't going to change size, because each basis vector is of length 1 (and in the original coordinate system, 1 unit is 1 unit by definition).
- Because the axes are all orthogonal to each other, we're not going to get any squishing or dimension loss - a cube will stay cubic. (This would not be true if we had a projection matrix! Everything we say here is based on fairly limited use of the model-view matrix and will not be even remotely true for a projection matrix.)

If we want to reposition our model completely (rotate and translate) we need a translation component. In OpenGL we do that like this:

`[ x]`

[ R y]

[ z]

[0 0 0 1]


In this matrix, R is our 3x3 rotation matrix, which is orthogonal, x y z is the offset to apply to all points. If we apply this to vectors of the form (x,y,z,1) then the math works out to first rotate the points x,y,z by r, and then add x,y,z after rotation. The last coordinate 'w' will remain "1" for future use. The upper right 3x3 matrix is orthogonal, but the whole matrix is not; if this were a 4-dimensional basis change, the vector (x,y,z,1) would not necessarily be normalized, nor would it be perpendicular to all other bases.There's a name for this too: an affine transformation matrix. If we ever have a liner transform (of which a set of orthonormal basis vectors is one) plus a translation, with 0....1 on the bottom, we have an affine transformation.

Affine Transformation As Model Position

If we have an affine transform matrix built from three orthonormal basis vectors (our old axes in the new coordinate system) plus an offset, we have everything we need to position a model in 3-d space. Imagine we have a house model, authored as points located around an origin. We want to position it at many locations in our 3-d world and draw it each time. We can build the transform matrix we want. Typically we'd do a sequence like:

glTranslate(x,y,z);That is, first move the models origin to this place in world space, then rotate it. This forms an affine matrix where the right most column is x,y,z,1 and the left three columns are the location of the model's X, Y, and Z axes in world space (with 0 in the last digit). The bottom row is 0 0 0 1.

glRotate(heading,0,1,0);

glRotate(pitch,1,0,0);

glRotate(roll,0,0,1);

Usually it's cheaper storage-wise to store the component parts of a model's transform than the entire transform matrix. But if we do want to store the object in the format of a transform, we do know a few things:

- The bottom row is 0 0 0 1 so we can simply delete it, cutting our matrix down from 16 floats to 12.
- We can get the object "location" in world-space directly out of the right-hand column.
- The upper-left 3x3 matrix contains all of the rotations.

The main reason to store model location as a matrix (and not the original offset and rotation angles) is for hardware instancing; we can stream a buffer of 12-float matrices to the GPU and ask it to iterate over the mesh using something like

[GL_ARB_draw_instanced](http://www.opengl.org/registry/specs/ARB/draw_instanced.txt). But if you're on an embedded platform and stuck in fixed point, replacing angles (which require trig to decode) with the matrix might also be a win.

glScale Wasn't Invited To The Party

We cannot scale our model using glScale and still have an orthonormal basis; doing so with any scale values other than 1 or -1 would make the basis vectors be non-unit-length, and then it would not be orthonormal. We can have mirroring operations - there is no requirement that an orthonormal basis maintain the "right-handedness" of a coordinate system.

With X-Plane we don' do either of these things (scale or mirror); in the first case, we don't need it, and it's a big win to know that your upper left 3x3 is orthonormal - it means you can use it to transform normal vectors directly. (If the upper left 3x3 of your model-view scales uniformly, your normals change length, which must be fixed in shader. If your model-view scales non-uniformly, the direction of your normals get skewed.) We don't mirror because there's no need for it, and for a rendering system like OpenGL that uses triangle direction to back-face-cull, changing the coordinate system from right-handed to left-handed would require changing back-face culling to match.

Stupid Matrix Tricks

There are a few nice mathematical properties of orthogonal matrices. First, the transpose of the matrix is its inverse. To demonstrate this, take an orthogonal matrix and multiply it by its transpose. You'll find that every component is either the dot product of two orthogonal vectors or a unit length vector with itself, thus it forms the 0s and 1s of an identity matrix.

That's cool right there - it means we can use a fast operation (transpose) instead of a slow operation (invert) on our upper left 3x3. It also means that the inverse of an orthogonal matrix is orthogonal too. (Since the inverse is the transpose, you can first invert your matrix by transposing, then multiply that new matrix by its transpose, which is the original, and multiply the components out - you'll find the same identity pattern again.)

If an orthogonal matrix's inverse is orthogonal, so is its transpose, and from that you can show that multiplying two orthogonal matrices forms a new orthogonal matrix - that is, batching up orthogonal matrix transforms preserves the orthognality. (You can calculate the components of the two matrices, and calculate the transpose from the multiplication of the transposes of the sources in opposite order. When you manipulate the algebra, you can show that the multiplication of the two orthogonal matrices has its transpose as its inverse too.)

If we know that an orthogonal matrix stays orthogonal when we multiply them, we can also show that affine matrices stay affine when we multiply them. (To do this, apply an affine matrix to another affine matrix and note that the orthogonal upper left 3x3 is only affected by the other matrices' upper 3x3, and the bottom row stays 0 0 0 1.) That's handy because it means that we can pre-multiply a pile of affine transform matrices and still know that it's affine, and that all of our tricks apply.

Camera Transforms

Camera transforms are funny beasts: when we move the camera, we do the opposite transforms of moving the model, and we do them in the opposite order. So while we positioned our model by first translating, then rotating, we position our camera by first rotating, then translating, and we do everything in the opposite order. (Consider if we want to position the camera at 10,0,0 in world space, we really achieve this by moving the model to -10,0,0.)

This means we can't recover information about our camera location directly from the modelview matrix. But thanks to all of the properties above, we can make camera angle recovery cheap.

Our orthogonal matrix contains the location of the old coordinate system's axes (in terms of the new coordinate system) as columns. But since its transpose is its inverse, it also contains the location of the new coordinate sytem's axes (in terms of the old coordinate system) as rows. Our model view matrix transforms from world space to camera space. So we have the axes of the camera space (that is, the "X" axis of camera space/eye space is an axis going to the right on your monitor) in terms of world space, right there in the rows. Thus we can use the first, second and third row of the upper left 3x3 of an affine transform matrix to know the billboard vectors of an affine modelview matrix.

The location of the camera is slightly trickier. The right most column isn't the negative of the position of the camera. Why not? Well, remember our "model positioning" transform was a translate-then-rotate matrix, with the translation in the right column. But camera transforms happen in the opposite order (negative-, then negative-translate). So the location of the camera is already "pre-rotated". Doh.

Fortunately we have the inverse of the rotation - it's just the transpose of the orthogonal 3x3 upper left of our affine matrix. So to restore the camera location from a model-view matrix we just need to multiply the upper right 1x3 column (the translation) by the transpose of the upper left 3x3 (the rotation) and then negate.

Having the camera direction and location in terms of the modelview matrix is handy when we have code that applies a pile of nested transforms. If we have gone from world to aircraft to engine coordinates (and the engine might be canted), we're in pretty deep. What are the billboarding vectors? How far from the engine are we? Fortunately we can get them right off of the modelview matrix.

EDIT: one quick note: an affine transform is still affine even if the upper left matrix isn't orthogonal; it only needs to be linear. But if we do have an orthogonal matrix in the upper left of our affine matrix, multiplying two of these "affine-orthogonal" matrices together does preserve both the affine-ness of the whole matrix and the orthogonality of the upper left. I'm not sure if there is an official name for an affine matrix with an orthogonal upper left.

## No comments:

## Post a Comment