---
title: VoronatorSharp
url: https://www.boristhebrave.com/2022/09/10/voronator-sharp/
author: Boris
published: '2022-09-10'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve relased a new library, [ VoronatorSharp](https://github.com/BorisTheBrave/voronator-sharp).

VoronatorSharp is a C# library that computes [Voronoi diagrams](https://en.wikipedia.org/wiki/Voronoi_diagram). The Voronoi diagram for a collection of points is the polygons that enclose the areas nearest each of those sites.

Voronoi diagrams have applications in a number of areas such as computer graphics.

This library features:

- Computes Voronoi diagrams and
[Delaunay triangulations](https://en.wikipedia.org/wiki/Delaunay_triangulation). - Voronoi polygons can be clipped to a rectangular area.
- Uses a
`n log(n)`

[sweephull algorithm](https://github.com/mapbox/delaunator#papers). - The implementation attempts to minimize memory allocations.
- Integrates with Unity or can be be used standalone.
- Uses
[robust orientation code](https://github.com/govert/RobustGeometry.NET). - Handles Voronoi diagrams with only 1 or 2 points, and collinear points.