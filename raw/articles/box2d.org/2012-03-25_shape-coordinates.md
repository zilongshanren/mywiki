---
title: Shape Coordinates
url: https://box2d.org/posts/2012/03/shape-coordinates/
published: '2012-03-25'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

Keep in mind that a shape does not know about bodies and stand apart from the dynamics system. Shapes are stored in a compact form that is optimized for size and performance. As such, shapes are not easily moved around. You have to manually set the shape vertex positions to move a shape. However, when a shape is attached to a body using a fixture, the shapes move rigidly with the host body. In summary:

- When a shape is
**not**attached to a body, you can view it’s vertices as being expressed in world-space. - When a shape is attached to a body, you can view it’s vertices as being expressed in local coordinates.