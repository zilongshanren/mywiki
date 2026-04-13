---
title: 'fma: A faster, more accurate instruction'
url: http://momentsingraphics.de/FMA.html
published: '2021-12-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# fma: A faster, more accurate instruction

When people look at my shader code, one of the most frequently asked questions is why I use the GLSL [ fma](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/fma.xhtml) instruction (or its HLSL equivalent

[) so frequently. In spite of the punny title of this post,](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/mad)

`mad`

`fma`

actually stands for fused multiply-add, i.e. it implements the formula `fma(a,b,c)=a*b+c`

. It is faster than separate multiplication and addition because on most CPUs and GPUs it counts as one instruction. It also introduces less rounding error. The real question is whether you should rely on the compiler to use it as appropriate or not. This post explains why I don't and shows a few neat numerical tricks that benefit from `fma`

.## Accuracy, speed and availability

My claim that `fma`

is more accurate is not really backed by the [GLSL specification](https://www.khronos.org/registry/OpenGL/specs/gl/GLSLangSpec.4.60.pdf). If the return value of `fma`

contributes to the value of a variable designated with the `precise`

keyword, the computation *can* be more accurate but it is not guaranteed. In absence of the `precise`

keyword, compilers are allowed to treat `fma(a,b,c)`

as `a*b+c`

. Vice versa, the `precise`

keyword, prohibits conversion of multiplication and addition to fused multiply-add, so it may make code slower and less accurate (but with more predictable behavior). HLSL follows similar rules.

In spite of these lax guarantees, it works as desired on practically all hardware. For many years, all notable GPUs and CPUs have supported fused multiply-add. On GPUs, it may be thought of as the cheapest instruction. Latency is low, throughput is high. Multiplication is equally expensive and so is addition. In my experience, compilers also take the hint when you use `fma`

or `mad`

and reliably use fused multiply-add, even when the `precise`

keyword is not used. There may be exceptions though. Fused multiply-add is also available on CPUs, e.g. through [ std::fma](https://en.cppreference.com/w/cpp/numeric/math/fma) in C++11.

To understand in what sense exactly `fma`

is more accurate, we should look at how different implementations of this formula introduce rounding errors in floats. We begin with a naive implementation of `a*b+c`

:

- First \(ab\) is evaluated.
- The result of \(ab\) gets rounded to the nearest float. We call this rounded result \(d\).
- Now \(d+c\) is evaluated.
- The result gets rounded to the nearest float.

Note how we get rounding errors twice, once for the multiplication and once for the addition. Here is what `fma(a,b,c)`

does:

- First \(ab+c\) is evaluated.
- The result gets rounded to the nearest float.

Thus, we only get rounding errors once. In situations where numeric cancellation may arise, that can make a big difference. As an example, consider \(a=1.00000011920929\), \(b=53400708\) and \(c=-b\). The value of \(a\) is chosen to be representable by a 32-bit float with almost no error. Then \(ab\) is going to be slightly bigger than \(b\). Overall, it is pretty big and big floats have lower absolute precision. The small perturbation due to the \(0.00000011920929\) part of \(a\) gets impacted by rounding errors heavily. In fact, it ends up being an integer. Then we add \(c\) (i.e. we subtract \(b\)) so this small perturbation is all that remains. With \(ab+c\) evaluated naively with 32-bit floats, the result is \(8\). With `fma`

the result is \(6.365860462\), which is what it should be (64-bit floats give the same digits). Without `fma`

, we do not get a single correct decimal digit. With `fma`

, we get ca. 8 correct digits, which is as much as we can hope for with 32-bit floats.

Of course, this is a contrived example. The point is that it is wrong to think that rounding once instead of twice gives you half as much rounding error. It can make the difference between complete loss of accuracy and perfectly accurate results. Below, we will encounter a few clever ways to make use of this guarantee on accuracy.

## Counting instructions

Most of the time, when I use `fma`

it is not due to a clever numerical trick. I just want to keep track of how many instructions get issued in compute-intense numerical code. When I see an invocation of `fma`

, I can be pretty sure that it maps to one instruction. When I see multiplication or addition, it is harder to reason about the cost. In the ideal case, all multiplications and additions can be paired up and fused so that there are exactly as many instructions as multiplications. Then additions are free. But that is not always possible. For example, \((a+b+c)de\) has two additions and two multiplications but there is no way to implement this formula with less than four instructions. By using `fma`

most of the time, I'm more aware of the actual cost and sometimes that inspires me to rearrange an expression in a way that will make better use of this hardware feature. Compilers are also quite limited in how they can rearrange expressions due to IEEE compliance. The next section has an example where that leads to an increased instruction count.

## Predictable results

Another benefit of using `fma`

is that results are more predictable in terms of numerical accuracy. If I implement a numerical procedure (e.g. [solving cubic equations](http://momentsingraphics.de/CubicRoots.html) or [sampling of linear lights](http://momentsingraphics.de/HPG2021.html)) using `fma`

in most suitable places, the compiler has less freedom in how it implements this code. Thus, it is a bit safer to assume that code, which produces accurate results on my system, will also do so on other systems.

And sometimes, I rely on the extra precision offered by `fma`

explicitly. Consider, for example this line of code from the method for [sampling of linear lights](http://momentsingraphics.de/HPG2021.html):

`fma(dot_0, dir.s, fma(angle, line.normal.t, -cdf))`


The following line of code implements the same mathematical expression:

`dot_0 * dir.s + angle * line.normal.t - cdf`


Addition of floats is not associative, so the compiler is forced to implement this expression like:

`(dot_0 * dir.s + angle * line.normal.t) - cdf`


My system then apparently turns this into:

`fma(dot_0, dir.s, angle * line.normal.t) - cdf`


That is one `fma`

, one multiplication and one addition, compared to only two `fma`

with the first version. More importantly, I know that the substraction of `cdf`

is prone to cancellation in certain regions (see Section 3.4 of [the paper](http://momentsingraphics.de/HPG2021.html)). Performing it inside the `fma`

instruction gives a big improvement in accuracy. By using `fma`

, I can be fairly certain that this more accurate formulation is being used.

A lot of the time, this sort of effort is not necessary but there are many problems in computer graphics where it is hard to formulate truly stable solutions. In such cases, it makes sense to analyze intermediate values and to understand which computations are particularly prone to cancellation. Placing `fma`

strategically can then alleviate these problems.

## Readability

Of course, using `fma`

all the time can harm readability of code. I've made used to it but mapping code to formulas still takes a bit more mental effort. It also makes the code more confusing to novices. That is reason enough not to overdo it. For performance-sensitive code with strong demands on numerical accuracy, it makes sense. Otherwise, not so much. A middle ground could be to avoid `fma`

but to try to nudge the compiler towards using it in the intended way by placing more parentheses. Though, that isn't exactly pretty either and mostly sacrifices the benefits discussed above.

## Horner's method

There are a few more or less well-known tricks that benefit from `fma`

directly. One of them is Horner's method for evaluation of polynomials. Say, I have a cubic polynomial
\[
p(x):=ax^3 + bx^2 + cx + d.
\]
A naive way to evaluate it at \(x\) is as follows:

```
float x2 = x * x;
float x3 = x2 * x;
float p = a * x3 + b * x2 + c * x + d;
```


This code uses five multiplications and three additions. A compiler may implement it as if it were:

```
float x2 = x * x;
float x3 = x2 * x;
float p = fma(c, x, fma(a, x3, b * x2)) + d;
```


Now we are down to six instructions. We also need at least two registers to store `x2`

and `x3`

. That is not great.

The trick in Horner's method is to rewrite the polynomial like this:
\[
p(x)=((ax + b)x + c)x + d
\]
We still multiply \(a\) by \(x\) three times, so we have \(ax^3\) in there as intended. And it works out similarly for \(b\) and \(c\). Mapping Horner's method to code using `fma`

is easy:

`float p = fma(fma(fma(a, x, b), x, c), x, d);`


That brings us down to three instructions and we also do not need the registers for `x2`

and `x3`

anymore. In terms of speed, it does not get better than that. It naturally generalizes to polynomials of arbitrary degree. Numerical stability is still not great but at least better than with the naive method.

## Kahan's algorithm

When it is applicable, `fma`

is a blessing in terms of numerical accuracy. But often the reasons for a cancellation cannot be pinned down to an expression as simple as \(ab+c\). One pattern that comes up often is computing \(ab-cd\). For example, determinants of \(2\times 2\) matrices, entries of cross products and dot products of vectors with two entries can all be computed in this manner. We have two naive options to implement this with `fma`

:

```
fma(a, b, -c * d)
fma(-c, d, a * b)
```


Both take only two instructions. Though, choosing one over the other is tricky. And we still have a multiplication in there. Its result gets rounded prior to the subtraction, so we do not really avoid cancellation.

Kahan's algorithm is a wonderful way to avoid accuracy problems in this situation. I first learned about it in a [blog post by Matt Pharr](https://pharr.org/matt/blog/2019/11/03/difference-of-floats). It goes as follows:

```
float kahan(float a, float b, float c, float d) {
float cd = c * d;
float error = fma(c, d, -cd);
float result = fma(a, b, -cd);
return result - error;
}
```


The line that computes `error`

is key to understanding it. It implements the formula \(cd-cd\), so that value should be zero. In fact, when it is written without `fma`

, it gets optimized away. But in floating-point arithmetic it is not zero. The value of `cd`

has rounding errors. Through `fma`

, we get the difference (rounded to a float) between the exact product and the computed product. Usually, this rounding error would also be present in the end result. In an ingenious move, the last line subtracts this error from the end result, thus making it more accurate.

This intuitive explanation does not give us any hard guarantees but the method is thoroughly studied. It is proven that, as long as no underflow or overflow occurs, the error in `kahan(a,b,c,d)`

is at most 1.5 units of least precision (ulps), i.e. three times bigger than the rounding error expected in a single addition [[Jeannerod2013]](http://momentsingraphics.de#_Jeannerod2013). Cancellation, which could cause arbitrarily many ulps of error as demonstrated above, is no concern at all. This infinite improvement of the worst-case error is accomplished by doubling the instruction count (from two to four).

Kahan’s algorithm can be used in many places but of course, it should be restricted to cases, which really need it. For example, my algorithm for [sampling of polygonal lights](http://momentsingraphics.de/Siggraph2021.html) needs to compute the cross product of vectors from the shading point to two different vertices of a polygonal light. If the light is small and distant, these vectors are nearly parallel. Then each entry of the cross product is prone to cancellation. That has caused seldom but visible artifacts. Using Kahan's algorithm resolved the problem.

## Unevaluated sums

With Kahan's algorithm in mind, one may ask whether there is a more general way to improve the accuracy. Unevaluated sums are an answer to that [[Thall2007]](http://momentsingraphics.de#_Thall2007). They let you double the precision of a floating-point type. The idea is to decompose a number in the form \(a=a_\mathrm{hi}+a_\mathrm{lo}\), where \(a_\mathrm{hi}\) is a float representation of \(a\) and \(a_\mathrm{lo}\) is the rounding error in this representation. All common mathematical operations can be implemented in terms of these unevaluated sums without losing the extra precision. That is possible with or without `fma`

but with `fma`

, it is faster.

For example, here is what multiplication of unevaluated sums looks like (modified version of [Andrew Thall's code](http://momentsingraphics.de/andrewthall.org/dist/extPrecision.cg.zip), not tested):

```
vec2 df64_mult(vec2 a, vec2 b) {
precise vec2 p;
p.x = a.x * b.x;
p.y = fma(a.x, b.x, -p.x);
p.y += a.x * b.y;
p.y += a.y * b.x;
float s = p.x + p.y;
return vec2(s, p.y - (s - p.x));
}
```


Unevaluated sums are sortof a big gun. But when it is not possible to make do with less precision and the hardware does not support more, they are a reliable way to accomplish the goal. And thanks to `fma`

they are not all that slow. Double precision arithmetic is available on most GPUs now but unevaluated sums can be used to push the available precision beyond that.

## Conclusions

Most of the computation done by GPUs is fused multiply-add on floats. There are other pipes for special functions, integer arithmetic and more but usually, `fma`

is the bulk of the work. From a performance standpoint, it is important to understand that multiplication, addition and fused multiply-add are equally expensive. Thus, placing a few parentheses or using `fma`

explicitly can reduce the instruction count. When the code is limited by throughput of the `fma`

-pipe, that will give a speedup. And when it comes to numerical stability, a cleverly used `fma`

can work wonders. The beauty of it is that it is fast *and* accurate. My practice of writing it out may be slightly obnoxious, but it helps to make my implementations faster and more accurate.

## References

[ Jeannerod, Claude-Pierre and Louvet, Nicolas and Muller, Jean-Michel (2013). Further analysis of Kahan’s algorithm for the accurate computation of \(2\times 2\) determinants. Mathematics of Computation 82. AMS. ][Official version](https://doi.org/10.1090/S0025-5718-2013-02679-8)

[ Thall, Andrew (2007). Extended-Precision Floating-Point Numbers for GPU Computation. Technical Report CIM-007-01. The University of North Carolina at Chapel Hill. ][Author's version](http://andrewthall.org/papers/df64_qf128.pdf)