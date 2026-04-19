---
title: Algorithms do not have 'a complexity' | Sebastian Schöner
url: https://blog.s-schoener.com/2019-12-09-complexity-vs-runtime/
author: Sebastian Schöner
published: '2019-12-09'
source_blog: Hi there! | Sebastian Schöner
source_site: https://blog.s-schoener.com/
category: graphics
fetched: '2026-04-19'
---

Computational complexity theory (CC) is the study of problems and how to solve them algorithmically. The holy grail of CC is to fully determine the complexity of a problem, that is to answer: How difficult is it to solve this problem? This involves establishing the minimum amount of resources that is necessary and sufficient to solve it. In practice, this is done by giving an algorithm that solves the problem, determine its resource usage, and then prove that there is no algorithm that uses less.

The *algorithmic complexity* of a problem is the worst case runtime of the best algorithm that solves it. Computational complexity theory is however not interested in the ‘complexity’ of algorithms. What would that even mean? Cyclomatic complexity? - It may sound very silly, but I cry a little inside whenever someone talks about the ‘complexity’ of an algorithm when they actually mean the worst case runtime.

And yes, there are plenty of books and academics that will disagree on how this is used, but if words can mean whatever we want them to, why not choose a meaning that actually makes sense?