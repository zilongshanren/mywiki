---
title: 💡 LogicBlocks
url: https://chickensoft.games/docs/logic_blocks
source_blog: Chickensoft — Open source tools for Godot and C# Blog
source_site: https://chickensoft.games/blog
category: game programming
fetched: '2026-04-13'
---

# 💡 LogicBlocks

Introduction to logic blocks.

[LogicBlocks](https://github.com/chickensoft-games/LogicBlocks) is a serializable, hierarchical state machine package for C# that works well when targeting ahead-of-time (AOT) environments. LogicBlocks draws inspiration from [statecharts](https://statecharts.dev/), [state machines](https://en.wikipedia.org/wiki/Finite-state_machine), and [blocs](https://www.flutteris.com/blog/en/reactive-programming-streams-bloc).

Instead of elaborate transition tables, states are simply defined as self-contained class records that read like ordinary code using the [state pattern](https://en.wikipedia.org/wiki/State_pattern). Logic blocks are designed with performance, adaptability, and error tolerance in mind, making them refactor-friendly and suitable for high performance scenarios (such as games).

Logic blocks grow with your code: you can start with a simple state machine and easily scale it into a nested, hierarchical statechart that represents a more complex system — even while you're working out what the system should be.

![LogicBlocks logo](../../assets/ffb05ca78dc9ed45.img)

Logic blocks are based on *statecharts*. You may also know them as hierarchical state machines (HSM's).

-
**Beginner**: overview for those who are new to statecharts. -
**Intermediate**: all the statechart concepts in one place. -
**Expert**: all the juicy technical details are here. -
**In a hurry?**Learn about hierarchical states and logic blocks all at once!

*A logic block is a class that receives inputs, maintains a single state instance, and produces outputs.*

*Logic blocks enable you to efficiently model complex behaviors* 1.

LogicBlocks provides a source generator that can generate [UML state diagrams](https://en.wikipedia.org/wiki/UML_state_machine) of your code.

Generated UML diagrams are placed alongside the code for your logic block with the `*.g.puml`

extension. You can use [PlantUML](https://plantuml.com/) (and/or the [PlantUML VSCode Extension](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)) to visualize the generated diagram code.

A diagram explains all of the high level behavior of a state machine in a single picture. Without a diagram, you would have to read and scroll through all the relevant code files to understand the machine (especially if you weren't the author, or forgot how it worked since you had written it).

In the interest of convenience, logic blocks have a few subtle differences from statecharts:

-
💂♀️ No explicit guards

Use conditional logic in an input handler

-
🪢 Attach/Detach callbacks

These are an implementation specific detail that are called whenever the state

*instance*changes, as opposed to only being called when the state type hierarchy (i.e., state configuration) changes. -
🕰️ No event deferral

Non-handled inputs are simply discarded. There's nothing to stop you from implementing

[input buffering](https://supersmashbros.fandom.com/wiki/Input_Buffering)on your own, though: you may even use the[boxless queue](https://github.com/chickensoft-games/Collections?tab=readme-ov-file#boxless-queue)collection that LogicBlocks uses internally.

LogicBlocks also uses different terms for some of the statechart concepts to make them more intuitive or disambiguate them from other C# terminology.

| statecharts | logic blocks |
|---|---|
| internal transition | self transition |
| event | input |
| action | output |

-
Simple behaviors, like the light switch example, are considerably more verbose than they need to be. Logic blocks shine brightest when they're used for things that actually require hierarchical state machines.

[↩](https://chickensoft.games#user-content-fnref-1)