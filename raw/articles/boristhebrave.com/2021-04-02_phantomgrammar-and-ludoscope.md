---
title: PhantomGrammar and Ludoscope
url: https://www.boristhebrave.com/2021/04/02/phantomgrammar-and-ludoscope/
author: Boris
published: '2021-04-02'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

[Last time](https://www.boristhebrave.com/2021/04/02/graph-rewriting/), I took inspiration from a game called [Unexplored](https://store.steampowered.com/app/506870/Unexplored/), and wrote about about a system of rule evaluation called **Graph Rewriting**.

In developing Unexplored and earlier games and academic papers, developer Joris Dormans has over the years developed an entire software library centered around graph rewriting. It’s called **PhantomGrammar**, and it comes with an accompanying UI called **Ludoscope **(sadly, neither is publically available currently).

I think it’s worth discussing how it works, as it turns the previous theoretical ideas into something pratical to work with.

## Rules

In PhantomGrammar, replacement rules are stored in a custom format that looks like the following.

`rule: myRule = GRAPH 1:A 2:B 0:edge(1,2) > {0 = GRAPH 1:a 2:A 3:b 4:B 0:edge(1,3) 5:edge(3,4) 6:edge(4,2) }`


It’s much easier to work with the rules in the UI, which provides a graphical representation and contains tools for testing and debugging rules.

![](../../assets/15c3cf8258e067f5.png)

Like in the example in the Graph Rewriting article, this rule finds a node of type A with an edge leading to type B, and replaces it with a more complex set of nodes, by creating two new nodes, three new edges, and deleting the original edge.

PhantomGrammar goes beyond the basic operations of replacement. It has a number of extensions to increase its flexibility and control.

- It operates on extended graphs. These extended graphs still contain nodes and edges, but every node and edge can have abritrary amounts of attributes attached to it. Nodes can even contain arbitrary subgraphs inside them, though mercifully this feature is rarely used.
- It works with tilesets, strings and other objects too.
- Find patterns are sophisticated and can match based on attributes. They can also contain conditional expressions, such as counting the number of incoming edges, or checking the value of a given attribute.
- Replacement patterns can specify a random choice of alternatives, include code to run when the replacement is done, and simple expressions for randomizing values.

## Recipes

Rules are only half of what PhantomGrammar does. Unexplored has over 5000 rules, if they were all applied at once, it would be chaos. Instead, execution of generation is broken up into modules, and each module has a “recipe”. Recipes are sequential series of instructions that dictate what rules to apply.

![](../../assets/0283304d0997f3dc.png)

The most important instructions let you iterate/execute a set of rules in one of three modes. Iterating a ruleset means applying a single random rule once. Executing a ruleset means iterating it many times, either a fixed count, or until nothing matches. The three modes control how the rules apply to multiple matches:

- Normal iteration just applies the rule to a random match found.
- LSystem iteration searches in a fixed order, and applies the rule to every match found. The rules can therefore change the graph while it is being searched.

This mode is designed to match the behaviour in string rewriting systems like[Lindenmayer systems](https://en.wikipedia.org/wiki/L-system), or “Replace All” in most text editors. - Cellular iteration finds as many matches as possible, then applies the rules afterwards. The replacements patterns must be carefully written so they don’t cause conflicts.

This mode is designed to match the behaviour of[Cellular Automatons](https://en.wikipedia.org/wiki/Cellular_automaton).

For example, we could apply these different modes to find and replace. Supose we were to find “`AA`

” and replace it with “`AB`

” in the string “`AAAAAA`

“.

- Normal mode might give “
`ABAAAA`

” or “`AAABAA`

“, etc. - LSystem mode would give “
`ABABAB`

“. - Cellular mode would give “
`ABBBBB`

“.

Cellular and LSystem modes are fairly useful concepts for graph rewriting, but in fact PhantomGrammar supports doing replacements on strings and tilemaps too, so you can literally do Lindeymayer systems and cellular automata with the same language. Indeed, Unexplored uses some cellular automata to give caves a nice rough edge, which is a [standard technique](http://roguebasin.roguelikedevelopment.org/index.php?title=Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels).

There are a number of instructions that are closer to procedural programming, such as setting variables. There’s no control flow or method invocation, but it’s not needed. Instead, rules can have a recipe attached to them which is run when the replacement is successfully applied. As those instructions can themselves invoke rules, a stack of execution is formed.

## Limitations

PhantomGrammar is not the ultimate generation system. Find-and-replace is good for making small local edits that compound to something interesting, but not for expressing for traditional algorithms. One consequence of this is that unlike Enter the Gungeon, Unexplored has no way to layout graphs – it cannot take a positionless graph and figure out how to place it sensibly on a 2d map.

Another annoyance of the system is that due to the lack of abstraction, and the limits of the matching system, it’s often necessary to break down quite simple operations into several steps. For example, to find the furthest point from a given node, you’d have to first make a pattern that calculates distances from that node, then some custom code to find the max, then another pattern to pick a node with max value. Similar small steps need to be coded over and over again to achieve various geometric effects.

## Summary

PhantomGrammar must have been the work of years – Dormans [has used it](https://ubm-twvideo01.s3.amazonaws.com/o1/vault/gdceurope2013/Presentations/824494JorisDormans.pdf) in many of the [games](https://www.facebook.com/Bezircle/) he’s [developed](https://www.facebook.com/dulesgame/), and it has formed the testbed for many papers too. For example, [it’s used here](https://danielkaravolos.nl/wp-content/uploads/2015/12/vanarkeletal-2015-pcg-collaborative-gameplay.pdf) to generate Spelunky style random walk levels. It could make an excellent low code platform for procgen and gamedev.

Dormans studied exactly how far one can take these sorts of tools, and experimented with what works best. [Later, you can read on to see how he applied these insights in Unexplored](https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/), his most advanced game to date.