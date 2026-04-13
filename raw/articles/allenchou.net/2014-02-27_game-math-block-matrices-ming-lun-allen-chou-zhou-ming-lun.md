---
title: 'Game Math: Block Matrices | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/02/game-math-block-matrices/
author: Allen Chou
published: '2014-02-27'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

### Splitting Matrices into Blocks

When performing matrix multiplication, we can split matrices into “blocks”. The matrix multiplication can then be performed as if each block is a single matrix element, given that we split the matrices in a way that the multiplication of block matrices are of legal dimensions.

For instance, a product of two 4-by-4 matrices can be viewed as a product of 2-by-2 matrices, where each matrix element is a 2-by-2 block matrix. Since a 2-by-2 matrix can be legally multiplied by another 2-by-2 matrix, such splitting scheme is valid.

Let’s look at an example with numbers:

![Rendered by QuickLaTeX.com \[ A = {\left[ {\begin{array}{cccc} 1 & 1 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 1 & 1 \\ \end{array} } \right]} , B = {\left[ {\begin{array}{cccc} 2 & 1 & 0 & 0 \\ 1 & -1 & 0 & 0 \\ 0 & 0 & 2 & 1 \\ 0 & 0 & 1 & -1 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b3ed23feb4a1c0964a20e5f10a1c335b_l3.png)


We can split each of these matrices into four 2-by-2 block matrices:

![Rendered by QuickLaTeX.com \[ A = {\left[ {\begin{array}{cc} C & O \\ O & C \\ \end{array} } \right]} , B = {\left[ {\begin{array}{cc} D & O \\ O & D \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d31775ce1584993af851b7d878e543c5_l3.png)


where ![Rendered by QuickLaTeX.com C = {\left[ {\begin{array}{cc} 1 & 1 \\ 1 & 1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b3a0da100ff3c79cb960e596e21afdd9_l3.png)

![Rendered by QuickLaTeX.com D = {\left[ {\begin{array}{cc} 2 & 1 \\ 1 & -1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-76ba266d1a4250951fbe5e59092639a1_l3.png)

![Rendered by QuickLaTeX.com O = {\left[ {\begin{array}{cc} 0 & 0 \\ 0 & 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-32db1a818211993bc6094feea907fb60_l3.png)



If we perform the matrix multiplication ![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


![Rendered by QuickLaTeX.com \[ AB = {\left[ {\begin{array}{cc} CD + OO & OC + DO \\ DO + OC & OO + CD \\ \end{array} } \right]}, = {\left[ {\begin{array}{cc} CD & O \\ O & CD \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-81f19ca2d53fbbe709398448dda74118_l3.png)


We can find out that ![Rendered by QuickLaTeX.com CD = {\left[ {\begin{array}{cc} 3 & 0 \\ 3 & 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5408de7540efab5a16eda976a4c9de63_l3.png)

![Rendered by QuickLaTeX.com CD](../../assets/f8d63069780e286c.png)

![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


![Rendered by QuickLaTeX.com \[ AB = {\left[ {\begin{array}{cc} CD & O \\ O & CD \\ \end{array} } \right]} = {\left[ {\begin{array}{cccc} 3 & 0 & 0 & 0 \\ 3 & 0 & 0 & 0 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 3 & 0 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-35659c0db3c2114ee8e14cad264e175f_l3.png)


We can easily verify that this is the same matrix we will get if we multiply out the matrix product ![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


### Transformation Matrices

In computer graphics, we represent points and vectors as 4D vectors with the ![Rendered by QuickLaTeX.com w](../../assets/fdb8d80aa4044c76.png)


![Rendered by QuickLaTeX.com \[ M = {\left[ {\begin{array}{cccc} R_{00} & R_{01} & R_{02} & T_0 \\ R_{10} & R_{11} & R_{12} & T_1 \\ R_{20} & R_{21} & R_{22} & T_2 \\ 0 & 0 & 0 & 1 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-8c488039cdffa8c0ef3f59533321ccb5_l3.png)


We can split a 4-by-4 transformation matrix into a 2-by-2 matrix, with the top-left element a 3-by-3 matrix, the top-right element a 3-by-1 matrix, the bottom-left element a 1-by-3 zero matrix, and the bottom-right element the 1-by-1 identity matrix:

![Rendered by QuickLaTeX.com \[ M = {\left[ {\begin{array}{cc} R & T \\ O & I \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5f81e70bea3402eaab216d0e1ea54d83_l3.png)


where ![Rendered by QuickLaTeX.com R = {\left[ {\begin{array}{ccc} R_{00} & R_{01} & R_{02} \\ R_{10} & R_{11} & R_{12} \\ R_{20} & R_{21} & R_{22} \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-95d7b735a9cf4247f5763445e05629c7_l3.png)

![Rendered by QuickLaTeX.com T = {\left[ {\begin{array}{c} T_0 \\ T_1 \\ T_2 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d432bafea40cec80d14f7263239c7f47_l3.png)

![Rendered by QuickLaTeX.com O = {\left[ {\begin{array}{ccc} 0 & 0 & 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-2216fe3798478788ad4d59c1d4bae650_l3.png)

![Rendered by QuickLaTeX.com I = {\left[ {\begin{array}{c} 1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d540ebe9740f56f4bf8b2aad7603dff7_l3.png)


Now if we were to concatenate two transformation matrices:

![Rendered by QuickLaTeX.com \[ M_1 = {\left[ {\begin{array}{cc} R_1 & T_1 \\ O & I \\ \end{array} } \right]}, M_2 = {\left[ {\begin{array}{cc} R_2 & T_2 \\ O & I \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-c5b8acad1aaf25e12c2031e49f8a7043_l3.png)


we can simply perform a 2-by-2 matrix multiplication and get:

![Rendered by QuickLaTeX.com \[ M_2 M_1 = {\left[ {\begin{array}{cc} R_2 R_1 + T_2 O & R_2 T_1 + T_2 I \\ O R_1 + I O & O T_1 + I I \\ \end{array} } \right]} = {\left[ {\begin{array}{cc} R_2 R_1 & R_2 T_1 + T_2 \\ O & I \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9036f8a2fe47f44bdfcdc56c9eb5a1b3_l3.png)


You might have seen the formula above before in a book or class on computer graphics. This is one way we can derive this formula, using block matrices.

Using this formula, we can save a lot of computation time if we know beforehand that the two 4-by-4 matrices we are multiplying together are of the form ![Rendered by QuickLaTeX.com M = {\left[ {\begin{array}{cc} R & T \\ O & I \\ \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-70c5fc714f9c9a16a7bfcd141c826fed_l3.png)


### Inverting Transformation Matrices

Splitting matrices into blocks can also help us find the inverses of matrices. Let’s use the 4-by-4 transformation matrix as an example again:

![Rendered by QuickLaTeX.com \[ M = {\left[ {\begin{array}{cc} R & T \\ O & I \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5f81e70bea3402eaab216d0e1ea54d83_l3.png)


With careful inspection, we can find that:

![Rendered by QuickLaTeX.com \[ M^{-1} = {\left[ {\begin{array}{cc} R^{-1} & -R^{-1}T \\ O & I \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-8e928688aadcfae8a86a9c7747602306_l3.png)


We can verify that ![Rendered by QuickLaTeX.com M^{-1}](../../assets/daa8a371f1ace70d.png)

![Rendered by QuickLaTeX.com M](../../assets/91ac030eac3e8e2e.png)


![Rendered by QuickLaTeX.com \[ M M^{-1} = {\left[ {\begin{array}{cc} R R^{-1} + T O & -R R^{-1} T + T I \\ O R + I O & O T + I I \\ \end{array} } \right]} = {\left[ {\begin{array}{cc} I_{3 \times 3} & O^T \\ O & I \\ \end{array} } \right]} = I_{4 \times 4} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-74be16c22d18d2caba70145250bbe785_l3.png)


where ![Rendered by QuickLaTeX.com I_{3 \times 3}](../../assets/f858d0f955dae78b.png)

![Rendered by QuickLaTeX.com I_{4 \times 4}](../../assets/18fd060788cee2b1.png)


### End of Block Matrices

As you have seen, if we can split matrices in a matrix product into simple block matrices (like identity matrices and zero matrices), we can save a lot of computation time, because many block matrices can possibly be simplified or even zeroed out when multiplied with simple block matrices. The block matrix technique can also help us simplify matrix inversion with matrices in certain forms.