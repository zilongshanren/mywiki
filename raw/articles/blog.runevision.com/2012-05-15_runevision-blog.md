---
title: runevision blog
url: https://blog.runevision.com/2012/
published: '2012-05-15'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I got a mail from Robert Stehwien asking me how to generate an environment tree ([as described on Squidi.net](http://www.squidi.net/three/entry.php?id=4)) from a 2D maze - something I [wrote](http://blog.runevision.com/2010/08/eas-demo-of-procedural-environment.html) [previously](http://blog.runevision.com/2011/08/forcing-structure-in-procedural-spaces.html) that I do in my game [The Cluster](http://blog.runevision.com/search/label/TheCluster) but didn't go in details with.

An environment tree is basically a [tree structure](http://en.wikipedia.org/wiki/Tree_structure) representing connectivity in a spatial space, where inner nodes represent junctions where for example a corridor splits into two or more, and leaf nodes represent dead ends. An environment tree of a 2D maze would have inner nodes where the maze corridors split into two or more and leaf nodes at dead ends.

![](https://runevision.com/multimedia/cavex/level_generation_a.jpg)

I wrote the code for doing it more than five years ago. It's rather convoluted but anyway, this is how it works:

I use a ["recursive back-tracker"](http://www.astrolog.org/labyrnth/algrithm.htm#solve) algorithm which is basically the same as a depth-first search. Despite the name of the method, I implemented it as a loop and not as a recursive function. Every time it hits a dead end, it marks the cell as a leaf node and adds it to a list of nodes. While backtracking, every time it hits a junction (3 or 4 passages meeting up) it marks the cell as an internal node and adds it to the list as well if that cell wasn't already added before. While walking the maze it also stores for each cell what the previous cell is. After this process we have a flat list of all nodes in the tree and a way to always go backwards towards the root.

Next, it simply iterate through all the nodes in the list and for each walk backwards towards the root until it hits a cell that's a node too. It marks this node as the parent of the other node and continues the iteration. At the end, all nodes except the root should have a parent, and from this it can also easily find out what the children of any nodes are. And thus the tree structure is complete.

Should I write the code today I'd have done it with an actual recursive function instead. Though I haven't tested it, I think it would take a parent node, the cell of that node, and an initial direction to walk in as parameters. Then it would walk along that path until it either reached a junction or a dead end. At a junction it would create an internal node for that junction, mark it as the child of the node passed as parameter, and call the function recursively for each direction in the junction except the direction it came from. At a dead end it would create a leaf node and mark it as the child node of the node passed as parameter, and return the function with no further recursive calls. At the end the tree structure would be complete.


Though I haven't posted about it for the good part of a year, I haven't dropped my game The Cluster. Google AI Challenge ended up taking up quite some time last fall and after that was a period where I was preoccupied with other things, but I've recently gotten some new ideas and enthusiasm for continuing this long-running spare time project.

Stay tuned...

![](../../assets/04c414cbff799886.png)


I just got this mail from one of the Google AI organizers:

Hello,

Thanks for taking part in the latest AI Challenge. I hope you enjoyed it!

Since you ranked in the top 100, Google really wants to see your resume (curriculum vitae). If you want to be contacted by a Google recruiter, send me a quick reply letting me know.

I will put in a good word for anybody who is interested. With more than 7000 entries in the final tournament, ranking in the top 100 is a serious achievement. I was really impressed by the skill of all the top-ranking bots.

If you are unsure, my advice is to go for it. It's a wonderful opportunity if you love figuring out tough problems and writing awesome code. Your recruiter will be happy to answer any questions you have!


I'm not unsure though. With my [4th place](http://blog.runevision.com/2011/12/4th-place.html) I guess I'd be high on their want list, but I'm happy with my job at [Unity](http://unity3d.com). I'll apply my "love for figuring out tough problems and writing awesome code" there instead. :)

By the way; sorry for never getting around to writing part 2 and 3 of the [explanation of my bot](http://blog.runevision.com/2011/12/ai-challenge-my-bot-explained-part-i.html). After seeing how the announcement of the winners got practically no attention anywhere I got a bit demotivated. You can still download the source though and see how it's done, and if you have any questions, just ask.