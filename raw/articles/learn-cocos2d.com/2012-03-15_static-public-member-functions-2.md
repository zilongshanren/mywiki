---
title: Static Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_app_store_helper/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <KKAppStoreHelper.h>`


| NSString * |
|

Helper methods for App Store & iTunes related things

| NSString* KKAppStoreHelper::appStoreURLforSearchTerm: | ( | const NSString *const | searchTerm | ) | ` [static, virtual]` |

Creates an App Store URL for the iPhone's App Store that shows the desired search term. This seems to be the only way to show all the Apps of a particular company. Original code obtained from here: [http://arstechnica.com/apple/news/2008/12/linking-to-the-stars-hacking-itunes-to-solicit-reviews.ars](http://arstechnica.com/apple/news/2008/12/linking-to-the-stars-hacking-itunes-to-solicit-reviews.ars)

| NSString* KKAppStoreHelper::artistURL: | ( | const NSString *const | artist | ) | ` [static, virtual]` |

Returns the URL of an artist (developer).