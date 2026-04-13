---
title: Linearly Transformed Spherical Harmonics Expansions
url: http://momentsingraphics.de/LinearlyTransformedSH.html
published: '2020-12-02'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Linearly Transformed Spherical Harmonics Expansions

In my job at the [Karlsruhe Institute of Technology](https://cg.ivd.kit.edu), I usually supervise two bachelor or master theses per term (four per year). By handing out topics that have a sufficiently narrow scope but tap directly into current rendering research, I try to pass on my passion for this subject.

With Jan Allmenröder that clearly worked. His bachelor thesis investigates a project suggested as [future work by Laurent Belcour](https://doi.org/10.1145/3015459). Laurent's paper explains how to integrate spherical harmonics expansions over polygons. Combined with [linearly transformed cosines](https://doi.org/10.1145/2897824.2925895) this technique gives rise to linearly transformed spherical harmonics expansions. The resulting technique lets you compute specular shading due to polygonal area lights. The quality is superior to linearly transformed cosines but the current implementation (based on code by [Jingwen Wang](https://doi.org/10.1145/3197517.3201291)) is also much slower.

If that sounds interesting, I have good news: Jan wrote a [blog post about his thesis](http://www.jallmenroeder.de/2020/11/19/linearly-transformed-spherical-harmonics/), made the [thesis](http://www.jallmenroeder.de/wp-content/uploads/2020/10/LTSH_BA_Thesis_final.pdf) itself available and published his [Falcor based demo](https://github.com/jallmenroeder/falcor_ltsh) on github.

That's all on my part, so please go ahead and read Jan's post.