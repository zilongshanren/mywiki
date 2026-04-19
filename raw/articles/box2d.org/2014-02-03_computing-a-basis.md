---
title: Computing a Basis
url: https://box2d.org/posts/2014/02/computing-a-basis/
published: '2014-02-03'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

Feb 3, 2014

Given a normalized 3D vector, here’s an efficient method for computing a full basis. The computed basis is axis aligned if the input vector is axis aligned.

```
void ComputeBasis(const Vec& a, Vec* b, Vec* c)
{
// Suppose vector a has all equal components and is a unit vector:
// a = (s, s, s)
// Then 3*s*s = 1, s = sqrt(1/3) = 0.57735. This means that at
// least one component of a unit vector must be greater or equal
// to 0.57735.
if (Abs(a.x) >= 0.57735f)
b->Set(a.y, -a.x, 0.0f);
else
b->Set(0.0f, a.z, -a.y);
b = Normalize(b);
*c = Cross(a, *b);
}
```


In SSE land you can eliminate the branch using a select operation.