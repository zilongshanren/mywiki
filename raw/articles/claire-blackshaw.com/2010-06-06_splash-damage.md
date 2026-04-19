---
title: Splash Damage
url: https://claire-blackshaw.com/blog/2010/06/splash-damage/
author: Claire Blackshaw
published: '2010-06-06'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Splash Damage](../../assets/4e402aebc4c1a4e8.png)

### Splash Damage

Okay some actions can affect multiple targets, my old model ignored this and hence broke in a few places. I’ve now fixed this. This resolves a few graph query issues I was having.

### Containers

Aaah yes arbitrary containers are extremely useful in a graph systems. They give information based on context. I was using them in all my drawings and notes, but not in code. This has now been fixed and cleans things up.

### Multiple Children

I started with a query as a single path in the graph. Then I got lost a bit and thought, of course multiple children are needed. So the query changed from a path to a sub-graph.

The confusion arose because the response is multiple nodes.

This is messy and muddies the model. After trying to handle the sub-graph query I decided it adds nothing, as multiple paths can be submitted consecutively.

So now the **query is path**, **response is a node list**.