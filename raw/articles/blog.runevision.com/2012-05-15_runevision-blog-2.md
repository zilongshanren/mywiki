---
title: runevision blog
url: https://blog.runevision.com/2012/05/
published: '2012-05-15'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I got a mail from Robert Stehwien asking me how to generate an environment tree ([as described on Squidi.net](http://www.squidi.net/three/entry.php?id=4)) from a 2D maze - something I [wrote](http://blog.runevision.com/2010/08/eas-demo-of-procedural-environment.html) [previously](http://blog.runevision.com/2011/08/forcing-structure-in-procedural-spaces.html) that I do in my game [The Cluster](http://blog.runevision.com/search/label/TheCluster) but didn't go in details with.

An environment tree is basically a [tree structure](http://en.wikipedia.org/wiki/Tree_structure) representing connectivity in a spatial space, where inner nodes represent junctions where for example a corridor splits into two or more, and leaf nodes represent dead ends. An environment tree of a 2D maze would have inner nodes where the maze corridors split into two or more and leaf nodes at dead ends.

![](../../assets/0185f87115eb9cba.jpg)

I wrote the code for doing it more than five years ago. It's rather convoluted but anyway, this is how it works:

I use a ["recursive back-tracker"](http://www.astrolog.org/labyrnth/algrithm.htm#solve) algorithm which is basically the same as a depth-first search. Despite the name of the method, I implemented it as a loop and not as a recursive function. Every time it hits a dead end, it marks the cell as a leaf node and adds it to a list of nodes. While backtracking, every time it hits a junction (3 or 4 passages meeting up) it marks the cell as an internal node and adds it to the list as well if that cell wasn't already added before. While walking the maze it also stores for each cell what the previous cell is. After this process we have a flat list of all nodes in the tree and a way to always go backwards towards the root.

Next, it simply iterate through all the nodes in the list and for each walk backwards towards the root until it hits a cell that's a node too. It marks this node as the parent of the other node and continues the iteration. At the end, all nodes except the root should have a parent, and from this it can also easily find out what the children of any nodes are. And thus the tree structure is complete.

Should I write the code today I'd have done it with an actual recursive function instead. Though I haven't tested it, I think it would take a parent node, the cell of that node, and an initial direction to walk in as parameters. Then it would walk along that path until it either reached a junction or a dead end. At a junction it would create an internal node for that junction, mark it as the child of the node passed as parameter, and call the function recursively for each direction in the junction except the direction it came from. At a dead end it would create a leaf node and mark it as the child node of the node passed as parameter, and return the function with no further recursive calls. At the end the tree structure would be complete.