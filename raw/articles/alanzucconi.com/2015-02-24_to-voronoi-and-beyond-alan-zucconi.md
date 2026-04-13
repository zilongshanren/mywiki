---
title: To Voronoi and Beyond - Alan Zucconi
url: https://www.alanzucconi.com/2015/02/24/to-voronoi-and-beyond/
author: Alan Zucconi
published: '2015-02-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

## Voronoi Diagrams

This tutorial is a primer on Voronoi diagrams: what they are, what you need them for and how to generate them using a Shader in Unity. You can download the complete Unity page in Part 4.

Technically speaking, Voronoi diagrams are a way to tassellate a space. It means that the end result of Voronoi is a set of “puzzle pieces” which completely fills the space. To start, we need a set of points (often called *seeds*) in the space. Each seed will generate a piece of this puzzle. The way Voronoi works is by assigning every point of the space to its closest seed. The final result heavily depends on the way distance is measured in the space.

#### Euclidean distance

![Voronoi_1](../../assets/c90fda96378f11ba.png)

Most Voronoi diagrams are are based on the [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance). The *cost* between two points is given by the length of the shortest segment which connects them both. It can be calculated easily with the [Pythagorean theorem](https://en.wikipedia.org/wiki/Pythagorean_theorem):

![Rendered by QuickLaTeX.com \[D=\sqrt\left({\Delta x}^2+{\Delta y}^2 \right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d133fde51aaa6a9256f749a27f5b4c54_l3.png)


In Cg, this function is already implemented and is called `distance`

. The picture on the left shows a Voronoi diagram based on the Euclidean distance, drawn with 100 points. On the right, the same diagram uses a gradient to visualise the actual distance from a pixel to the closest one.

![Voronoi](../../assets/927867ede01a4873.png)

![Voronoi distance](../../assets/2c8d42d0b9087a53.png)

The distance diagram has been calculated using `minDist`

to sample a gradient from black to white.

#### Manhattan distance

![Voronoi_2](../../assets/f1828cc201760087.png)

As the name suggests, the Manhattan distance takes his name from the homonym city. The shortest path between two locations is not a straight line, since Manhattan is full of buildings. The shortest distance is the one which goes around building.

![Rendered by QuickLaTeX.com \[D=\left | \Delta x \right |+ \left | \Delta y \right |\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-32ebe7fb1b2082663c782ea990ee0f0c_l3.png)


half distance_manhattan(float2 a, float2 b) { return abs(a.x - b.x) + abs(a.y - b.y); }

Compared to the Euclidean distance, It is sensibly less expensive to calculate.

![manhattan](../../assets/6ec53d2fe34302ac.png)

![manhattan distance](../../assets/00df67345772bc42.png)

Using the Manhattan distance produces very intriguing patterns which resemble circuit boards. This is not a coincidence: many boards are designed to minimise circuit length and avoid curves.

#### Minkowski distance

![Voronoi_3](../../assets/9bee828e28dc11ed.png)

Despite looking very different, both the Euclidean and the Manhattan distances are both special cases of a more general metric: the [Minkowsi distance](https://en.wikipedia.org/wiki/Minkowski_distance). To understand why, you have to remind some algebra. In the same way multiplication and division are the same operator (dividing by ![Rendered by QuickLaTeX.com 10](../../assets/9d8a85c6b878c053.png)

![Rendered by QuickLaTeX.com \frac{1}{10}](../../assets/aaf18dc17c863b00.png)

![Rendered by QuickLaTeX.com \sqrt[n]{x} = x^{ 1/n }](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c2493b7dad422922308065cc3e4af173_l3.png)


![Rendered by QuickLaTeX.com \[D= \left( { \left| {\Delta x} \right | ^p+\left| {\Delta y} \right |^p } \right)^{1/p}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f19c85f15795b7ab8cad6a1dbf85465c_l3.png)


When ![Rendered by QuickLaTeX.com p=1](../../assets/111814dc24d14d57.png)

![Rendered by QuickLaTeX.com p=2](../../assets/e4b3ed9e60c6b889.png)


half distance_minkowski(float2 a, float2 b, float p) { return pow(pow(abs(a.x - b.x),p) + pow(abs(a.y - b.y),_P),1/p); }

The most fascinating aspect is that is provides a way to smoothly transitioning from the Euclidean to the Manhattan distance, and the other way round.

![m2v](../../assets/3948a52ca1210329.gif)

![m2v_d](../../assets/5dbe0416098672e8.gif)

If you are in a higher dimension, the Minkowski distance can be still used, providing that you calculate it on all the components of two points ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com b](../../assets/0bcd696a7c0431b0.png)


![Rendered by QuickLaTeX.com \[D= \left( {\sum_i^n \left|{a_i - b_i}\right |^p } \right)^{1/p}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f849cef2cf0ce282fb872a7b96e93f9b_l3.png)


The next part of this tutorial will focus on the applications of Voronoi diagrams.

## Applications

Despite looking pretty, not a single application has been indicated for Voronoi diagrams yet. In actuality, they play a very important role in Science, and many games can benefits from them.

#### In games

Breaking object realistically is a very challenging task, that requires to know how pressure waves propagates through a material. A simpler way to create plausible fractures in an object is to rely on a Voronoi 3D tassellation. You start choosing random points within the object you want to break, then each Voronoi cell become one of its chunks. In games, breakable objects don’t break: they are already broken, and your interaction makes the piece falling apart.

![fracturedcube-e1358120248710](../../assets/63083a83da3839fa.jpg)

The famous [Fracturing & Destruction](https://www.assetstore.unity3d.com/en/#!/content/9411) plugin on the Asset Store, for instance, uses this technique to generate breakable objects. A future post will show how to replicate this effect at no cost.

#### In path finding

As a game developer, you might be familiar with path finding. A* is notoriously the most known, but there are many other ways one can find the optimal path between two points. So far, Voronoi diagrams have been seen as independent regions of space although there is an alternative way of interpreting them. If we put a node every time two segments connects, Voronoi produces a graph. The segments (now edges of the graph) represent the paths which are as far as possible from the seeds. In terms of gaming, seeds can be enemies you want to avoid; travelling on the edges provides the safest route possible. Brent Owens has written a very nice [tutorial](http://gamedevelopment.tutsplus.com/tutorials/how-to-use-voronoi-diagrams-to-control-ai--gamedev-11778) about this.

![Voronoi_diagrams_for_AI-9-voronoi_safe_path](../../assets/fd04dc9619d4011c.jpg)

Conversely, Voronoi diagrams can be also used to approximate the shortest path. The dual graph of a Voronoi diagram (known as the [Delaunay triangulation](http://mathworld.wolfram.com/DelaunayTriangulation.html)) allows to find paths which are as close as possible to the seeds. When coupled with the Manhattan distance, it can be used to generate the [fastest route within a city](http://i11www.iti.uni-karlsruhe.de/en/projects/geonet/cvd#voronoi_regions_that_take_roads_into_account), considering how fast you can go on different roads.

![cityvoronoi](../../assets/e2d97392d01f4d3e.png)

#### In nature

![2000px-Circle_packing_(hexagonal).svg](../../assets/7301897c5a8025d3.png)

[Circle packing](https://en.wikipedia.org/wiki/Circle_packing) is the problem of fitting as many circles as possible in a given space. The best possible solution to this problem is shown on the left; circles are arranged in a hexagonal lattice, which resemble a honeycomb. This is actually why honeycomb cells have a hexagonal structure: if all circle expands at the same time to fill all the space around them, they’ll end up pressing against each other until they create a perfect hexagonal lattice. The same pattern can be found in several other phenomena, like [cooling magma](http://beautifulplacestovisit.com/wp-content/uploads/2011/12/Fingals_Cave_Staffa_Scotland_02.jpg) and [soap bubbles](http://www.cd-adapco.com/sites/default/files/iStock_000012676217Large.jpg). The latter, provide an excellent (and transparent) example of how Voronoi diagrams look in three dimensions.

The next part of this tutorial will show how to generate Voronoi diagrams using Shaders.

## Generation

![Fortunes-algorithm-slowed](../../assets/68dafe505e4b8b59.gif)

There are several algorithms you can rely on to generate Voronoi diagrams. Every point is independent from the other, so this is one of those perfect applications for a shader. Traditionally the [Fortune’s algorithm](https://en.wikipedia.org/wiki/Fortune%27s_algorithm) (left) is commonly used, but it is very hard to implement within a shader. The tricky part, in this case, is how to provide a list of points to the Material, since the Unity APIs don’t provide any `SetArray`

function. Luckily, there is an undocumented feature you can use to pass arrays and matrices to a shaders, and it has been discussed in [this post](https://www.alanzucconi.com/2016/01/27/arrays-shaders-heatmaps-in-unity3d/). We will use one array for the position of the points (in a 2D space) and another one for the colours. A variable called `_Length`

is used to indicate how many points are there since Cg doesn’t support arrays of arbitrary dimensions.

uniform int _Length = 0; uniform half2 _Points[100]; uniform fixed3 _Colors[100];

The actual code of the Voronoi diagram is implemented in the fragment function. For each pixel, it simply loops over all the points and finds the closest one. Its index is then used to find the right colour to use:

fixed4 frag(vertOutput output) : COLOR { half minDist = 10000; // (Infinity) int minI = 0; for (int i = 0; i < _Length; i++) { half dist = distance(output.worldPos.xy, _Points[i].xy); if (dist < minDist) { minDist = dist; minI = i; } } return fixed4(_Colors[minI], 1); }

Different types of diagrams are possible simply by replacing the function distance with the appropriate metric. If you want to draw the distance diagram instead, you can sample a ramp texture using `minDist`

. You can also set the texture mode to “Repeat” rather than “Clamp” for some bizarre effects.

half4 color = tex2D(_RampTex, fixed2(minDist, 0.5)); color.a = 1; return color;

#### Weighted Voronoi diagrams

Interesting results can be obtained by mixing different metric, or altering the “attraction” of the seeds by providing an extra coefficient to the shader. The distance is now:

half dist = distance(output.worldPos.xy, _Points[i].xy) + _Weights[i];

This takes the name of [weighted Voronoi](https://en.wikipedia.org/wiki/Weighted_Voronoi_diagram) (also known as Dirichlet tessellation) and it can be used to generate beautiful effects, like Milan Domkář did with his [foam](http://domkar.cz/?stranka=generovani&generovaniID=foam&nas_jazyk=en):

![01](../../assets/b82d7dfca4708a17.png)

#### Cone projection

![cones.gif](../../assets/92450d30060a5772.gif)

There is a smarter approach to generate Voronoi diagrams (almost!) for free, and [Chris Wellons](http://nullprogram.com/blog/2014/06/01/) is beautifully explaining it in its blog. You can generate a Voronoi tessellation by projecting cones out of the starting points. The cones will eventually intersect and seeing them it from the above will produce the same effect.

You can download the full Unity package in the last part of this tutorial.

## Conclusion & Download

Voronoi diagrams are a way to tessellate the space which has many applications, from game development to city planning. This tutorial has shown how to generate them using a shader; you can download the complete [Unity package here](https://drive.google.com/file/d/0B4nCcaMlgxV2cVRnXzBabnptUlk/view?usp=sharing).

#### Other resources

[How to Use Voronoi Diagrams to Control AI](http://gamedevelopment.tutsplus.com/tutorials/how-to-use-voronoi-diagrams-to-control-ai--gamedev-11778): How Voronoi diagrams can be used to create very good AIs which avoids enemy;[Pathing Excursions](http://www.gamasutra.com/blogs/SvenBergstrom/20140109/208374/Pathing_Excursions__more_natural_paths.php): A way to create very realistic AIs which can patrol around buildings;[A GPU Approach to Voronoi Diagrams](http://nullprogram.com/blog/2014/06/01/): How to render Voronoi diagrams on the GPU, in a very smart way;[Voronoi Diagram for the City-Metric](http://i11www.iti.uni-karlsruhe.de/en/projects/geonet/cvd#voronoi_regions_that_take_roads_into_account): Voronoi diagrams applied to city planning;[foam](http://domkar.cz/?stranka=generovani&generovaniID=foam&nas_jazyk=en): a bubble-like lattice created using weighted Voronoi diagrams.[Voronoi Diagrams on the GPU](http://rykap.com/graphics/skew/2016/02/25/voronoi-diagrams/)

## Leave a Reply Cancel reply