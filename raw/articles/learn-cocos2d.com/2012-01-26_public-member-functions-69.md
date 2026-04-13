---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_game_kit_helper/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <KKGameKitHelper.h>`


| void |
|

Singleton that wraps a lot of common Game Kit and Game Center functionality and forwards events to a delegate implementing the GameKitHelperProtocol. It ensures that certain functions are only called if Game Center is available on the current device and the local player is authenticated. It also caches achievements so that they don't get lost if the connection is interrupted.

| void KKGameKitHelper::addPlayersToMatch: | ( | GKMatchRequest * | request | ) | ` [virtual]` |

Request to add players to a match.

| void KKGameKitHelper::authenticateLocalPlayer | ( | ) | ` [virtual]` |

try to authenticate the local player

| void KKGameKitHelper::cancelMatchmakingRequest | ( | ) | ` [virtual]` |

Cancels any matchmaking request currently in progress.

| void KKGameKitHelper::disconnectCurrentMatch | ( | ) | ` [virtual]` |

Disconnect from the current match

| void KKGameKitHelper::findMatchForRequest: | ( | GKMatchRequest * | request | ) | ` [virtual]` |

Request a match for the given request.

| GKAchievement* KKGameKitHelper::getAchievementByID: | ( | NSString * | identifier | ) | ` [virtual]` |

returns a cached achievement by its identifier

| void KKGameKitHelper::getLocalPlayerFriends | ( | ) | ` [virtual]` |

request the local player's friends

| void KKGameKitHelper::getPlayerInfo: | ( | NSArray * | players | ) | ` [virtual]` |

requests info about a set of players

| void KKGameKitHelper::loadAchievements | ( | ) | ` [virtual]` |

Starts obtaining the local player's achievements from Game Center.

| void KKGameKitHelper::queryMatchmakingActivity | ( | ) | ` [virtual]` |

Request the matchmaking activity to get an indicator on how many games are played.

| void KKGameKitHelper::reportAchievementWithID:percentComplete: | ( | NSString * | identifier, |
| [percentComplete] float | percent |
||
| ) | ` [virtual]` |

Send an achievement update to Game Center. The message will only be sent if completion percent is greater than any percent previously submitted (Game Center does not allow achievements to regress and would simply ignore such a message).

| void KKGameKitHelper::reportCachedAchievements | ( | ) | ` [virtual]` |

Try to send any cached Achievements to Game Center. If updating an achievement fails for any reason, the achievement is cached. By default, GameKitHelper will call this method when the local player is authenticated, so that any previously gained achievements are hopefully sent the next time the player runs the App.

| void KKGameKitHelper::resetAchievements | ( | ) | ` [virtual]` |

Resets all achievement progress. Be very careful with this, should only be run after the player has understood the consequences. You'll use it rather often during development however. It will also clean all cached achievements.

| void KKGameKitHelper::retrieveScoresForPlayers:category:range:playerScope:timeScope: | ( | NSArray * | players, |
| [category] NSString * | category, |
||
| [range] NSRange | range, |
||
| [playerScope] GKLeaderboardPlayerScope | playerScope, |
||
| [timeScope] GKLeaderboardTimeScope | timeScope |
||
| ) | ` [virtual]` |

request the scores of a set of players, in a given category, range and scopes

| void KKGameKitHelper::retrieveTopTenAllTimeGlobalScores | ( | ) | ` [virtual]` |

convenience method, requests the Top 10 all time global highscores

| void KKGameKitHelper::saveCachedAchievements | ( | ) | ` [virtual]` |

Saves all cached achievements to persist them between sessions. By default every time an achievement is cached the cached achievements are saved to disk, so they also persist even when the App crashes.

| void KKGameKitHelper::sendDataToAllPlayers: | ( | NSData * | data | ) | ` [virtual]` |

sends the given NSData to all players (unreliably)

| void KKGameKitHelper::sendDataToAllPlayers:length: | ( | void * | data, |
| [length] NSUInteger | length |
||
| ) | ` [virtual]` |

sends the given pointer with the given length to all players (unreliably)

| void KKGameKitHelper::sendDataToAllPlayers:length:reliable: | ( | void * | data, |
| [length] NSUInteger | length, |
||
| [reliable] BOOL | reliable |
||
| ) | ` [virtual]` |

sends the given pointer with the given length to all players either reliably (safe but slow) or unreliably (arrival not guaranteed, but fast)

| void KKGameKitHelper::sendDataToAllPlayers:reliable: | ( | NSData * | data, |
| [reliable] BOOL | reliable |
||
| ) | ` [virtual]` |

sends the given NSData to all players either reliably (safe but slow) or unreliably (arrival not guaranteed, but fast)

| void KKGameKitHelper::setupMatchInvitationHandlerWithMinPlayers:maxPlayers: | ( | int | minPlayers, |
| [maxPlayers] int | maxPlayers |
||
| ) | ` [virtual]` |

creates the handler for processing match invitations from other players

| void KKGameKitHelper::showAchievements | ( | ) | ` [virtual]` |

Brings up the Game Center Achievements view.

| void KKGameKitHelper::showLeaderboard | ( | ) | ` [virtual]` |

Brings up the Game Center Leaderboard view.

| void KKGameKitHelper::showMatchmakerWithInvite: | ( | GKInvite * | invite | ) | ` [virtual]` |

Brings up the Game Center Matchmaking view after receiving an invite.

| void KKGameKitHelper::showMatchmakerWithRequest: | ( | GKMatchRequest * | request | ) | ` [virtual]` |

Brings up the Game Center Matchmaking view with a match request.

| void KKGameKitHelper::submitScore:category: | ( | int64_t | score, |
| [category] NSString * | category |
||
| ) | ` [virtual]` |

submit a score to Game Center

NSMutableDictionary * KKGameKitHelper::achievements` [read, assign]` |

The cached achievements of the local player. GameKitHelper will save the achievements between sessions to ensure that achievements are updated on Game Center on next app start even if connection was lost.

GKMatch * KKGameKitHelper::currentMatch` [read, write, retain]` |

The current match object. May be nil if there's no match.

BOOL KKGameKitHelper::isGameCenterAvailable` [read, assign]` |

NSError * KKGameKitHelper::lastError` [read, assign]` |

If your delegate receives an error message, you can check this property for the actual NSError object. This allows you to print out the cause of the error to console log or display an Alert view.

BOOL KKGameKitHelper::matchStarted` [read, assign]` |

Indicates whether the current match has already started.