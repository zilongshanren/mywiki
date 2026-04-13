---
title: 'Unreal: Am I On The Server'
url: https://www.executionunit.com/blog/2022/09/24/unreal-am-i-on-the-server/
published: '2022-09-24'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

I’ve been working on an Unreal game for the past few months. One of the things that the whole team has found very frustrating is knowing if the code we are writing is running on the server or the client.

Lots of code only needs to run on one or the other and some code needs to run on both. Unreal has a powerful and slightly confusing networking model combined with numerous ways to run the game from within the editor.

To help me understand the different modes I created the following table. I wrote a small bit of code in my GameMode class to extract some values. I added a break point just after this code so that I could record the values.

1 2 3 4 5 |
|

`PlayMode`

is the mode you select in the editor (in the Play button drop down).

`#`

is the number of players selected in editor

`BP`

is the number of times my break point is hit. So for two players I would expect to hit it twice
(note that this isn’t true in one case).

`Has Game Mode`

technically the game mode only ever exists in the server.

| Play Mode | # | BP | Net Mode | System Role | Has Game Mode | Has Authority |
|---|---|---|---|---|---|---|
| StandAlone | 1 | 1 | NM_StandAlone | Role_Authority | 1 | 1 |
| StandAlone | 2 | 1 | NM_StandAlone | Role_Authority | 1 | 1 |
| 2 | NM_StandAlone | Role_Authority | 1 | 1 | ||
| Listen Server | 1 | 1 | NM_ListenServer | Role_Authority | 1 | 1 |
| Listen Server | 2 | 1 | NM_ListenServer | Role_Authority | 1 | 1 |
| 2 | NM_Client | Role_SimulatedProxy | 0 | 0 | ||
| Client | 1 | 1 | NM_DedicatedServer | Role_Authority | 1 | 1 |
| 1 | 2 | NM_Client | Role_SimulatedProxy | 0 | 0 | |
| Client | 2 | 1 | NM_DedicatedServer | Role_Authority | 1 | 1 |
| 2 | NM_Client | Role_SimulatedProxy | 0 | 0 | ||
| 3 | NM_Client | Role_SimulatedProxy | 0 | 0 |

It all makes sense to me apart from in StandAlone mode. In all other scenarios `NetMode`

and `SystemRole`

have
reasonable values. You can easily say “this code is running on the server” when `NetMode == NM_ListenServer`

or
`NetMode == NM_DedicatedServer`

.

So what is going on in **Stand Alone** mode? In standalone mode everything is running inside one process,
the same process the editor is in. So The code is both the server and the client. This makes some
things easier to debug and other things just plain confusing. I think this is the scenario for a split
screen game, so it’s important your code works in this mode as well.

As a side note [Visual Studio has a plugin](https://marketplace.visualstudio.com/items?itemName=vsdbgplat.MicrosoftChildProcessDebuggingPowerTool) to enable child process debugging. With this plugin you can
launch the editor from VS, play the game and launch child clients and the debugger will attach to them
and allow you to set break points and view memory, very useful.

Hope this helps.

EOL.

## Comments