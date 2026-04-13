---
title: 'GraphWaGu: GPU Powered Large Scale Graph Layout Computation and Rendering
  for the Web'
url: https://www.willusher.io/publications/graphwagu/
published: '2022-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# GraphWaGu: GPU Powered Large Scale Graph Layout Computation and Rendering for the Web

#### Landon Dyken, Pravin Poudel, Will Usher, Steve Petruzza, Jake Y. Chen, Sidharth Kumar

In *Eurographics Symposium on Parallel Graphics and Visualization*, 2022.

## Abstract

Large scale graphs are used to encode data from a variety of application domains such as social networks, the web, biological
networks, road maps, and finance. Computing enriching layouts and interactive rendering play an important role in many of
these applications. However, producing an efficient and interactive visualization of large graphs remains a major challenge,
particularly in the web-browser. Existing state of the art web-based visualization systems such as D3.js, Stardust, and NetV.js
struggle to achieve interactive layout and visualization for large scale graphs. In this work, we leverage the latest WebGPU
technology to develop GraphWaGu, the first WebGPU-based graph visualization system. WebGPU is a new graphics API that
brings the full capabilities of modern GPUs to the web browser. Leveraging the computational capabilities of the GPU using this
technology enables GraphWaGu to scale to larger graphs than existing technologies. GraphWaGu embodies both fast parallel
rendering and layout creation using modified Frutcherman-Reingold and Barnes-Hut algorithms implemented in WebGPU
compute shaders. Experimental results demonstrate that our solution achieves the best performance, scalability, and layout
quality when compared to current state of the art web-based graph visualization libraries. All of our source code for the project
is available at [https://github.com/harp-lab/GraphWaGu](https://github.com/harp-lab/GraphWaGu) .

`@inproceedings{dyken_graphwagu_2022, booktitle = {Eurographics Symposium on Parallel Graphics and Visualization}, editor = {Bujack, R. and Tierny, J. and Sadlo, F.}, title = {{GraphWaGu:} {GPU} {Powered} {Large} {Scale} {Graph} {Layout} {Computation} and {Rendering} for the {Web}}, author = {Dyken, Landon and Poudel, Pravin and Usher, Will and Petruzza, Steve and Chen, Jake Y. and Kumar, Sidharth}, DOI = {10.2312/pgv.20221067}, year = {2022}, }`