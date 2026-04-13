---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-extensions/html/interface_c_c_slider/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

| id |
|

for Cocos2D. Designed with SFX/Music level options in mind.

| id CCSlider::initWithBackgroundFile:thumbFile: | ( | NSString * | bgFile, |
| [thumbFile] NSString * | thumbFile |
||
| ) | ` [virtual]` |

Easy init - filenames instead of CCSprite & CCMenuItem. Uses designated init inside.

| thumbFile | Filename, that is used to create normal & selected images for thumbMenuItem. Selected sprite is darker than normal sprite. |
| bgFile | Filename for background CCSprite. |

| id CCSlider::initWithBackgroundSprite:thumbMenuItem: | ( | CCSprite * | bgSprite, |
| [thumbMenuItem] CCMenuItem * | aThumb |
||
| ) | ` [virtual]` |

Designated init.

| bgSprite | CCSprite, that is used as a background. It's bounding box is used to determine max & min x position for a thumb menu item. |
| aThumb | MenuItem that is used as a thumb. Used without CCMenu, so CCMenuItem::activate doesn't get called. |

| id CCSlider::sliderWithBackgroundFile:thumbFile: | ( | NSString * | bgFile, |
| [thumbFile] NSString * | thumbFile |
||
| ) | ` [static, virtual]` |

| id CCSlider::sliderWithBackgroundSprite:thumbMenuItem: | ( | CCSprite * | bgSprite, |
| [thumbMenuItem] CCMenuItem * | aThumb |
||
| ) | ` [static, virtual]` |

Creates slider with given bg sprite and menu item as a thumb.

float CCSlider::value` [read, write, assign]` |

Current chosen value, min is 0.0f, max is 1.0f.