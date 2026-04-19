---
title: Raytracing, Ray-Plane Testing
url: https://www.4rknova.com/blog/2018/01/01/raytracing-ray-plane-testing
author: Nikolaos Papadopoulos
published: '2018-01-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Definitions

A Ray is defined as:

\(\enclose{circle}[mathcolor="white"]{\color{white}{1}} \;\;\) \(P = P_0 + t * D\)

A Plane is defined as:

\(\enclose{circle}[mathcolor="white"]{\color{white}{2}} \;\;\) \(P \cdot N - C = 0\)

This formula is known as *Hesse Normal Form*. The symbols are interpreted as follows:

| Symbol | Interpretation |
|---|---|
| \(P_0\) | ray origin |
| \(D\) | ray direction (unit vector) |
| \(N\) | plane normal (unit vector) |
| \(C\) | plane distance from axis origin |

# Derivation

Substituting \(P\) in \(\enclose{circle}[mathcolor="white"]{\color{white}{2}}\) from \(\enclose{circle}[mathcolor="white"]{\color{white}{1}}\):

\[(P_0 + t * D) \cdot N - C = 0\] \[(P_0 \cdot N) + t * (D \cdot N) - C = 0\] \[P_0 \cdot N - C = -t * (D \cdot N)\]Solving for \(t\):

\(\enclose{circle}[mathcolor="white"]{\color{white}{3}} \;\;\) \(t = -\frac{(P_0 \cdot N - C)}{D \cdot N}\)

The ray is parallel to the plane and no intersection point exists if:

\[(D \cdot N) = 0\]If \(t\) is negative it means that the ray intersects the plane behind the ray’s origin point, at the opposite direction. Otherwise, there is a single intersection point at position \(P\) with:

\[P = P_0 + t * D\]Note the formula to calculate \(t\) can be manipulated a bit further to optimize the implementation.

Representing the plane distance as a dot product of a point \(X\) with the plane normal:

\[C = X \cdot N\]Therefore:

\[-(P_0 \cdot N - C) = C - P_0 \cdot N = X \cdot N - P_0 \cdot N = (X - P_0) \cdot N\]Substituting in \(\enclose{circle}[mathcolor="white"]{\color{white}{3}}\):

\[t = \frac{(X - P_0) \cdot N}{D \cdot N}\]# Implementation

```
bool Plane::intersection(const Ray &ray, HitRecord* i_info) const
{
// check if the ray is travelling parallel to the plane.
// if the ray is in the plane then we ignore it.
double n_dot_dir = dot(normal, ray.direction);
if (fabs(n_dot_dir) < EPSILON) return false;
Vector3f v = normal * distance;
Vector3f vorigin = v - ray.origin;
double n_dot_vo = dot(vorigin, normal);
double t = n_dot_vo / n_dot_dir;
if (t < EPSILON) return false;
if (i_info) {
i_info->t = t;
i_info->point = ray.origin + ray.direction * t;
i_info->normal = normal;
}
return true;
}
```