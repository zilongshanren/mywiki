---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[List of all members.](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_t_m_x_map_info-members/)

Public Member Functions
|
| id | [initWithTMXFile:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/#abf5c2eb34a812084e7c7ef2a19f2e49e) (NSString *tmxFile) |
Static Public Member Functions
|
| id | [formatWithTMXFile:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/#ac760f51bd8ff84e073a171de41675066) (NSString *tmxFile) |
Protected Attributes
|
NSMutableString * | **currentString** |
BOOL | **storingCharacters** |
int | **layerAttribs** |
int | **parentElement** |
unsigned int | **parentGID_** |
NSString * | **filename_** |
int | **orientation_** |
CGSize | **mapSize_** |
CGSize | **tileSize_** |
NSMutableArray * | **layers_** |
NSMutableArray * | **tilesets_** |
NSMutableArray * | **objectGroups_** |
NSMutableDictionary * | **properties_** |
NSMutableDictionary * | **tileProperties_** |
Properties
|
int | **orientation** |
CGSize | **mapSize** |
CGSize | **tileSize** |
NSMutableArray * | **layers** |
NSMutableArray * | **tilesets** |
NSString * | **filename** |
NSMutableArray * | **objectGroups** |
NSMutableDictionary * | **properties** |
NSMutableDictionary * | **tileProperties** |


## Member Function Documentation

| id CCTMXMapInfo::formatWithTMXFile: |
( |
NSString * |
*tmxFile* | ) |
` [static, virtual]` |

creates a TMX Format with a tmx file

| id CCTMXMapInfo::initWithTMXFile: |
( |
NSString * |
*tmxFile* | ) |
` [virtual]` |

initializes a TMX format witha tmx file


The documentation for this interface was generated from the following file: