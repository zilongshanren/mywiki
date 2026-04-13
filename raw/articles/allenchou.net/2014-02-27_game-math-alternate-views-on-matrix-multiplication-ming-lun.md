---
title: 'Game Math: Alternate Views on Matrix Multiplication | Ming-Lun "Allen" Chou
  | 周明倫'
url: https://allenchou.net/2014/02/game-math-alternate-views-on-matrix-multiplication/
author: Allen Chou
published: '2014-02-27'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

### Definition of Matrix Multiplication

Let ![Rendered by QuickLaTeX.com A_{l \times m}](../../assets/de40616a7b2a81ff.png)

![Rendered by QuickLaTeX.com B_{m \times n}](../../assets/5848949b530b61d0.png)

![Rendered by QuickLaTeX.com l](../../assets/7ecd210b585111ee.png)

![Rendered by QuickLaTeX.com m](../../assets/53d492fff6de1c67.png)

![Rendered by QuickLaTeX.com m](../../assets/53d492fff6de1c67.png)

![Rendered by QuickLaTeX.com n](../../assets/97eb473973e93376.png)

![Rendered by QuickLaTeX.com A_{ij}](../../assets/196bca08b9c2863b.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com j](../../assets/cfc978999b2989ec.png)

![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com j](../../assets/cfc978999b2989ec.png)


From the definition of matrix multiplication, we know that:

![Rendered by QuickLaTeX.com \[ (AB)_{ij} = \sum\limits_{k = 0}^{m - 1} {A_{ik} B_{kj}} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-95dbdea036a6e37f283e6e1d3e7600e7_l3.png)


Essentially, element (![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com j](../../assets/cfc978999b2989ec.png)

![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)

__dot product__ of ![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com j](../../assets/cfc978999b2989ec.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)


We can compute matrix multiplication by performing __one dot product per element__ in the resulting matrix product ![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


### Linear Combination of Columns

The ![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)

__left matrix__ ![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

__right matrix__ ![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)



Let’s look at a product of two 3-by-3 matrices as an example:

![Rendered by QuickLaTeX.com \[ A = {\left[ {\begin{array}{ccc} A_{00} & A_{01} & A_{02} \\ A_{10} & A_{11} & A_{12} \\ A_{20} & A_{21} & A_{22} \\ \end{array} } \right]} = {\left[ {\begin{array}{ccc} C_A^0 & C_A^1 & C_A^2 \\ \end{array} } \right]} , \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-60b8115d2131d1d92ff05716c4fb8ef6_l3.png)


![Rendered by QuickLaTeX.com \[ B = {\left[ {\begin{array}{ccc} B_{00} & B_{01} & B_{02} \\ B_{10} & B_{11} & B_{12} \\ B_{20} & B_{21} & B_{22} \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-af325715559cb29c273e9a5964dbea49_l3.png)


where ![Rendered by QuickLaTeX.com C_A^i](../../assets/ed21ebe6af512e3e.png)

![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)


Then the ![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


![Rendered by QuickLaTeX.com \[ C_{AB}^i = B_{0i} C_A^0} + B_{1i} C_A^1 + B_{2i} C_A^2 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-ec9bcd772b71411e9a1b28c43eb488f8_l3.png)


Now let’s look at an example with real numbers:

![Rendered by QuickLaTeX.com \[ A = {\left[ {\begin{array}{ccc} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \\ \end{array} } \right]} , B = {\left[ {\begin{array}{ccc} 1 & -1 & 0 \\ 2 & 1 & -2 \\ 0 & 2 & 3 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-3345a183f4c2861eaea0819c3cb0004b_l3.png)


The columns of ![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 1 \\ 4 \\ 7 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-da366fc447e9d93d8d1ea73bd5a37974_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 2 \\ 5 \\ 8 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-3cd371798bf02ef5fd9d136c5fc42a23_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 3 \\ 6 \\ 9 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-057aa359a8226599a132d21227c9b68f_l3.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 1 \\ 2 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-13903bd1b7429254f55160db9162c335_l3.png)

![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


![Rendered by QuickLaTeX.com \[ C_{AB}^0 = 1 {\left[ {\begin{array}{c} 1 \\ 4 \\ 7 \end{array} } \right]} + 2 {\left[ {\begin{array}{c} 2 \\ 5 \\ 8 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 3 \\ 6 \\ 9 \end{array} } \right]} = {\left[ {\begin{array}{c} 5 \\ 14 \\ 23 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4a1a2d64aee11af71b955a0030093a78_l3.png)


Similarly, the second and third columns of the matrix product ![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


![Rendered by QuickLaTeX.com \[ C_{AB}^1 = -1 {\left[ {\begin{array}{c} 1 \\ 4 \\ 7 \end{array} } \right]} + 1 {\left[ {\begin{array}{c} 2 \\ 5 \\ 8 \end{array} } \right]} + 2 {\left[ {\begin{array}{c} 3 \\ 6 \\ 9 \end{array} } \right]} = {\left[ {\begin{array}{c} 7 \\ 13 \\ 19 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-85d5eeb68fa32841d7449fb1b66da2ea_l3.png)


![Rendered by QuickLaTeX.com \[ C_{AB}^2 = 0 {\left[ {\begin{array}{c} 1 \\ 4 \\ 7 \end{array} } \right]} - 2 {\left[ {\begin{array}{c} 2 \\ 5 \\ 8 \end{array} } \right]} + 3 {\left[ {\begin{array}{c} 3 \\ 6 \\ 9 \end{array} } \right]} = {\left[ {\begin{array}{c} 5 \\ 8 \\ 11 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5392714d4015d64ba949a309316a383d_l3.png)


So the matrix product is:

![Rendered by QuickLaTeX.com \[ AB = {\left[ {\begin{array}{ccc} 5 & 7 & 5 \\ 14 & 13 & 8 \\ 23 & 19 & 11 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-56c161bf9944709d5526d8fd0ca8f569_l3.png)


### Linear Combination of Rows

Alternatively, we can view matrix multiplication from a row perspective.

The ![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)

__right matrix__ ![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

__left matrix__ ![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)


Let ![Rendered by QuickLaTeX.com R_A^i](../../assets/852e9c543a0800b5.png)

![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)


I will skip the symbolic notations and jump right back into the previous example we used:

![Rendered by QuickLaTeX.com \[ A = {\left[ {\begin{array}{ccc} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \\ \end{array} } \right]} , B = {\left[ {\begin{array}{ccc} 1 & -1 & 0 \\ 2 & 1 & -2 \\ 0 & 2 & 3 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-3345a183f4c2861eaea0819c3cb0004b_l3.png)


The rows of ![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{ccc} 1 & -1 & 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-bbdc0d1e02d0fe1fad7614252e657f14_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{ccc} 2 & 1 & -2 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-de360793016916b228a7f9fc43e62dd8_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{ccc} 0 & 2 & 3 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5b7e57d676de544a69c64a4fb85f14db_l3.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{ccc} 1 & 2 & 3 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-fabba2a004dc95c9bb0deaf0f863ddb6_l3.png)

![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


![Rendered by QuickLaTeX.com \[ R_{AB}^0 = 1 {\left[ {\begin{array}{ccc} 1 & -1 & 0 \end{array} } \right]} + 2 {\left[ {\begin{array}{ccc} 2 & 1 & -2 \end{array} } \right]} + 3 {\left[ {\begin{array}{ccc} 0 & 2 & 3 \end{array} } \right]} = {\left[ {\begin{array}{ccc} 5 & 7 & 5 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1672e8f10556c78e1baf540cb337d72d_l3.png)


Similarly, the second and third rows of the matrix product ![Rendered by QuickLaTeX.com AB](../../assets/76e31db09af6a8fd.png)


![Rendered by QuickLaTeX.com \[ R_{AB}^1 = 4 {\left[ {\begin{array}{ccc} 1 & -1 & 0 \end{array} } \right]} + 5 {\left[ {\begin{array}{ccc} 2 & 1 & -2 \end{array} } \right]} + 6 {\left[ {\begin{array}{ccc} 0 & 2 & 3 \end{array} } \right]} = {\left[ {\begin{array}{ccc} 14 & 13 & 8 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-479a16c94bbdfb8eeceed8d47df9fc43_l3.png)


![Rendered by QuickLaTeX.com \[ R_{AB}^2 = 7 {\left[ {\begin{array}{ccc} 1 & -1 & 0 \end{array} } \right]} + 8 {\left[ {\begin{array}{ccc} 2 & 1 & -2 \end{array} } \right]} + 9 {\left[ {\begin{array}{ccc} 0 & 2 & 3 \end{array} } \right]} = {\left[ {\begin{array}{ccc} 23 & 19 & 11 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-6aff5401d47d3b474f75853bbfa1d184_l3.png)


So the matrix product is:

![Rendered by QuickLaTeX.com \[ AB = {\left[ {\begin{array}{ccc} 5 & 7 & 5 \\ 14 & 13 & 8 \\ 23 & 19 & 11 \\ \end{array} } \right]} , \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1839cf40e35b595cab7cdf2521dfa80e_l3.png)


same as what we got before.

### End of Alternate Views on Matrix Multiplication

Now that you understand the two alternative views of matrix multiplication, you are well equipped to make your life easier when dealing with various matrix operations. For instance, I will show how to quickly eyeball the inverse of small matrices using this technique in [another post](http://allenchou.net/2014/02/game-math-how-to-eyeball-the-inverse-of-a-matrix/).