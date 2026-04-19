---
title: Defining Chess Piece Moves using Regular Expressions
url: https://www.boristhebrave.com/2022/10/22/defining-chess-piece-moves-using-regular-expressions/
author: Boris
published: '2022-10-22'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Suppose you wanted to code a simple chess game. One key bit of game logic is to describe what are legal moves for each piece. There’s only 6 types of piece (pawn, knight, bishop, rook, queen, king) so this isn’t exactly a hard task. You can write rules such as:

```
def canRookMove(from, to):
# Ignores questions about colliding with other pieces
return (from.x == to.x or from.y == to.y) and from is not to
```


But these days, I’ve been thinking a lot about grids, and the above approach just doesn’t *generalize*. What if you wanted to play chess on a stranger grid?

![](../../assets/3024cbfd41a6b9d5.jpg)

[CC BY 2.0](https://creativecommons.org/licenses/by/2.0),

[source](https://www.flickr.com/photos/30247563@N00/272995622/))

What would it mean to play chess on the grid above, or a hexagonal grid, and so on? You’d have to write a whole new set of rules, and they could get very complicated depending on the grid in question. What I want is a language that describes how pieces move, which generalizes to any board. And I think I’ve found it, using [regular expressions](https://en.wikipedia.org/wiki/Regular_expression).

## Describing a move

We’re going to treat the the chess board as a [rotation graph](https://www.boristhebrave.com/2022/07/31/rotation-graphs/) and deliberately ignore the regular grid shape. Rotation graphs are a useful tool for reducing grids to just the details of motion. You can find more details in the linked article.

But essentially, it means we should consider a piece sitting in a particular square, and facing a particular cardinal direction. Chess pieces don’t normally face a particular direction, but we’ll imagine that they do. The only ways we’ll consider a piece to move are “turn left”, “turn right” and “move forward”. Forward is always relative to the current facing direction. Basically, [Logo](https://en.wikipedia.org/wiki/Logo_(programming_language)), or [tank controls](https://en.wikipedia.org/wiki/Tank_controls). There’s no diagonal moves, no jumping.

So to descibe a move like a knight’s we must reduce it to those basic operations. E.g. a single knight’s move you might go forward twice, turn right 90 degrees, then forward once again.

We’ll use F for forward, L for left, and R for right. So, moving forward one square could be described by the string “F”, and the knight’s move above would be “FFRF”. We’ll call these strings **paths** as they describe a move step by step.

To move one square diagonally, you could either go “FLF”, i.e. forward one square, then turn left, and go forward again. Another diagonal path would be “LFRF”. Both these paths finish on the same square in a normal chess board. But in the general case, they are not the same, as we’ll see below.

The nice thing about this sort of move description is it works on any rotation graph. You don’t need a well defined co-ordinate system, you don’t even need cells to have a consistent number of sides!

## Regular Expressions

[Regular expressions](https://en.wikipedia.org/wiki/Regular_expression) (regex for short) are a useful programmer tool for matching certain strings. You probably see where I’m going with this. If all moves can be described by a path, and all paths are a string of characters, and strings can be matched via a regex, then a regex basically describes a set of possible moves. (this set is called a [regular language](https://en.wikipedia.org/wiki/Regular_language) in computer science jargon)

To be specific, we’ll assume pieces start facing a particular direction, and can turn like a tank does. Then for example, a rook move could be described as `/L*F+/`

, which is to say, turn left (L) any amount of times (*), then move forward (F) at least once (+). (The full syntax of regular expressions can be found [online)](https://www.regular-expressions.info/quickstart.html). We include an arbitrary number of left turns at the start so that the piece can start by turning to any cardinal direction. All pieces except pawns have regexes starting that way, because in the real rules of chess, pieces except pawns are directionless and don’t have a particular facing.

We can write regexes for all the pieces:

| Piece | Move Regex |
|---|---|
| Pawn | `/F$/` |
| Pawn (first move) | `/F$F?$/` |
| Pawn (capturing) | `/F(LFR|RFL)$/` |
| Knight | `/L*FF(L|R)F$/` |
| Bishop | `/L*(FLFR$|LFRF$)+/` |
| Rook | `/L*(F$)+/` |
| Queen | rook|bishop |
| King | `/L*(F|FLF|FRF)$/` |

I’ve added a `$`

symbol to indicate a special assertion that the chess engine should check if the cell the path is currently at is occupied, so it can handle captures and obstructing pieces.

I’ve also tried to define all diagonals so that pieces have the option of walking the diagonal from either side. That gives the pieces maximum flexibility when we come to non square grids. And I’ve also decided that knights move forward 2, then sideways 1, as the order does matter in some cases. But obviously, there are many other ways of extending the chess rules to other grids.

With these rules, we can figure out how knights and bishops move alone that tricky center section in three-way chess. Turns out the knight has difficulty crossing into the opposite section, while the bishops moves “split” depending on if you go round the diagonals left or right.

We can also apply the same result to [hexagons](https://en.wikipedia.org/wiki/Hexagonal_chess) too. If you color the tiles sensibly, then bishops are still stuck on one color, and knights must jump to a different color every turn.

We could easily imagine further extensions as needed for grids with odd-sided polygons, or other special cases needed for [fairy chess](https://en.wikipedia.org/wiki/Fairy_chess).

## Use in practise

One annoyance of this system, is that it’s not actually easy to answer “can a piece move from A to B?”. There’s a huge number of paths that all go from A to B, and you’d need to check them all versus the regex.

What you *can* do however, is list all possible moves that can be made with a given regex. That’s because regexes can be boiled down to finite state machines. It’s easy to list all possible paths – simply start with the empty path and keep adding F,L or R to it, and check that this doesn’t put the regex’s state machine in a failure state. If it does, remove a letter and try again with the next one. In other words, you can do a depth first search.

This swiftly explores all possible paths, though it can get stuck exploring infinite length paths that just go in a circle. To do better, track the state of the chess pieces, which is simply the cell its currently on and the direction facing it has. If we ever come across the same combination of `(cell, direction, regex state)`

twice, then we’re in a loop, and we can stop exploring that set of possibilities.

## Conclusion

Well, I’m struggling to see how this is remotely useful. It’s just a cool idea. But it’s giving me a deeper understanding of rotation graphs. I’m planning to turn that understanding into a [new open source library](https://twitter.com/boris_brave/status/1579746943655612416) that assists you with all sorts of grid operations. But it’s not ready yet!

Clever stuff. The bishop move on the hexagonal shaped board is most interesting.

I can relate to this as I play 5 minute chess + 3 second increment quite a lot. I also own an hexagonal chess set made up of 91 smaller hexagons or ‘cells’ and three player chess on a trigonal board. I since adapted the latter for two players that included a ‘lite’ version. Maybe you would like to see it – I could send it via email with pictures?