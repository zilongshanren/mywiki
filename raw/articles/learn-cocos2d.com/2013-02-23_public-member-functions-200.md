---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[List of all members.](/)

Public Member Functions
|
| (id) | - [initWithTMXFile:](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/#abf5c2eb34a812084e7c7ef2a19f2e49e) |
| (id) | - [initWithXML:resourcePath:](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/#a5b653ed1281ede9b7d1ff879ae33bde0) |
Static Public Member Functions
|
| (id) | + [formatWithTMXFile:](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/#ac760f51bd8ff84e073a171de41675066) |
| (id) | + [formatWithXML:resourcePath:](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_t_m_x_map_info/#aa9b632e0ace2fc883e8e915dcdee34e1) |
Protected Attributes
|
NSMutableString * | **_currentString** |
BOOL | **_storingCharacters** |
int | **_layerAttribs** |
int | **_parentElement** |
unsigned int | **_parentGID** |
unsigned int | **_currentFirstGID** |
NSString * | **_filename** |
NSString * | **_resources** |
int | **_orientation** |
CGSize | **_mapSize** |
CGSize | **_tileSize** |
NSMutableArray * | **_layers** |
NSMutableArray * | **_tilesets** |
NSMutableArray * | **_objectGroups** |
NSMutableDictionary * | **_properties** |
NSMutableDictionary * | **_tileProperties** |
Properties
|
int | **orientation** |
CGSize | **mapSize** |
CGSize | **tileSize** |
NSMutableArray * | **layers** |
NSMutableArray * | **tilesets** |
NSString * | **filename** |
NSString * | **resources** |
NSMutableArray * | **objectGroups** |
NSMutableDictionary * | **properties** |
NSMutableDictionary * | **tileProperties** |


## Member Function Documentation

creates a TMX Format with a tmx file

| + (id) formatWithXML: |
|
(NSString *) |
*tmxString* |
| resourcePath: |
|
(NSString *) |
*resourcePath* |
|
|
| |

creates a TMX Format with an XML string and a TMX resource path

initializes a TMX format with a tmx file

| - (id) initWithXML: |
|
(NSString *) |
*tmxString* |
| resourcePath: |
|
(NSString *) |
*resourcePath* |
|
|
| |

initializes a TMX format with an XML string and a TMX resource path


The documentation for this class was generated from the following file: