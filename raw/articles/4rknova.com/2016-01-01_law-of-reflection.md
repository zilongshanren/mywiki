---
title: Law of Reflection
url: https://www.4rknova.com/blog/2016/01/01/law-of-reflection
author: Nikolaos Papadopoulos
published: '2016-01-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

The law of reflection defines how incident light rays reflect off the surface of a conducting material, and is governed by the following principles:

- The incident ray, the reflected ray, and the normal to the surface at the point of incidence all lie in the same plane.
- The angle of reflection is equal to the angle of incidence.

# Derivation

The reflected ray for normalized normal vector \(n\) and incidence vector \(i\) pointing towards the surface, is calculated as follows:

\[r = i − 2 (i \cdot n) n\]The formula is easy to derive. Starting with the second principle of the law of reflection, which states that the angle of reflection is equal to the angle of incidence, we get:

\[\theta_i = \theta_r \\\ cos(\theta_i) = cos(\theta_r) \\\ |n| cos(\theta_i) = |n| cos(\theta_r) \\\ |i| |n| cos(\theta_i) = |r| |n| cos(\theta_r)\]Since the incident ray \(i\) is directed towards the surface, it needs to be reversed.

\(\enclose{circle}[mathcolor="white"]{\color{white}{1}}\) \(-i \cdot n = r \cdot n\)

Let

| \(n_i = (-i \cdot n) n\) | be the projection of \(-i\) on to \(n\) |
| \(n_r = ( r \cdot n) n\) | be the projection of \(r\) on to \(n\) |

From the diagram above it’s easy to see that:

\[\vec{rn} = - \vec{in} \\\ r - n_r = -(-i - n_i) \\\ r - (r \cdot n) n = - (-i - (-i \cdot n) n) \\\ r - (r \cdot n) n = i + (-i \cdot n) n \\\ r = (r \cdot n) n + i + (-i \cdot n) n\]Substituting from \(\enclose{circle}[mathcolor="white"]{\color{white}{1}}\)

\[r = (-i \cdot n) n + i + (-i \cdot n) n \\\ r = i + 2 (-i \cdot n) n \\\ r = i - 2 (i \cdot n) n\]# Implementation

Below you can find a sample implementation in c:

```
static inline vec2_t vec2_reflect(vec2_t i, vec2_t n)
{
vec2_t normal = vec2_normalize(n);
vec2_t incident = vec2_normalize(i);
scalar_t val = 2 * vec2_dot(incident, normal);
return vec2_sub(incident, vec2_scale(normal, val));
}
```