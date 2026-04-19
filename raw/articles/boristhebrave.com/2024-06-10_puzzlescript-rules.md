---
title: PuzzleScript Rules
url: https://www.boristhebrave.com/2024/06/10/puzzlescript-rules/
author: Boris
published: '2024-06-10'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I was watching [ThinkyCon](https://thinkygames.com/thinkycon/), a conference on making puzzle games, and many designers mentioned that they use **PuzzleScript** to prototype their ideas. [PuzzleScript](https://www.puzzlescript.net/) is a puzzle design environment created by [increpare](http://www.increpare.com/), the designer behind [Stephen’s Sausage Roll](https://store.steampowered.com/app/353540/Stephens_Sausage_Roll/) and many other puzzle games.

PuzzleScript is a marvel of economic design. A single text file specifies, all the graphics, levels, sound effects, and all the rules of the puzzle. It uses a custom system to concisely express rules. So concise that the rules of [Sokoban](https://en.wikipedia.org/wiki/Sokoban) can be expressed in [a single line](https://www.puzzlescript.net/Documentation/rules101.html).

This efficiency comes because rules are expressed as find-replace rules. That makes it a grammar replacement system, which I last discussed when looking at [Ludoscope](https://www.boristhebrave.com/2021/04/02/phantomgrammar-and-ludoscope/) and [Unexplored](https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/). But it has many pragmatic features geared toward puzzle design, which I’ll explore in this article.

## Overview

The world of a puzzle script level is a rectangular grid of cells. Filling those cells are various objects, each of which has a simple sprite associated. There can be multiple objects in one cell, e.g. there’s always a background object in a cell which is the sprite to show when nothing else is occupying it.

The rules are expressed like this:

`[ Player | Crate ] -> [ Player | ]`


All rules are a find and replace like this. The left hand side of the `->`

is the find pattern, and the right hand side the replacement. In this case, the find pattern is a 2 by 1 rectangle, with a Player in the first cell, and a Crate in the second. And the replacement removes the Crate, while keeping the Player around. Patterns are made of a line of cells, there’s no direct way to match a 2 by 2 rectangle.

Rules in PuzzleScript are considered in all 4 directions by default, so this rule will delete a Crate that is adjacent to the player on any side.

Rules are evaluated in order from top to bottom. There are some looping to control if rules need to be retried, and rules can be marked as `late`

to be run after the movement phase.

The matching rules can be quite sophisticated, can you find all the stuff that is possible [in the docs](https://www.puzzlescript.net/Documentation/documentation.html).

## Frozen Motion

Commonly puzzle rules are often concerned with change and motion. *“When a player pushes a block, move it”. *But PuzzleScript rules only match the current state of the world, they can’t express events occuring, or changes.

The solution to this is inspired. Every game object can be tagged with the motion it is about to undertake. Then the user presses left, the Player object is tagged as left-moving, then the rules run, then the game processes the movement, and finally the `late`

rules run.

Movement tags can be matched in find rules, and set in replace rules. This rule

`[ > Player | Crate ] -> [ > Player | > Crate ]`


Finds a Player object that is moving towards a Create object, and sets the Crate object moving in the same direction. Essentially acting a push operation.

![](../../assets/7a98ba72e3b8cc90.gif)

The actual movement is a core engine feature, it’s not done by rules. It handles the fiddlier details of collisions.

## Some neat features

Beyond basic rules, there are a number of features that struck me as a great payoff of simplicity to utility.

### Multipatterns

Rules like

`[> Player | Lever] [Door] -> [Player | Lever] [Door]`


have multiple patterns in the find section. The rule only fires if both patterns are matched somewhere on the level, but they don’t need be near each other Each pattern has its own replacement.

### Variable Size Patterns

Rules like

`[ > Kitty | ... | Fruit ] -> [ | ... | Kitty ]`


can match a Player and Crate in a line from each other, at any distance. In other words, it stands for an infinite set of rules:

```
[ > Kitty | Fruit ] -> [ | Kitty]
[ > Kitty| | Fruit ] -> [ | | Kitty]
[ > Kitty| | | Fruit ] -> [ | | | Kitty]
etc
```


![](../../assets/33b5e4b22b41135e.gif)

Variable sized patterns like this was one of the biggest weaknesses I noted in Ludoscope, it’s nice to see such an elegant solution.

### Hidden State

This is more a coding technique than specifically part of the engine, but you can create transparent objects with no collision, which essentially serve as variables without having to break away from the replacement rules paradigm.

These hidden objects can track all sorts of details. The manual notes, for example, you can create a “shadow” behind an object at the start of evaluation to detect if it has moved by the end.

## Drawbacks

PuzzleScript rules are much much simpler than the [graph rewriting rules](https://www.boristhebrave.com/2021/04/02/graph-rewriting/) we’ve seen before. The authors note that it’s not “a general purpose puzzle game making tool”. But what are some specific problems?

I think one fundamental problem is object identity. PuzzleScript doesn’t really say whether the Player object in the find pattern is the same Player as in the replacement pattern. In a sense, they are identical objects, so there’s no difference between relocating an object, and destroying and creating an object in a new place.

But this ambiguity does cause some problems. It’s impossible to animate a PuzzleScript rule without guessing. And rules like

`[ Player | Crate ] -> [ Crate | Player ]`


can backfire as the Player will inherit Crate’s movement tags and visa versa, when a naive reading suggests it is swapping the position of two objects.

It’s also very hard express some simple concepts. Matching on diagonals, doing counting operations, and path finding all require multiple rules, and often copy-pasting.

## Conclusion

What I love about PuzzleScript is how well suited replacement rules are for simple 2d puzzles. The discrete nature of replacements and the logical evaluation order naturally matches the main properties of this sort of game.

The idea of treating motion as a state, rather than a change, is an incredible insight, and one I’ll be trying to apply eleswhere.

The rules themselves may be simple and powerful, but that doesn’t always translate to simple to code. If you browse the [gallery of games](https://www.puzzlescript.net/Gallery/index.html), you’ll find many with dozens, or hundreds of rules. Combined with hidden state, loops and so one, they can be tricky to write and hard to debug. My feeling is that replacement rules are a powerful tool, but they can’t serve as sole source of logic for a game. But I’ve yet to really see a system embrace that.

But I think we can all agree: PuzzleScript rules!

Great article, thanks.