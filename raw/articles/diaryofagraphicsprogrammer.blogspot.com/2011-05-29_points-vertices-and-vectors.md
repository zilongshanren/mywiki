---
title: Points, Vertices and Vectors
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/05/points-vertices-and-vectors.html
author: Wolfgang Engel
published: '2011-05-29'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This post covers some facts about Points, Vertices and Vectors that might be useful. This is a collection of ideas to create a short math primer for engineers that want to explore computer graphics. The resulting material will be used in future computer graphics classes. Your feedback is highly welcome!



A 3D point is a location in space, in a 3D coordinate system. We can find a point


Two points define a line segment between them, three points define a triangle with corners at those points, and several interconnected triangles can be used to define the surface of an object; sometimes also called mesh.


Points that are used to define geometric entities like triangles, are often called vertices. In graphics programming, vertices are an array of structures or a structure of arrays and not only describe a position but also include other data like for example color, a normal vector or texture coordinates.


The difference of two points is a vector:




While a point is a reference to a location, a vector is the difference between two points which describes a direction and a distance -length-, or a displacement.


Like points, vectors can be represented by three coordinates. Those three values are retrieved by subtracting the tail from the vector from its head.


Δx = (x

Δy = (y

Δz = (z





Two vectors are equal if they have the same values. Thus considering a value as a difference of two points, there are any number of vectors with the same direction and length.






The difference between between points and vectors is reiterated by saying they live in a different space, the Euclidean space

and the vector space

. Read more in [Farin].


The primary reason for differentiating between points and vectors is to achieve geometric constructions which are coordinate independent. Such constructions are manipulations applied to objects that produce the same result regardless of the location of the coordinate origin.






A vector


![](http://www.codecogs.com/eq.latex? \ v = \left[ {\begin{array}{*{20}{c}} 2\\ 3\\ 4\\ 0\\ \end{array}} \right] then 2v = \left[ {\begin{array}{*{20}{c}} 4\\ 6\\ 8\\ 0\\ \end{array}}\right])



![](http://www.codecogs.com/eq.latex? \ v = \left[ {\begin{array}{*{20}{c}} n1\\ n2\\ n3\\ 0\\ \end{array}} \right]\, \, then \, \lambda \, v = \left[ {\begin{array}{*{20}{c}} \lambda n1\\ \lambda n2\\ \lambda n3\\ 0\\ \end{array}}\right]\, where \, [\lambda\, \in \,\mathbb{R}^3])



Similarly dividing the vector by 2 halves its components. The direction of the vector remains unchanged, only its magnitude changes.


The result of adding two vectors





Placing the tail of w to the head of






Similar to addition, the tail of the vector that should be subtracted -


Alternatively, by the parallelogram law, the vector sum can be seen as the diagonal of the parallelogram formed by the two vectors.





The vectors


All the vector additions and subtractions are coordinate independent operations, since vectors are defined as difference of points.




Representing both points and vectors with three coordinates can be confusing. Homogeneous coordinates are a useful tool to make the distinction explicit. Adding a fourth coordinate, named w, allows us to describe a direction or a vector by setting this coordinate to 0. In all other cases we have a point or location.


Dividing a homogeneous point [


The reason why this coordinate system is called "homogeneous" is because it is possible to transform functions f(x, y, z) into the form f(x/w, y/w, z/w) without disturbing the degree of the curve. This is useful in the field of projective geometry. For example a collection of 2D homogeneous points (x/t, y/t, t) exist on a xy-plane where t is the z-coordinate as illustrated in figure 6.







Homogeneous coordinates are also used to create a translation transform.


In game development, some math libraries have dedicated point and vector classes. The main distinction is made by setting the fourth channel to zero for vectors and one for points [Eberly].






The length or magnitude of a vector can be obtained by applying the Pythagorean Theorem. The opposite -b- and adjacent -a- side of a right-angled triangle represents orthogonal directions. The hypotenuse is the shortest path distance between those.


![](http://www.codecogs.com/eq.latex? \ a^2 + b^2 = c^2)






It helps thinking of the Pythagorean Theorem as a tool to compare "things" moving at right angles. For example if a is 3, b equals 4, then c equals 5 [Azad].


The Pythagorean Theorem can also be applied to right-angled triangles chained together.






![](http://www.codecogs.com/eq.latex? \ a^2 + b^2 = c^2)



![](http://www.codecogs.com/eq.latex? \ c^2 + d^2 = e^2)



Replacing

with

leads to


![](http://www.codecogs.com/eq.latex? \ a^2 + b^2 + d^2 = e^2)




is now written in three orthogonal components. Instead of lining the triangles flat, we can now tilt the green one a bit and therefore consider an additional dimension.





Renaming the sides to x, y and z instead of a, b and d we get:


![](http://www.codecogs.com/eq.latex? \ x^2 + y^2 + z^2 = distance^2)



This works with any number of dimensions.


The Pythagorean Theorem is the basis for computing distance between two points. Consider the following two triangles:






The distance from the tip of the blue triangle at coordinate (4, 3) to the tip of the green triangle at coordinate (8, 5) can be calculated by creating a virtual triangle between those points. Subtracting the points leads to a 2D vector.


Δx = (x

Δy = (y


![](http://www.codecogs.com/eq.latex? \ |v| = \sqrt {{{(\Delta x)}^2} + {{(\Delta y)}^2}}})



In this case


Δx = 8 - 4 = 4

Δy = 5 - 3 = 2


![](http://www.codecogs.com/eq.latex? \ |v| = \sqrt {{{(4)}^2} + {{(2)}^2}}})



![](http://www.codecogs.com/eq.latex? \ |v| = \sqrt {20})



![](http://www.codecogs.com/eq.latex? \ |v| = 4.47)



Extending the idea to three dimensions shows the well-known equation:


![](http://www.codecogs.com/eq.latex? \ |v| = \sqrt {{{(\Delta x)}^2} + {{(\Delta y)}^2 + {{(\Delta z)}^2}}})







A unit vector has a length or magnitude of 1. This is a useful property for vector multiplications, because those consider the magnitude of a vector and the computation time can be reduced if this magnitude is one (more on this later). A unit column vector might look like this:


![](http://www.codecogs.com/eq.latex? \ v = \left[ {\begin{array}{*{20}{c}} 1\\ 0\\ 0\\ 0\\ \end{array}}\right])



and


![](http://www.codecogs.com/eq.latex? \ |v| = 1)



Converting a vector into a unit form is called normalizing and is achieved by dividing a vector's components by its magnitude. Its magnitude is retrieved by applying the Pythagorean Theorem.


![](http://www.codecogs.com/eq.latex? |v| = \sqrt {{x^2} + {y^2} + {z^2}})



![](http://www.codecogs.com/eq.latex? \ {v_{unit}} = \frac{1}{{|v|}}\left[ {\begin{array}{*{20}{c}} x\\ y\\ z\\ \end{array}} \right])



An example might be:


![](http://www.codecogs.com/eq.latex? \ v = \left[ {\begin{array}{*{20}{c}} 1\\ 2\\ 3\\ 0\\ \end{array}}\right])



![](http://www.codecogs.com/eq.latex? |v| = \sqrt {{1^2} + {2^2} + {3^2}} = \sqrt {14})



![](http://www.codecogs.com/eq.latex? \ {v_{unit}} = \frac{1}{{\sqrt{14}}}\left[ {\begin{array}{*{20}{c}} 1\\ 2\\ 3\\ \end{array}} \right] \approx \left[ {\begin{array}{*{20}{c}} 0.267\\ 0.535\\ 0.802\\ 0 \end{array}}\right])





Now that we have investigated the scalar multiplication of vectors, vector addition and subtraction and unit vectors, we can combine those to permit the algebraic manipulation of vectors (read more at [Vince][Lengyel]). A tool that helps to achieve this is called Cartesian unit vectors. The three Cartesian unit vectors i, j and k are aligned with the x-, y- and z-axes.


![](http://www.codecogs.com/eq.latex? \ i = \left[ {\begin{array}{*{20}{c}} 1\\ 0\\ 0\\ 0\\ \end{array}}\right] j = \left[ {\begin{array}{*{20}{c}} 0\\ 1\\ 0\\ 0\\ \end{array}}\right] k = \left[ {\begin{array}{*{20}{c}} 0\\ 0\\ 1\\ 0\\ \end{array}}\right])



Any vector aligned with the x-, y- and z-axes can be defined by a scalar multiple of the unit vectors


By employing the rules of vector addition and subtraction, we can compose a vector


![](http://www.codecogs.com/eq.latex? \ R = ai + bj + ck)



This is equivalent to writing


![](http://www.codecogs.com/eq.latex? \ R = \left[ {\begin{array}{*{20}{c}} a\\ b\\ c\\ 0\\ \end{array}}\right])



The magnitude of R would then be computed as


![](http://www.codecogs.com/eq.latex? |R| = \sqrt {{a^2} + {b^2} + {c^2}})



Any pair of Cartesian vectors such as R and S can be combined as follows


![](http://www.codecogs.com/eq.latex? \ R = ai + bj + ck)



![](http://www.codecogs.com/eq.latex? \ S = di + ej + fk)



![](http://www.codecogs.com/eq.latex? \ R \pm S = (a \pm d)i + (b \pm e)j + (c \pm f)k)



An example would be


![](http://www.codecogs.com/eq.latex? \ R = 2i + 3j + 4k)



![](http://www.codecogs.com/eq.latex? \ S = 5i + 6j + 7k)



![](http://www.codecogs.com/eq.latex? \ R + S = 7i + 9j + 11k)



![](http://www.codecogs.com/eq.latex? \ |R + S| = \sqrt {{7^2} + {9^2} + {11^2}} \approx 15.84)





Vector multiplication provides some powerful ways of computing angles and surface orientations. While the multiplication of two scalars is a familiar operation, the multiplication of vectors is a multiplication of two 3D lines, which is not an easy operation to visualize. In vector analysis, there are generally two ways to multiply vectors: one results in a scalar value and the other one in a vector.




Multiplying the magnitude of two vectors |R| and |S| is a valid operation but it ignores the orientation of the vectors, which is one of their important features. Therefore we want to include the angles between the vectors. In case of the scalar product, this is done by projecting one vector onto the other.


![](http://altdevblogaday.com/wp-content/uploads/2011/04/dotProductGeometric-1024x605.jpg)





The projection of


![](http://www.codecogs.com/eq.latex? \ |R|cos\beta)



Then we can multiply the projected length of


![](http://www.codecogs.com/eq.latex? \ R \cdot S = |S||R|cos\beta)



or commonly written


![](http://www.codecogs.com/eq.latex? \ R \cdot S = |R||S|cos\beta)



The

symbol is used to represent scalar multiplications and to distinguish it from the vector product, which employs the

symbol. Because of this symbol, the scalar product is often referred to as the dot product. This geometric interpretation of the scalar product shows that in case the magnitude of

. The following figure shows a number of dot product scenarios.






The geometric representation of the dot product is useful to imagine how it works but it doesn't map well to computer hardware. The algebraic representation maps better to computer hardware and is calculated with the help of Cartesian components:

![](http://www.codecogs.com/eq.latex? \ R = R_xi + R_yj + R_zk)



![](http://www.codecogs.com/eq.latex? \ S = S_xi + S_yj + S_zk)



![](http://www.codecogs.com/eq.latex? \\ R \cdot S = (R_xi + R_yj + R_zk) \cdot (S_xi + S_yj + S_zk) \\ = R_xi \cdot (S_xi + S_yj + S_zk) + R_yi \cdot (S_xi + S_yj + S_zk) + R_zi \cdot (S_xi + S_yj + S_zk))



![](http://www.codecogs.com/eq.latex? \\ R \cdot S = R_xS_xi \cdot i + R_xS_yi \cdot j + R_xS_zi \cdot k \\ + R_yS_xj \cdot i + R_yS_yj \cdot j + R_yS_zj \cdot k \\ + R_zS_xk \cdot i + R_zS_yk \cdot j + R_zS_zk \cdot k)



There are various dot product terms such as

etc. in this equation. With the help of the geometric representation of the dot product it can be determined that terms that are mutually perpendicular like

are zero because the cosinus of 90 degrees is zero. This leads to


![](http://www.codecogs.com/eq.latex? \\ R \cdot S = R_xS_xi \cdot i + R_yS_yj \cdot j + R_zS_zk \cdot k)



Finally, terms with two vectors that are parallel to themselve lead to a value of one because the cosinus of a degree of zero is one. Additionally the Cartesian vectors are all unit vectors, which leads to


![](http://www.codecogs.com/eq.latex? \\ i \cdot i = |i||i|cos(0)= 1)



So we end up with the familiar equation


![](http://www.codecogs.com/eq.latex? \\ R \cdot S = R_xS_x + R_yS_y + R_zS_z)



An example:


![](http://www.codecogs.com/eq.latex? \ R = \left[ {\begin{array}{*{20}{c}} 2\\ 0\\ 4\\ 0\\ \end{array}}\right] S = \left[ {\begin{array}{*{20}{c}} 5\\ 6\\ 10\\ 0\\ \end{array}}\right])



The algebraic representation results in:








The geometric representation starts out with:


![](http://www.codecogs.com/eq.latex? \\ R \cdot S= |R||S|cos \beta)



![](http://www.codecogs.com/eq.latex? |R| = \sqrt {{2^2} + {0^2} + {4^2}} \approx 4.472)



![](http://www.codecogs.com/eq.latex? |S| = \sqrt {{5^2} + {6^2} + {10^2}} \approx 12.689)



Solving for the angle between the vectors by plugging in the result of the algebraic representation:


![](http://www.codecogs.com/eq.latex? \\ R \cdot S= |R||S|cos \beta = 2 *5 + 0 * 6 + 4 * 10 = 50)



![](http://www.codecogs.com/eq.latex? \\ R \cdot S= 12.689 * 4.472 cos \beta = 50)



![](http://www.codecogs.com/eq.latex? \\ cos \beta = \frac{50}{12.689 * 4.472} \approx 0.8811)



Solving for

leads to the angle between the two vectors:


![](http://www.codecogs.com/eq.latex? \\ \beta = cos^{-1} (0.8811) \approx 28.22^\circ)



The resulting angle will be always between

and

, because, as the angle between two vectors increases beyond

the returned angle

is always the smallest angle associated with the geometry.




Many games utilize the Blinn-Phong lighting model (see


Let's assume our light source is located in our reference space for lighting at (20, 30, 40), while our normal vector is normalized and located at (0, 11, 0). The point where the intensity of illumination is measured is located at (0, 10, 0).






The light and normal vector are calculated by subtracting the position of the point where the intensity is measured -representing their tails- from their heads.


![](http://www.codecogs.com/eq.latex? \ L = \left[ {\begin{array}{*{20}{c}} 20 - 0\\ 30 - 10\\ 40 - 0\\ 0\\ \end{array}}\right] N = \left[ {\begin{array}{*{20}{c}} 0\\ 11 - 10\\ 0\\ 0\\ \end{array}}\right])



![](http://www.codecogs.com/eq.latex? \\ L \cdot N= |L||N|cos \beta = 20 * 0 + 20 * 1 + 40 * 0 = 20)



![](http://www.codecogs.com/eq.latex? |L| = \sqrt {{20^2} + {20^2} + {40^2}} \approx 48.9898)



![](http://www.codecogs.com/eq.latex? |N| = 1)



![](http://www.codecogs.com/eq.latex? \\ L \cdot N= 48.9898 * 1.0 * cos \beta = 20)



![](http://www.codecogs.com/eq.latex? \\ cos \beta = \frac{20}{48.9898 * 1.0} \approx 0.4082)



Instead of using the original light vector, the following scalar product normalizes the light vector first, before using it in the lighting equation.


![](http://www.codecogs.com/eq.latex? \ {L_{unit}} = \frac{1}{{|L|}}\left[ {\begin{array}{*{20}{c}} x\\ y\\ z\\ \end{array}} \right])



![](http://www.codecogs.com/eq.latex? \ {L_{unit}} = \frac{1}{{48.9898}}\left[ {\begin{array}{*{20}{c}} 20\\ 20\\ 40\\ 0\\ \end{array}} \right] \approx \left[ {\begin{array}{*{20}{c}} 0.4082\\ 0.4082\\ 0.8165\\ 0 \end{array}}\right])



To test if the light vectors magnitude is one:

![](http://www.codecogs.com/eq.latex? |L| = \sqrt {{0.4082^2} + {0.4082^2} + {0.8165^2}} \approx 1.0)



Plugging the unit light vector and the unit normal vector into the algebraic representation of the scalar product.


![](http://www.codecogs.com/eq.latex? \\ L \cdot N= |L||N|cos \beta = 0.4082 * 0 + 0.4082 * 1 + 0.8165 * 0 = 0.4082)



Now solving the geometrical representation for the cosine of the angle.


![](http://www.codecogs.com/eq.latex? \\ L \cdot N= |L||N|cos \beta = 0.4082)



![](http://www.codecogs.com/eq.latex? \\ cos \beta = \frac{0.4082}{1.0 * 1.0} = 0.4082)



In case the light and the normal vector are unit vectors, the result of the algebraic scalar product calculation equals the cosinus of the angle. The algebraic scalar product is implemented in the dot product intrinsic available for the CPU and GPU. In other words, in case the involved vectors are unit vectors, a processor can calculate the cosine of the angle faster. This is the reason why normalized vectors might be more efficient in programming computer hardware.


Following Lambert's law, the intensity of illumination on a diffuse surface is proportional to the consine of the angle between the surface normal and the light source direction. That means that the point at (0, 10, 0) receives about 0.4082 of the original light intensity at (20, 30, 40) (attenuation is not considered in this example).


Coming back to image 12, in case, the unit light vector would have a y component that is one or minus one and therefore its x and y component would be zero, it would point in the same or opposite direction as the normal and therefore the last equation would result in one or minus one. If the unit light vector would have a z or x component equaling to one and therefore the other components would be zero, those equations would result in zero.




Like the scalar product, the vector or cross product depends on the modulus of two vectors and the angle between them, but the result of the vector product is essentially different: it is another vector, at right angles to both the original vectors.


![](http://www.codecogs.com/eq.latex? \\ R \times S = T)



and


![](http://www.codecogs.com/eq.latex? \\ |T| = |R||S|sin\theta)



For an understanding of the vector product







The angle

between the directions of the vectors suffices

. There are two possible choices for the direction of the vector, each the negation of the other; the one chosen here is determined by the right-hand rule. Hold your right hand so that your forefinger points forward, your middle finger points out to the left, and your thumb points up. If you roughly align your forefinger with






The resulting vector of the cross product is perpendicular to


![](http://www.codecogs.com/eq.latex? \\ R \cdot T = 0)



and


![](http://www.codecogs.com/eq.latex? \\ S \cdot T = 0)



This makes the vector product an ideal way of computing normals. The two vectors


Let's multiply two vectors together using the vector product.


![](http://www.codecogs.com/eq.latex? \ R = R_xi + R_yj + R_zk)


![](http://www.codecogs.com/eq.latex? \ S = S_xi + S_yj + S_zk)



![](http://www.codecogs.com/eq.latex? \\ R \times S = (R_xi + R_yj + R_zk) \times (S_xi + S_yj + S_zk) \\ = R_xi \times (S_xi + S_yj + S_zk) + R_yi \times (S_xi + S_yj + S_zk) + R_zi \times (S_xi + S_yj + S_zk))



![](http://www.codecogs.com/eq.latex? \\ R \times S = R_xS_xi \times i + R_xS_yi \times j + R_xS_zi \times k \\ + R_yS_xj \times i + R_yS_yj \times j + R_yS_zj \times k \\ + R_zS_xk \times i + R_zS_yk \times j + R_zS_zk \times k)



There are various vector product terms such as

etc. in this equation. The terms

will result in a vector whose magnitude is zero, because the angle between those vectors is

, and sin

. This leaves


![](http://www.codecogs.com/eq.latex? \\ R \times S = R_xS_yi \times j + R_xS_zi \times k + R_yS_xj \times i + R_yS_zj \times k + R_zS_xk \times i + R_zS_yk \times j)



The other products between the unit vectors can be reasoned as:


![](http://www.codecogs.com/eq.latex? \\i \times j = k \\ j \times i = -k \\ j \times k = i \\ k \times j = -i \\ k \times i = j \\ i \times k = -j)



Those results show, that the commutative multiplication law is not applicable to vector products. In other words


![](http://www.codecogs.com/eq.latex? \\i \times j != j \times i)



Applying those findings reduces the vector product term to


![](http://www.codecogs.com/eq.latex? \\ R \times S = R_xS_yk - R_xS_zj - R_yS_xk + R_yS_zi + R_zS_xj - R_zS_yi)



Now re-grouping the equation to bring like terms together leads to:


![](http://www.codecogs.com/eq.latex? \\ R \times S = (R_yS_z - R_zS_y)i + (R_zS_x - R_xS_z)j + (R_xS_y - R_yS_x)k)



To achieve a visual pattern for remembering the vector product, some authors reverse the sign of the


![](http://www.codecogs.com/eq.latex? \\ R \times S = (R_yS_z - R_zS_y)i - (R_xS_z - R_zS_x)j + (R_xS_y - R_yS_x)k)



Re-writing the vector product as determinants might help to memorize it as well.


![](http://www.codecogs.com/eq.latex? \\ R \times S = \begin{vmatrix} R_y & R_z \\ S_y & S_z \end{vmatrix} i - \begin{vmatrix} R_x & R_z \\ S_x & S_z\end{vmatrix}j + \begin{vmatrix} R_x & R_y \\ S_x & S_y \end{vmatrix}k)



A 2x2 determinant is the difference between the product of the diagonal terms. With determinants a "recipe" for a vector product consists of the following steps:


1. Write the two vectors that should be multiplied as Cartesian vectors


![](http://www.codecogs.com/eq.latex? \ R = R_xi + R_yj + R_zk)



![](http://www.codecogs.com/eq.latex? \ S = S_xi + S_yj + S_zk)



2. Write the cross product of those two vectors in determinant form, if this helps to memorize the process; otherwise skip to step 3.


![](http://www.codecogs.com/eq.latex? \\ R \times S = \begin{vmatrix} R_y & R_z \\ S_y & S_z \end{vmatrix} i - \begin{vmatrix} R_x & R_z \\ S_x & S_z\end{vmatrix}j + \begin{vmatrix} R_x & R_y \\ S_x & S_y \end{vmatrix}k)



3. Then compute by plugging in the numbers into


![](http://www.codecogs.com/eq.latex? \\ R \times S = (R_yS_z - R_zS_y)i - (R_xS_z - R_zS_x)j + (R_xS_y - R_yS_x)k)



A simple example of a vector product calculation is to show that the assumptions that were made above, while simplifying the vector product, hold up.


![](http://www.codecogs.com/eq.latex? \\i \times j = k \\ j \times i = -k \\ j \times k = i \\ k \times j = -i \\ k \times i = j \\ i \times k = -j)



To show that there is a sign reversal when the vectors are reversed

, let's calculate the cross product of those terms.


![](http://www.codecogs.com/eq.latex? \ i = 1i + 0j + 0k)



![](http://www.codecogs.com/eq.latex? \ k = 0i + 0j + 1k)



![](http://www.codecogs.com/eq.latex? \\ i \times k = \begin{vmatrix} 0 & 0 \\ 0 & 1 \end{vmatrix} i - \begin{vmatrix} 1 & 0 \\ 0 & 1\end{vmatrix}j + \begin{vmatrix} 1 & 0 \\ 0 & 0 \end{vmatrix}k)



![](http://www.codecogs.com/eq.latex? \\ i \times k = (0 * 1 - 0 * 0)i - (1 * 1 - 0 * 0)j + (1 * 0 - 0 * 0)k)



The i and k terms are both zero, but the j term is -1, which makes

. Now reversing the vector product


![](http://www.codecogs.com/eq.latex? \ k = 0i + 0j + 1k)



![](http://www.codecogs.com/eq.latex? \ i = 1i + 0j + 0k)



![](http://www.codecogs.com/eq.latex? \\ k \times i = \begin{vmatrix} 0 & 1 \\ 0 & 0 \end{vmatrix} i - \begin{vmatrix} 0 & 1 \\ 1 & 0\end{vmatrix}j + \begin{vmatrix} 0 & 0 \\ 1 & 0 \end{vmatrix}k)



![](http://www.codecogs.com/eq.latex? \\ k \times i = (0 * 0 - 1 * 0)i - (0 * 0 - 1 * 1)j + (0 * 0 - 0 * 1)k)



Which shows![](http://www.codecogs.com/eq.latex? \\k \times i = j)





Image 16 shows a triangle with vertices defined in anti-clockwise order. The side pointing towards the viewer is defined as the visible side in this scene. That means that the normal is expected to point roughly in the direction of where the viewer is located.





The vertices of the triangle are:


P1 (0, 2, 1)

P2 (0, 1, 4)

P3 (2, 0, 1)


The two vectors


Δx = (x

Δy = (y

Δz = (z


Bringing the result into the Cartesian form


![](http://www.codecogs.com/eq.latex? \ R = 0-2i + 2-0j + 1-1k)



![](http://www.codecogs.com/eq.latex? \ S = 0-2i + 1-0j + 4-1k)



![](http://www.codecogs.com/eq.latex? \\ R \times S = \begin{vmatrix} 2 & 0 \\ 1 & 3 \end{vmatrix} i - \begin{vmatrix} -2 & 0 \\ -2 & 3\end{vmatrix}j + \begin{vmatrix} -2 & 2 \\ -2 & 1 \end{vmatrix}k)



![](http://www.codecogs.com/eq.latex? \\ R \times S = (2 * 3 - 0 * 1)i - (-2 * 3 - 0 * -2)j + (-2 * 1 - 2 * -2)k)


![](http://www.codecogs.com/eq.latex? \\ N = 6i + 6j + 2k)



![](http://www.codecogs.com/eq.latex? |N| = \sqrt {{6^2} + {6^2} + {2^2}})


![](http://www.codecogs.com/eq.latex? |N| = \sqrt {{76}} = 8.7178)



![](http://www.codecogs.com/eq.latex? \ {N_{unit}} = \frac{1}{{|N|}}\left[ {\begin{array}{*{20}{c}} 6\\ 6\\ 2\\ \end{array}} \right])


![](http://www.codecogs.com/eq.latex? \ {N_{unit}} = \frac{1}{{8.7178}}\left[ {\begin{array}{*{20}{c}} 6\\ 6\\ 2\\ \end{array}} \right] = \left[ {\begin{array}{*{20}{c}} 0.6882\\ 0.6882\\ 0.2294\\ \end{array}} \right])





It is a common mistake to believe that if


![](http://www.codecogs.com/eq.latex? \\ |T| = |R||S|sin\theta)



Please read in [Van Verth] about CPU implementation details.



The vector product might be used to determine the area of a parallelogram or a triangle (with the vertices at P






The height h is

, therefore the area of the parallelogram is


![](http://www.codecogs.com/eq.latex? \\ area = |R|*h = |R||S|sin\theta)



This equals the magnitude of the cross product vector


area of parallelogram =![](http://www.codecogs.com/eq.latex? \\ |T|)


area of triangle =![](http://www.codecogs.com/eq.latex? \\ \frac{1}{{2}}|T|)



or


area of triangle =![](http://www.codecogs.com/eq.latex? \\ \frac{1}{{2}}|R \times S|)



To compute the surface area of a mesh constructed from triangles or parallelograms, the magnitude of its non-normalized normals can be used like this.


![](http://www.codecogs.com/eq.latex? \\ \frac{MagnitudeOfAllNormals }{{2}})



The sign of the magnitude of the normal shows if the vertices are clockwise or counter-clockwise oriented.





[Azad] Kalid Azad, "Math Better Eplained",


[Eberly] David H. Eberly, "3D Game Engine Design", p. 15, 2nd Edition, Morgan Kauffman 2007


[Farin] Gerald Farin, Dianne Hansford, "The Geometry Toolbox - For Graphics and Modeling", p. 16, AK Peters 1998


[Lengyel] Eric Lengyel, Mathematics for 3D Game Programming and Computer Graphics, Second Edition, Charles River Media 2003


[Vince] John Vince, "Mathematics for Computer Graphics", Springer, 3rd Edition, 2010


[Van Verth] James M. Van Verth, Lars M. Bishop, "Essential Mathematics for Games & Interactive Applications - A Programmer's Guide", Morgan Kaufmann 2004

**Points**A 3D point is a location in space, in a 3D coordinate system. We can find a point

*P*with coordinates [*P*x,*P*y,*P*z] by starting from the origin at [0, 0, 0] and moving the distance*P*x,*P*yand*P*zalong the x, y and z axis.Two points define a line segment between them, three points define a triangle with corners at those points, and several interconnected triangles can be used to define the surface of an object; sometimes also called mesh.

Points that are used to define geometric entities like triangles, are often called vertices. In graphics programming, vertices are an array of structures or a structure of arrays and not only describe a position but also include other data like for example color, a normal vector or texture coordinates.

The difference of two points is a vector:

**V**=*P*-*Q***Vectors**While a point is a reference to a location, a vector is the difference between two points which describes a direction and a distance -length-, or a displacement.

Like points, vectors can be represented by three coordinates. Those three values are retrieved by subtracting the tail from the vector from its head.

Δx = (x

h- xt)Δy = (y

h- yt)Δz = (z

h- zt)![Vector components](http://altdevblogaday.com/wp-content/uploads/2011/04/Vector-1024x563.jpg)

![Vector components](http://altdevblogaday.com/wp-content/uploads/2011/04/Vector-1024x563.jpg)

*Figure 1 - Vector components Δx, Δy and Δz*Two vectors are equal if they have the same values. Thus considering a value as a difference of two points, there are any number of vectors with the same direction and length.

![](http://altdevblogaday.com/wp-content/uploads/2011/04/InstancesOfVector-1024x590.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/InstancesOfVector-1024x590.jpg)

*Figure*2 - Instances of one vectorThe difference between between points and vectors is reiterated by saying they live in a different space, the Euclidean space

The primary reason for differentiating between points and vectors is to achieve geometric constructions which are coordinate independent. Such constructions are manipulations applied to objects that produce the same result regardless of the location of the coordinate origin.

**Scalar Multiplication, Addition and Subtraction of Vectors**A vector

**V**can be multiplied by a scalar. Multiplying by 2 doubles the vectors components.Similarly dividing the vector by 2 halves its components. The direction of the vector remains unchanged, only its magnitude changes.

The result of adding two vectors

**V**and**W**can be obtained geometrically.![](http://altdevblogaday.com/wp-content/uploads/2011/04/VectorAddition.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/VectorAddition.jpg)

*Figure*3 - Adding two vectorsPlacing the tail of w to the head of

**V**leads to the resulting vector, going from**V**'s tail to**W**'s head. In a similar manner vector subtraction can visualized.![](http://altdevblogaday.com/wp-content/uploads/2011/04/VectorSubtraction.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/VectorSubtraction.jpg)

*Figure*4 - Subtracting two vectorsSimilar to addition, the tail of the vector that should be subtracted -

**W**- is placed to the head of**V**. Then the vector that should be subtracted is negated. The resulting vector runs from**V**'s tail to**W**'s head.Alternatively, by the parallelogram law, the vector sum can be seen as the diagonal of the parallelogram formed by the two vectors.

![](http://altdevblogaday.com/wp-content/uploads/2011/04/VectorParallelogrammRule.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/VectorParallelogrammRule.jpg)

*Figure*5 - Parallelogram ruleThe vectors

**V**-**W**and**V**+**W**are the diagonals of the parallelogram defined by**V**and**W**. Arithmetically, vectors are added or subtracted by adding or subtracting the components of each vector.All the vector additions and subtractions are coordinate independent operations, since vectors are defined as difference of points.

**Homogeneous Coordinates**Representing both points and vectors with three coordinates can be confusing. Homogeneous coordinates are a useful tool to make the distinction explicit. Adding a fourth coordinate, named w, allows us to describe a direction or a vector by setting this coordinate to 0. In all other cases we have a point or location.

Dividing a homogeneous point [

*P*x,*P*y,*P*z,*P*w] by the w component leads to the corresponding 3D point. If the w component equals to zero, the point would be infinitely far away, which is then interpreted as a direction. Using any non-zero value for w, will lead to points all corresponding to the same 3D point. For example the point (3, 4, 5) has homogeneous coordinates (6, 8, 10, 2) or (12, 16, 20, 4).The reason why this coordinate system is called "homogeneous" is because it is possible to transform functions f(x, y, z) into the form f(x/w, y/w, z/w) without disturbing the degree of the curve. This is useful in the field of projective geometry. For example a collection of 2D homogeneous points (x/t, y/t, t) exist on a xy-plane where t is the z-coordinate as illustrated in figure 6.

![](http://altdevblogaday.com/wp-content/uploads/2011/04/ProjectiveGeometry-1024x592.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/ProjectiveGeometry-1024x592.jpg)

*Figure*6 - 2D homogenous coodinates can be visualized as a plane in 3D space*Figure*6 shows a triangle on the t = 1 plane, and a similar triangle much larger on a distant plane. This creates an arbitrary xy plane in three dimensions. The t- or z-coordinate of the plane is immaterial because the x- and y-coordinates are eventually scaled by t.Homogeneous coordinates are also used to create a translation transform.

In game development, some math libraries have dedicated point and vector classes. The main distinction is made by setting the fourth channel to zero for vectors and one for points [Eberly].

**Pythagorean Theorem**The length or magnitude of a vector can be obtained by applying the Pythagorean Theorem. The opposite -b- and adjacent -a- side of a right-angled triangle represents orthogonal directions. The hypotenuse is the shortest path distance between those.

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheorem.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheorem.jpg)

*Figure*7 - Pythagorean TheoremIt helps thinking of the Pythagorean Theorem as a tool to compare "things" moving at right angles. For example if a is 3, b equals 4, then c equals 5 [Azad].

The Pythagorean Theorem can also be applied to right-angled triangles chained together.

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheoremChainedTogether-814x1024.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheoremChainedTogether-814x1024.jpg)

*Figure*8 - Pythagorean Theorem with two triangles chained togetherReplacing

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheoremin3D-1024x605.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheoremin3D-1024x605.jpg)

*Figure*9 - Pythagorean Theorem in 3DRenaming the sides to x, y and z instead of a, b and d we get:

This works with any number of dimensions.

The Pythagorean Theorem is the basis for computing distance between two points. Consider the following two triangles:

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheoremDistance-1024x636.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/PythagoreanTheoremDistance-1024x636.jpg)

*Figure*10 - Pythagorean Theorem used for distance calculationsThe distance from the tip of the blue triangle at coordinate (4, 3) to the tip of the green triangle at coordinate (8, 5) can be calculated by creating a virtual triangle between those points. Subtracting the points leads to a 2D vector.

Δx = (x

head- xtail)Δy = (y

head- ytail)In this case

Δx = 8 - 4 = 4

Δy = 5 - 3 = 2

Extending the idea to three dimensions shows the well-known equation:

**Unit Vectors**A unit vector has a length or magnitude of 1. This is a useful property for vector multiplications, because those consider the magnitude of a vector and the computation time can be reduced if this magnitude is one (more on this later). A unit column vector might look like this:

and

Converting a vector into a unit form is called normalizing and is achieved by dividing a vector's components by its magnitude. Its magnitude is retrieved by applying the Pythagorean Theorem.

An example might be:

**Cartesian Unit Vectors**Now that we have investigated the scalar multiplication of vectors, vector addition and subtraction and unit vectors, we can combine those to permit the algebraic manipulation of vectors (read more at [Vince][Lengyel]). A tool that helps to achieve this is called Cartesian unit vectors. The three Cartesian unit vectors i, j and k are aligned with the x-, y- and z-axes.

Any vector aligned with the x-, y- and z-axes can be defined by a scalar multiple of the unit vectors

**i**,**j**and**k**. For example a vector 15 units long aligned with the y-axis is simply 15**j**. A vector 25 units long aligned with the z axis is 25**k**.By employing the rules of vector addition and subtraction, we can compose a vector

**R**by summing three Cartesian unit vectors as follows.This is equivalent to writing

**R**asThe magnitude of R would then be computed as

Any pair of Cartesian vectors such as R and S can be combined as follows

An example would be

**Vector Multiplication**Vector multiplication provides some powerful ways of computing angles and surface orientations. While the multiplication of two scalars is a familiar operation, the multiplication of vectors is a multiplication of two 3D lines, which is not an easy operation to visualize. In vector analysis, there are generally two ways to multiply vectors: one results in a scalar value and the other one in a vector.

**Scalar or Dot Product**Multiplying the magnitude of two vectors |R| and |S| is a valid operation but it ignores the orientation of the vectors, which is one of their important features. Therefore we want to include the angles between the vectors. In case of the scalar product, this is done by projecting one vector onto the other.

![](http://altdevblogaday.com/wp-content/uploads/2011/04/dotProductGeometric-1024x605.jpg)

*Figure*11 - Projecting**R**on**S**The projection of

**R**on**S**creates the basis for the scalar product, because it takes into account their relative orientation. The length of**R**on**S**isThen we can multiply the projected length of

**R**with the magnitude of**S**or commonly written

The

**R**and**S**is one -in other words they are unit vectors- the calculation of the scalar product only relies on![](http://altdevblogaday.com/wp-content/uploads/2011/04/dotProductVectors-1024x661.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/04/dotProductVectors-1024x661.jpg)

*Figure*12 - Dot productThe geometric representation of the dot product is useful to imagine how it works but it doesn't map well to computer hardware. The algebraic representation maps better to computer hardware and is calculated with the help of Cartesian components:

There are various dot product terms such as

Finally, terms with two vectors that are parallel to themselve lead to a value of one because the cosinus of a degree of zero is one. Additionally the Cartesian vectors are all unit vectors, which leads to

So we end up with the familiar equation

An example:

The algebraic representation results in:

The geometric representation starts out with:

Solving for the angle between the vectors by plugging in the result of the algebraic representation:

Solving for

The resulting angle will be always between

**Scalar Product in Lighting Calculations**Many games utilize the Blinn-Phong lighting model (see

[Wikipedia](http://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_shading_model); ignore the code on this page). A part of the diffuse component of this lighting model is the Lambert's Law term published in 1760. Lambert stated that the intensity of illumination on a diffuse surface is proportional to the cosine of the angle between the surface normal vector and the light source direction.Let's assume our light source is located in our reference space for lighting at (20, 30, 40), while our normal vector is normalized and located at (0, 11, 0). The point where the intensity of illumination is measured is located at (0, 10, 0).

![](http://altdevblogaday.com/wp-content/uploads/2011/05/DotProductLighting-1024x765.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/05/DotProductLighting-1024x765.jpg)

*Figure*13 - Lighting CalculationThe light and normal vector are calculated by subtracting the position of the point where the intensity is measured -representing their tails- from their heads.

Instead of using the original light vector, the following scalar product normalizes the light vector first, before using it in the lighting equation.

To test if the light vectors magnitude is one:

Plugging the unit light vector and the unit normal vector into the algebraic representation of the scalar product.

Now solving the geometrical representation for the cosine of the angle.

In case the light and the normal vector are unit vectors, the result of the algebraic scalar product calculation equals the cosinus of the angle. The algebraic scalar product is implemented in the dot product intrinsic available for the CPU and GPU. In other words, in case the involved vectors are unit vectors, a processor can calculate the cosine of the angle faster. This is the reason why normalized vectors might be more efficient in programming computer hardware.

Following Lambert's law, the intensity of illumination on a diffuse surface is proportional to the consine of the angle between the surface normal and the light source direction. That means that the point at (0, 10, 0) receives about 0.4082 of the original light intensity at (20, 30, 40) (attenuation is not considered in this example).

Coming back to image 12, in case, the unit light vector would have a y component that is one or minus one and therefore its x and y component would be zero, it would point in the same or opposite direction as the normal and therefore the last equation would result in one or minus one. If the unit light vector would have a z or x component equaling to one and therefore the other components would be zero, those equations would result in zero.

**The Vector Product**Like the scalar product, the vector or cross product depends on the modulus of two vectors and the angle between them, but the result of the vector product is essentially different: it is another vector, at right angles to both the original vectors.

and

For an understanding of the vector product

**R**and**S**, it helps to imagine a plane through those two vectors as shown in figure 14.![](http://altdevblogaday.com/wp-content/uploads/2011/05/VectorProductInAPlane-1024x680.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/05/VectorProductInAPlane-1024x680.jpg)

*Figure*14 - Vector ProductThe angle

**R**, and your middle finger with**S**, then the cross product will point in the direction of your thumb.![](http://altdevblogaday.com/wp-content/uploads/2011/05/VectorProductHandRule.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/05/VectorProductHandRule.jpg)

*Figure*15 - Right-Hand rule Vector ProductThe resulting vector of the cross product is perpendicular to

**R**and**S**, that isand

This makes the vector product an ideal way of computing normals. The two vectors

**R**and**S**can be orthogonal but do not have to be. A property of the vector product that will be covered later is, that the magnitude of**T**is the area of the parallelogram defined by**R**and**S**.Let's multiply two vectors together using the vector product.

There are various vector product terms such as

The other products between the unit vectors can be reasoned as:

Those results show, that the commutative multiplication law is not applicable to vector products. In other words

Applying those findings reduces the vector product term to

Now re-grouping the equation to bring like terms together leads to:

To achieve a visual pattern for remembering the vector product, some authors reverse the sign of the

**j**scalar term.Re-writing the vector product as determinants might help to memorize it as well.

A 2x2 determinant is the difference between the product of the diagonal terms. With determinants a "recipe" for a vector product consists of the following steps:

1. Write the two vectors that should be multiplied as Cartesian vectors

2. Write the cross product of those two vectors in determinant form, if this helps to memorize the process; otherwise skip to step 3.

3. Then compute by plugging in the numbers into

A simple example of a vector product calculation is to show that the assumptions that were made above, while simplifying the vector product, hold up.

To show that there is a sign reversal when the vectors are reversed

The i and k terms are both zero, but the j term is -1, which makes

Which shows

**Deriving a Unit Normal Vector for a Triangle**Image 16 shows a triangle with vertices defined in anti-clockwise order. The side pointing towards the viewer is defined as the visible side in this scene. That means that the normal is expected to point roughly in the direction of where the viewer is located.

![](http://altdevblogaday.com/wp-content/uploads/2011/05/DerivingAUnitNormal-1024x589.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/05/DerivingAUnitNormal-1024x589.jpg)

*Figure*16 - Deriving a Unit Normal VectorThe vertices of the triangle are:

P1 (0, 2, 1)

P2 (0, 1, 4)

P3 (2, 0, 1)

The two vectors

**R**and**S**are retrieved by subtracting the vertex at the head from the vertex at its tail.Δx = (x

h- xt)Δy = (y

h- yt)Δz = (z

h- zt)Bringing the result into the Cartesian form

It is a common mistake to believe that if

**R**and**S**are unit vectors, the cross product will also be a unit vector. The vector product equation shows that this is only true when the angle between the two vectors is 90 degrees and therefore the sinus of the angle theta is 1.Please read in [Van Verth] about CPU implementation details.

**Areas**The vector product might be used to determine the area of a parallelogram or a triangle (with the vertices at P

1- P3). Image 17 shows the two vectors helping to form a parallelogram and a triangle.![](http://altdevblogaday.com/wp-content/uploads/2011/05/VectorProductAreaCalculation-1024x590.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/05/VectorProductAreaCalculation-1024x590.jpg)

*Figure*17 - Deriving the Area of a Parallelogramm / Triangle with the Vector ProductThe height h is

This equals the magnitude of the cross product vector

**T**. Thus when we calculate the vector product of**R**and**S**, the length of the normal vector equals the area of the parallelogram formed by those vectors. The triangle forms half of the parallelogram and therefore half of the area.area of parallelogram =

area of triangle =

or

area of triangle =

To compute the surface area of a mesh constructed from triangles or parallelograms, the magnitude of its non-normalized normals can be used like this.

The sign of the magnitude of the normal shows if the vertices are clockwise or counter-clockwise oriented.

**References**[Azad] Kalid Azad, "Math Better Eplained",

[http://betterexplained.com/articles/math-betterexplained-ebook-available/](http://betterexplained.com/articles/math-betterexplained-ebook-available/)[Eberly] David H. Eberly, "3D Game Engine Design", p. 15, 2nd Edition, Morgan Kauffman 2007

[Farin] Gerald Farin, Dianne Hansford, "The Geometry Toolbox - For Graphics and Modeling", p. 16, AK Peters 1998

[Lengyel] Eric Lengyel, Mathematics for 3D Game Programming and Computer Graphics, Second Edition, Charles River Media 2003

[Vince] John Vince, "Mathematics for Computer Graphics", Springer, 3rd Edition, 2010

[Van Verth] James M. Van Verth, Lars M. Bishop, "Essential Mathematics for Games & Interactive Applications - A Programmer's Guide", Morgan Kaufmann 2004

## 3 comments:

Great Post!


will you continue with this kind of post? (advancing in complexity)

I am looking into posting at some point a matrix tutorial ... it seems like it takes me a long time :-)

Wolfagang,


This post was really useful.

Thanks.

Post a Comment