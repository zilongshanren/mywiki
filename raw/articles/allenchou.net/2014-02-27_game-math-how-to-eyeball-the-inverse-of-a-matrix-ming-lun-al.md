---
title: 'Game Math: How to Eyeball the Inverse of a Matrix | Ming-Lun "Allen" Chou
  | 周明倫'
url: https://allenchou.net/2014/02/game-math-how-to-eyeball-the-inverse-of-a-matrix/
author: Allen Chou
published: '2014-02-27'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

### Matrix Multiplication as Linear Combinations of Columns/Rows

As shown in [this post](http://allenchou.net/2014/02/game-math-alternate-views-on-matrix-multiplication/), matrix multiplication can be viewed as linear combinations of columns from the left matrix or rows from the right matrix. We can reverse this process and utilize this fact to help us eyeball inverses of matrices without having to do any calculation by hand or calculator.

The product of a matrix with its inverse gives the identity matrix:

![Rendered by QuickLaTeX.com \[ M M^{-1} = I \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d44a78930bf3fd42a91b0714e710a2f1_l3.png)


Viewing from the column perspective, columns of the identity matrix are linear combinations of the columns from the left matrix ![Rendered by QuickLaTeX.com M](../../assets/91ac030eac3e8e2e.png)

![Rendered by QuickLaTeX.com M^{-1}](../../assets/daa8a371f1ace70d.png)


Let us use a 3-by-3 matrix as an example:

![Rendered by QuickLaTeX.com \[ M = {\left[ {\begin{array}{ccc} 0 & 1 & 1 \\ 1 & 2 & 3 \\ 0 & 0 & 1 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-6086ea30e24655aebb352d835179c15a_l3.png)


We want to linearly combine the columns to form the three columns from the 3-by-3 identity matrix, namely ![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 1 \\ 0 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5034dfa655dbe133caba30d01b194958_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 0 \\ 1 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-8be304fe0baac730b63db03723c5ab48_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 0 \\ 0 \\ 1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-0e25280f402372953d003175dba75c52_l3.png)



For the first column, we can find the coefficients by eyeballing the columns from ![Rendered by QuickLaTeX.com M](../../assets/91ac030eac3e8e2e.png)


![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{c} 1 \\ 0 \\ 0 \end{array} } \right]} = -2 {\left[ {\begin{array}{c} 0 \\ 1 \\ 0 \end{array} } \right]} + 1 {\left[ {\begin{array}{c} 1 \\ 2 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 1 \\ 3 \\ 1 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9a4246b9101d12bc83347d181801f21c_l3.png)


Thus, the first column of ![Rendered by QuickLaTeX.com M^{-1}](../../assets/daa8a371f1ace70d.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} -2 \\ 1 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-39a3ab1c3dba229938d98046edb33a18_l3.png)


We can figure out the rest of the coefficients for the other two columns as well:

![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{c} 0 \\ 1 \\ 0 \end{array} } \right]} = 1 {\left[ {\begin{array}{c} 0 \\ 1 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 1 \\ 2 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 1 \\ 3 \\ 1 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-93b6d600731cc1e9e9b2ebb634180015_l3.png)


![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{c} 0 \\ 0 \\ 1 \end{array} } \right]} = -1 {\left[ {\begin{array}{c} 0 \\ 1 \\ 0 \end{array} } \right]} - 1 {\left[ {\begin{array}{c} 1 \\ 2 \\ 0 \end{array} } \right]} + 1 {\left[ {\begin{array}{c} 1 \\ 3 \\ 1 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-632cbe5b3d51a4c500883639ee81d2d8_l3.png)


So the second and third columns of ![Rendered by QuickLaTeX.com M^{-1}](../../assets/daa8a371f1ace70d.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 1 \\ 0 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5034dfa655dbe133caba30d01b194958_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} -1 \\ -1 \\ 1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-82774a53b262f0e72bc612acab1bd610_l3.png)


And now we have our inverse figured out, hands-free!

![Rendered by QuickLaTeX.com \[ M^{-1} = {\left[ {\begin{array}{ccc} -2 & 1 & -1 \\ 1 & 0 & -1 \\ 0 & 0 & 1 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-32a4d6fe493634575d7e373d0e49c93b_l3.png)


We can perform the same trick from the row perspective:

![Rendered by QuickLaTeX.com \[ M^{-1} M = I \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-ae280644eb244d59fb698db89bc8d1c4_l3.png)


The rows of the 3-by-3 identity matrix are linear combinations of rows from ![Rendered by QuickLaTeX.com M](../../assets/91ac030eac3e8e2e.png)

![Rendered by QuickLaTeX.com M^{-1}](../../assets/daa8a371f1ace70d.png)

![Rendered by QuickLaTeX.com M](../../assets/91ac030eac3e8e2e.png)


For the first row of the identity matrix, we can quickly find out that:

![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{ccc} 1 & 0 & 0 \end{array} } \right]} = -2 {\left[ {\begin{array}{ccc} 0 & 1 & 1 \end{array} } \right]} + 1 {\left[ {\begin{array}{ccc} 1 & 2 & 3 \end{array} } \right]} - 1 {\left[ {\begin{array}{ccc} 0 & 0 & 1 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-407deeee493bcb29d9b5697aa80b3d79_l3.png)


So the first row of ![Rendered by QuickLaTeX.com M^{-1}](../../assets/daa8a371f1ace70d.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{ccc} -2 & 1 & -1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-c950689a2082cc296d9eb937ddc5a108_l3.png)


And for the other two rows of the identity matrix, we can see that:

![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{ccc} 0 & 1 & 0 \end{array} } \right]} = 1 {\left[ {\begin{array}{ccc} 0 & 1 & 1 \end{array} } \right]} + 0 {\left[ {\begin{array}{ccc} 1 & 2 & 3 \end{array} } \right]} - 1 {\left[ {\begin{array}{ccc} 0 & 0 & 1 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-fdadb5759d5d143b8eec6d8e62ea0b72_l3.png)


![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{ccc} 0 & 0 & 1 \end{array} } \right]} = 0 {\left[ {\begin{array}{ccc} 0 & 1 & 1 \end{array} } \right]} + 0 {\left[ {\begin{array}{ccc} 1 & 2 & 3 \end{array} } \right]} + 1 {\left[ {\begin{array}{ccc} 0 & 0 & 1 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-81916621e401c42abb97b8009a9715c1_l3.png)


Thus, the second and third rows of ![Rendered by QuickLaTeX.com M^{-1}](../../assets/daa8a371f1ace70d.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{ccc} 1 & 0 & -1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-a33a3ab2497970182b2c87f8496592f6_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{ccc} 0 & 0 & 1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-bc7f45ff68f3158b726cc9cffaa3a3e4_l3.png)


We have found our inverse, hands-free again:

![Rendered by QuickLaTeX.com \[ M^{-1} = {\left[ {\begin{array}{ccc} -2 & 1 & -1 \\ 1 & 0 & -1 \\ 0 & 0 & 1 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-32a4d6fe493634575d7e373d0e49c93b_l3.png)


### Inverses of Perspective Projection Matrices

Okay, the example above might be a little bit contrived with pretty numbers. Now let’s look at something in the real world that we can apply this technique to.

The perspective projection matrix (negative Z being the view direction in camera space) is of the form:

![Rendered by QuickLaTeX.com \[ P = {\left[ {\begin{array}{cccc} A & 0 & 0 & 0 \\ 0 & B & 0 & 0 \\ 0 & 0 & C & D \\ 0 & 0 & -1 & 0 \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4d583f8fb518d9b2ead232081bd74888_l3.png)


If you look up [3D Mouse Picking](https://www.google.com/search?q=3d+mouse+picking&rlz=1C1CHFX_enUS572US572&oq=3d+mouse+picking&aqs=chrome..69i57j0l5.3384j0j7&sourceid=chrome&espv=210&es_sm=122&ie=UTF-8), you’ll see that we need the inverse of the perspective projection matrix to perform this operation.

“No big deal,” you might say, “Our math library already provides a function to invert a 4-by-4 matrix.”

But is it really necessary to use a full-blown 4-by-4 matrix inversion calculation when we can achieve the same thing with just a few scalar operations? We can do better.

Let’s see how we can linearly combine the four columns of ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 1 \\ 0 \\ 0 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5ac66cc40ada46c964f2d5ae491a34e8_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 0 \\ 1 \\ 0 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-08c6baf8ff385b5eff2a914089d36f06_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 0 \\ 0 \\ 1 \\ 0 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-33a4d6ed6bda78a5edf420f64c76c201_l3.png)

![Rendered by QuickLaTeX.com {\left[ {\begin{array}{c} 0 \\ 0 \\ 0 \\ 1 \end{array} } \right]}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5ac549cba43250c0f440fdf4194e90b4_l3.png)


![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{c} 1 \\ 0 \\ 0 \\ 0 \end{array} } \right]} = \frac{1}{A} {\left[ {\begin{array}{c} A \\ 0 \\ 0 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ B \\ 0 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ 0 \\ C \\ -1 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ 0 \\ D \\ 0 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-00e816eb267bc0f8dd3dc448b8f793e6_l3.png)


![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{c} 0 \\ 1 \\ 0 \\ 0 \end{array} } \right]} = 0 {\left[ {\begin{array}{c} A \\ 0 \\ 0 \\ 0 \end{array} } \right]} + \frac{1}{B} {\left[ {\begin{array}{c} 0 \\ B \\ 0 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ 0 \\ C \\ -1 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ 0 \\ D \\ 0 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-abee6d2e6d9aa59e7e7c449530c65c99_l3.png)


![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{c} 0 \\ 0 \\ 1 \\ 0 \end{array} } \right]} = 0 {\left[ {\begin{array}{c} A \\ 0 \\ 0 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ B \\ 0 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ 0 \\ C \\ -1 \end{array} } \right]} + \frac{1}{D} {\left[ {\begin{array}{c} 0 \\ 0 \\ D \\ 0 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d1a584feaa374899a23b1a89d0217092_l3.png)


![Rendered by QuickLaTeX.com \[ {\left[ {\begin{array}{c} 0 \\ 0 \\ 0 \\ 1 \end{array} } \right]} = 0 {\left[ {\begin{array}{c} A \\ 0 \\ 0 \\ 0 \end{array} } \right]} + 0 {\left[ {\begin{array}{c} 0 \\ B \\ 0 \\ 0 \end{array} } \right]} -1 {\left[ {\begin{array}{c} 0 \\ 0 \\ C \\ -1 \end{array} } \right]} + \frac{C}{D} {\left[ {\begin{array}{c} 0 \\ 0 \\ D \\ 0 \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-55304fba0cb0e89bf218fea55a4cd497_l3.png)


So the inverse of the perspective projection matrix is:

![Rendered by QuickLaTeX.com \[ P^{-1} = {\left[ {\begin{array}{cccc} \frac{1}{A} & 0 & 0 & 0 \\ 0 & \frac{1}{B} & 0 & 0 \\ 0 & 0 & 0 & -1 \\ 0 & 0 & \frac{1}{D} & \frac{C}{D} \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-61274145e0734a7b4d8683731ae08b2f_l3.png)


Using this formula is definitely more efficient than using a generic 4-by-4 matrix inversion. The best part is that you don’t even have to memorize the formula for ![Rendered by QuickLaTeX.com P^{-1}](../../assets/6d0ab4cc7a8ce9fb.png)


### End of How to Eyeball The Inverse of A Matrix

Viewing matrix multiplication as linear combinations of columns of the left matrix or rows of the right matrix is a valuable technique. It grants us the ability to quickly eyeball the inverse of a reasonably-sized matrix.