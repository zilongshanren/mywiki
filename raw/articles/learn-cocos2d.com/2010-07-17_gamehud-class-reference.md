---
title: GameHUD Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_h_u_d/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Displays Score Labels and could also be used to show the graphic frames enclosing score labels (optional).
[More...](http://www.learn-cocos2d.com#_details)

`#import <`

[GameHUD.h](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_game_h_u_d_8h_source/)>

| (id) | -
|

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

` [implementation]`

Displays Score Labels and could also be used to show the graphic frames enclosing score labels (optional).

Is drawn just above the [GameBackground](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_background/) but below all [GameObjects](http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_objects/).

| - (void) dealloc | ` [implementation]` |

| + (unsigned int) getScore |

returns the current score

| + (id) hud |

initializes class and returns an autoreleased instance of the class

| + (void) increaseScore |

increases score by one

| - (id) init |

initializes class and returns an instance of the class, you must take care of allocating the object yourself

| - (void) loadBestScore | ` [implementation]` |

load the best score from "disk" using NSKeyedUnarchiver.

There are several ways for save/load and this illustrates just one. The most flexible being NSCoding support for classes that need to be saved/loaded.

| + (void) resetScore |

resets the score to 0

| - (void) saveBestScore | ` [implementation]` |

saves the best score from "disk" using NSKeyedArchiver.

There are several ways for save/load and this illustrates just one. The most flexible being NSCoding support for classes that need to be saved/loaded.

| - (void) updateBestScoreLabel | ` [implementation]` |

| - (void) updateScoreLabel | ` [implementation]` |

| - (void) updateScores: | (ccTime) | delta |
` [implementation]` |