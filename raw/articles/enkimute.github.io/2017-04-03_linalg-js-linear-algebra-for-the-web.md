---
title: linalg.js - Linear Algebra for the web.
url: https://enkimute.github.io/linalg.js/
author: Enki's blog
published: '2017-04-03'
source_blog: Enki's blog – Math, Graphics, Programming.
source_site: https://enkimute.github.io/
category: graphics
fetched: '2026-04-19'
---

![not yet ..](../../assets/cb9f317b98c6b74a.png)

# linalg.js - Linear Algebra for the web.

Linear Algebra Expressions and operator overloading on the web.. or can you ?

Since every post should start with a nice image, here’s a rank 15,10,5 and 2 approximation of an image calculated in javascript :

And here’s the script that generates it :

```
var img = new Image();
img.src = '../res/testimage.jpg';
img.onload = Matrix(function() {
var U=Matrix(this), S, V, R;
"[U,S,V]=U.SVD"
[15,10,5,2].forEach(j=>{
for (var i=j; i < S.rows; i++) S[i]=0;
"R=U*S~*V'"
Matrix.show(R,document.body);
});
});
```


Hey - wait a minute .. what’s that string line inside the function ? And why is the function wrapped in a Matrix call ?

Lets look at another example to see how linalg.js will make your world easier. and more readable.

```
// Find the rigid transform that transforms pointset A to pointset B.
// A and B are matrices with nr_of_points rows and nr_of_dimensions columns.
// It returns a square nr_of_dimensions dimensional matrix T so that A*T=B
var findTransform = Matrix(function(A,B){
var mA, mB, U, S, V, COV;
// Center dataset by subtracting average row..
"mA = A-A.avg"
"mB = B-B.avg"
// Calculate covariance matrix.
"COV = mA'*mB"
// do SVD factorisation on covariance matrix.
"[U,S,V] = COV.SVD"
// Find transformation that brings A to B
"return U*V'"
});
```


That’s right .. full matrix math, factorisation and operator overloading .. just a string quote away from being javascript..

## enter linalg.js

12861 bytes - [https://enkimute.github.io/res/linalg.min.js](https://enkimute.github.io/res/linalg.min.js)

All features of linalg.js are accessed through a single global function call, appropriately named ‘Matrix’.

#### you use it to create matrices ..

```
// a skinny matrix.
var A = Matrix([[1,2],[3,4],[5,6],[7,8]]);
// an empty matrix.
var B = Matrix(4,2);
// a matrix from an image, video or canvas :
var C = Matrix(document.getElementById('myImage'));
```


#### Or solve some simple expressions ..

```
// Solve (x=0,x=1,y=0)
var solution = Matrix("[[1,0],[1,0],[0,1]]\\[0,1,0]");
// add the transpose of a to b then multiply with c
var D = Matrix("(A'+B)*C");
// Multiply B with the inverse of A :
var E = Matrix("B*A^-1");
// you can store these expressions as functions.
// simpy add the arguments list as second parameter.
var solve = Matrix("(A'*A)^-1*A'*Y","A,Y");
var solution2 = solve([[1,0],[1,0],[0,1]],[0,1,0]);
```


#### or wrap your functions in it ..

.. so that you can put linear algebra expressions between string quotes on their own line ..

```
var sample = Matrix(function(){
var A=[[1,0],[1,0],[0,1]];
var Y=[0,1,0];
"return A\Y"
});
var solve = Matrix(function(A,Y){
var Ai = Matrix(A);
"Ai = (A'*A)^-1*A'"
"return Ai*Y"
});
solve([[1,0],[1,0],[0,1]],[0,1,0]);
```


#### Together with modern javascript features ..

you can write some pretty readable algebra code.

```
var fitCubic = Matrix(function (data) {
var Vandermonde = data.map(x=>[x[0]*x[0]*x[0],x[0]*x[0],x[0],1]);
var Rhs = data.map(x=>x[1]);
"return Vandermonde\Rhs"
});
```


In just a few lines we can implement various popular least squares methods ..

```
// Linear Least squares, regularised linear least squares, weighted linear least squares.
var lls = Matrix("A\\Y","A,Y");
var rlls = Matrix("(A'*A + l*I)^-1*A'*Y","A,Y,I,l");
var wlls = Matrix("(A'*W~*A)^-1*A'*W~*Y","A,Y,W");
// Find intersection of the system ( y=0, x=1, y=2, x=3 )
var A=[[0,1],[1,0],[0,1],[1,0]];
var Y=[0,1,2,3];
// Using linear least squares
lls(A,Y).log();
// Regularised .. importance of arg size is 0.1
rlls(A,Y,Matrix.identity(2),0.1).log();
// Weighted .. first two more important.
wlls(A,Y,[1,1,0.5,0.5]).log();
```


## List of supported operators and functions.

All operators work with Matrix,Vector and Scalar types as appropriate. All functions will upcast their arguments to Matrix objects if needed.

| Operator | Description | Example |
|---|---|---|
| + | Overloaded add | C=A+B |
| - | Overloaded minus | C=A-B |
| * | Overloaded multiply | C=A*B |
| ’ | Overloaded transpose | B=A’ |
| ^ | Overloaded pow | B=A^-1 |
| ~ | Diagonalise vector into matrix. | A=V~ |
| \ | Overloaded solve | X=A\Y |
| () | Parentheses | D=(A+B)*C |


| Decomposition | Expression |
|---|---|
| Matrix.factorCholesky(A); | C=A.Cholesky |
| Matrix.factorLU(A); | LU=A.LU |
| Matrix.factorLUP(A); | [LU,P]=A.LUP |
| Matrix.factorSVD(A,S,V); | [U,S,V]=A.SVD |


| Inversion | Expression |
|---|---|
| Matrix.invertCholesky(A); | |
| Matrix.invertLU(A); | |
| Matrix.invertLUP(A); | B=A^-1 |
| Matrix.invertSVD(A); |


| Solver | Expression |
|---|---|
| Matrix.solveCholesky(C,Y); | |
| Matrix.solveLU(LU,Y); | |
| Matrix.solveLUP(LU,P,Y); | |
| Matrix.solveSVD(U,S,V,Y) | |
| Matrix.solveSeidel(A,Y,iter); | |
| Matrix.solve(A,Y); | X=A\Y |


| Special Matrices | Description |
|---|---|
| Matrix.identity(x); | Identity matrix of size x |
| Matrix.hankel(V,c); | Hankel matrix of column V and count c |
| Matrix.toHankel(A); | Convert to Hankel form |
| Matrix.toeplitz(V,c); | Toeplitz matrix of vector V and count c |
| Matrix.augment(A,B,AB); | Augment A with B |


| Metrics/Norms | Description |
|---|---|
| Matrix.equals(A,B); | compare |
| Matrix.len(A); | length matrix or vector |
| Matrix.normalize(A); | matrix or vector |
| Matrix.avg(A); | return average row. |


| Utility | description |
|---|---|
| Matrix.cmul(A,B); | component wise multiply |
| Matrix.print(A); | pretty console log |
| Matrix.show(A,htmlElement) | Append a matrix as image. |
| Matrix.row(A,x,c); | extract rows from A |
| Matrix.repeat(r,x); | repeat row r x times. |


| Filters | Description |
|---|---|
| Matrix.blackman(n); | Generate blackman vector of size n |
| Matrix.hamming(n); | Generate hamming vector of size n |
| Matrix.sinc(n,sampling,cutoff); | Generate a sinc vector of size n and given sampling and cutoff |