---
title: Preventing players from getting stuck in puzzle games
url: https://gamedevcoder.wordpress.com/2014/05/23/preventing-players-from-getting-stuck-in-puzzle-games/
published: '2014-05-23'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I’ve been developing my puzzle game [Rainbow Hero](http://www.pixelelephant.com/rainbowhero) (to be released soon on PC) for a while now and while doing so I designed a lot of puzzle levels. It was fun but it was also great opportunity for me to learn about good and bad ways to design puzzles.

Now I’ve just came across an article that talks specifically about that. If you’re into designing puzzles you should totally give it a go: [How Are Puzzle Games Designed?](http://devmag.org.za/2011/06/04/how-are-puzzle-games-designed-conclusion/). It’s great read and I couldn’t agree more with anything there but I’d like to add a couple of my own tips on one particular topic of **how to prevent players from getting stuck** (and as a result stop playing the game).

It is very challenging to make a puzzle game that would appeal to many players – both casual and hardcore ones. Making puzzles too easy or too difficult might easily break the game for many. But there’s some ways that can make the game fun for casual players without lowering difficulty level too much thus offering challenge for hardcore players as well.

Here’s my tips:

1) Provide alternative puzzles. Don’t let your game unlock exactly one puzzle after completing another. Make it unlock 2 or more so as to always give a choice to the player. There might be other ways to it but the main idea stays the same – never leave the player with one (or too few) puzzles left.

2) Don’t require player to solve all puzzles in order to solve “the big puzzle” (be it game chapter/world or some other part of the game).

I bet you, as a developer, would much prefer to have lots of players who completed the game even if that means solving only 50% of all puzzles rather than have lots of players who got stuck after completing 10% of the game and never played it again.

3) If the game makes it possible to get into non-obviously unrecoverable states (totally easy in a game such as e.g. [sokoban](http://en.wikipedia.org/wiki/Sokoban)) provide undo or time rewind option. Actually provide it even if it’s obviously unrecoverable because the player might have made a tiny mistake (e.g. pressed the wrong button) and would otherwise have to replay the whole level and start solving the puzzle from scratch.

Some puzzle games, such as [Braid](http://en.wikipedia.org/wiki/Braid_(video_game)) or [Time Ducks](https://www.youtube.com/watch?v=evAcp7SX-9A), have even made time rewind feature their core mechanic.