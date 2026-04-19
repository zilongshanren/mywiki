---
title: 'HOG-Diff: Higher-Order Guided Diffusion for Graph Generation'
url: https://circle-group.github.io/research/hog-diff/
author: Yiming Huang
published: '2026-01-01'
source_blog: CIRCLE Group
source_site: https://circle-group.github.io/
category: graphics
fetched: '2026-04-19'
---

- Introduces cell complex filtering to extract higher-order skeletons from graphs as informative generation guides.
- Proposes a coarse-to-fine graph generation framework guided by higher-order topology via a generalized OU diffusion bridge.
- Provides theoretical analysis showing faster score-matching convergence and tighter reconstruction bounds.
- Demonstrates state-of-the-art performance on molecular and generic graph benchmarks under both pairwise and higher-order metrics.

**HOG-Diff**framework and its performance. (

**Left**) The dashed trajectory above illustrates the classical generation process, where graphs rapidly degrade into structureless randomness. In contrast, as shown in the coloured region below, HOG-Diff adopts a coarse-to-fine generation curriculum via a diffusion bridge, explicitly learning higher-order structures during intermediate steps. (

**Middle**and

**right**) Relative improvements over prior state-of-the-art on pairwise and higher-order topological metrics.

## Abstract

Graph generation is a critical yet challenging task, as empirical analyses require a deep understanding of complex, non-Euclidean structures.
Diffusion models have recently made significant achievements in graph generation, but these models are typically adapted from image generation frameworks and overlook inherent higher-order topology, limiting their ability to capture graph topology.
In this work, we propose **Higher-order Guided
Diffusion (HOG-Diff)**, a principled framework that progressively generates plausible graphs with inherent topological structures.
HOG-Diff follows a coarse-to-fine generation curriculum, guided by higher-order topology and implemented via diffusion bridges.
We further prove that our model admits stronger theoretical guarantees than classical diffusion frameworks.
Extensive experiments across eight graph generation benchmarks, spanning diverse domains and including large-scale settings, demonstrate the scalability of our method and its superior performance on both pairwise and higher-order topological metrics.

## Core Contributions

## Experiments

The paper evaluates HOG-Diff on eight benchmarks across molecular and generic graph domains, including large-scale settings. The reported results show consistent gains over strong baselines on both distributional fidelity and higher-order structural metrics.

**Molecular Benchmarks**

**Generic Graph Benchmarks**

## Poster

![HOG-Diff poster](../../assets/7645f2ebb6d63a84.png)

## Miscellaneous

## BibTeX

```
@inproceedings{huang2026hogdiff,
title = {HOG-Diff: Higher-Order Guided Diffusion for Graph Generation},
author = {Huang, Yiming and Birdal, Tolga},
booktitle = {International Conference on Learning Representations (ICLR)},
year = {2026}
}
```


## Contact

Please contact
[y.huang24@imperial.ac.uk](mailto:y.huang24@imperial.ac.uk)
or
[yimingh999@gmail.com](mailto:yimingh999@gmail.com)
for any inquiries related to this work.