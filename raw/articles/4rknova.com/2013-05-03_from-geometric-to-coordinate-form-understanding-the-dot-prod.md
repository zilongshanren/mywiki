---
title: 'From Geometric to Coordinate Form: Understanding the Dot Product'
url: https://www.4rknova.com/blog/2013/05/03/dot-product
author: Nikolaos Papadopoulos
published: '2013-05-03'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

The dot product is more than just a formula, it tells us important information about the relationship between two vectors:

**Shows how much one vector points in the direction of another:**It measures how much of one vector lies along the other.**Indicates the angle between vectors:**It can tell whether vectors point in the same direction, opposite directions, or are perpendicular.**Used in physics for work:**It helps calculate work done when a force moves an object.**Measures similarity:**In higher-dimensional spaces, it shows how closely two vectors align in direction.

# Geometric Definition

For two vectors \(\mathbf a\) and \(\mathbf b\), the dot product is defined as:

\[\mathbf a \cdot \mathbf b = \lvert \mathbf a \rvert \, \lvert \mathbf b \rvert \cos\theta\]where:

- \(\lvert \mathbf a \rvert\) and \(\lvert \mathbf b \rvert\) are the lengths (magnitudes) of \(\mathbf a\) and \(\mathbf b\),
- \(\theta\) is the angle between the two vectors.

# Coordinate Definition

For vectors in 3D space:

\[\mathbf a = (a_1, a_2, a_3), \quad \mathbf b = (b_1, b_2, b_3),\]the dot product can also be expressed in component form:

\[\mathbf a \cdot \mathbf b = a_1b_1 + a_2b_2 + a_3b_3\]# Derivation: From Geometric to Coordinate Form

We can derive the coordinate formula starting from the geometric definition.

## Step 1: Law of Cosines

The vector difference \(\mathbf a - \mathbf b\) has length:

\[\lvert \mathbf a - \mathbf b \rvert^2 = \lvert \mathbf a \rvert^2 + \lvert \mathbf b \rvert^2 - 2 \lvert \mathbf a \rvert \, \lvert \mathbf b \rvert \cos\theta\]## Step 2: Write the difference in terms of components

Let \(\mathbf a = (a_1, a_2, a_3)\) and \(\mathbf b = (b_1, b_2, b_3)\). Then

\[\mathbf a - \mathbf b = (a_1 - b_1, a_2 - b_2, a_3 - b_3)\]and its squared length is

\[\lvert \mathbf a - \mathbf b \rvert^2 = (a_1 - b_1)^2 + (a_2 - b_2)^2 + (a_3 - b_3)^2\]Expanding the squares:

\[\begin{aligned} \lvert \mathbf a - \mathbf b \rvert^2 &= (a_1^2 - 2a_1b_1 + b_1^2) + (a_2^2 - 2a_2b_2 + b_2^2) + (a_3^2 - 2a_3b_3 + b_3^2) \\ &= (a_1^2 + a_2^2 + a_3^2) + (b_1^2 + b_2^2 + b_3^2) - 2(a_1b_1 + a_2b_2 + a_3b_3) \\ &= \lvert \mathbf a \rvert^2 + \lvert \mathbf b \rvert^2 - 2 \sum_{i=1}^3 a_i b_i \end{aligned}\]## Step 3: Compare with geometric law of cosines

From Step 1:

\[\lvert \mathbf a - \mathbf b \rvert^2 = \lvert \mathbf a \rvert^2 + \lvert \mathbf b \rvert^2 - 2 \lvert \mathbf a \rvert \, \lvert \mathbf b \rvert \cos\theta\]Compare with Step 2:

\[\lvert \mathbf a \rvert^2 + \lvert \mathbf b \rvert^2 - 2 \sum_{i=1}^3 a_i b_i = \lvert \mathbf a \rvert^2 + \lvert \mathbf b \rvert^2 - 2 \lvert \mathbf a \rvert \, \lvert \mathbf b \rvert \cos\theta\]Canceling \(\lvert \mathbf a \rvert^2 + \lvert \mathbf b \rvert^2\) and dividing by -2 gives:

\[\sum_{i=1}^3 a_i b_i = \lvert \mathbf a \rvert \, \lvert \mathbf b \rvert \cos\theta\]Thus, the **coordinate formula** of the dot product is: