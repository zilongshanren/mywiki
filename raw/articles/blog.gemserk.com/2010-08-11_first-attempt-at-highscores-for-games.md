---
title: First attempt at Highscores for games
url: https://blog.gemserk.com/2010/08/11/first-attempt-at-highscores-for-games/
published: '2010-08-11'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

We are doing our first attempt at implementing online highscores for our games.

Our Score structure right now is:

Score { id : String - The unique identifier name : String - The name of the player points : long - The value of the score timestamp : date - The time when the score was submitted tags : Set[String] - A set of tags of the score data : Map - Extra data of the score }

The tags are used to classify the scores by different criteria, for example, the difficulty, the level, etc.

Data is a map of simple values used to add extra information of the score, like bombs left when the user died or enemies killed of each type, etc.

The idea is to have an online application for the highscores of all the games. All comunication is performed using a gameKey which is unique for each game and allow us to separate the scores by game.

Our current API consist of a submit method and a query method and it is based in HTTP and [JSON](http://www.json.org/).

submit(gamekey : String, name : String, tags : Set[String], points : long, data : JSONString) : String

This method allows us to submit a new score and returns the generated id for it. The extra data attached to the score is specified by a JSON string. The timestamp is generated at the moment the score is stored.

scores(gamekey, tags, limit, ascending) : List[Score]

This method allows us to query for scores of a game by using:

- tags : returned scores must have every tag in tags
- limit : returned quantity must be less than limit
- ascending : if true scores are returned ordered by points ascending

Our first implementation will be based in google app engine but is not online yet, and Jylonwars will be the first game using it.

There are some features we are thinking about:

- Security: the submitted scores should be encrypted and validated (we know it is not totally safe but it would prevent casual tampering)
- Online scores board

Also, we are thinking about making the server project opensource.</p>