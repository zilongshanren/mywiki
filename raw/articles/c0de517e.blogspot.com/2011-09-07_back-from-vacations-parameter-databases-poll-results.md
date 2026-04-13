---
title: Back from vacations, Parameter Databases poll results.
url: http://c0de517e.blogspot.com/2011/09/back-from-vacations-parameter-databases.html
published: '2011-09-07'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Back after Siggraph and some well-deserved vacations, I have many posts to prepare. For now, here there are the results from my last poll.

![]() |

The poll was: "Parameter Database systems should use..." and here are the final results. Didn't get too many votes this time (32), maybe people were in vacation as well, or maybe the subject was boring, anyhow:

- Reflection (53%)
- Code-Generation (28%)
- Handles/Dynamic Types (18%)
- Immutable Data (in-game) (18%)
- Data Inheritance (18%)
- Schema Inheritance (18%)
- Relational DB (15%)
- Live-editing via tool (78%)
- Live-editing in-game (40%)
- Serialization via tool (53%)
- Serialization in-game (34%)

Predictably I'd say, people prefer to keep editing and serialization in a tool instead of in-game, having the in-game client only to load/listen to the data changes.

As for the database type, relational systems do not seem to be favored, I guess most parameter systems are still key-values. Low scores are also assigned to dynamic typing, data and schema (class) inheritance.

What is maybe surprising that reflection wins over code-generation, even if in C++ there is no easy way to implement the former.

I've noticed how often we, as engineers, have a perverse aesthetic sense for which a C++ disgusting macro based reflection system is considered "prettier" than mixing different languages or crafting languages and tools.

To be fair, reflection could also be done more simply by parsing PDBs or using C++ parsers, but I doubt these are really widespread.

The good thing about reflection though is that code changes can "break" data, or require data changes, but the opposite is not true. With code-generation data changes can "break" code which is arguably worse.

## No comments:

Post a Comment