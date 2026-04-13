---
title: CSGJS-CPP on GitHub
url: https://www.executionunit.com/blog/2020/04/24/csgjs-cpp-on-github/
published: '2020-04-24'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

I spent some time playing around with [CSGJS](https://github.com/evanw/csg.js/) over the weekend. It’s a great library. I thought it might be interesting to port it to C++.

After quite a lot of googling I found that someone had already done most of the hard work [here](https://github.com/dabroz/csgjs-cpp) which was nice and they had kept the MIT license which was even better.

I decided I’d take their work and see if I could improve it a little and learn how it worked.

The fundamental algorithm used is to take two sets of convex polygons that make up a 3D model, create separate [BSP trees](https://en.wikipedia.org/wiki/Binary_space_partitioning) and then perform union, subtract or difference algorithms upon the target BSP tree. The algorithm is actually very nice and well documented here [Constructive Solid Geometry Using BSP Tree - Christian Segura1, Taylor Stine2, Jackie Yang](https://pdfs.semanticscholar.org/eeb5/014f86750c54a87f214b03246799e970d114.pdf).

The code I took worked pretty well but I managed to optimize making it about 40% faster and removed the memory leaks.

Here are some examples of the output.

**A gourd with a cylinder subtracted**

![](../../assets/4ac7aa0e71516865.png)


**The same gourd with the cylinder added (union)**

![](../../assets/aec1d75c40ee40be.png)


**Cube with a sphere union and cylinder subtracted along x, y and z axis**

![](../../assets/605d4be38a668137.png)


The good thing about the algorithm is that it’s recursive nature and simple testable stages make it pretty easy to implement and test. The downside is that the creation of BSP trees both at the initial “list of polygons to BSP” stage and the processing stage cause a lot of allocations making this unsuitable for real time operations.

Anyway, all my changes and test harness are available on [git hub](https://github.com/executionunit/csgjs-cpp) for people to play with.

## Comments