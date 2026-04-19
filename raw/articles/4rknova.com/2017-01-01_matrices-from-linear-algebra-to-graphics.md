---
title: 'Matrices: From Linear Algebra to Graphics'
url: https://www.4rknova.com/blog/2017/01/01/matrix-xforms
author: Nikolaos Papadopoulos
published: '2017-01-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Matrices are a powerful mathematical tool, used everywhere from solving systems of equations to rendering 3D graphics. In this post, we’ll explore the key matrix operations: transpose, conjugate, inverse, determinant, and also see how matrices drive geometric transformations in computer graphics.

# Core Linear Algebra Operations

Below are the basic operations that a graphics programmers will typically come across.

## Transpose

The transpose of a matrix is obtained by flipping it over its diagonal. This means the rows become columns and the columns become rows.

\[A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}, \quad A^T = \begin{bmatrix} 1 & 3 \\ 2 & 4 \end{bmatrix}\]## Conjugate

The conjugate of a matrix is found by taking the complex conjugate of each entry. If the entries are real numbers, the conjugate is simply the same matrix.

\[A = \begin{bmatrix} 1+i & 2 \\ 3 & 4-i \end{bmatrix}, \quad \overline{A} = \begin{bmatrix} 1-i & 2 \\ 3 & 4+i \end{bmatrix}\]## Determinant

The determinant is a scalar value that can be computed from a square matrix. It is essential because it tells us whether a matrix is invertible (determinant is not 0).

### 2×2 matrix

\[\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc\]**Example:**

### 3×3 matrix

\[\det \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg)\]**Example:**

This matrix is singular (non-invertible).

## Inverse

The inverse of a square matrix \(A\) is another matrix \(A^{-1}\) such that:

\[A \cdot A^{-1} = A^{-1} \cdot A = I\]with

\[A^{-1} = \frac{1}{\det(A)} \operatorname{adj}(A)\] \[\operatorname{det}(A) \neq 0\]### 2×2 Matrix Formula

For a \(2 \times 2\) matrix:

\[A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}, \quad A^{-1} = \frac{1}{ad-bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}\]This works only if \(ad - bc \neq 0\).

### 3×3 Matrix, Adjugate / Cofactor Method

- Compute the determinant of \(A\). If \(\det(A) = 0\), the inverse does not exist.
- Compute the matrix of minors (determinants of smaller submatrices).
- Apply cofactor signs (checkerboard of \(+\) and \(-\) to form the cofactor matrix.
- Take the transpose of the cofactor matrix to get the adjugate.
- Divide the adjugate by \(\det(A)\):

### 3×3 Matrix, Gauss–Jordan Elimination

- Form the augmented matrix \([A \mid I]\).
- Use row operations to reduce the left side to the identity matrix.
- The right side then becomes \(A^{-1}\).

This method works for any square matrix and is commonly used in software.

# Matrix Transformations in Computer Graphics

The majority of geometric operations used in computer graphics can be performed using **matrix operations**. Compound transformations are implemented simply by multiplying matrices together, combining all operations into a single matrix.

## Identity

The identity matrix is the equivalent of a no-operation:

\[\begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]## Translation

To translate by \((x,y,z)\):

\[\begin{pmatrix} 1 & 0 & 0 & x \\ 0 & 1 & 0 & y \\ 0 & 0 & 1 & z \\ 0 & 0 & 0 & 1 \end{pmatrix}\]## Scaling

To scale by \((x,y,z)\):

\[\begin{pmatrix} x & 0 & 0 & 0 \\ 0 & y & 0 & 0 \\ 0 & 0 & z & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]## Rotation

Rotate \(\theta\) radians around the X axis:

\[\begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & \cos(\theta) & -\sin(\theta) & 0 \\ 0 & \sin(\theta) & \cos(\theta) & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]Rotate \(\theta\) radians around the Y axis:

\[\begin{pmatrix} \cos(\theta) & 0 & \sin(\theta) & 0 \\ 0 & 1 & 0 & 0 \\ -\sin(\theta) & 0 & \cos(\theta) & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]Rotate \(\theta\) radians around the Z axis:

\[\begin{pmatrix} \cos(\theta) & -\sin(\theta) & 0 & 0 \\ \sin(\theta) & \cos(\theta) & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]Note: 2D rotation is equivalent to rotation around the Z axis, so removing the last row and column gives a usable 2D rotation matrix.

## Mirroring

To mirror across the X axis:

\[\begin{pmatrix} -1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]To mirror across the Y axis:

\[\begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]To mirror across the Z axis:

\[\begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}\]