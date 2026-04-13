---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_g_l_matrix/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3GLMatrix.h>`


|

A wrapper class for a 4x4 OpenGL matrix array.

This matrix wrapper is implemented as a class cluster design pattern. Different concrete implementation classes are provided to handle different underlying matrix data storage requirements. You do not need to be aware of the concrete classes, which aare selected and instantiated automatically by the class allocation methods.

| void CC3GLMatrix::copyMatrix:into: | ( | GLfloat * | srcGLMatrix, |
| [into] GLfloat * | destGLMatrix |
||
| ) | ` [static, virtual]` |

Copies all data from the source matrix to the destination matrix.

Both matrices must be a standard 4x4 OpenGL matrices in column-major order.

Extracts and returns the 'forward' direction vector from the rotation component of this matrix.

Extracts and returns the 'forward' direction vector from the rotation component of the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Extracts the rotation component of this matrix and returns it as a quaternion.

Extracts the rotation component of the specified matrix and returns it as a quaternion.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Extracts and returns the 'right' direction vector from the rotation component of this matrix.

Extracts and returns the 'right' direction vector from the rotation component of the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Extracts the rotation component of this matrix and returns it as an Euler rotation vector, assuming the rotations should be applied in YXZ order, which is the OpenGL default.

Each element of the returned rotation vector represents an Euler angle in degrees.

Extracts the rotation component of the specified matrix and returns it as an Euler rotation vector, assuming the rotations should be applied in YXZ order, which is the OpenGL default.

The matrix must be standard 4x4 OpenGL matrix in column-major order. Each element of the returned rotation vector represents an Euler angle in degrees.

Extracts the rotation component of the specified matrix and returns it as an Euler rotation vector, assuming the rotations should be applied in ZYX order.

The matrix must be standard 4x4 OpenGL matrix in column-major order. Each element of the returned rotation vector represents an Euler angle in degrees.

Extracts and returns the 'up' direction vector from the rotation component of this matrix.

Extracts and returns the 'up' direction vector from the rotation component of the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| id CC3GLMatrix::identity | ( | ) | ` [static, virtual]` |

Allocates and returns an initialized autoreleased instance with all elements populated as an identity matrix (ones on the diagonal, zeros elsewhere).

| id CC3GLMatrix::init | ( | ) | ` [virtual]` |

Returns an initialized instance with all elements set to zero.

| id CC3GLMatrix::initFromGLMatrix: | ( | GLfloat * | aGLMtx | ) | ` [virtual]` |

Returns an initialized instance with all elements copied from the specified GL matrix, which must be a standard 4x4 OpenGL matrix in column-major order.

| id CC3GLMatrix::initIdentity | ( | ) | ` [virtual]` |

Returns an initialized instance with all elements populated as an identity matrix (ones on the diagonal, zeros elsewhere).

| id CC3GLMatrix::initOnGLMatrix: | ( | GLfloat * | aGLMtx | ) | ` [virtual]` |

Returns an initialized instance that wraps the specified GL matrix, which must be a standard 4x4 OpenGL matrix in column-major order.

Changes to this matrix instance will change the underlying data passed here. This is useful when the matrix data was supplied and loaded by some other mechanism, such as a file loader. Rather than copying the data into a new matrix, resulting in two copies of the matrix data, a [CC3GLMatrix](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_g_l_matrix/) instance can be initialized to wrap the data.

| id CC3GLMatrix::initWithElements: | ( | GLfloat | e00, |
| [,] | ... |
||
| ) | ` [virtual]` |

Returns an initialized instance with elements populated from the specified variable arguments, which must consist of 16 elements in column-major order.

| BOOL CC3GLMatrix::invert | ( | ) | ` [virtual]` |

Inverts this matrix by using the algorithm of calculating the classical adjoint and dividing by the determinant.

The contents of the matrix are changed.

Not all matrices are invertable. Returns whether the matrix was inverted. If this method returns NO, then the matrix was not inverted and remains in the state it was when this method was invoked.

Matrix inversion is an computationally-expensive algorithm. If it is known that the matrix contains only rotation and translation, use the invertRigid method instead, which is between one and two orders of magnitude faster than this method.

Also, be aware that rounding inaccuracies accumulated during the inversion calculations can often result in the inverse matrix that is not affine (the bottom row of the matrix is not {0, 0, 0, 1}), even when the initial matrix was affine. These accumulated errors can often be significant when applied to the bottom row and will affect further calculations.

If it is known that a matrix represents an affine transformation, use the invertAffine method instead, which forces the bottom row back to {0, 0, 0, 1} after the inversion to maintain the inverted matrix as an affine transformation.

Affine transforms include all combinations of rotation, scaling, shearing, translation, and orthographic projection, so all matrices encountered while working with 3D graphics, with the exception of perspective projection, will be affine transforms. Unless you are working with the projection matrix, or a custom, non-affine matrix, it is recommended that you use invertAffine instead of this method.

| BOOL CC3GLMatrix::invert: | ( | GLfloat * | aGLMatrix | ) | ` [static, virtual]` |

Inverts the specified matrix by using the algorithm of calculating the classical adjoint and dividing by the determinant.

The contents of the matrix are changed. The matrix must be a standard 4x4 OpenGL matrix in column-major order.

Not all matrices are invertable. Returns whether the matrix was inverted. If this method returns NO, then the matrix was not inverted and remains in the state it was when this method was invoked.

Matrix inversion is an computationally-expensive algorithm. If it is known that the matrix contains only rotation and translation, use the invertRigid: method instead, which is between one and two orders of magnitude faster than this method.

Also, be aware that rounding inaccuracies accumulated during the inversion calculations can often result in the inverse matrix that is not affine (the bottom row of the matrix is not {0, 0, 0, 1}), even when the initial matrix was affine. These accumulated errors can often be significant when applied to the bottom row and will affect further calculations.

If it is known that a matrix represents an affine transformation, use the invertAffine: method instead, which forces the bottom row back to {0, 0, 0, 1} after the inversion to maintain the inverted matrix as an affine transformation.

Affine transforms include all combinations of rotation, scaling, shearing, translation, and orthographic projection, so all matrices encountered while working with 3D graphics, with the exception of perspective projection, will be affine transforms. Unless you are working with the projection matrix, or a custom, non-affine matrix, it is recommended that you use invertAffine: instead of this method.

| BOOL CC3GLMatrix::invertAffine | ( | ) | ` [virtual]` |

Inverts this matrix by using the algorithm of calculating the classical adjoint and dividing by the determinant.

The contents of the matrix are changed.

Not all matrices are invertable. Returns whether the matrix was inverted. If this method returns NO, then the matrix was not inverted and remains in the state it was when this method was invoked.

Matrix inversion is an computationally-expensive algorithm. If it is known that the matrix contains only rotation and translation, use the invertRigid method instead, which is between one and two orders of magnitude faster than this method.

This method uses the invert: method, but differs in that it assumes that the matrix represents an affine transform (the bottom row of the matrix is {0, 0, 0, 1}), and that accumulated inaccuracies in the inversion calculations should be removed from the bottom row of the resulting inverted matrix. After inversion, the bottom row of the inverted matrix is forced back to exactly {0, 0, 0, 1}.

This can be quite useful, as this row is particularly sensitive to the accumulation of inaccuracies and can often have a drastic impact on the accuracy of subsequent matrix and vector calculations. If it is known that a matrix represents an affine transformation, use this method instead of the invert method.

Affine transforms include all combinations of rotation, scaling, shearing, translation, and orthographic projection, so all matrices encountered while working with 3D graphics, with the exception of perspective projection, will be affine transforms. Unless you are working with the projection matrix, or a custom, non-affine matrix, it is recommended that you use this method instead of the invert method.

| BOOL CC3GLMatrix::invertAffine: | ( | GLfloat * | aGLMatrix | ) | ` [static, virtual]` |

Inverts the specified matrix by using the algorithm of calculating the classical adjoint and dividing by the determinant.

The contents of the matrix are changed. The matrix must be a standard 4x4 OpenGL matrix in column-major order.

Not all matrices are invertable. Returns whether the matrix was inverted. If this method returns NO, then the matrix was not inverted and remains in the state it was when this method was invoked.

Matrix inversion is an computationally-expensive algorithm. If it is known that the matrix contains only rotation and translation, use the invertRigid: method instead, which is between one and two orders of magnitude faster than this method.

This method uses the invert: method, but differs in that it assumes that the matrix represents an affine transform (the bottom row of the matrix is {0, 0, 0, 1}), and that accumulated inaccuracies in the inversion calculations should be removed from the bottom row of the resulting inverted matrix. After inversion, the bottom row of the inverted matrix is forced back to exactly {0, 0, 0, 1}.

This can be quite useful, as this row is particularly sensitive to the accumulation of inaccuracies and can often have a drastic impact on the accuracy of subsequent matrix and vector calculations. If it is known that a matrix represents an affine transformation, use this method instead of the invert: method.

Affine transforms include all combinations of rotation, scaling, shearing, translation, and orthographic projection, so all matrices encountered while working with 3D graphics, with the exception of perspective projection, will be affine transforms. Unless you are working with the projection matrix, or a custom, non-affine matrix, it is recommended that you use this method instead of the invert: method.

| void CC3GLMatrix::invertRigid | ( | ) | ` [virtual]` |

Inverts this matrix using transposition and translation.

The contents of this matrix are changed.

This method assumes that the matrix represents a rigid transformation, containing only rotation and translation. Use this method only if it is known that this is the case.

Inversion of a rigid transform matrix can be accomplished very quickly using transposition and translation, and is consistently one to two orders of magnitude faster than using either the invert or invertAffine methods. It is recommended that this method be used wherever possible.

| void CC3GLMatrix::invertRigid: | ( | GLfloat * | aGLMatrix | ) | ` [static, virtual]` |

Inverts the specified matrix using transposition and translation.

The contents of this matrix are changed. The matrix must be a standard 4x4 OpenGL matrix in column-major order.

This method assumes that the matrix represents a rigid transformation, containing only rotation and translation. Use this method only if it is known that this is the case.

Inversion of a rigid transform matrix can be accomplished very quickly using transposition and translation, and is consistently one to two orders of magnitude faster than using either the invert: or invertAffine: methods. It is recommended that this method be used wherever possible.

| void CC3GLMatrix::leftMultiply:byMatrix: | ( | GLfloat * | aGLMatrix, |
| [byMatrix] GLfloat * | anotherGLMatrix |
||
| ) | ` [static, virtual]` |

Multiplies a matrix by another matrix, where, in the matrix multiplication equation, the first matrix is on the right and the second matrix is on the left.

The contents of the first matrix are changed. The contents of the second matrix remain unchanged.

Both matrices must be a standard 4x4 OpenGL matrices in column-major order.

Multiplies a matrix by the specified matrix, where, in the matrix multiplication equation, the specified matrix is on the left and this matrix is on the right.

The contents of this matrix are changed. The contents of the specified matrix remain unchanged.

If the specified matrix is nil, it is treated as an identity matrix, and this matrix remains unchanged.

| id CC3GLMatrix::matrix | ( | ) | ` [static, virtual]` |

Allocates and returns an initialized autoreleased instance with all elements set to zero.

| id CC3GLMatrix::matrixByMultiplying:by: | ( |
|

` [static, virtual]`

Allocates and returns an initialized autoreleased instance that is the result of multiplying the first matrix by the second (m1 x m2).

Neither of the two input matrices is modified.

| id CC3GLMatrix::matrixFromGLMatrix: | ( | GLfloat * | aGLMtx | ) | ` [static, virtual]` |

Allocates and returns an initialized autoreleased instance with all elements copied from the specified GL matrix, which must be a standard 4x4 OpenGL matrix in column-major order.

| id CC3GLMatrix::matrixOnGLMatrix: | ( | GLfloat * | aGLMtx | ) | ` [static, virtual]` |

Allocates and returns an initialized autoreleased instance that wraps the specified GL matrix, which must be a standard 4x4 OpenGL matrix in column-major order.

Changes to this matrix instance will change the underlying data passed here. This is useful when the matrix data was supplied and loaded by some other mechanism, such as a file loader. Rather than copying the data into a new matrix, resulting in two copies of the matrix data, a [CC3GLMatrix](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_g_l_matrix/) instance can be initialized to wrap the data.

| id CC3GLMatrix::matrixWithElements: | ( | GLfloat | e00, |
| [,] | ... |
||
| ) | ` [static, virtual]` |

Allocates and returns an initialized autoreleased instance with elements populated from the specified variable arguments, which must consist of 16 elements in column-major order.

| void CC3GLMatrix::multiply:byMatrix: | ( | GLfloat * | aGLMatrix, |
| [byMatrix] GLfloat * | anotherGLMatrix |
||
| ) | ` [static, virtual]` |

Multiplies a matrix by another matrix, where, in the matrix multiplication equation, the first matrix is on the left and the second matrix is on the right.

The contents of the first matrix are changed. The contents of the second matrix remain unchanged.

Both matrices must be a standard 4x4 OpenGL matrices in column-major order.

Multiplies a matrix by the specified matrix, where, in the matrix multiplication equation, this matrix is on the left, and the specified matrix is on the right.

The contents of this matrix are changed. The contents of the specified matrix remain unchanged.

If the specified matrix is nil, it is treated as an identity matrix, and this matrix remains unchanged.

| void CC3GLMatrix::populate:fromFrustumLeft:andRight:andBottom:andTop:andNear:andFar: | ( | GLfloat * | aGLMatrix, |
| [fromFrustumLeft] GLfloat | left, |
||
| [andRight] GLfloat | right, |
||
| [andBottom] GLfloat | bottom, |
||
| [andTop] GLfloat | top, |
||
| [andNear] GLfloat | near, |
||
| [andFar] GLfloat | far |
||
| ) | ` [static, virtual]` |

Populates the specified matrix as a perspective projection matrix with the specified frustum dimensions.

The matrix must be a standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::populate:toLookAt:withEyeAt:withUp: | ( | GLfloat * | aGLMatrix, |
| [toLookAt]
|

` [static, virtual]`

Populates the specified matrix so that it will transform a vector between the targetLocation and the eyeLocation to point along the negative Z-axis, and transforms the specified upDirection to the positive Y-axis.

The matrix must be a standard 4x4 OpenGL matrix in column-major order.

This transform works in the direction from model-space to view-space, and therefore includes an implied inversion relative to the directToward:withUp: method. When applied to the camera, this has the effect of locating the camera at the eyeLocation and pointing it at the targetLocation, while orienting it so that 'up' appears to be in the upDirection, from the viewer's perspective.

| void CC3GLMatrix::populate:toPointTowards:withUp: | ( | GLfloat * | aGLMatrix, |
| [toPointTowards]
|

` [static, virtual]`

Populates the specified matrix so that it will transform a vector pointed down the negative Z-axis to point in the specified forwardDirection, and transforms the positive Y-axis to point in the specified upDirection.

The matrix must be a standard 4x4 OpenGL matrix in column-major order.

When applied to a targetting object (such as a camera, light, gun, etc), this has the effect of pointing that object in a direction and orienting it so that 'up' is in the upDirection.

This method works in model-space, and does not include an implied inversion. So, when applied to the camera, this matrix must be subsequently inverted to transform from model-space to view-space.

Populates this instance from data copied from the specified matrix instance.

If the specified matrix is nil, it is treated as the identity matrix, and this matrix will be populated as an identity matrix.

| void CC3GLMatrix::populateFromFrustumLeft:andRight:andBottom:andTop:andNear:andFar: | ( | GLfloat | left, |
| [andRight] GLfloat | right, |
||
| [andBottom] GLfloat | bottom, |
||
| [andTop] GLfloat | top, |
||
| [andNear] GLfloat | near, |
||
| [andFar] GLfloat | far |
||
| ) | ` [virtual]` |

Populates this matrix as a perspective projection matrix with the specified frustum dimensions.

| void CC3GLMatrix::populateFromGLMatrix: | ( | GLfloat * | aGLMtx | ) | ` [virtual]` |

Populates this instance from data copied from the specified GL matrix, which must be a standard 4x4 OpenGL matrix in column-major order.

Populates this instance with the rotation data provided by the specified quaternion.

The resulting matrix can be used to perform rotation operations on other matrices through matrix multiplication.

Populates this instance with the rotation data provided by the specified rotation vector.

Each element of the rotation vector represents an Euler angle in degrees, and rotation is performed in YXZ order, which is the OpenGL default.

The resulting matrix can be used to perform rotation operations on other matrices through matrix multiplication.

Populates this instance with the scaling data provided by the specified scaling vector.

The resulting matrix can be used to perform scaling operations on other matrices through matrix multiplication.

Populates this instance with the translation data provided by the specified translation vector.

The resulting matrix can be used to perform translation operations on other matrices through matrix multiplication.

| void CC3GLMatrix::populateIdentity | ( | ) | ` [virtual]` |

Populates this instance as an identity matrix (ones on the diagonal, zeros elsewhere).

| void CC3GLMatrix::populateOrtho:fromFrustumLeft:andRight:andBottom:andTop:andNear:andFar: | ( | GLfloat * | aGLMatrix, |
| [fromFrustumLeft] GLfloat | left, |
||
| [andRight] GLfloat | right, |
||
| [andBottom] GLfloat | bottom, |
||
| [andTop] GLfloat | top, |
||
| [andNear] GLfloat | near, |
||
| [andFar] GLfloat | far |
||
| ) | ` [static, virtual]` |

Populates the specified matrix as a parallel projection matrix with the specified frustum dimensions.

The matrix must be a standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::populateOrthoFromFrustumLeft:andRight:andBottom:andTop:andNear:andFar: | ( | GLfloat | left, |
| [andRight] GLfloat | right, |
||
| [andBottom] GLfloat | bottom, |
||
| [andTop] GLfloat | top, |
||
| [andNear] GLfloat | near, |
||
| [andFar] GLfloat | far |
||
| ) | ` [virtual]` |

Populates this matrix as a parallel projection matrix with the specified frustum dimensions.

| void CC3GLMatrix::populateToLookAt:withEyeAt:withUp: | ( |
|

` [virtual]`

Populates this matrix so that it will transform a vector between the targetLocation and the eyeLocation to point along the negative Z-axis, and transforms the specified upDirection to the positive Y-axis.

This transform works in the direction from model-space to view-space, and therefore includes an implied inversion relative to the directToward:withUp: method. When applied to the camera, this has the effect of locating the camera at the eyeLocation and pointing it at the targetLocation, while orienting it so that 'up' appears to be in the upDirection, from the viewer's perspective.

| void CC3GLMatrix::populateToPointTowards:withUp: | ( |
|

` [virtual]`

Populates this matrix so that it will transform a vector pointed down the negative Z-axis to point in the specified forwardDirection, and transforms the positive Y-axis to point in the specified upDirection.

When applied to a targetting object (such as a camera, light, gun, etc), this has the effect of pointing that object in a direction and orienting it so that 'up' is in the upDirection.

This method works in model-space, and does not include an implied inversion. So, when applied to the camera, this matrix must be subsequently inverted to transform from model-space to view-space.

| void CC3GLMatrix::populateZero | ( | ) | ` [virtual]` |

Populates this instance so that all elements are zero.

| void CC3GLMatrix::rotate:byQuaternion: | ( | GLfloat * | aGLMatrix, |
| [byQuaternion]
|

` [static, virtual]`

Rotates the specified matrix by the rotation specified in the given quaternion.

Since this operation rotates a matrix that potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within the specified matrix. If the matrix rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by the matrix.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::rotate:byX: | ( | GLfloat * | aGLMatrix, |
| [byX] GLfloat | degrees |
||
| ) | ` [static, virtual]` |

Rotates the specified matrix around the X-axis by the specified number of degrees.

Since this operation rotates a matrix that potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within the specified matrix. If the matrix rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by the matrix.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::rotate:byY: | ( | GLfloat * | aGLMatrix, |
| [byY] GLfloat | degrees |
||
| ) | ` [static, virtual]` |

Rotates the specified matrix around the Y-axis by the specified number of degrees.

Since this operation rotates a matrix that potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within the specified matrix. If the matrix rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by the matrix.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::rotate:byZ: | ( | GLfloat * | aGLMatrix, |
| [byZ] GLfloat | degrees |
||
| ) | ` [static, virtual]` |

Rotates the specified matrix around the Z-axis by the specified number of degrees.

Since this operation rotates a matrix that potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within the specified matrix. If the matrix rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by the matrix.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Rotates this matrix by the specified amount.

Each element of the rotation vector represents an Euler angle in degrees, and rotation is performed in YXZ order, which is the OpenGL default.

Since this matrix may potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within this matrix. If the existing rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by this matrix, which is almost always not the desired effect.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to this matrix.

Rotates this matrix by the rotation specified in the given quaternion.

Since this matrix may potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within this matrix. If the existing rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by this matrix, which is almost always not the desired effect.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to this matrix.

| void CC3GLMatrix::rotateByX: | ( | GLfloat | degrees | ) | ` [virtual]` |

Rotates this matrix around the X-axis by the specified number of degrees.

Since this matrix may potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within this matrix. If the existing rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by this matrix, which is almost always not the desired effect.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to this matrix.

| void CC3GLMatrix::rotateByY: | ( | GLfloat | degrees | ) | ` [virtual]` |

Rotates this matrix around the Y-axis by the specified number of degrees.

Since this matrix may potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within this matrix. If the existing rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by this matrix, which is almost always not the desired effect.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to this matrix.

| void CC3GLMatrix::rotateByZ: | ( | GLfloat | degrees | ) | ` [virtual]` |

Rotates this matrix around the Z-axis by the specified number of degrees.

Since this matrix may potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within this matrix. If the existing rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by this matrix, which is almost always not the desired effect.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to this matrix.

Rotates the specified matrix by the specified amount.

Each element of the rotation vector represents an Euler angle in degrees, and rotation is performed in YXZ order, which is the OpenGL default.

Since this operation rotates a matrix that potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within the specified matrix. If the matrix rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by the matrix.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Rotates the specified matrix by the specified amount.

Each element of the rotation vector represents an Euler angle in degrees, and rotation is performed in XYZ order.

Since this operation rotates a matrix that potentially already contains rotations, the new rotation is performed first, followed by the rotation already contained within the specified matrix. If the matrix rotations were performed first, the new rotation would be performed in the rotated coordinate system defined by the matrix.

In mathematical terms, the incoming rotation is converted to matrix form, and is left-multiplied to the specified matrix.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Scales this matrix in three dimensions by the specified scaling vector.

Non-uniform scaling can be achieved by specifying different values for each element of the scaling vector.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::scale:byX: | ( | GLfloat * | aGLMatrix, |
| [byX] GLfloat | scaleFactor |
||
| ) | ` [static, virtual]` |

Scales this matrix along the X-axis by the specified factor.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::scale:byY: | ( | GLfloat * | aGLMatrix, |
| [byY] GLfloat | scaleFactor |
||
| ) | ` [static, virtual]` |

Scales this matrix along the Y-axis by the specified factor.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::scale:byZ: | ( | GLfloat * | aGLMatrix, |
| [byZ] GLfloat | scaleFactor |
||
| ) | ` [static, virtual]` |

Scales this matrix along the Z-axis by the specified factor.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::scale:uniformlyBy: | ( | GLfloat * | aGLMatrix, |
| [uniformlyBy] GLfloat | scaleFactor |
||
| ) | ` [static, virtual]` |

Scales this matrix uniformly in three dimensions by the specified factor.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Scales this matrix in three dimensions by the specified scaling vector.

Non-uniform scaling can be achieved by specifying different values for each element of the scaling vector.

| void CC3GLMatrix::scaleByX: | ( | GLfloat | scaleFactor | ) | ` [virtual]` |

Scales this matrix along the X-axis by the specified factor.

| void CC3GLMatrix::scaleByY: | ( | GLfloat | scaleFactor | ) | ` [virtual]` |

Scales this matrix along the Y-axis by the specified factor.

| void CC3GLMatrix::scaleByZ: | ( | GLfloat | scaleFactor | ) | ` [virtual]` |

Scales this matrix along the Z-axis by the specified factor.

| void CC3GLMatrix::scaleUniformlyBy: | ( | GLfloat | scaleFactor | ) | ` [virtual]` |

Scales this matrix uniformly in three dimensions by the specified factor.

| void CC3GLMatrix::transform:translateBy:rotateBy:scaleBy: | ( | GLfloat * | aGLMatrix, |
| [translateBy]
|

` [static, virtual]`

Translates, rotates and scales (in that order) the specified matrix by the specified amounts.

Each element of the rotation vector represents an Euler angle in degrees, and rotation is performed in YXZ order, which is the OpenGL default. The matrix must be standard 4x4 OpenGL matrix in column-major order.

Transforms the specified direction vector using this matrix, and returns the transformed direction.

During multiplication, the fourth element of the direction vector is assumed to have a value of zero. This matrix and the original specified direction vector remain unchanged.

|

` [static, virtual]`

Transforms the specified direction vector using the specified matrix, and returns the transformed direction.

During multiplication, the fourth element of the location vector is assumed to have a value of zero. The matrix and the original specified direction vector remain unchanged. The matrix must be a standard 4x4 OpenGL matrix in column-major order.

Transforms the specified homogeneous vector using this matrix, and returns the transformed homogeneous vector.

This matrix and the original specified homogeneous vector remain unchanged.

|

` [static, virtual]`

Transforms the specified homogeneous vector using the specified matrix, and returns the transformed homogeneous vector.

The matrix and the original specified homogeneous vector remain unchanged. The matrix must be a standard 4x4 OpenGL matrix in column-major order.

Transforms the specified location vector using this matrix, and returns the transformed location.

During multiplication, the fourth element of the location vector is assumed to have a value of one. This matrix and the original specified location vector remain unchanged.

|

` [static, virtual]`

Transforms the specified location vector using the specified matrix, and returns the transformed location.

During multiplication, the fourth element of the location vector is assumed to have a value of one. The matrix and the original specified location vector remain unchanged. The matrix must be a standard 4x4 OpenGL matrix in column-major order.

Translates this matrix in three dimensions by the specified translation vector.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::translate:byX: | ( | GLfloat * | aGLMatrix, |
| [byX] GLfloat | distance |
||
| ) | ` [static, virtual]` |

Translates this matrix along the X-axis by the specified amount.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::translate:byY: | ( | GLfloat * | aGLMatrix, |
| [byY] GLfloat | distance |
||
| ) | ` [static, virtual]` |

Translates this matrix along the Y-axis by the specified amount.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

| void CC3GLMatrix::translate:byZ: | ( | GLfloat * | aGLMatrix, |
| [byZ] GLfloat | distance |
||
| ) | ` [static, virtual]` |

Translates this matrix along the Z-axis by the specified amount.

The matrix must be standard 4x4 OpenGL matrix in column-major order.

Translates this matrix in three dimensions by the specified translation vector.

| void CC3GLMatrix::translateBy:rotateBy:scaleBy: | ( |
|

` [virtual]`

Translates, rotates and scales (in that order) this matrix by the specified amounts.

Each element of the rotation vector represents an Euler angle in degrees, and rotation is performed in YXZ order, which is the OpenGL default.

| void CC3GLMatrix::translateByX: | ( | GLfloat | distance | ) | ` [virtual]` |

Translates this matrix along the X-axis by the specified amount.

| void CC3GLMatrix::translateByY: | ( | GLfloat | distance | ) | ` [virtual]` |

Translates this matrix along the Y-axis by the specified amount.

| void CC3GLMatrix::translateByZ: | ( | GLfloat | distance | ) | ` [virtual]` |

Translates this matrix along the Z-axis by the specified amount.

| void CC3GLMatrix::transpose | ( | ) | ` [virtual]` |

Transposes this matrix.

The contents of this matrix are changed.

| void CC3GLMatrix::transpose: | ( | GLfloat * | aGLMatrix | ) | ` [static, virtual]` |

Transposes the specified matrix.

The contents of the matrix are changed. The matrix must be a standard 4x4 OpenGL matrix in column-major order.

GLfloat* CC3GLMatrix::glMatrix` [read, assign]` |

Returns a pointer to the underlying array of 16 GLfloats stored in column-major order.

This can be passed directly into the standard OpenGL ES matrix functions.

BOOL CC3GLMatrix::isIdentity` [read, assign]` |

Indicates whether this matrix is an identity matrix.

This can be useful for short-circuiting many otherwise consumptive calculations. For example, this class is implemented so that, matrix multiplication is not performed as a raw calculation if one of the matrices is an identity matrix. In addition, transposition and inversion of an identity matrix are no-ops.

This values is set to YES after the matrix is initialized or populated as an identity matrix, or populated by an identity transform. It is set to NO whenever an operation is performed on this matrix that no longer results in it being an identity matrix.

This flag is only set to YES if the matrix is deliberately populated as an identity matrix. It will not be set to YES if an operation results in the contents of this matrix matching those of an identity matrix by accident.