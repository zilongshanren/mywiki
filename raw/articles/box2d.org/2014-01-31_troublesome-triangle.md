---
title: Troublesome Triangle
url: https://box2d.org/posts/2014/01/troublesome-triangle/
published: '2014-01-31'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

I ran into a problem computing a polygon normal using Newell’s method as described in Christer Ericson’s excellent book Real-Time Collision Detection. In this case the polygon happens to a be a triangle that is close to the origin. So I would guess that Newell’s method would yield a great result. However, this is not true. I only get 2 digits of accuracy in single precision.

Here is the triangle:

```
p1 = (0.331916571, 0.382771939, -0.465963870)
p2 = (0.378853887, -0.246981591, -0.440359056)
p3 = (0.331879079, 0.382861078, -0.465974003)
```


I knew I was getting a bad normal because some of my convex hull code was failing. So I decided to analyze the problem. First of all, this triangle has edge lengths of around 0.6320, 0.6321, and 1e-4. So this is a sliver and it is well known that slivers can be numerically challenging.

I computed a baseline normal using doubles. Doubles yielded the following normal vector (truncated to 6 digits):

normal_doubles = (0.206384 -0.0243884 -0.978167).

I got the same result computing the normal in many different ways. So I am confident that this is accurate.

Then I computed the normal many several different ways using single precision:

- 1 way using Newell’s method as stated in Christer’s book
- 3 ways using edge cross products
- 3 ways using Newell’s method on the triangle shifted to each vertex (suggested by Christer)
- 1 way using Newell’s method on the triangle shifted to the centroid

Here is the code:

```
#include <math.h>
#include <stdio.h>
typedef float Real; // change this to double to get a high accuracy result
inline float Sqrt(float s)
{
return sqrtf(s);
}
inline double Sqrt(double s)
{
return sqrt(s);
}
struct Vec
{
Vec() {}
Vec(Real x_, Real y_, Real z_) { x = x_; y = y_; z = z_; }
Real x, y, z;
};
inline Vec operator-(const Vec& a, const Vec& b)
{
return Vec(a.x - b.x, a.y - b.y, a.z - b.z);
}
inline Vec operator+(const Vec& a, const Vec& b)
{
return Vec(a.x + b.x, a.y + b.y, a.z + b.z);
}
inline Vec Cross(const Vec& a, const Vec& b)
{
return Vec(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}
inline Vec Newell(const Vec& a, const Vec& b)
{
return Vec((a.y - b.y) * (a.z + b.z), (a.z - b.z) * (a.x + b.x), (a.x - b.x) * (a.y + b.y));
}
inline Vec Normalize(const Vec& a)
{
float d = Sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
return Vec(a.x/d, a.y/d, a.z/d);
}
inline Real Length(const Vec& a)
{
return Sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
}
int main()
{
Vec p1(0.331916571f, 0.382771939f, -0.465963870f);
Vec p2(0.378853887f, -0.246981591f, -0.440359056f);
Vec p3(0.331879079f, 0.382861078f, -0.465974003f);
Vec newell = Normalize(Newell(p1, p2) + Newell(p2, p3) + Newell(p3, p1));
Vec e1 = p2 - p1;
Vec e2 = p3 - p2;
Vec e3 = p1 - p3;
Real d1 = Length(e1);
Real d2 = Length(e2);
Real d3 = Length(e3);
Vec n1 = Cross(e3, e1);
Vec n2 = Cross(e1, e2);
Vec n3 = Cross(e2, e3);
Real s1 = Length(n1);
Real s2 = Length(n2);
Real s3 = Length(n3);
n1 = Normalize(n1);
n2 = Normalize(n2);
n3 = Normalize(n3);
Vec shift1 = Normalize(Newell(p1-p1, p2-p1) + Newell(p2-p1, p3-p1) + Newell(p3-p1, p1-p1));
Vec shift2 = Normalize(Newell(p1-p2, p2-p2) + Newell(p2-p2, p3-p2) + Newell(p3-p2, p1-p2));
Vec shift3 = Normalize(Newell(p1-p3, p2-p3) + Newell(p2-p3, p3-p3) + Newell(p3-p3, p1-p3));
Vec c = p1 + p2 + p3;
c.x = c.x / 3.0f;
c.y = c.y / 3.0f;
c.z = c.z / 3.0f;
Vec shiftc = Normalize(Newell(p1-c, p2-c) + Newell(p2-c, p3-c) + Newell(p3-c, p1-c));
printf("%g %g %g\n", newell.x, newell.y, newell.z);
printf("%g %g %g\n", n1.x, n1.y, n1.z);
printf("%g %g %g\n", n2.x, n2.y, n2.z);
printf("%g %g %g\n", n3.x, n3.y, n3.z);
printf("%g %g %g\n", shift1.x, shift1.y, shift1.z);
printf("%g %g %g\n", shift2.x, shift2.y, shift2.z);
printf("%g %g %g\n", shift3.x, shift3.y, shift3.z);
printf("%g %g %g\n", shiftc.x, shiftc.y, shiftc.z);
}
```


And here are the results:

```
0.205007 -0.0244907 -0.978454
0.206384 -0.0243884 -0.978167
0.206417 -0.0243837 -0.97816
0.206384 -0.0243884 -0.978167
0.206377 -0.0243887 -0.978168
0.206453 -0.024386 -0.978153
0.206315 -0.0243899 -0.978182
0.206375 -0.0243882 -0.978169
```


Exact:

```
0.206384 -0.0243884 -0.978167
```


As you can see, Newell’s method is only giving 2 digits of accuracy. Every other method is giving close to 4 digits of accuracy or more. The best result is from n1 and n2. Both of these are cross products that include the shortest edge. This agrees with Gino van den Bergen’s comments on [Twitter](https://twitter.com/erin_catto/status/408711096631971841).

Shifting the triangle origin to one of the vertices or the centroid all improve Newell’s method substantially. I’m a little disappointed that Newell’s method is still not as good as *any* of the cross products. The price of generality?

Bottom line:

- Shift a vertex to the origin before applying Newell’s method.
- Cross products can produce triangle normals that are superior to the results of Newell’s method.
- Switching to doubles can solve numerical problems, but it is better to first understand the underlying issue.