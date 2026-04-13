---
title: DagNN vs Standard 2-Layer fully connected networks
url: https://www.jonolick.com/home/dagnn-vs-standard-2-layer-fully-connected-networks
author: Hot Etoile link
published: '2017-11-04'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
A quick post about the results for my first comparison here of a 2-layer fully connected network vs a DagNN. I've removed most of the random variables here for this example so that the comparison is pretty accurate. The only random variable left is the order in which things are trained due to SGD - however, as I removed more and more random variables the differences got more in favor of DagNN and not less. The conclusion of this test is that DagNN is better node-for-node per epoch than the standard 2-layer fully connected network - at least in this example. This at least follows intuition a bit, that more weights between the same number of nodes increases overall computational power of the network.
More rigorous comparisons in some of the standard test cases needs to be done, but this is a good first step offering some preliminary credibility.
|
## Archives
## Categories |