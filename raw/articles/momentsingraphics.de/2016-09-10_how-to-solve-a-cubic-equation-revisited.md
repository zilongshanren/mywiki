---
title: How to solve a cubic equation, revisited
url: http://momentsingraphics.de/CubicRoots.html
published: '2016-09-10'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# How to solve a cubic equation, revisited

This post covers a little gem worth sharing: The fastest solution to cubic equations with three real roots that I am aware of. It is also fairly robust and I implemented it in HLSL. It is based on the work by Jim Blinn [[Blinn07b]](http://momentsingraphics.de#_Blinn07b) but tweaked for double speed.

**Listing 1:**Returns the three real roots of the cubic polynomial

`Coefficient[0]`

\(\cdot x^0\)+ ... +`Coefficient[3]`

\(\cdot x^3\). Behavior is undefined if the polynomial does not have three real roots. The order of the returned roots is undefined.```
float3 SolveCubic(float4 Coefficient){
// Normalize the polynomial
Coefficient.xyz/=Coefficient.w;
// Divide middle coefficients by three
Coefficient.yz/=3.0f;
// Compute the Hessian and the discrimant
float3 Delta=float3(
mad(-Coefficient.z,Coefficient.z,Coefficient.y),
mad(-Coefficient.y,Coefficient.z,Coefficient.x),
dot(float2(Coefficient.z,-Coefficient.y),Coefficient.xy)
);
float Discriminant=dot(float2(4.0f*Delta.x,-Delta.y),Delta.zy);
// Compute coefficients of the depressed cubic
// (third is zero, fourth is one)
float2 Depressed=float2(
mad(-2.0f*Coefficient.z,Delta.x,Delta.y),
Delta.x
);
// Take the cubic root of a normalized complex number
float Theta=atan2(sqrt(Discriminant),-Depressed.x)/3.0f;
float2 CubicRoot;
sincos(Theta,CubicRoot.y,CubicRoot.x);
// Compute the three roots, scale appropriately and
// revert the depression transform
float3 Root=float3(
CubicRoot.x,
dot(float2(-0.5f,-0.5f*sqrt(3.0f)),CubicRoot),
dot(float2(-0.5f, 0.5f*sqrt(3.0f)),CubicRoot)
);
Root=mad(2.0f*sqrt(-Depressed.y),Root,-Coefficient.z);
return Root;
}
```


I spent several days figuring this out because I wanted to improve the robustness of [prefiltered single scattering with six moments](http://momentsingraphics.de/I3D2016.html). The original implementation used a [closed form from Wikipedia](https://en.wikipedia.org/wiki/Cubic_function#General_formula). As shown in [Figure 1](http://momentsingraphics.de#OldRootComputation), this approach gave wrong results for some pixels where `Coefficient[3]`

vanishes. A Newton iteration could diminish these artifacts but at a cost. The new solution fixes them and is substantially faster ([Figure 2](http://momentsingraphics.de#NewRootComputation)).

I won't explain how [Listing 1](http://momentsingraphics.de#CubicEquationFast) works because in this regard Jim Blinn does a good job with his 80 page column [[Blinn06a]](http://momentsingraphics.de#_Blinn06a), [[Blinn06b]](http://momentsingraphics.de#_Blinn06b), [[Blinn06c]](http://momentsingraphics.de#_Blinn06c), [[Blinn07a]](http://momentsingraphics.de#_Blinn07a), [[Blinn07b]](http://momentsingraphics.de#_Blinn07b). However, I do want to point out how the algorithm presented here differs and why.

Jim Blinn computes the roots of largest and least magnitude separately. Roughly speaking, he makes the substitution \(y:=x^{-1}\) and then multiplies by \(y^3\) to obtain a “flipped” polynomial where these roots are swapped. This way, both branches have to compute the root of largest magnitude, which ensures great numerical stability. The third root is easily found once two roots are available. At the time, this has been a reasonable design because as Jim Blinn points out SIMD instructions parallelize these computations. However, this argument is obsolete on current hardware and thus the approach would double the cost.

[Listing 1](http://momentsingraphics.de#CubicEquationFast) just computes all three roots in one go. It is less robust but twice as fast. The solution is still more robust than everything else I tried (various other closed forms, iterative solutions and mixtures thereof). If you are looking for a solution that covers cubic polynomials having only one real root, Jim Blinn also has a solution [[Blinn07b]](http://momentsingraphics.de#_Blinn07b).

## References

[ Blinn, J. F. (2006). How to solve a cubic equation, part 1: The shape of the discriminant. IEEE Computer Graphics and Applications, 26(3):84-93.
][Official version](http://dx.doi.org/10.1109/MCG.2006.60) | [Author's version](https://courses.cs.washington.edu/courses/cse590b/13au/lecture_notes/cubic.pdf)

[ Blinn, J. F. (2006). How to solve a cubic equation, part 2: The 11 case. IEEE Computer Graphics and Applications, 26(4):90-100.
][Official version](http://dx.doi.org/10.1109/MCG.2006.81) | [Author's version](https://courses.cs.washington.edu/courses/cse590b/13au/lecture_notes/solvecubic_p2.pdf)

[ Blinn, J. F. (2006). How to solve a cubic equation, part 3: General depression and a new covariant. IEEE Computer Graphics and Applications, 26(6):92-102.
][Official version](http://dx.doi.org/10.1109/MCG.2006.129) | [Author's version](https://courses.cs.washington.edu/courses/cse590b/13au/lecture_notes/solvecubic_p3.pdf)

[ Blinn, J. F. (2007). How to solve a cubic equation, part 4: The 111 case. IEEE Computer Graphics and Applications, 27(1):100-103.
][Official version](http://dx.doi.org/10.1109/MCG.2007.10) | [Author's version](https://courses.cs.washington.edu/courses/cse590b/13au/lecture_notes/solvecubic_p4.pdf)

[ Blinn, J. F. (2007). How to solve a cubic equation, part 5: Back to numerics. IEEE Computer Graphics and Applications, 27(3):78–89.
][Official version](http://dx.doi.org/10.1109/MCG.2007.60) | [Author's version](https://courses.cs.washington.edu/courses/cse590b/13au/lecture_notes/solvecubic_p5.pdf)