---
title: 'LearnCocosTV 7: Tic Tac To Lua'
url: http://www.learn-cocos2d.com/2012/03/learncocostv-7-tic-tac-lua/
author: Pavel Says
published: '2012-03-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A presentation about **KoboldScript** with a demonstration of a Tic Tac Toe game with Scene changes and transitions. You’ll see more KoboldScript code and learn more about its key concepts in this episode.

##### Episode #7 - Tic Tac To Lua

• KoboldScript Demo #2

o Tic Tac Toe

o Presentation

• iDevBlogADay: Donations

• Angry Ninjas Starterkit

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I’m wondering is it much of an overhead polling each X and O tile each cycle for the touched state. Will it scale for bigger number of nodes, number of states? Battery drain considered, would it be better removed to a single handler from where it can update affected tiles?

Whether you do between 1-9 function calls or always 18 calls per frame doesn’t really matter in this case. Of course if you have hundreds of nodes it will start to make a difference. In that case you can use a controller type function which iterates over all the nodes, or move the code to Objective-C as a statemachine action or an Ability/Behavior.