---
title: Random Paths via Chiseling
url: https://www.boristhebrave.com/2018/04/28/random-paths-via-chiseling/
author: Boris
published: '2018-04-28'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I went over a previous project to [randomly generate paths between points](https://www.boristhebrave.com/www.boristhebrave.com/2017/07/15/random-path-algorithm/) and came up with a much more efficient and versitile algorithm.

(**EDIT**: [In 2022 I found an even better way](https://www.boristhebrave.com/2022/03/20/chiseled-paths-revisited/).)

The algorithm is simple. Start with the entire area covered in path tiles, then and remove tiles one by one until only a thin path remains. When removing tiles, you cannot remove any tile that will cause the ends of the path to become disconnected. These are called articulation points (or cut-vertices). I use a [fast algorithm based on DFS](https://stackoverflow.com/questions/15873153/explanation-of-algorithm-for-finding-articulation-points-or-cut-vertices-of-a-gr) to find the articulation points. I had to modify the algorithm slightly so it only cares about articulation points that separate the ends, rather than anything which cuts the area in two. After identifying articulation points it’s just a matter of picking a random tile from the remaining points, and repeating. When there are no more removable tiles, you are done. Or you can stop early, to give a bit of a different feel.

I call it “chiseling” as you are carving the path out of a much larger space, piece by piece.

See on [github ](https://github.com/BorisTheBrave/chiseled-random-paths).


I don’t think I’ve seen anyone propose this technique before – it generates quite organic looking paths and is pretty easy to implement.

It’s quite flexible as it works on any graph, and you can control the generation by changing the probability of each tile being selected. It can connect together any number of endpoints. I also made a version that generates paths with a fixed number of tiles but no specific endpoints.

Here’s a demo below showing both sorts of generation.