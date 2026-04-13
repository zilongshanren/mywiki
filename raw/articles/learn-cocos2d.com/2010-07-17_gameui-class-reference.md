---
title: GameUI Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_u_i/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Displays the User Interface the player can interact with during the game.
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[GameUI.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_game_u_i_8h_source/)>

| (id) | -
|

` [implementation]`

` [implementation]`

` [implementation]`

Displays the User Interface the player can interact with during the game.

Typical use is to display a pause button which brings up the pause menu. Many line-drawing games also have a FastForward button as the early gameplay can be slow and experienced players like to speed things up until it gets "interesting" for them. The UI is drawn above everything else and touches to UI buttons override any touches to a [MovingObject](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/), so be sure that you place the UI buttons at the screen borders and make them small but not too small that they're too hard to touch correctly. Try Flight Control & Harbor Master as reference. The UI can also be used to draw a frame around the screen, if you like that. See Harbor Master as an example.

| - (void) alertView: | (UIAlertView*) | alertView |
||
| clickedButtonAtIndex: | (NSInteger) | buttonIndex | ||
` [implementation]` |

| - (void) dealloc | ` [implementation]` |

| - (id) init |

initializes class and returns an instance of the class, you must take care of allocating the object yourself

| - (void) onPauseButton: | (id) | sender |
` [implementation]` |

| - (void) showPauseGameDialog |

| + (id) ui |

initializes class and returns an autoreleased instance of the class