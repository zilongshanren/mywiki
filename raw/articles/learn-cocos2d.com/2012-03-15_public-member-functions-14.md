---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/protocol_k_k_game_kit_helper_protocol-p/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <KKGameKitHelper.h>`


| void |
|

Defines the delegate methods that are forwarded from GameKitHelper.

| void
|

` [optional, virtual]`

Called when achievement was reported to Game Center.

| void
|

` [optional, virtual]`

Called when achievement list was received from Game Center.

Called when the achievements view was closed.

Called when friend list was received from Game Center.

Called when the leaderboard view was closed.

Called when local player was authenticated or logged off.

Called when a match was found.

Called when the matchmaking view was closed.

Called for any generic error in the matchmaking view.

Called when a player connected to the match.

Called when a player disconnected from a match.

Called when player info was received from Game Center.

Called to indicate whether adding players to a match was successful.

| void
|

` [optional, virtual]`

Called whenever data from another player was received.

| void
|

` [optional, virtual]`

Called when matchmaking activity was received from Game Center.

Called to indicate whether the reset achievements command was successful.

Called when scores were received from Game Center.

Called when scores where submitted. This can fail, so check for success.