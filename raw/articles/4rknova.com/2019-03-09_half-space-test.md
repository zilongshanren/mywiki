---
title: Half-Space Test
url: https://www.4rknova.com/blog/2019/03/09/half-space-test
author: Nikolaos Papadopoulos
published: '2019-03-09'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

In computer graphics we sometimes need to determine which half-space a point is located in with regards to a plane. Perhaps the most common application of this is frustum culling, where we need to resolve whether a point lies within the camera frustum by testing against all of the frustum’s planes.

# Mathematical Formulation

For a given point \(m\) and a plane \(P\) defined by a normal vector \(\vec{N}\) and a point \(x\) on \(P\), test which half-space \(m\) lies in.

# Solution

The derivation is fairly simple:

Let \(d\) be the dot product between the plane’s normal and the vector pointing from a point on the surface of the plane to \(m\).

\[\vec{L} = m - x\] \[d = \vec{N} \cdot \vec{L}\]Depending on the sign of d, we identify one of three possible scenarios:

| \(d \gt 0\) | \(m\) lies on the half-space that \(\vec{N}\) is pointing to. |
| \(d \lt 0\) | \(m\) lies on the half-space opposite to \(\vec{N}\). |
| \(d = 0\) | \(m\) lies on the plane. |

In an alternative representation, a plane can be defined by its normal \(\vec{N}\) and a scalar distance \(k\) from the axis origin. In this format, we can easily calculate point \(x\).

\[x = k * \vec{N}\]In the diagram above \(m_0\) lies the half-space at the direction of the normal as the angle between the two vectors is less than \(\pi\). On the other hand \(m_1\) lies on the opposite half-space as the angle between the two vectors is greater than \(\pi\).

In practice to avoid issues that arise due to the finite precision of floating point numbers, the test condition is modified slightly to account for an error margin value \(\epsilon\).

| \(\,\,d \,\,\,\gt\,\,\,\,e\) | \(m\) lies on the half-space that \(\vec{N}\) is pointing to. |
| \(\,\,d \,\,\lt -e\) | \(m\) lies on the half-space opposite to \(\vec{N}\) |
| \(|d| \,\lt\,\,\,\,e\) | \(m\) lies on the plane. |