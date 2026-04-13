---
title: Month Archives for March 2020
url: https://blog.eyas.sh/2020/03/
author: Eyas Sharaiha
published: '2020-03-08'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

There’s a little-known pattern in software architecture that deserves more
attention. Data-Oriented Architecture was first described by Rajive Joshi in a
[2007 whitepaper at RTI](http://community.rti.com/sites/default/files/archive/Data-Oriented_Architecture.pdf),
and again in 2017 by Christian Vorhemus and Erich Schikuta at the University of
Vienna in [this iiWAS paper](https://dl.acm.org/doi/10.1145/3151759.3151770).
DOA is an inversion of the traditional dichotomy between a monolithic binary and
data store (monolithic architecture) on the one hand, and small, distributed,
independent binaries each with their own data stores (microservices, and
service-oriented architecture) on the other. In data-oriented architecture, a
monolithic data store is the sole source of state in the system, which is being
acted on by loosely-coupled, stateless microservices.

I was lucky that my [former employer](https://www.broadwaytechnology.com/) also
fell upon this unusual architectural choice. It was a reminder that things *can*
be done differently. Data-oriented architecture isn’t a silver bullet by any
means; it has its own unique set of costs and benefits. What I did find, though,
is that a lot of large companies and ecosystems are stuck at exactly the type of
bottleneck that data-oriented architecture is meant to resolve.

[Read more →](https://blog.eyas.sh/2020/03/data-oriented-architecture/)